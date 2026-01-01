import cv2


def frames_to_jpeg_bytes(frame, resolution=(640, 480)):
    resized = cv2.resize(frame, resolution)
    ret, jpeg = cv2.imencode(".jpg", resized)
    if not ret:
        return None
    return jpeg.tobytes()

def exposure_percentage_to_value(
    percentage: int, 
    min_exposure: float = -13.0, 
    max_exposure: float = -1.0
) -> float:
    """Convert 0-100 percentage to camera exposure value.
    
    Args:
        percentage: Exposure level from 0 (darkest) to 100 (brightest)
        min_exposure: Minimum exposure value (darkest)
        max_exposure: Maximum exposure value (brightest)
        
    Returns:
        float: Exposure value in camera's native range
        
    Example:
        >>> exposure_percentage_to_value(0)   # Darkest
        -13.0
        >>> exposure_percentage_to_value(50)  # Middle
        -7.0
        >>> exposure_percentage_to_value(100) # Brightest
        -1.0
    """
    if not 0 <= percentage <= 100:
        raise ValueError(f"Percentage must be 0-100, got {percentage}")
    
    # Linear interpolation
    exposure = min_exposure + (percentage / 100.0) * (max_exposure - min_exposure)
    return exposure