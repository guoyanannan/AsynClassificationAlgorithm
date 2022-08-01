import os
import math
import time

import numpy as np
from PIL import Image
from cls_models.utils.common_oper import delete_batch_file,re_print
IMG = ['bmp', 'jpg', 'jpeg', 'png']


def thread_load_data(read_q,roi_dir_path,batch_size,img_size,logger):
    total_time = 0
    total_num = 0
    while True:
        try:
            currd_times=0
            curw_times=0
            start_time = time.time()
            # file_name_list = sorted(os.listdir(rois_dir), key=lambda x: os.path.getmtime(os.path.join(rois_dir, x)))
            files_path = [os.path.join(roi_dir_path, fileName) for fileName in os.listdir(roi_dir_path) if fileName.rsplit('.', 1)[-1].lower() in IMG]
            if files_path:
                num_bs = math.ceil(len(files_path) / batch_size)
                for i in range(num_bs):
                    bs_time = time.time()
                    image_path_list = []
                    image_arr_list = []
                    image_list = []
                    batch_img_path = files_path[i * batch_size:(i + 1) * batch_size]
                    for filename in batch_img_path:
                        break_num = 0
                        while True:
                            try:
                                img = Image.open(filename)
                                img_ = np.array(img)
                                img = img.convert('RGB')
                                img = img.resize((img_size, img_size))  # train_on_batch
                                # img = img.resize((img_size,img_size), Image.NEAREST) # train_genarator
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
                    delete_batch_file(batch_img_path)
                    brd_time = time.time()
                    if len(image_arr_list) != 0:
                        image_arr = np.array(image_arr_list)
                        if len(image_arr.shape) == 4:
                            read_q.put((image_arr, image_list, image_path_list))
                    bw_time = time.time()
                    currd_times += brd_time-bs_time
                    curw_times += bw_time-brd_time

                end_time = time.time()
                total_time += end_time-start_time
                total_num += len(files_path)
                re_print(
                        f'thread-read:'
                        f'当前读取{len(files_path)}张图片，总耗时{(end_time - start_time):.2f}s,读{currd_times:.2f}s,写{curw_times:.2f}s,'
                        f'累计读取{total_num}张图片，FPS {(total_num/total_time+1e-10):.2f}，'
                        )

        except Exception as E:
            logger.info(f'数据加载出现异常:{E}')
            raise



