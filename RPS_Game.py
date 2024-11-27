import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import streamlit as st
from PIL import Image
import numpy as np

# Set up Streamlit
st.title("Rock-Paper-Scissors Game")
st.write("Play Rock-Paper-Scissors using hand gestures!")
st.sidebar.header("Game Controls")

# Game States
if "start_game" not in st.session_state:
    st.session_state.start_game = False
if "scores" not in st.session_state:
    st.session_state.scores = [0, 0]  # [AI Score, Player Score]

# Detector setup
detector = HandDetector(maxHands=1)

# Load background image
imgBG = cv2.imread("RPS_Resources/BG.png")

# Start Game
if st.sidebar.button("Start Game"):
    st.session_state.start_game = True
    st.session_state.initial_time = time.time()
    st.session_state.state_result = False
    st.session_state.timer = 0
    st.session_state.ai_move = None

# Capture player input
camera_input = st.camera_input("Take a photo to play!")

if camera_input:
    # Convert to OpenCV image
    file_bytes = np.asarray(bytearray(camera_input.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    # Resize and crop
    imagescaled = cv2.resize(img, (0, 0), fx=0.875, fy=0.875)
    imagescaled = imagescaled[:, 80:480]

    # Detect hands
    hands, img = detector.findHands(imagescaled)

    if st.session_state.start_game:
        # Timer logic
        if not st.session_state.state_result:
            st.session_state.timer = time.time() - st.session_state.initial_time
            st.write(f"Timer: {int(st.session_state.timer)} seconds")

        if st.session_state.timer > 3:
            st.session_state.state_result = True
            st.session_state.timer = 0

            if hands:
                # Detect player move
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                playermove = None
                if fingers == [0, 0, 0, 0, 0]:
                    playermove = 1  # Rock
                elif fingers == [1, 1, 1, 1, 1]:
                    playermove = 2  # Paper
                elif fingers in ([0, 1, 1, 0, 0], [1, 1, 1, 0, 0]):
                    playermove = 3  # Scissors

                # Generate AI move
                st.session_state.ai_move = random.randint(1, 3)
                imgAI = cv2.imread(f"RPS_Resources/{st.session_state.ai_move}.png", cv2.IMREAD_UNCHANGED)

                # Determine winner
                if (playermove == 1 and st.session_state.ai_move == 3) or \
                   (playermove == 2 and st.session_state.ai_move == 1) or \
                   (playermove == 3 and st.session_state.ai_move == 2):
                    st.session_state.scores[1] += 1  # Player wins
                elif (st.session_state.ai_move == 1 and playermove == 3) or \
                     (st.session_state.ai_move == 2 and playermove == 1) or \
                     (st.session_state.ai_move == 3 and playermove == 2):
                    st.session_state.scores[0] += 1  # AI wins

    # Overlay AI move on background
    if st.session_state.state_result and st.session_state.ai_move:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # Display scores
    cv2.putText(imgBG, str(st.session_state.scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 6)
    cv2.putText(imgBG, str(st.session_state.scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 6)

    # Render the final image in Streamlit
    st.image(imgBG, channels="BGR", caption="Game Background")

# Display final scores
st.sidebar.write(f"AI Score: {st.session_state.scores[0]}")
st.sidebar.write(f"Player Score: {st.session_state.scores[1]}")
