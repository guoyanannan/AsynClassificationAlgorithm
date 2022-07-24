import glob
import os
import time
import shutil

IMG = ['bmp','jpg','png','jpeg']


def copy_img(input_dir,output_dir):
    while 1:
        t1 = time.time()
        for img_name in os.listdir(input_dir):
            img_mat = img_name.rsplit('.',1)[-1]
            if img_mat in IMG:
                src_path = os.path.join(input_dir,img_name)
                dst_path = os.path.join(output_dir,img_name)
                try:
                    shutil.copyfile(src_path,dst_path)
                except:
                    continue
        t2 = time.time()
        print(f'已存储{len(os.listdir(input_dir))}张图片,耗时{t2-t1}s')
        time.sleep(1)
        break



if __name__ == '__main__':
    copy_img('testimg_1','testimg')