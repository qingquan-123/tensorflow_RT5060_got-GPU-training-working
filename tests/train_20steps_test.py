# train_20steps_test.py - run a small CNN training loop to measure real per-step time
# Run with: C:\Users\16231\anaconda3\envs\tf-od\python.exe -u train_20steps_test.py
import os, sys, time
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # keep output clean (errors/warnings only)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

import tensorflow as tf

print('== TF version:', tf.__version__)
print('GPU devices:', [d.name for d in tf.config.list_physical_devices('GPU')])

# small CNN close to a classification head used in detection pipelines
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(8, 3, activation='relu', input_shape=(32, 32, 3)),
    tf.keras.layers.MaxPooling2D(2),
    tf.keras.layers.Conv2D(16, 3, activation='relu'),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(10, activation='softmax'),
])
model.compile(optimizer='sgd', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# synthetic mini-batch
x = tf.random.normal([64, 32, 32, 3])
y = tf.random.uniform([64], maxval=10, dtype=tf.int64)

steps = 20
times = []
for i in range(steps):
    t0 = time.time()
    model.train_on_batch(x, y)
    dt = time.time() - t0
    times.append(dt)
    print('STEP %02d time: %.3f s' % (i + 1, dt), flush=True)

print('== PER_STEP_TIMES ==', ' '.join('%.3f' % t for t in times))
print('== SUMMARY ==')
print('total: %.3f s' % sum(times))
print('avg all: %.3f s' % (sum(times) / len(times)))
print('avg first 5: %.3f s' % (sum(times[:5]) / 5))
print('avg last 5: %.3f s' % (sum(times[-5:]) / 5))
print('slowest: %.3f s (step %d)' % (max(times), times.index(max(times)) + 1))
print('fastest: %.3f s (step %d)' % (min(times), times.index(min(times)) + 1))
print('== TEST DONE ==')
