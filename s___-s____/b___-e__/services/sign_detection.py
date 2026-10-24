
import cv2
import mediapipe as mp


class SignDetector:
    def __init__(self, detection_confidence=0.6, tracking_confidence=0.6):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

    def detect(self, frame):
        """
        Process one OpenCV BGR frame.

        Returns:
            annotated_frame: frame with detected hand landmarks
            results: MediaPipe hand detection results
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame, results

    def close(self):
        """Release MediaPipe resources."""
        self.hands.close()


def run_webcam():
    """Run a local webcam hand-landmark detection demo."""
    detector = SignDetector()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        detector.close()
        return

    print("Hand detection started. Press Q to quit.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Error: Could not read webcam frame.")
                break

            # Mirror the image for a more natural preview.
            frame = cv2.flip(frame, 1)
            annotated_frame, results = detector.detect(frame)

            if results.multi_hand_landmarks:
                cv2.putText(
                    annotated_frame,
                    "Hand detected",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
            else:
                cv2.putText(
                    annotated_frame,
                    "Show your hand",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2
                )

            cv2.imshow("SignSpeak - Hand Detection", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        detector.close()


if __name__ == "__main__":
    run_webcam()
