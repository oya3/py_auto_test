import os
import cv2
# import matplotlib.pyplot as plt
import numpy as np
import pdb

image1_path = r'screenshots\notepad\memo\boot\001.png'
image2_path = r'screenshots\notepad\memo\boot\001.bak.png'
diff_path = '000.png'

# 画像を読み込む
image1 = cv2.imread(image1_path)
image2 = cv2.imread(image2_path)

if 0:
    # 差分画像を計算
    diff = cv2.absdiff(image1, image2)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(diff_path, diff_gray)

if 1:
    diff = cv2.absdiff(image1, image2)  # ２枚の差分
    gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)  # 1枚目のグレイスケール
    # gray = gray // 2
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # 差分のグレイスケール
    norm_diff = diff_gray / np.max(diff_gray)  # 差分グレイスケールの正規化
    diff_img = cv2.addWeighted(gray, 0.1, diff_gray, 2, 100)  # １枚目に差分マージ
    cv2.imwrite(diff_path, diff_img)
