# Hand Gesture Recognition (Computer Vision)
### Gradient Tech Recruitment Task - 2026

## 🎥 Demo & Output
* **[Click Here to Watch the Demo Video](https://drive.google.com/file/d/1B8FNFlVi_P2Mr9khG5IzU8dSEJfVnDpJ/view?usp=sharing)**

  
* <img width="1580" height="835" alt="Screenshot 2026-02-15 213300" src="https://github.com/user-attachments/assets/8639b414-08ca-4491-8b4b-af42eb2d9d06" />
<img width="1585" height="833" alt="Screenshot 2026-02-15 213222" src="https://github.com/user-attachments/assets/499a9ced-704d-4950-be44-464f51baf3e1" />
<img width="1578" height="834" alt="Screenshot 2026-02-15 204800" src="https://github.com/user-attachments/assets/7776273d-a401-486a-99e9-c43e59a4c743" />





---


## Project Goal
I built a real-time hand gesture recognizer using **OpenCV** and Python. 
My goal was to create a system that detects gestures using **pure geometric logic** rather than relying on heavy, pre-built AI models like MediaPipe. This approach helps demonstrate a clear understanding of image processing fundamentals.

## How it Works (The Logic)
Instead of using a black-box AI, I used a 5-step mathematical approach:

1.  **Skin Detection (HSV):** I convert the video frame to HSV color space to filter out skin tones. This isolates the hand from the background.

2.  **Contour Extraction:** The code finds the boundary/outline of the hand in the masked image.

3.  **Convex Hull & Defects:** I apply a "Convex Hull" (a polygon envelope) around the hand. The gaps between the hull and the fingers are called "defects."

4.  **Trigonometry (Cosine Rule):** I use the Cosine Rule to measure the angle of these defects.
    * **Logic:** If the angle is sharp (< 90°), it is a gap between fingers.
    * **Counting:** By counting these valid gaps, I can determine if the hand is a Fist (0 gaps), Peace Sign (1 gap), or Open Hand (4 gaps).

## How to Run
1.  **Install OpenCV:**
    ```bash
    pip install opencv-python numpy
    ```
2.  **Run the script:**
    ```bash
    python app.py
    ```

*Note: Please keep your hand inside the Green Box for detection to work correctly.*
