# od_patch9.py - Keras3: also shim tf.keras.backend.set_learning_phase (tf compat namespace)
p = '/home/devcontainers/od/object_detection/__init__.py'
s = open(p, encoding='utf-8', errors='ignore').read()

ADD = '''

# ---- Keras3 compat: shim tf.keras.backend.set_learning_phase (tf-compat namespace differs from keras.backend) ----
try:
    import tensorflow as _tf
    if not hasattr(_tf.keras.backend, 'set_learning_phase'):
        _tf.keras.backend.set_learning_phase = lambda v: None
except Exception as e:
    print('TFKBP_SHIM_SKIP', e)
# ---- end tfkbp shim ----
'''
s = s + ADD
compile(s, p, 'exec')
open(p, 'w', encoding='utf-8').write(s)
print('TFKBP_SHIM_ADDED')
