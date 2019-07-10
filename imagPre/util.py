import os
import sys
import math
import random
import functools
import numpy as np
from PIL import Image, ImageEnhance

def rotate(img_path, degree, num):
    img = Image.open(img_path)
    
    save_path = './rotate/'
    mkdir(save_path)

    i = 1
    while i <= num:
        img = img.rotate(degree)
        img_arr = os.path.basename(img_path).split('.')
        img_name = save_path + img_arr[0] + '_' + str(degree * i) + '.' + img_arr[1]
        img.save(img_name, quality=95)
        i += 1
        print('save to ' + img_name)



def randomCrop(img_path, size, cnt,scale=[0.08, 1.0], ratio=[3. / 4., 4. / 3.]):
    img = Image.open(img_path)
    aspect_ratio = math.sqrt(np.random.uniform(*ratio))
    w = 1. * aspect_ratio
    h = 1. / aspect_ratio

    bound = min((float(img.size[0]) / img.size[1]) / (w**2),
                (float(img.size[1]) / img.size[0]) / (h**2))
    scale_max = min(scale[1], bound)
    scale_min = min(scale[0], bound)

    target_area = img.size[0] * img.size[1] * np.random.uniform(scale_min,
                                                             scale_max)
    target_size = math.sqrt(target_area)
    w = int(target_size * w)
    h = int(target_size * h)

    i = np.random.randint(0, img.size[0] - w + 1)
    j = np.random.randint(0, img.size[1] - h + 1)

    img = img.crop((i, j, i + w, j + h))
    img = img.resize((size, size), Image.LANCZOS)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    save_path = './random_crop/'
    mkdir(save_path)
    img_name = save_path + str(cnt) + os.path.basename(img_path)
    img.save(img_name, quality=95)
    print('save to ' + img_name)
    return img

def resize(img_path, size):
    img = Image.open(img_path)

    img = img.resize((size, size), Image.ANTIALIAS)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    # save_path = './resize_' + bytes(size) + '/'
    save_path = './resize_' + str(size) + '/'
    mkdir(save_path)
    img_name = save_path + os.path.basename(img_path)
    img.save(img_name, quality=95)
    print('save to ' + img_name)
    return img

def convertToRGB(img_path):
    img = Image.open(img_path)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    save_path = './convert/'
    mkdir(save_path)
    img_name = save_path + os.path.basename(img_path)
    img.save(img_name, quality=95)
    print('save to ' + img_name)
    return img

def convertToL(img_path):
    #a = np.array(Image.open(img_path).convert('L')).astype('float')
    # 
    #depth = 10.
    #grad = np.gradient(a)
    #grad_x, grad_y = grad
    # 
    #grad_x = grad_x*depth/100.
    #grad_y = grad_y*depth/100.
    #A = np.sqrt(grad_y**2+grad_y**2+1)
    #uni_x = grad_x/A
    #uni_y = grad_y/A
    #uni_z = 1./A
    # 
    #vec_el = np.pi/2.2
    #vec_az = np.pi/4
    #dx = np.cos(vec_el)*np.cos(vec_az)
    #dy = np.cos(vec_el)*np.sin(vec_az)
    #dz = np.sin(vec_el)
    # 
    #b = 255*(dx*uni_x+dy*uni_y+dz*uni_z)
    #b = b.clip(0, 225)
    # 
    #im = Image.fromarray(b.astype('uint8'))
    # 

    im = Image.open(img_path)
    im = im.convert('L')
    save_path = './toL/'
    mkdir(save_path)
    img_name = save_path + os.path.basename(img_path)
    print('success save to ' + img_name)
    im.save(img_name, quality=95)

def convertTo1(img_path, threshold):
    im = Image.open(img_path)
    Lim = im.convert('L' )

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    
    bim = Lim.point(table, '1' )

    save_path = './to_binarization/'
    mkdir(save_path)
    img_arr = os.path.basename(img_path).split('.')
    img_name = save_path + img_arr[0] + '__' + str(threshold) + '.' + img_arr[1]

    print('success save to ' + img_name)

    bim.save(img_name, quality=95)

def imgList(dir, suffix = '.jpg'):
    
    assert os.path.isdir(dir)

    list = []
    for file in os.listdir(dir):
        img_path = os.path.join(dir, file)
        if os.path.splitext(img_path)[1] == ".jpg":
            list.append(img_path)
    return list

def mkdir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

if __name__ == '__main__':
    resize(r"./test",500)
