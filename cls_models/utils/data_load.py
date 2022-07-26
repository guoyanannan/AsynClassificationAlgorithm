import os
import math
import time
import numpy as np
from PIL import Image
from threading import Thread
from cls_models.utils.common_oper import delete_batch_file,re_print
IMG = ['bmp', 'jpg', 'jpeg', 'png']


def get_batch_images(read_q,files,bs,imsze,th_flag):
    num_bs = math.ceil(len(files) / bs)
    th_total_time = 0
    th_read_time = 0
    th_write_time = 0
    th_del_time = 0
    for i in range(num_bs):
        bs_time = time.time()
        image_path_list = []
        image_arr_list = []
        image_list = []
        batch_img_path = files[i * bs:(i + 1) * bs]
        for filename in batch_img_path:
            break_num = 0
            while True:
                try:
                    img = Image.open(filename)
                    img_ = np.array(img)
                    img = img.convert('RGB')
                    # train_on_batch
                    img = img.resize((imsze, imsze))
                    # train_genarator
                    # img = img.resize((img_size,img_size), Image.NEAREST)
                    # img_1 = cv2.resize(img_1,(self.imgsize, self.imgsize),interpolation=cv2.INTER_NEAREST_EXACT)
                    img = np.array(img)
                    img = img / 255
                    break
                except Exception as E:
                    print(E)
                    time.sleep(0.01)
                    break_num += 1
                    if break_num < 5:
                        continue
                    else:
                        break
            image_list.append(img_)
            image_arr_list.append(img)
            image_path_list.append(filename)
        be_time = time.time()
        if len(image_arr_list) != 0:
            image_arr = np.array(image_arr_list)
            if len(image_arr.shape) == 4:
                read_q.put((image_arr, image_list, image_path_list))
        bq_time = time.time()
        delete_batch_file(batch_img_path)
        br_time = time.time()
        th_total_time += br_time-bs_time
        th_read_time += be_time-bs_time
        th_write_time += bq_time-be_time
        th_del_time += br_time-bq_time
    re_print(f'thread-{th_flag}:读取图片{len(files)}张,共耗时{th_total_time:.2f}s,FPS {(len(files)/(th_total_time+1e-10)):.2f},'
             f'读耗时{th_read_time:.2f}s,写入队列耗时{th_write_time:.2f}s,删除耗时{th_del_time:.2f}s')


def load_data(read_q,roi_dir_path,batch_size,img_size,logger):
    total_time = 0
    total_num = 0
    while True:
        try:
            start_time = time.time()
            # file_name_list = sorted(os.listdir(rois_dir), key=lambda x: os.path.getmtime(os.path.join(rois_dir, x)))
            files_path = [os.path.join(roi_dir_path, fileName) for fileName in os.listdir(roi_dir_path) if fileName.rsplit('.', 1)[-1].lower() in IMG]
            if files_path:
                img_th_num = math.ceil(len(files_path) / 6)
                th_list = []
                for i in range(6):
                    th = Thread(target=get_batch_images,args=(read_q,files_path[i*img_th_num:(i+1)*img_th_num],batch_size,img_size,i),)
                    th.start()
                    th_list.append(th)
                for th in th_list:
                    th.join()
                for th_ in th_list:
                    del th_
                del th_list

                end_time = time.time()
                total_time += end_time-start_time
                total_num += len(files_path)
                re_print(f'process-{os.getpid()} 当前读取{len(files_path)}张图片，耗时{(end_time-start_time):.2f}s，当前累计读取{total_num}张图片，平均FPS {(total_num/(total_time+1e-10)):.2f}')
        except Exception as E:
            logger.info(f'数据加载出现异常:{E}')
            raise



