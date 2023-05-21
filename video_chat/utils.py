#!/usr/bin/env python3
import time
import cv2
import socket
import numpy as np
from config import *
import struct

class Fps:
    def __init__(self):
        self.time_prev = 0
        self.counter = 0
        self.fps = 0
    def calc_draw_fps(self, image):
        self.counter+=1
        if self.counter%FREQUENCY == 9:
            self.time_prev = time.time()
        if self.counter%FREQUENCY == 0: 
            self.counter = 0 # reset counter
            self.fps = int(1/(time.time() - self.time_prev))
        cv2.putText(image,"FPS:%d"%self.fps,FPS_POSITION,FPS_TEXT,1,FPS_COLOR,2)
        return image

def send_image(socket, image):
    encode_image = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])[1].tobytes()
    # encode_image = cv2.imencode('.jpg', np.zeros((480,640,3)).astype(np.uint8))[1].tobytes()
    ### tell the server(robot) how much data should it receive
    socket.sendall(len(encode_image).to_bytes(4, byteorder='big'))
    while len(encode_image) > 0: # encode_image will varies in the while loop, so cannot use encode_image_length
        ### send BYTE_PER_TIME bytes of data per time to avoid bottleneck and better manage the flow of data
        chunk = encode_image[:BYTE_PER_TIME]
        socket.sendall(chunk)
        encode_image = encode_image[BYTE_PER_TIME:]

def recv_image(socket):
    buffer = b''
    while True:
        data = socket.recv(BYTE_PER_TIME)

        ### close server and client simultaneously
        if not data: break
        
        buffer += data
        encode_image_length = int.from_bytes(buffer[:4], byteorder='big')
        if len(buffer) > encode_image_length + 4:
            encode_image = buffer[4:encode_image_length+4]
            buffer = buffer[encode_image_length+4:]
            image = np.frombuffer(encode_image, dtype=np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            cv2.imshow('recv_image', image)
            cv2.waitKey(1)

def send_pose(socket, pose):
    ### pose: can be a list or tuple contains FOUR floating points
    data = struct.pack('!4f', *pose)
    socket.sendall(data)

def recv_pose(socket):
    ### 32 means 32 byte. ASSUME one floating points is 64bit (8 bytes) in python. 4*8=32
    data = socket.recv(32)
    pose = struct.unpack('!4f', data)
    return pose

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1640,
    capture_height=1232,
    display_width=640,
    display_height=480,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )