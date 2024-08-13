import cv2
import mediapipe as mp
import numpy as np
import csv
# import pandas
# Initialize MediaPipe Hands
mp_h = mp.solutions.hands
hands_model = mp_h.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                         min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Placeholder calibration data (to be replaced with actual calibration data)
cal_data = {
    'Thumb': 6,  # Example: Actual physical distance for Thumb
    'Index': 8.2,  # Example: Actual physical distance for Index finger
    'Middle': 9.3,  # Example: Actual physical distance for Middle finger
    'Ring': 8.5,  # Example: Actual physical distance for Ring finger
    'Pinky': 6.8  # Example: Actual physical distance for Pinky finger
}


# Function to detect hands, draw outlines, and measure finger dimensions
# Function to detect hands, draw outlines, and measure finger dimensions
# Function to detect hands, draw outlines, and measure finger dimensions
def detect_hands_and_fingers(frame, csv_file):
    # Convert frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe Hands
    results = hands_model.process(frame_rgb)

    # Flag to indicate if finger dimensions have been written to CSV
    dimensions_written = False

    # Check if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Measure finger dimensions in centimeters if palm distance is close to desired value
            palm_distance = measure_palm_distance(hand_landmarks)
            if np.isclose(palm_distance, 0.82, atol=0.02) and not dimensions_written:
                finger_dims = calculate_finger_dimensions(hand_landmarks)
                # Write finger dimensions to CSV file
                try:
                    with open(csv_file, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Finger", "Dimension (cm)"])
                        for finger, dim in finger_dims.items():
                            writer.writerow([finger, dim])
                        print("Finger dimensions written to CSV successfully.")  # Debugging statement
                    dimensions_written = True
                except Exception as e:
                    print("Error writing to CSV:", e)

            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_h.HAND_CONNECTIONS)

            # Display palm distance message
            if np.isclose(palm_distance, 0.82, atol=0.02):
                for i, (finger, dim) in enumerate(finger_dims.items()):
                    cv2.putText(frame, f'{finger} Dimension: {dim:.2f} cm', (10, 30 + i * 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(frame, f'Adjust palm distance to 0.82 cm', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 255), 2)


# Function to calculate palm distance from the screen based on index finger tip landmark
def measure_palm_distance(hand_landmarks):
    # Extract palm landmark (wrist)
    palm_landmark = hand_landmarks.landmark[mp_h.HandLandmark.WRIST]
    # Extract index finger tip landmark
    index_tip_landmark = hand_landmarks.landmark[mp_h.HandLandmark.INDEX_FINGER_TIP]
    # Calculate Euclidean distance between palm and index finger tip
    palm_distance = np.sqrt((palm_landmark.x - index_tip_landmark.x) ** 2 +
                            (palm_landmark.y - index_tip_landmark.y) ** 2 +
                            (palm_landmark.z - index_tip_landmark.z) ** 2)
    return palm_distance


# Function to calculate finger dimensions
def calculate_finger_dimensions(hand_landmarks):
    finger_dims = {}
    for finger, landmarks in finger_landmarks.items():
        # Get the landmark indices representing the tip and base of the finger
        tip_index = mp_h.HandLandmark[landmarks['Tip']].value
        base_index = mp_h.HandLandmark[landmarks['Base']].value

        # Get the landmarks for the tip and base
        tip_lm = hand_landmarks.landmark[tip_index]
        base_lm = hand_landmarks.landmark[base_index]

        # Calculate the pixel distance between the tip and base landmarks
        px_distance = np.linalg.norm(np.array([tip_lm.x, tip_lm.y]) -
                                     np.array([base_lm.x, base_lm.y]))

        # Convert pixel distance to physical distance in centimeters using calibration data
        conv_factor = cal_data[finger]
        finger_dims[finger] = px_distance * conv_factor * 2.3

    return finger_dims


# Define finger landmarks for each finger
finger_landmarks = {
    'Thumb': {'Tip': 'THUMB_TIP', 'Base': 'WRIST'},
    'Index': {'Tip': 'INDEX_FINGER_TIP', 'Base': 'INDEX_FINGER_MCP'},
    'Middle': {'Tip': 'MIDDLE_FINGER_TIP', 'Base': 'MIDDLE_FINGER_MCP'},
    'Ring': {'Tip': 'RING_FINGER_TIP', 'Base': 'RING_FINGER_MCP'},
    'Pinky': {'Tip': 'PINKY_TIP', 'Base': 'PINKY_MCP'}
}


# Main function
def Fing_Measure():
    # Capture video from webcam
    cap = cv2.VideoCapture(0)

    # Define the CSV file path
    csv_file = "finger_values.csv"

    while True:
        # Read frame from webcam
        ret, frame = cap.read()

        if not ret:
            print("Error reading frame from webcam.")
            break

        # Detect hands, draw outlines, and measure finger dimensions
        detect_hands_and_fingers(frame, csv_file)

        # Display frame
        cv2.imshow('Hand Tracking', frame)

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release capture and destroy windows
    cap.release()
    cv2.destroyAllWindows()


# Execute main function
if __name__ == '__main__':

    Fing_Measure()
