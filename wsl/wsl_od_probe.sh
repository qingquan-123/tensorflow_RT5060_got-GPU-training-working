echo "--- models-master 结构 ---"
ls /mnt/e/Object-Detection-Tensorflow/models-master/ 2>&1 | head -10
echo "--- research/object_detection 关键文件 ---"
ls /mnt/e/Object-Detection-Tensorflow/models-master/research/ 2>&1 | head -10
ls /mnt/e/Object-Detection-Tensorflow/models-master/research/object_detection/protos/*.proto 2>&1 | wc -l
echo "--- setup.py ---"
ls -la /mnt/e/Object-Detection-Tensorflow/models-master/research/setup.py /mnt/e/Object-Detection-Tensorflow/models-master/research/object_detection/packages/tf2/setup.py 2>&1 | head -5