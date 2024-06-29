import cv2
import mediapipe as mp
import pyautogui

# Initialize camera and hand detector
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

index_y = 0
middle_y = 0
ring_y = 0
pinky_y = 0
thumb_y = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:  # Index finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    pyautogui.moveTo(index_x, index_y)

                if id == 12:  # Middle finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    middle_x = screen_width / frame_width * x
                    middle_y = screen_height / frame_height * y

                if id == 16:  # Ring finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    ring_x = screen_width / frame_width * x
                    ring_y = screen_height / frame_height * y

                if id == 20:  # Pinky finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    pinky_x = screen_width / frame_width * x
                    pinky_y = screen_height / frame_height * y

                if id == 4:  # Thumb tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    # Debug information
                    print(f"Thumb Y: {thumb_y}, Index Y: {index_y}, Middle Y: {middle_y}, Ring Y: {ring_y}, Pinky Y: {pinky_y}")

                    # Check for gestures only if all necessary coordinates are updated
                    if index_y and middle_y and ring_y and pinky_y and thumb_y:
                        if abs(index_y - thumb_y) < 10:
                            print('Left Click')
                            pyautogui.click()
                            pyautogui.sleep(1)
                        elif abs(pinky_y - thumb_y) < 10:
                            print('Right Click')
                            pyautogui.rightClick()
                            pyautogui.sleep(1)
                        elif abs(middle_y - thumb_y) < 10:
                            print('Scroll Up')
                            pyautogui.scroll(100)
                            pyautogui.sleep(1)
                        elif abs(ring_y - thumb_y) < 10:
                            print('Scroll Down')
                            pyautogui.scroll(-100)
                            pyautogui.sleep(1)

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
