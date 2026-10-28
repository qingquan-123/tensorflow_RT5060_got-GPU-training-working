# od_patch8.py - Keras3: no-op shim for removed keras.backend.set_learning_phase
p = '/home/devcontainers/od/object_detection/__init__.py'
s = open(p, encoding='utf-8', errors='ignore').read()

ADD = '''

# ---- Keras3 compat: restore removed keras.backend.set_learning_phase (no-op; training phase is explicit in Keras3) ----
try:
    import keras as _keras
    if not hasattr(_keras.backend, 'set_learning_phase'):
        _keras.backend.set_learning_phase = lambda v: None
except Exception as e:
    print('KBP_SHIM_SKIP', e)
# ---- end kbp shim ----
'''
s = s + ADD
compile(s, p, 'exec')
open(p, 'w', encoding='utf-8').write(s)
print('KBP_SHIM_ADDED')
