import sys
import cv2
import mediapipe as mp
import numpy as np

choice = "Bicep"

counter = 0
stage = None
# Angle between any 3 points

def calculateAngle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Second
    c = np.array(c)  # Third

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
        np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Setup A Meadiapipe Instance


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Setup A Opencv Instance

cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.55, min_tracking_confidence=0.55) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

    # Detection and Rendering

        # Flipping the Image (To correct lateral inversion)
        frame = cv2.flip(frame, 1)

        # Recolour the Image to Mediapipe Format
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make Detections
        results = pose.process(image)

        # Recolour the Image to cv2 Format
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract Landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            # print(landmarks)

            def ExcerciseCount(option):
                global counter
                global stage
                if option == 'Bicep':
                    # Excercise Counter Variables
                    # counter = 0
                    # stage = None
                    # Get Coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    # Calculate Angle
                    angle = calculateAngle(shoulder, elbow, wrist)
                    #             Visualise the angle
                    # cv2.putText(image, str(angle),
                    #     tuple(np.multiply(elbow, [640,480]).astype(int)),
                    #         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                    #     )

                    # Curl Counter Logic

                    if angle > 160:
                        stage = "down"
                    if angle < 30 and stage == 'down':
                        stage = "up"
                        counter += 1
                        #print(counter)

                    # Render Curl Counter

                    # Setup Status Box

                    cv2.rectangle(image, (0, 0), (150, 73), (245, 117, 16), -1)

                   # Rep Data

                    cv2.putText(image, "REPS", (20, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                                    0, 0, 0), 1, cv2.LINE_AA
                                )
                    cv2.putText(image, str(counter), (20, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (
                                    0, 63, 125), 2, cv2.LINE_AA
                                )

                    # Stage Data

                    cv2.putText(image, "STAGE", (70, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                                    0, 0, 0), 1, cv2.LINE_AA
                                )
                    cv2.putText(image, stage, (60, 55),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (
                                    0, 63, 125), 2, cv2.LINE_AA
                                )

                    # Render Detections
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(
                                                  color=(245, 117, 66), thickness=2, circle_radius=2),
                                              mp_drawing.DrawingSpec(
                                                  color=(245, 66, 230), thickness=2, circle_radius=2)
                                              )
                    # print(results)

                elif option == 'Shoulder':
                    # Excercise Counter Variables
                    # counter = 0
                    # stage = None
                    # Get Coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    # Calculate Angle
                    angle = calculateAngle(shoulder, elbow, wrist)

                    # Visualise the angle
                    # cv2.putText(image, str(angle),
                    #             tuple(np.multiply(elbow, [640,480]).astype(int)),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                    #             )

                    # Counter Logic
                    if angle < 80:
                        stage = "down"
                    if angle > 160 and stage == 'down':
                        stage = "up"
                        counter += 1
                        # print(counter)
                    # Render Curl Counter

                    # Setup Status Box

                    cv2.rectangle(image, (0, 0), (150, 73), (245, 117, 16), -1)

                   # Rep Data

                    cv2.putText(image, "REPS", (20, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                                    0, 0, 0), 1, cv2.LINE_AA
                                )
                    cv2.putText(image, str(counter), (20, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (
                                    0, 63, 125), 2, cv2.LINE_AA
                                )

                    # Stage Data

                    cv2.putText(image, "STAGE", (70, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                                    0, 0, 0), 1, cv2.LINE_AA
                                )
                    cv2.putText(image, stage, (60, 55),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (
                                    0, 63, 125), 2, cv2.LINE_AA
                                )

                    # Render Detections
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(
                                                  color=(245, 117, 66), thickness=2, circle_radius=2),
                                              mp_drawing.DrawingSpec(
                                                  color=(245, 66, 230), thickness=2, circle_radius=2)
                                              )
                    # print(results)

                elif option == 'Squat':
                    # Excercise Counter Variables
                    # counter = 0
                    # stage = None
                    # Get Coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    foot_index = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]

                    # Calculate Angle
                    shoulder_hip_angle = calculateAngle(shoulder, hip, knee)
                    hip_knee_angle = calculateAngle(hip, knee, ankle)
                    knee_ankle_angle = calculateAngle(knee, ankle, foot_index)

                    # Visualise the angle
                    # cv2.putText(image, str(shoulder_hip_angle),
                    #             tuple(np.multiply(hip, [640,480]).astype(int)),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                    #             )
                    # cv2.putText(image, str(hip_knee_angle),
                    #             tuple(np.multiply(knee, [640,480]).astype(int)),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                    #             )
                    # cv2.putText(image, str(knee_ankle_angle),
                    #             tuple(np.multiply(ankle, [640,480]).astype(int)),
                    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                    #             )

                    # Curl Counter Logic
                    if (shoulder_hip_angle > 160 and hip_knee_angle > 160 and knee_ankle_angle > 85):
                        stage = "up"
                    if ((shoulder_hip_angle < 50 and hip_knee_angle < 100 and knee_ankle_angle > 70) and stage == 'up'):
                        stage = "down"
                        counter += 1
                    # Render Curl Counter

                    # Setup Status Box

                    cv2.rectangle(image, (0, 0), (150, 73), (245, 117, 16), -1)

                   # Rep Data

                    cv2.putText(image, "REPS", (20, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                                    0, 0, 0), 1, cv2.LINE_AA
                                )
                    cv2.putText(image, str(counter), (20, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (
                                    0, 63, 125), 2, cv2.LINE_AA
                                )

                    # Stage Data

                    cv2.putText(image, "STAGE", (70, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (
                                    0, 0, 0), 1, cv2.LINE_AA
                                )
                    cv2.putText(image, stage, (60, 55),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (
                                    0, 63, 125), 2, cv2.LINE_AA
                                )

                    # Render Detections
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(
                                                  color=(245, 117, 66), thickness=2, circle_radius=2),
                                              mp_drawing.DrawingSpec(
                                                  color=(245, 66, 230), thickness=2, circle_radius=2)
                                              )
                    # print(results)
            ExcerciseCount(choice)

        except:
            pass

        cv2.imshow("Mediapipe Feed", image)

        if (cv2.waitKey(10) & 0xFF == ord('q')):
            break


cap.release()
cv2.destroyAllWindows()
