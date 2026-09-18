import cv2
import mediapipe as mp
import Utils
import serial
import time

ser = serial.Serial('your port name' , 115200 , timeout=1)
time.sleep(1)

mpHands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mpHands.Hands(
    max_num_hands = 1,
    min_detection_confidence = 0.6,
    min_tracking_confidence = 0.6
)

cap = cv2.VideoCapture(0)

while True:
    ret , frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame , 1)
    height , width , _ = frame.shape
    rgb_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks,result.multi_handedness):

            ThumbFingerState , IndexFingerState , MiddleFingerState , RingFingerState , PinkyFingerState = map(str , map(int , Utils.FingerController(hand_landmarks , handedness)))

            label = handedness.classification[0].label
            middle_tip = hand_landmarks.landmark[12]

            Data = str()
            if (label=="Right"):
                Data = ThumbFingerState + IndexFingerState + MiddleFingerState + RingFingerState + PinkyFingerState + "\n"
            else:
                Data = PinkyFingerState + RingFingerState + MiddleFingerState + IndexFingerState + ThumbFingerState + "\n"

            BinaryData = Data.encode('utf-8')

            x_pos = int(width * middle_tip.x)
            y_pos = int(height * middle_tip.y)

            FingersStatesText = f"T:{str(ThumbFingerState):<5} I:{str(IndexFingerState):<5} M:{str(MiddleFingerState):<5} R:{str(RingFingerState):<5} P:{str(PinkyFingerState):<5}"

            ser.write(BinaryData)
            cv2.putText(frame , FingersStatesText , (15 , 40) , fontFace=cv2.FONT_HERSHEY_SIMPLEX , color=(255,0,0) , fontScale=1 , thickness=2)
            cv2.putText(frame , label , (x_pos , y_pos - 15) , fontFace=cv2.FONT_HERSHEY_SIMPLEX , color=(0,255,0) , fontScale=1 , thickness=2)

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mpHands.HAND_CONNECTIONS
            )

    cv2.imshow("Hello!" , frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
hands.close()
ser.close()
cv2.destroyAllWindows()