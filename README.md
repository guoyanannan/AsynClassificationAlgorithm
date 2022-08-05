# AsynClassificationAlgorithm
3080 cpu 40/80核,基准速度3.10，内存64G，固态盘(无板载缓存)

【
10000张数据(D盘固态):
bs32 读取 181FPS 推理 171FPS
bs64 读取 190FPS 推理 293FPS
bs128 读取 200FPS 推理 366FPS

10000张数据(E盘机械):
bs128 读取 184FPS 推理 366FPS
】

显卡3070，cpu20内核，基准速度2.40，内存64G，固态盘或阵列2G缓存
PERC H730P 高性能硬件RAID卡带有2G缓存和电池 支持RAID 0 1 5 6 10 50 60
【
20000张缺陷小图：
每个批次64张，读取约160FPS，模型推理约245FPS
】

显卡3060


1660ti 10000 cpu speed base 2.6，核数6/12  tf2.5.0
[
bs64  读取 284  推理167    model()
bs64  读取 303 推理124    model.predict()
bs64  读取 303 推理124    model.predict_on_batch()
]



