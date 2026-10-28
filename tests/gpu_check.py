# gpu_check.py - verify TensorFlow GPU visibility in WSL tf2 env
import tensorflow as tf

print('TF', tf.__version__)
gpus = tf.config.list_physical_devices('GPU')
print('GPU list:', gpus)
if gpus:
    print('GPU_COUNT', len(gpus))
else:
    print('GPU_COUNT 0 - CUDA libs missing or not linked')
