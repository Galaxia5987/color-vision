import cv2 as cv
import numpy as np

class ColorCalibrator:
    def __init__(self, cap):
        self.cap = cap
        self.window_name = "Color Calibration"
        
        cv.namedWindow(self.window_name)
        
        cv.createTrackbar("H Min", self.window_name, 0, 179, self.nothing)
        cv.createTrackbar("H Max", self.window_name, 179, 179, self.nothing)
        cv.createTrackbar("S Min", self.window_name, 0, 255, self.nothing)
        cv.createTrackbar("S Max", self.window_name, 255, 255, self.nothing)
        cv.createTrackbar("V Min", self.window_name, 0, 255, self.nothing)
        cv.createTrackbar("V Max", self.window_name, 255, 255, self.nothing)
    
    def nothing(self, x):
        pass
    
    def get_hsv_values(self):
        """Get current trackbar values"""
        h_min = cv.getTrackbarPos("H Min", self.window_name)
        h_max = cv.getTrackbarPos("H Max", self.window_name)
        s_min = cv.getTrackbarPos("S Min", self.window_name)
        s_max = cv.getTrackbarPos("S Max", self.window_name)
        v_min = cv.getTrackbarPos("V Min", self.window_name)
        v_max = cv.getTrackbarPos("V Max", self.window_name)
        
        lower = [h_min, s_min, v_min]
        upper = [h_max, s_max, v_max]
        return lower, upper
    
    def run(self):
        """Run calibration loop"""
        print("Adjust trackbars to isolate your target color")
        print("Press 's' to save values")
        print("Press 'q' to quit")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Get current HSV range
            lower, upper = self.get_hsv_values()
            
            # Convert and create mask
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, np.array(lower), np.array(upper))
            
            # Apply mask to frame
            result = cv.bitwise_and(frame, frame, mask=mask)
            
            # Stack images for display
            frame_small = cv.resize(frame, (320, 240))
            mask_colored = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
            mask_small = cv.resize(mask_colored, (320, 240))
            result_small = cv.resize(result, (320, 240))
            
            # Combine into one display
            top_row = np.hstack([frame_small, mask_small])
            bottom_row = np.hstack([result_small, np.zeros_like(frame_small)])
            combined = np.vstack([top_row, bottom_row])
            
            cv.putText(combined, "Original", (10, 30), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv.putText(combined, "Mask", (330, 30), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv.putText(combined, "Result", (10, 270), 
                      cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv.imshow(self.window_name, combined)
            
            key = cv.waitKey(1) & 0xFF
            
            if key == ord('s'):
                self.save_values(lower, upper)
            elif key == ord('q'):
                break
        
        self.cleanup()
    
    def save_values(self, lower, upper):
        """Save calibrated values to file"""
        print(f"\nCalibrated HSV Range:")
        print(f"Lower: {lower}")
        print(f"Upper: {upper}")
        
        with open('color_config.txt', 'w') as f:
            f.write(f"lower = {lower}\n")
            f.write(f"upper = {upper}\n")
        
        print("Values saved to color_config.txt")
    
    def cleanup(self):
        """Release resources"""
        self.cap.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    camera = cv.VideoCapture(0)
    calibrator = ColorCalibrator(camera)
    calibrator.run()