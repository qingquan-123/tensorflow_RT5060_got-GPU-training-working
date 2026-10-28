echo "--- 恢复 TF 2.21.0（--no-deps，防降级） ---"
/home/devcontainers/miniconda3/envs/tf2/bin/pip install tensorflow==2.21.0 --no-deps 2>&1 | tail -2
echo "--- 验证版本与 GPU ---"
export LD_LIBRARY_PATH=$(ls -d /home/devcontainers/miniconda3/envs/tf2/lib/python3.11/site-packages/nvidia/*/lib 2>/dev/null | tr '\n' ':')$LD_LIBRARY_PATH
/home/devcontainers/miniconda3/envs/tf2/bin/python -c "
import tensorflow as tf
print('TF', tf.__version__)
print('GPU_COUNT', len(tf.config.list_physical_devices('GPU')))
" > /tmp/gpu_check3.txt 2>&1
cat /tmp/gpu_check3.txt | grep -E 'TF |GPU_COUNT|compute capability'