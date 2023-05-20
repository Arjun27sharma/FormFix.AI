import cv2
import mediapipe as mp 
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculateAngle(a,b,c):
    
    """
    Calculates the angle between three points in a 2D plane.

    :param a: A tuple or list containing the (x,y) coordinates of the first point.
    :type a: tuple or list of int or float
    :param b: A tuple or list containing the (x,y) coordinates of the second point.
    :type b: tuple or list of int or float
    :param c: A tuple or list containing the (x,y) coordinates of the third point.
    :type c: tuple or list of int or float
    :return: The angle in degrees between the line segments connecting point a to b and point b to c.
    :rtype: float
    """
    
    a = np.array(a) #First
    b = np.array(b) #Second
    c = np.array(c) #Third
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle

#Camera and it's Resolution

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Curl Counter Variables

counter = 0
stage = None

# Setup A Meadiapipe Instance

with mp_pose.Pose(min_detection_confidence = 0.55, min_tracking_confidence = 0.55) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
    #Detection and Rendering
        
        #Flipping the Image (To correct lateral inversion)
        
        frame = cv2.flip(frame, 1)
        
        #Recolour the Image to Mediapipe Format
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        #Make Detections
        
        results = pose.process(image)
        
        #Recolour the Image to cv2 Format
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        #Extract Landmarks
        
        try:
            landmarks = results.pose_landmarks.landmark
            #print(landmarks)
            
            #Get Coordinates
            
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            #Calculate Angle 
            
            angle = calculateAngle(shoulder, elbow, wrist)
            
            #Visualise the angle

            cv2.putText(image, str(angle),
                          tuple(np.multiply(elbow, [width,height]).astype(int)),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
                        )
            
            #Curl Counter Logic
            
            if(counter != 0):
                if(angle > 170):
                    cv2.putText(image, "Dont hyperextend your elbows, Extend upto your thighs", 
                                  tuple(np.multiply([0.6,0.2], [width,height]).astype(int)),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2, cv2.LINE_AA)
    
            if angle > 160:
                stage = "Down"
            if angle < 30 and stage == 'Down':
                stage = "Up"
                counter += 1
                #print(counter)
            
        except:
            pass
        
        #Render Curl Counter 
        
        #Setup Status Box
        
        cv2.rectangle(image, (0,0), (150,73), (245,117,16), -1)
        
        #Rep Data
        
        cv2.putText(image, "REPS", (15,20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA
                   )
        cv2.putText(image, str(counter), (20,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,63,125), 2, cv2.LINE_AA
                   )

        #Stage Data
        
        cv2.putText(image, "STAGE", (75,20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA
                   )
        if (stage == 'Up'):
            cv2.putText(image, stage, (78,60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,63,125), 2, cv2.LINE_AA
                       )
        else:
            cv2.putText(image, stage, (60,55),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,63,125), 2, cv2.LINE_AA
                       )
        
       #Render Detections

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color = (245,117,66), thickness = 2, circle_radius = 2),
                                 mp_drawing.DrawingSpec(color = (245,66,230), thickness = 2, circle_radius = 2)
                                 )
        
        #print(results)
        
        cv2.imshow("Mediapipe Feed", image)
        
        if(cv2.waitKey(10) & 0xFF == ord('q')):
            break
    
    cap.release()
    cv2.destroyAllWindows() 