from pathlib import Path
import subprocess
import re
from typing import List, Dict, Tuple, Optional


V4L_BY_ID = Path("/dev/v4l/by-id")


def resolve_device(name: str) -> str:
    """
    Resolve a V4L camera device by partial name match.
    Example name: "C920", "Logitech", "ELP"
    """
    if not V4L_BY_ID.exists():
        raise RuntimeError(f"{V4L_BY_ID} does not exist")

    for dev in sorted(V4L_BY_ID.iterdir()):
        if name in dev.name:
            return str(dev.resolve())

    raise RuntimeError(f"Camera '{name}' not found")


def list_devices() -> list[str]:
    """
    List all available V4L camera devices with stable names.
    """
    if not V4L_BY_ID.exists():
        return []

    devices: list[str] = []

    for dev in sorted(V4L_BY_ID.iterdir()):
        devices.append(str(dev.name))

    return devices

def list_v4l2_controls(device: str) -> List[str]:
    """
    Run `v4l2-ctl -d <device> --list-ctrls` and return non-empty output lines.
    Raises RuntimeError if v4l2-ctl is not available or the command fails.
    """
    cmd = ["v4l2-ctl", "-d", device, "--list-ctrls"]
    try:
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        raise RuntimeError("v4l2-ctl not found; please install v4l-utils")
    except subprocess.CalledProcessError as e:
        out = (e.stderr or e.stdout or "").strip()
        raise RuntimeError(f"v4l2-ctl failed: {out}") from e

    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def exposure_controls(device: str) -> List[str]:
    """
    Return the raw control lines that contain 'exposure' (case-insensitive).
    Equivalent to: v4l2-ctl -d /dev/videoX --list-ctrls | grep -i exposure
    """
    lines = list_v4l2_controls(device)
    pat = re.compile(r"exposure", re.IGNORECASE)
    return [line for line in lines if pat.search(line)]


def exposure_control_ids(device: str) -> List[str]:
    """
    Return the control identifiers (first token like 'exposure_auto') for controls
    that match 'exposure'.
    """
    controls = exposure_controls(device)
    ids: List[str] = []
    for line in controls:
        m = re.match(r"^([^\s(]+)", line)
        if m:
            ids.append(m.group(1))
    return ids


def has_exposure_control(device: str) -> bool:
    """
    True if any exposure-related control exists for the given device path.
    """
    return bool(exposure_control_ids(device))


def exposure_control_ranges(device: str) -> Dict[str, Tuple[int, int]]:
    """
    Return a mapping of exposure-related control id -> (min, max) where available.
    Parses the `min=` and `max=` values from v4l2-ctl --list-ctrls lines.
    """
    ranges: Dict[str, Tuple[int, int]] = {}
    for line in exposure_controls(device):
        m_id = re.match(r"^([^\s(]+)", line)
        if not m_id:
            continue
        cid = m_id.group(1)
        m_range = re.search(r"min=(-?\d+)\s+max=(-?\d+)", line)
        if m_range:
            ranges[cid] = (int(m_range.group(1)), int(m_range.group(2)))
    return ranges


def get_exposure_range(device: str, control_id: Optional[str] = None) -> Tuple[int, int]:
    """
    Get the (min, max) exposure range for a specific control_id, or the first
    exposure control that exposes a range if control_id is None.
    Raises RuntimeError if no suitable range is found.
    """
    ranges = exposure_control_ranges(device)
    if control_id:
        if control_id in ranges:
            return ranges[control_id]
        raise RuntimeError(f"Control '{control_id}' not found or has no range")
    if ranges:
        # return the first available range
        _, rng = next(iter(ranges.items()))
        return rng
    raise RuntimeError("No exposure control with a numeric range found")


def set_auto_exposure(device: str, enable: bool) -> None:
    """
    Set auto/manual exposure based on menu entries exposed by the exposure control.

    enable=True  -> set the control to the menu value whose label contains 'auto'
    enable=False -> set the control to the menu value whose label contains 'manual'

    The function will:
      - Prefer control named 'exposure_auto' if present.
      - Otherwise pick any exposure-related control id that contains 'auto'.
    Raises RuntimeError if no suitable control or menu value is found or if v4l2-ctl fails.
    """
    ids = exposure_control_ids(device)
    if not ids:
        raise RuntimeError("No exposure control found")

    # Prefer the canonical name if present
    if "exposure_auto" in ids:
        target_id = "exposure_auto"
    else:
        # pick any id that contains 'auto' or fall back to the first exposure-related id
        target_id = next((i for i in ids if "auto" in i.lower()), ids[0])

    # find the raw control line for the chosen id
    line = next((l for l in exposure_controls(device) if l.startswith(target_id)), None)
    if not line:
        raise RuntimeError(f"Control line for '{target_id}' not found")

    # parse menu items like "1: Manual, 3: Auto" from the line
    menu_items = re.findall(r"(\d+):\s*([^,)\n]+)", line)
    if not menu_items:
        raise RuntimeError(f"No menu items found for control '{target_id}'")

    desired = "auto" if enable else "manual"
    chosen_value: Optional[int] = None
    for val_str, label in menu_items:
        if desired in label.lower():
            chosen_value = int(val_str)
            break

    if chosen_value is None:
        # fallback: if enabling auto and there is any item containing 'auto' in id/name, try that
        for val_str, label in menu_items:
            if desired in label.lower():
                chosen_value = int(val_str)
                break

    if chosen_value is None:
        raise RuntimeError(f"No menu value matching '{desired}' for control '{target_id}'")

    cmd = ["v4l2-ctl", "-d", device, "-c", f"{target_id}={chosen_value}"]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        raise RuntimeError("v4l2-ctl not found; please install v4l-utils")
    except subprocess.CalledProcessError as e:
        out = (e.stderr or e.stdout or "").strip()
        raise RuntimeError(f"v4l2-ctl failed to set control: {out}") from e
