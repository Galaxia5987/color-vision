from pathlib import Path


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


def list_devices() -> list[dict]:
    """
    List all available V4L camera devices with stable names.
    """
    if not V4L_BY_ID.exists():
        return []

    devices: list[dict] = []

    for dev in sorted(V4L_BY_ID.iterdir()):
        devices.append({
            "id_name": dev.name,
            "device_path": str(dev.resolve()),
        })

    return devices
