sed -i 's|/mnt/e/Object-Detection-Tensorflow/dataset/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/checkpoint/ckpt-0|/home/devcontainers/od_train/ckpt/ckpt-0|' /home/devcontainers/od_train/pipeline.config
sed -i 's|/mnt/e/Object-Detection-Tensorflow/dataset/train.record|/home/devcontainers/od_train/train.record|' /home/devcontainers/od_train/pipeline.config
echo CONFIG_LOCAL_DONE
grep -E 'fine_tune_checkpoint|input_path' /home/devcontainers/od_train/pipeline.config | head -5