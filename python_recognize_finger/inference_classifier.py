import pickle

import cv2
import mediapipe as mp
import numpy as np
import time

from paho.mqtt import client as mqtt_client
import json
broker = 'test.mosquitto.org'
#broker = '192.168.43.252'
port = 1883
topic = 'hand_wait'
topic_sub = 'lis_hand'
# generate client ID with pub prefix randomly
client_id = ''
username = ''
password = ''
deviceId = ""

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc==0:
            print("Successfully connected to MQTT broker")
        else:
            print("Failed to connect, return code %d", rc)
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
def publish(client, status):
    msg = 'hand_wait'
    result = client.publish(msg,f'{status}')
    msg_status = result[0]
    if msg_status ==0:
        print(f"message : {msg} sent to topic {topic}")
    else:
        print(f"Failed to send message to topic {topic}")
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Recieved '{msg.payload.decode()}' from '{msg.topic}' topic")
        #y = json.loads(msg.payload.decode())
        #temp = y["notification"]["parameters"]["temp"]
        #hum = y["notification"]["parameters"]["humi"]
        #print("temperature: ",temp,", humidity:",hum)
    client.subscribe(topic_sub)
    client.on_message = on_message



model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: 'OFF', 1: 'ON', 2: 'NOTHING'}
tam = 'OFF'
client = connect_mqtt()
while True:
    subscribe(client)
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10

        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        prediction = model.predict([np.asarray(data_aux)])

        predicted_character = labels_dict[int(prediction[0])]
        print(predicted_character)
        if(predicted_character == 'OFF'): #and predicted_character!= tam):
            tam = predicted_character
            publish(client, 'off')

        if (predicted_character == 'ON'): #and predicted_character!= tam):
            tam = predicted_character
            publish(client, 'on')
        if (predicted_character == 'NOTHING'): #and predicted_character!= tam):
            tam = predicted_character
            publish(client, 'nothing')
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)


cap.release()
cv2.destroyAllWindows()
