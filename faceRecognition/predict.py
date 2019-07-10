# encoding:utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import cv2
from scipy import misc
import tensorflow as tf
import numpy as np
import os
from utils import file_processing,image_processing
import face_recognition
import faceRecognition.align.detect_face

resize_width = 160
resize_height = 160

def face_recognition_image(model_path,dataset_path, filename,image_path):
    # 加载数据库的数据
    dataset_emb,names_list=load_dataset(dataset_path, filename)
    # 初始化mtcnn人脸检测
    face_detect=face_recognition.Facedetection()
    # 初始化facenet
    face_net=face_recognition.facenetEmbedding(model_path)

    image = image_processing.read_image_gbk(image_path)
    # 获取 判断标识 bounding_box crop_image
    bboxes, landmarks = face_detect.detect_face(image)
    bboxes, landmarks = face_detect.get_square_bboxes(bboxes, landmarks, fixed="height")
    if bboxes == [] or landmarks == []:
        print("-----no face")
        exit(0)
    print("-----image have {} faces".format(len(bboxes)))
    face_images = image_processing.get_bboxes_image(image, bboxes, resize_height, resize_width)
    face_images = image_processing.get_prewhiten_images(face_images)
    pred_emb=face_net.get_embedding(face_images)
    pred_name,pred_score=compare_embadding(pred_emb, dataset_emb, names_list)
    # 在图像上绘制人脸边框和识别的结果
    show_info=[ n+':'+str(s)[:5] for n,s in zip(pred_name,pred_score)]
    print("showinfo 值为：",show_info)
    image_processing.show_image_bboxes_text("face_recognition", image,bboxes,show_info)



def face_recognition_image1(model_path,dataset_path, filename,frame):
    # 加载数据库的数据
    dataset_emb,names_list=load_dataset(dataset_path, filename)
    # 初始化mtcnn人脸检测
    face_detect=face_recognition.Facedetection()
    # 初始化facenet
    face_net=face_recognition.facenetEmbedding(model_path)

    image = image_processing.read_image1(frame)
    # 获取 判断标识 bounding_box crop_image
    bboxes, landmarks = face_detect.detect_face(image)
    bboxes, landmarks = face_detect.get_square_bboxes(bboxes, landmarks, fixed="height")
    if bboxes == [] or landmarks == []:
        print("-----no face")
        exit(0)
    print("-----image have {} faces".format(len(bboxes)))
    face_images = image_processing.get_bboxes_image(image, bboxes, resize_height, resize_width)
    face_images = image_processing.get_prewhiten_images(face_images)
    pred_emb=face_net.get_embedding(face_images)
    pred_name,pred_score=compare_embadding(pred_emb, dataset_emb, names_list)
    # 在图像上绘制人脸边框和识别的结果
    show_info=[ n+':'+str(s)[:5] for n,s in zip(pred_name,pred_score)]
    print("showinfo 值为：",show_info)
    image_processing.show_image_bboxes_text("face_recognition", image,bboxes,show_info)






def face_recognition_video(model_path,dataset_path, filename,video_path):
    # 加载数据库的数据
    dataset_emb, names_list = load_dataset(dataset_path, filename)
    # 初始化mtcnn人脸检测
    face_detect = face_recognition.Facedetection()
    # 初始化facenet
    face_net = face_recognition.facenetEmbedding(model_path)

    cap = cv2.VideoCapture(video_path)  # 获取视频数据
    face_cnt = 0  # 控制视频读取时候，每秒截取指定数量图片进行一次识别
    while cap.isOpened():
        ok, frame = cap.read()
        face_cnt += 1
        if not ok:
            break
        if(face_cnt % 5 == 0):
            frame = image_processing.read_image1(frame)
            bboxes, landmarks = face_detect.detect_face(frame)
            bboxes, landmarks = face_detect.get_square_bboxes(bboxes, landmarks, fixed="height")
            if bboxes == [] or landmarks == []:
                print("-----no face")
                continue
            print("-----image have {} faces".format(len(bboxes)))
            face_images = image_processing.get_bboxes_image(frame, bboxes, resize_height, resize_width)
            face_images = image_processing.get_prewhiten_images(face_images)
            pred_emb = face_net.get_embedding(face_images)
            pred_name, pred_score = compare_embadding(pred_emb, dataset_emb, names_list)
            # 在图像上绘制人脸边框和识别的结果
            show_info = [n + ':' + str(s)[:5] for n, s in zip(pred_name, pred_score)]
            print("showinfo:", show_info)
            image_processing.show_image_bboxes_text("face_recognition", frame, bboxes, show_info)

    cap.release()
    cv2.destroyWindow("face_recognition")




def load_dataset(dataset_path,filename):
    '''
    加载人脸数据库
    :param dataset_path: embedding.npy文件（faceEmbedding.npy）
    :param filename: labels文件路径路径（name.txt）
    :return:
    '''
    embeddings=np.load(dataset_path)
    names_list=file_processing.read_data(filename,split=None,convertNum=False)
    return embeddings,names_list

def compare_embadding(pred_emb, dataset_emb, names_list,threshold=0.65):
    # 为bounding_box 匹配标签
    pred_num = len(pred_emb)
    dataset_num = len(dataset_emb)
    pred_name = []
    pred_score=[]
    for i in range(pred_num):
        dist_list = []
        for j in range(dataset_num):
            dist = np.sqrt(np.sum(np.square(np.subtract(pred_emb[i, :], dataset_emb[j, :]))))
            dist_list.append(dist)
        min_value = min(dist_list)
        pred_score.append(min_value)
        if (min_value > threshold):
            pred_name.append('others')
        else:
            pred_name.append(names_list[dist_list.index(min_value)])
    return  pred_name,pred_score




if __name__=='__main__':
    model_path='models/20180408-102900'
    dataset_path='dataset/emb/faceEmbedding.npy'
    filename='dataset/emb/name.txt'
    image_path='dataset/test_images/t (5).jpg'
    video_path=r'C:\Users\SAM\Pictures\Camera Roll\胡歌.mp4'
    # video_path=r'D:\2019农行实习\人脸识别竞赛\A榜视频200个\004.avi'
    # face_recognition_image(model_path, dataset_path, filename,image_path)
    face_recognition_video(model_path, dataset_path, filename, 0)
    