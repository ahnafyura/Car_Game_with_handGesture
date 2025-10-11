import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0) 
        if not self.cap.isOpened():
            raise IOError("Tidak bisa membuka webcam. Pastikan tidak sedang digunakan aplikasi lain.")

        self.hands = mp.solutions.hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.drawing_utils = mp.solutions.drawing_utils
        
        # --- PERBAIKAN BUG #4: DEFINISIKAN WARNA KUSTOM UNTUK LANDMARK ---
        # Landmark (titik) akan berwarna hijau, koneksi (garis) akan berwarna putih
        self.landmark_drawing_spec = self.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3) # Hijau
        self.connection_drawing_spec = self.drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=2) # Putih

    def get_steering_input(self):
        success, frame = self.cap.read()
        if not success:
            return 0, None

        frame = cv2.flip(frame, 1) 
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        steering_input = 0 
        
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
            hands_landmarks = results.multi_hand_landmarks
            
            hand1_x = hands_landmarks[0].landmark[0].x
            hand2_x = hands_landmarks[1].landmark[0].x
            
            if hand1_x < hand2_x: 
                left_hand = hands_landmarks[0]
                right_hand = hands_landmarks[1]
            else:
                left_hand = hands_landmarks[1]
                right_hand = hands_landmarks[0]

            left_index_y = left_hand.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y
            right_index_y = right_hand.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y

            y_diff = left_index_y - right_index_y 
            
            deadzone = 0.08 
            if y_diff > deadzone: 
                steering_input = -1 
            elif y_diff < -deadzone: 
                steering_input = 1 
            
            # --- PERBAIKAN BUG #4: GAMBAR LANDMARK DENGAN WARNA KUSTOM ---
            self.drawing_utils.draw_landmarks(
                frame, left_hand, mp.solutions.hands.HAND_CONNECTIONS,
                self.landmark_drawing_spec, self.connection_drawing_spec)
            self.drawing_utils.draw_landmarks(
                frame, right_hand, mp.solutions.hands.HAND_CONNECTIONS,
                self.landmark_drawing_spec, self.connection_drawing_spec)

        return steering_input, frame

    def release(self):
        self.cap.release()