mkdir -p /home/devcontainers/od_train
cp /mnt/e/Object-Detection-Tensorflow/dataset/pipeline.config /home/devcontainers/od_train/pipeline.config
sed -i 's|E:/Object-Detection-Tensorflow|/mnt/e/Object-Detection-Tensorflow|g' /home/devcontainers/od_train/pipeline.config
sed -i 's|dataset/test.record|dataset/val.record|g' /home/devcontainers/od_train/pipeline.config
echo PREP_DONE
echo "--- 副本 pipeline 关键路径 ---"
grep -E 'fine_tune_checkpoint|input_path|label_map_path|num_steps|batch_size|num_classes' /home/devcontainers/od_train/pipeline.config | head -12
echo "--- 预训练权重检查 ---"
ls /mnt/e/Object-Detection-Tensorflow/dataset/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/checkpoint/ 2>/dev/null | head -6