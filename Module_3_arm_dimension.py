import cv2
import mediapipe as mp
import math
import csv

def ARM_DIM(frame, distance_text, csv_writer):
    # Initialize Mediapipe Pose model
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Camera parameters (field of view or distance to subject)
    # Adjust these values according to your camera setup
    field_of_view_degrees = 68.8  # Assuming a field of view of 68.8 degrees (in degrees)
    distance_to_subject_cm = 100  # Assuming a distance of 100 cm (in centimeters)

    # Convert frame to RGB (Mediapipe requires RGB input)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform pose estimation
    results = pose.process(frame_rgb)

    # Extract landmarks if pose is detected
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Get landmark coordinates for left and right wrist, elbow, and shoulder
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]

        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        # Calculate distances for left arm in pixels
        left_wrist_to_elbow_px = math.sqrt((left_elbow.x - left_wrist.x) ** 2 + (left_elbow.y - left_wrist.y) ** 2)
        left_elbow_to_shoulder_px = math.sqrt(
            (left_shoulder.x - left_elbow.x) ** 2 + (left_shoulder.y - left_elbow.y) ** 2)

        # Calculate distances for right arm in pixels
        right_wrist_to_elbow_px = math.sqrt((right_elbow.x - right_wrist.x) ** 2 + (right_elbow.y - right_wrist.y) ** 2)
        right_elbow_to_shoulder_px = math.sqrt(
            (right_shoulder.x - right_elbow.x) ** 2 + (right_shoulder.y - right_elbow.y) ** 2)

        # Convert pixel distances to centimeters
        # Use trigonometry to calculate the conversion factor based on camera parameters
        frame_height, frame_width, _ = frame.shape
        focal_length_px = (frame_width / 2) / math.tan(math.radians(field_of_view_degrees / 2))
        pixel_size_cm = (distance_to_subject_cm * 2 * math.tan(math.radians(field_of_view_degrees / 2))) / frame_width
        conversion_factor = distance_to_subject_cm / distance_text  # Use the provided distance_text
        left_wrist_to_elbow_cm = (left_wrist_to_elbow_px * pixel_size_cm / conversion_factor)*150000
        left_elbow_to_shoulder_cm = (left_elbow_to_shoulder_px * pixel_size_cm / conversion_factor)*150000
        right_wrist_to_elbow_cm = (right_wrist_to_elbow_px * pixel_size_cm / conversion_factor)*150000
        right_elbow_to_shoulder_cm = (right_elbow_to_shoulder_px * pixel_size_cm / conversion_factor)*150000

        # Draw circles only on the left and right wrist, elbow, and shoulder landmarks
        cv2.circle(frame, (int(left_wrist.x * frame_width), int(left_wrist.y * frame_height)), 5, (0, 255, 0), -1)
        cv2.circle(frame, (int(left_elbow.x * frame_width), int(left_elbow.y * frame_height)), 5, (0, 255, 0), -1)
        cv2.circle(frame, (int(left_shoulder.x * frame_width), int(left_shoulder.y * frame_height)), 5, (0, 255, 0), -1)
        cv2.circle(frame, (int(right_wrist.x * frame_width), int(right_wrist.y * frame_height)), 5, (0, 255, 0), -1)
        cv2.circle(frame, (int(right_elbow.x * frame_width), int(right_elbow.y * frame_height)), 5, (0, 255, 0), -1)
        cv2.circle(frame, (int(right_shoulder.x * frame_width), int(right_shoulder.y * frame_height)), 5, (0, 255, 0),
                   -1)

        # Draw lines for left arm
        cv2.line(frame, (int(left_wrist.x * frame_width), int(left_wrist.y * frame_height)),
                 (int(left_elbow.x * frame_width), int(left_elbow.y * frame_height)), (255, 0, 0), 2)
        cv2.line(frame, (int(left_elbow.x * frame_width), int(left_elbow.y * frame_height)),
                 (int(left_shoulder.x * frame_width), int(left_shoulder.y * frame_height)), (255, 0, 0), 2)

        # Draw lines for right arm
        cv2.line(frame, (int(right_wrist.x * frame_width), int(right_wrist.y * frame_height)),
                 (int(right_elbow.x * frame_width), int(right_elbow.y * frame_height)), (255, 0, 0), 2)
        cv2.line(frame, (int(right_elbow.x * frame_width), int(right_elbow.y * frame_height)),
                 (int(right_shoulder.x * frame_width), int(right_shoulder.y * frame_height)), (255, 0, 0), 2)

        # Display dimensions in centimeters
        cv2.putText(frame,
                    f"Left Hand: Wrist to Elbow: {left_wrist_to_elbow_cm:.2f} cm, Elbow to Shoulder: {left_elbow_to_shoulder_cm:.2f} cm",
                    (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame,
                    f"Right Hand: Wrist to Elbow: {right_wrist_to_elbow_cm:.2f} cm, Elbow to Shoulder: {right_elbow_to_shoulder_cm:.2f} cm",
                    (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Write dimensions to CSV file
        csv_writer.writerow([
            left_wrist_to_elbow_cm, left_elbow_to_shoulder_cm,
            right_wrist_to_elbow_cm, right_elbow_to_shoulder_cm
        ])

    return frame

def DISTFROMSCREEN():
    # Initialize Mediapipe Pose model
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    # Initialize video capture
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    # Camera parameters (field of view or distance to subject)
    # Adjust these values according to your camera setup
    field_of_view_degrees = 68.8  # Assuming a field of view of 68.8 degrees (in degrees)
    distance_to_subject_cm = 100  # Assuming a distance of 100 cm (in centimeters)

    # Open CSV file for writing
    with open('arm_values.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Left Wrist to Elbow (cm)', 'Left Elbow to Shoulder (cm)',
                             'Right Wrist to Elbow (cm)', 'Right Elbow to Shoulder (cm)'])

        while True:
            # Read frame from the camera
            ret, frame = cap.read()

            # Convert frame to RGB (Mediapipe requires RGB input)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform pose estimation
            results = pose.process(frame_rgb)

            # Extract landmarks if pose is detected
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                # Get landmark coordinates for nose and chest
                nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
                chest = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]

                # Calculate distance from screen in meters
                # Assume nose depth to be the Z-coordinate of the nose landmark
                nose_depth_cm = abs(nose.z) * distance_to_subject_cm
                distance_meters = nose_depth_cm / 100  # Convert centimeters to meters

                # Draw line from screen touching the chest
                # Calculate endpoint of the line based on chest position
                endpoint_x = int(chest.x * frame.shape[1])
                endpoint_y = int(chest.y * frame.shape[0])

                # Draw the line
                cv2.line(frame, (frame.shape[1] // 2, frame.shape[0] // 2), (endpoint_x, endpoint_y), (255, 0, 0), 2)

                # Display distance from screen in meters
                distance_text = f"Distance from screen: {distance_meters:.2f} m"
                cv2.putText(frame, distance_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Check user's distance from the screen
                if distance_meters < 0.5:
                    cv2.putText(frame, "Move backward", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                elif distance_meters > 0.7:
                    cv2.putText(frame, "Move closer", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    # Proceed with arm length measurements only when the person is approximately 0.60m away from the screen
                    desired_distance_cm = 60  # Desired distance from the screen in centimeters
                    if math.isclose(distance_meters, desired_distance_cm / 100, rel_tol=0.01):
                        frame = ARM_DIM(frame, distance_meters, csv_writer)

            # Display the resulting frame
            cv2.imshow('Pose Estimation', frame)

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

# Call the main function
DISTFROMSCREEN()
