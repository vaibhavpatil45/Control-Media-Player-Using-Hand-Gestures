import cv2
import numpy as np
import streamlit as st
import pyautogui
import time
import mediapipe as mp




def count_fingers(lst):
    cnt = 0
    thresh = (lst.landmark[0].y*100 - lst.landmark[9].y*100)/2

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:
        cnt += 1

    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) > thresh:
        cnt += 1

    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) > thresh:
        cnt += 1

    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) > thresh:
        cnt += 1

    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 6:
        cnt += 1


    return cnt 



def main():
    html_temp = """
    <div style="background-color:#f63366 ;padding:10px;margin-bottom:10px;">
    <h2 style="color:white;text-align:center;">Media Player Controler Using Hand Gestures</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    st.sidebar.title("Pages")
    # Add a selectbox to the sidebar:
    pages=['About Web App','Gesture Control Page']
    add_pages = st.sidebar.selectbox('', pages)

    st.sidebar.title("Made By:")
    html_temp6 = """
<ul style="font-weight:bold;">
<li>Sanskruti Ghadage</li>
<li>Shubham Palkar </li>
<li>Vaibhav Patil</li>
</ul>
    """
    st.sidebar.markdown(html_temp6, unsafe_allow_html=True)

    if add_pages=='About Web App':
        html_temp2 = """
    <body style="background-color:white;padding:10px;">
    <h3 style="color:#f63366 ;text-align:center;">About Web App</h3>
    The Main aim of this application is to use the most natural form i.e., Hand gestures to interact with the
computer system. These gestures are implemented in such a way that they are easy to perform, fast,
efficient and ensuring an immediate response.
The application uses your device's camera to give you touch-free and remote-free control over your media player application
(without any special hardware).It increases productivity and makes life easier and comfortable by
letting you control your device from a distance.

</body>
<div style="background-color:black;padding:10px;margin-bottom:10px;">
<h4 style="color:white;">Prepared using:</h4>
<ul style="color:white;">
<li>Opencv </li>
<li>MediaPipe </li>
<li>Streamlit </li>
<li>PyAutoGUI  </li>
</ul>
</div>
"""
        st.markdown(html_temp2, unsafe_allow_html=True)

    # elif add_pages =='Project Demo':
    #     html_temp3 = """
    # <body style="background-color:white;padding:5px;">
    # <h3 style="color:#f63366 ;text-align:center;">Demo of using Hand gestures to control Media player</h3>
    # """
    #     st.markdown(html_temp3, unsafe_allow_html=True)
    #     st.video("Demo.mp4")


    elif add_pages =='Gesture Control Page':
        html_temp5 = """
    <body style="background-color:white;padding:5px;">
    <h3 style="color:#f63366 ;text-align:center;">Control Media player using Hand Gestures </h3>
        <ul> Gestures and their Function
        <li>✋ or 🤚 : Palm : Play / Pause</li>
         <li>☝️: One Finger: Forward </li>
        <li>✌️: Two Finger: Rewind </li>
        <li>💅: Three Finger: Volume up</li>
        <li>✋: Four Finger: Volume Down </li>
        <li>No Hand : No gesture: No action  </li>
        </ul>
    """
        st.markdown(html_temp5, unsafe_allow_html=True)
        run = st.button('Start Web Camera')
        FRAME_WINDOW1 = st.image([])
        FRAME_WINDOW2 = st.image([])
        drawing = mp.solutions.drawing_utils
        hands = mp.solutions.hands
        hand_obj = hands.Hands(max_num_hands=1)
        start_init = False 
        prev = -1
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        #st.write("Test image")
        while run:
            end_time = time.time()
            rs, frm = camera.read()

            # Simulating mirror image
            res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
            raisedfingercount = 0
            if res.multi_hand_landmarks:
                            hand_keyPoints = res.multi_hand_landmarks[0]
                            cnt = count_fingers(hand_keyPoints)
                            raisedfingercount = cnt
                            drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)
                            if not(prev==cnt):
                                if not(start_init):
                                    start_time = time.time()
                                    start_init = True

                                elif (end_time-start_time) > 0.2:
                                    if (cnt == 1):
                                        pyautogui.press("right")
                                    
                                    elif (cnt == 2):
                                        pyautogui.press("left")

                                    elif (cnt == 3):
                                        pyautogui.press("up")

                                    elif (cnt == 4):
                                        pyautogui.press("down")

                                    elif (cnt == 5):
                                        pyautogui.press("space")

                                    prev = cnt
                                    start_init = False

                # Displaying the predictiont
                            # rc = raisedfingercount
                            # rc = str(rc)
                            # cv2.putText(frm, 'Raised Finger Count is '+ rc, (10, 220), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0), 1)
                            # raisedfingercount = 0
                                
            FRAME_WINDOW2.image(frm)
        camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
