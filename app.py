import cv2
import mediapipe as mp


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    frame = cv2.flip(frame, 1)
    
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
           
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark

            fingers = []

            if lm[4].x < lm[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

           
            tip_ids = [8, 12, 16, 20]
            for tip in tip_ids:
                if lm[tip].y < lm[tip - 2].y: 
                    fingers.append(1)
                else:
                    fingers.append(0)

            number = "0"

            if fingers == [0, 1, 0, 0, 0]:
                number = "1"
            elif fingers == [0, 1, 1, 0, 0]:
                number = "2"
            elif fingers == [0, 1, 1, 1, 0]:
                number = "3"
            elif fingers == [0, 1, 1, 1, 1]:
                number = "4"
            elif fingers == [1, 1, 1, 1, 1]:
                number = "5"
            elif fingers == [1, 1, 1, 1, 0]:
                number = "6"
            elif fingers == [1, 1, 1, 0, 1]:
                number = "7"
            elif fingers == [1, 1, 0, 1, 1]:
                number = "8"
            elif fingers == [1, 0, 1, 1, 1]:
                number = "9"
            elif fingers == [1, 0, 0, 0, 0]:
                number = "10"

            cv2.putText(frame, f"COUNT: {number}", (30, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (128, 0, 128), 3)

    # Render window
    cv2.imshow("Gesture Control", frame)


    if cv2.waitKey(1) & 0xFF == ord('w'):
        break

cap.release()
cv2.destroyAllWindows()