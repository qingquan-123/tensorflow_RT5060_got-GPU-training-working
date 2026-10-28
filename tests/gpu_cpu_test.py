# gpu_cpu_test.py - detect whether tf-od env actually trains on GPU or silently uses CPU
# Run with: C:\Users\16231\anaconda3\envs\tf-od\python.exe -u gpu_cpu_test.py
import os, sys, time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  # keep INFO logs (device placement)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

import tensorflow as tf

print('== TF version:', tf.__version__)

for d in tf.config.list_physical_devices():
    print('physical device:', d.device_type, '-', d.name)
print('GPU count:', len(tf.config.list_physical_devices('GPU')))
try:
    print('is_gpu_available:', tf.test.is_gpu_available())
except Exception as e:
    print('is_gpu_available ERROR:', repr(e))

tf.debugging.set_log_device_placement(True)

size = 2048
x = tf.random.normal([size, size])
y = tf.random.normal([size, size])

# 1) CPU baseline first (always completes, gives a reference number)
try:
    t0 = time.time()
    with tf.device('/CPU:0'):
        z = tf.matmul(x, y)
    z.numpy()
    print('RESULT CPU matmul 2048x2048 time: %.3f s' % (time.time() - t0))
except Exception as e:
    print('RESULT CPU matmul FAILED:', repr(e))

# 2) small GPU op - check which device TF actually places it on
try:
    t0 = time.time()
    a = tf.random.normal([256, 256])
    b = tf.random.normal([256, 256])
    c = tf.matmul(a, b)
    c.numpy()
    print('RESULT GPU small matmul 256x256 time: %.3f s' % (time.time() - t0))
    print('RESULT small matmul op device:', c.device)
except Exception as e:
    print('RESULT GPU small matmul FAILED:', repr(e))

# 3) large GPU matmul - triggers real cuBLAS kernel / PTX JIT path
try:
    t0 = time.time()
    z = tf.matmul(x, y)
    z.numpy()
    print('RESULT GPU matmul 2048x2048 time: %.3f s' % (time.time() - t0))
    print('RESULT large matmul op device:', z.device)
except Exception as e:
    print('RESULT GPU large matmul FAILED:', repr(e))

print('== TEST DONE ==')
