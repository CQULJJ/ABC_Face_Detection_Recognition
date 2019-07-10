# Face_Detection_Recognition

## 文件说明
> create_dataset.py:用于生产人脸数据库</br>
> predict.py:人脸预测文件</br>
> batch_test.py:批量测试文件</br>
> evaluation_test.py:评价文件，用于绘制模型ROC曲线，测试文件只使用了agedb_30.bin人脸数据库</br>

## 参考资料
> 参考博客地址:《利用MTCNN和facenet实现人脸检测和人脸识别》https://panjinquan.blog.csdn.net/article/details/84896733</br>
> FaceNet的人脸识别效果并不算法好，目前测试使用InsightFace模型，在开数据集可以达到99.6%，在自建的数据集可以达到93%的准确率，比虹软的人脸识别率还高一点 </br>

# imagePre是用来预处理文件的
## images 文件加内为图片处理

- 将某目录内图片全部转化成 500*500

```
python resize.py ./test/ 500
```
- 将某目录内图片随机切成 300*300

```
python randomCrop.py ./test/ 300
```

- 将某张图片按照阈值 60~150 生成 100张图片，用于选择合理的阈值
```
python getAllBinarizationImg.py test/汤浩.jpg
```
- 将某目录内图片翻转 45 度，共翻转 7 次，每翻转一次生成一张图。适合增加样本数量。还在在翻转中随机增加剪裁、灰度等丰富样本数据 

```
python rotate.py test 45 7
```

以上四种方法是主要采取的预处理方法，分别为像素大小预处理，然后就是随机切片，项目中切成100张左右，可以在代码中进行设置。再然后阈值处理、翻转处理。总共一张照片处理成500张左右。

- 将某目录内图片类型转为RGB

```
python convertToRGB.py ./test/
```
- 将某目录内图片转为灰度图

```
python convertToL.py ./test/
```
- 将某目录内图片做二值化处理，其中阈值为 120。二值化图像每个像素用 8 个bit表示，0 表示黑，255 表示白。阈值的作用就是大于阈值为白，小于阈值为黑
在图像检测中较常用，可以去掉过多的干扰和噪点

```
python convertTo1.py ./test/ 120
```
