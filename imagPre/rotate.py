import os
import sys
import math
import util
import random
import functools
import numpy as np
from PIL import Image, ImageEnhance


dir = sys.argv[1]
degree = sys.argv[2]
num = sys.argv[3]

for img_path in util.imgList(dir):
    util.rotate(img_path, int(degree), int(num))
