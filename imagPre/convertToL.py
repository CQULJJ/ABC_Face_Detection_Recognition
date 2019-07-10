import os
import sys
import math
import util
import random
import functools
import numpy as np
from PIL import Image, ImageEnhance


dir = sys.argv[1]

for img_path in util.imgList(dir):
    util.convertToL(img_path)
