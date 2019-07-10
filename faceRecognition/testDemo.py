# -*- coding: utf-8 -*-
# @Time    : 2019/6/17 15:23
# @Author  : LiJinjin
# @Email   : 1484972292@qq.com
# @File    : test1.py
# @Software: PyCharm
import sys
sys.path.append("..")

import cv2
import tensorflow as tf
import faceRecognition.align.detect_face

def test():
    # video = cv2.VideoCapture(0)
    # video = cv2.VideoCapture(r"C:\Users\SAM\Pictures\abctest\007.mp4")
    video = cv2.VideoCapture(r"D:\2019农行实习\人脸识别竞赛\A榜视频200个\004.avi")
    print('Creating networks and loading parameters')

    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = faceRecognition.align.detect_face.create_mtcnn(sess, None)
    minsize = 20
    threshold = [0.6, 0.7, 0.7]
    factor = 0.709
    while True:
        ret, frame = video.read()
        bounding_boxes, _ = faceRecognition.align.detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
        nrof_faces = bounding_boxes.shape[0]
        print('找到人脸数目为:{}'.format(nrof_faces))
        for face_position in bounding_boxes:
            face_position = face_position.astype(int)
            cv2.rectangle(frame, (face_position[0], face_position[1]), (face_position[2], face_position[3]),
                          (0, 255, 0), 2)
        cv2.imshow('show', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test()