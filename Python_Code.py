import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import serial

# Initialize serial port for Arduino communication
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)

cap = cv2.VideoCapture(0)  # Start video capture
cap.set(3, 640)  # Width of the frame
cap.set(4, 480)  # Height of the frame

detector = HandDetector(maxHands=1)  # Initialize hand detector

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # Scores list for AI and player

while True:
    imgBG = cv2.imread("Resources/BG.png")  # Load background image
    success, img = cap.read()  # Read image from camera

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)  # Scale down image
    imgScaled = imgScaled[:, 80:480]  # Crop image

    hands, img = detector.findHands(imgScaled)  # Detect hands

    # Start game on signal from Arduino
    if arduino.in_waiting > 0:
        signal = arduino.readline().decode('utf-8').strip()
        if signal == 'S':
            startGame = True
            initialTime = time.time()
            stateResult = False

    if startGame:
        if not stateResult:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)  # Get finger state
                    playerMove = None  # Default no move
                    # Assign moves based on finger patterns
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # Rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # Paper
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # Scissors

                    randomNumber = random.randint(1, 3)  # AI random move
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Determine winner
                    if ((playerMove == 1 and randomNumber == 3) or
                            (playerMove == 2 and randomNumber == 1) or
                            (playerMove == 3 and randomNumber == 2)):
                        scores[1] += 1  # Player wins
                        arduino.write(b'P')

                    elif ((playerMove == 3 and randomNumber == 1) or
                            (playerMove == 1 and randomNumber == 2) or
                            (playerMove == 2 and randomNumber == 3)):
                        scores[0] += 1  # AI wins
                        arduino.write(b'A')

    imgBG[234:654, 795:1195] = imgScaled  # Place scaled image in background

    # Update scores on display
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG", imgBG)  # Show the game background

    key = cv2.waitKey(1)
    if key == ord('q'):  # Quit on 'q' key
        break
