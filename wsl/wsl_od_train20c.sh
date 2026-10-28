export LD_LIBRARY_PATH=$(ls -d /home/devcontainers/miniconda3/envs/tf2/lib/python3.11/site-packages/nvidia/*/lib 2>/dev/null | tr '\n' ':')$LD_LIBRARY_PATH
export PYTHONPATH=/home/devcontainers/od:/home/devcontainers/od/slim
/home/devcontainers/miniconda3/envs/tf2/bin/python /mnt/e/Object-Detection-Tensorflow/models-master/research/object_detection/model_main_tf2.py \
  --pipeline_config_path=/home/devcontainers/od_train/pipeline.config \
  --model_dir=/home/devcontainers/od_train/train \
  --num_train_steps=20 \
  --alsologtostderr > /mnt/c/Users/16231/Doubao/chats/2026-10-28/new-chat/od_train_real.log 2>&1
echo RC=$? >> /mnt/c/Users/16231/Doubao/chats/2026-10-28/new-chat/od_train_real.log