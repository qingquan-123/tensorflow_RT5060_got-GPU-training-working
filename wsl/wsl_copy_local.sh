mkdir -p /home/devcontainers/od_train/ckpt
cp /mnt/e/Object-Detection-Tensorflow/dataset/train.record /home/devcontainers/od_train/train.record
cp -r /mnt/e/Object-Detection-Tensorflow/dataset/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/checkpoint/* /home/devcontainers/od_train/ckpt/
echo COPY_DONE
ls -la /home/devcontainers/od_train/ | head -8
ls -la /home/devcontainers/od_train/ckpt/ | head -6