echo "--- 当前 TF 版本 ---"
/home/devcontainers/miniconda3/envs/tf2/bin/pip show tensorflow 2>/dev/null | grep -E 'Version|Name'
echo "--- GPU 识别（TF 2.20） ---"
export LD_LIBRARY_PATH=$(ls -d /home/devcontainers/miniconda3/envs/tf2/lib/python3.11/site-packages/nvidia/*/lib 2>/dev/null | tr '\n' ':')$LD_LIBRARY_PATH
/home/devcontainers/miniconda3/envs/tf2/bin/python -c "
import tensorflow as tf
print('TF', tf.__version__)
print('GPU_COUNT', len(tf.config.list_physical_devices('GPU')))
print(tf.config.list_physical_devices('GPU'))
" > /tmp/gpu_check2.txt 2>&1
cat /tmp/gpu_check2.txt | grep -E 'TF |GPU_COUNT|PhysicalGPU|pciBusId'