# from flask import Flask, render_template, Response
# import cv2
# import mediapipe as mp

# app = Flask(__name__, template_folder='A:\\Deep Learning\\')

# # Initialize the video capture from the default camera (index 0)
# cap = cv2.VideoCapture(0)

# # Check if the camera opened successfully
# if not cap.isOpened():
#     print("Failed to open camera.")

# # Initialize MediaPipe Pose model
# mp_pose = mp.solutions.pose.Pose(
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
# )

# # Bicep curl counting variables
# count = 0
# position = None

# # Function to generate frames for the video stream
# def generate_frames():
#     global count, position
    
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()

#         # Check if the frame was captured successfully
#         if not ret:
#             print("Failed to capture frame from camera.")
#             break

#         # Process the frame using MediaPipe Pose model
#         image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         result = mp_pose.process(image)

#         # Draw landmarks on the frame
#         if result.pose_landmarks:
#             mp.solutions.drawing_utils.draw_landmarks(
#                 frame, result.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS
#             )

#             # Extract key landmarks for bicep curl counting
#             landmarks = result.pose_landmarks.landmark
#             if len(landmarks) >= 15:
#                 shoulder = landmarks[11].y
#                 elbow = landmarks[13].y
#                 wrist = landmarks[15].y

#                 # Check for bicep curl motion
#                 if shoulder >= elbow and elbow >= wrist:
#                     if position != "up":
#                         position = "up"
#                 elif shoulder <= elbow and elbow <= wrist:
#                     if position == "up":
#                         position = "down"
#                         count += 1
#                         print("Bicep curl count:", count)

#         # Overlay bicep curl count on the frame
#         cv2.putText(frame, f"Bicep Curl Count: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#         # Convert the frame to JPEG format
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         # Yield the frame as a response to the client
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# # Route for the video stream page
# @app.route('/')
# def index():
#     return render_template('abu.html')

# # Route for accessing the video stream
# @app.route('/bisup_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__, template_folder=r'A:\Deep Learning')

# Initialize the video capture from the default camera (index 0)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Failed to open camera.")

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Bicep curl counting variables
count = 0
position = None

# Function to generate frames for the video stream
def generate_frames():
    global count, position
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Failed to capture frame from camera.")
            break

        # Process the frame using MediaPipe Pose model
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = mp_pose.process(image)

        # Draw landmarks on the frame
        if result.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, result.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS
            )

            # Extract key landmarks for bicep curl counting
            landmarks = result.pose_landmarks.landmark
            if len(landmarks) >= 15:
                shoulder = landmarks[11].y
                elbow = landmarks[13].y
                wrist = landmarks[15].y

                # Check for bicep curl motion
                if shoulder >= elbow and elbow >= wrist:
                    if position != "up":
                        position = "up"
                elif shoulder <= elbow and elbow <= wrist:
                    if position == "up":
                        position = "down"
                        count += 1
                        print("Bicep curl count:", count)

        # Overlay bicep curl count on the frame
        cv2.putText(frame, f"Bicep Curl Count: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame as a response to the client
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for the video stream page
@app.route('/')
def index():
    return render_template('abu.html')

# Route for accessing the video stream
@app.route('/bisup_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
