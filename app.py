import cv2
import numpy as np
import math

# Start Camera
cap = cv2.VideoCapture(0)

while True:
    try:
        ret, frame = cap.read()
        if not ret: continue
        
        frame = cv2.flip(frame, 1)
        
        # 1. Define the Green Box (Region of Interest)
        cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 2)
        roi = frame[100:300, 100:300]

        # 2. Blur to remove noise
        kernel = np.ones((3, 3), np.uint8)
        roi = cv2.GaussianBlur(roi, (3, 3), 0)

        # 3. Detect Skin Color (HSV)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        mask = cv2.dilate(mask, kernel, iterations=4)
        mask = cv2.GaussianBlur(mask, (5, 5), 100)

        # 4. Find Contours (Hand Outline)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            cnt = max(contours, key=lambda x: cv2.contourArea(x))

            # 5. Convex Hull & Defects (The Gaps between fingers)
            epsilon = 0.0005 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            
            hull = cv2.convexHull(cnt)
            
            # Area calculations
            areahull = cv2.contourArea(hull)
            areacnt = cv2.contourArea(cnt)
            arearatio = ((areahull - areacnt) / areacnt) * 100

            # Find Defects
            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)

            l = 0 # Count of fingers

            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])

                # Triangle Math to find angles
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                
                # Apply Cosine Rule
                angle = math.acos((b**2 + c**2 - a**2) / (2*b*c)) * 57

                # If angle is sharp (<90), it's a finger gap
                if angle <= 90 and d > 30:
                    l += 1
                    cv2.circle(roi, far, 3, [255, 0, 0], -1)

                cv2.line(roi, start, end, [0, 255, 0], 2)

            l += 1 # 1 gap = 2 fingers, etc.

            # 6. Display Text
            font = cv2.FONT_HERSHEY_SIMPLEX
            if l == 1:
                if areacnt < 2000:
                    msg = 'Put hand in box'
                elif arearatio < 12:
                    msg = '0 - FIST'
                else:
                    msg = '1 - THUMBS UP'
            elif l == 2:
                msg = '2 - VICTORY'
            elif l == 3:
                msg = '3'
            elif l == 4:
                msg = '4'
            elif l == 5:
                msg = '5 - OPEN HAND'
            else:
                msg = 'Reposition'
                
            cv2.putText(frame, msg, (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
            
        cv2.imshow('Pure OpenCV - No MediaPipe', frame)
        cv2.imshow('Mask', mask)

    except Exception as e:
        pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()