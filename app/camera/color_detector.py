from turtle import up
import cv2 as cv
import numpy as np

from app import logging_config
from app.utils.cv_utils import frames_to_jpeg_bytes
from temp import DISABLED_STREAM_IMAGE

logger = logging_config.get_logger(__name__)

class ColorDetector:
    def __init__(self, lower, upper) -> None:
        self.lower = np.array(lower)
        self.upper = np.array(upper)

        self.latest_frame = DISABLED_STREAM_IMAGE
        self.latest_masked_frame = DISABLED_STREAM_IMAGE
        self.detections = []

    def proccess(self, frame):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        mask = cv.inRange(hsv, self.lower, self.upper)

        kernel = np.ones((5, 5), "uint8")
        mask = cv.erode(mask, kernel, iterations=1)
        mask = cv.dilate(mask, kernel, iterations=1)

        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


        detected_objects = []
        for contour in contours:
            area = cv.contourArea(contour)
            
            if area > 500:
                x, y, w, h = cv.boundingRect(contour)
                
                M = cv.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                else:
                    cx, cy = x + w//2, y + h//2
                
                detected_objects.append({
                    'center': (cx, cy),
                    'bbox': (x, y, w, h),
                    'area': area,
                    'contour': contour
                })
        
        self.latest_masked_frame = mask
        self.latest_frame = frame

        return detected_objects, mask
    
    def annotate_frame(self, frame, detected_objects):
        """Draw detections on the frame"""
        annotated = frame.copy()
        
        for obj in detected_objects:
            x, y, w, h = obj['bbox']
            cx, cy = obj['center']
            
            # BBox
            cv.rectangle(annotated, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Center
            cv.circle(annotated, (cx, cy), 5, (0, 0, 255), -1)
            
            cv.drawContours(annotated, [obj['contour']], -1, (255, 0, 0), 2)
            
            # Text
            cv.putText(annotated, f"Area: {int(obj['area'])}", 
                      (x, y-10), cv.FONT_HERSHEY_SIMPLEX, 
                      0.5, (0, 255, 0), 2)
        
        cv.putText(annotated, f"Detected: {len(detected_objects)}", 
                  (10, 30), cv.FONT_HERSHEY_SIMPLEX, 
                  1, (255, 255, 255), 2)
        
        return annotated
    
    def get_detections_jpeg(self):
        frame = self.latest_frame

        if frame is None:
            return None
        
        detections = self.detections

        annotated_frame = self.annotate_frame(frame, detections)

        return frames_to_jpeg_bytes(annotated_frame)
    
    def get_masked_frame(self):
        return frames_to_jpeg_bytes(self.latest_masked_frame)
