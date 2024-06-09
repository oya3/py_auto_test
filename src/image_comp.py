import os
import cv2
import numpy as np
# import matplotlib.pyplot as plt
# import numpy as np
# https://qiita.com/kagami_t/items/2b4db4e2464439a48fb4

class ImageComp:
    def __init__(self, image1_path, image2_path):
        self.image1_path = image1_path
        self.image2_path = image2_path

    def get_backup_file_name(self, filepath, append_ext):
        dirpath, filename = os.path.split(filepath)
        basename, ext = os.path.splitext(filename)
        new_filename = f"{basename}{append_ext}{ext}"
        new_filepath = os.path.join(dirpath, new_filename)
        new_filepath = new_filepath.replace("\\", "/")
        return new_filepath

    def run(self):
        diff1_pathfile = self.get_backup_file_name(self.image1_path, '.dff1')
        diff2_pathfile = self.get_backup_file_name(self.image1_path, '.dff2')
        # 画像を読み込む
        image1 = cv2.imread(self.image1_path)
        image2 = cv2.imread(self.image2_path)

        # # 差分画像を計算
        # diff = cv2.absdiff(image1, image2)
        # diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite(diff_pathfile, diff_gray)

        diff = cv2.absdiff(image1, image2)  # ２枚の差分
        gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)  # 1枚目のグレイスケール
        # gray = gray // 2
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # 差分のグレイスケール
        # diff_gray_norm = diff_gray / np.max(diff_gray)  # 差分グレイスケールの正規化
        diff_merge = cv2.addWeighted(gray, 0.1, diff_gray, 2, 100)  # １枚目に差分マージ
        cv2.imwrite(diff1_pathfile, diff)
        cv2.imwrite(diff2_pathfile, diff_merge)

        # cv2.imwrite('gray2.png', gray2)
        # cv2.imwrite('gray_diff.png', gray_diff)
        # cv2.imwrite('image1_rgb.png', cv2.cvtColor(image1_rgb, cv2.COLOR_RGB2BGR))  # Convert back to BGR for saving
        # cv2.imwrite('norm_diff.png', norm_diff * 255)  # Scale back to 8-bit for saving
        # cv2.imwrite('diff_img.png', diff_img)
