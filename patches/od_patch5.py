# od_patch5.py - Keras3: global SeparableConv2D compat shim registered at package import
p = '/home/devcontainers/od/object_detection/__init__.py'
s = open(p, encoding='utf-8', errors='ignore').read()

SHIM = '''

# ---- Keras3 compat shim: SeparableConv2D kernel_* -> pointwise_* ----
try:
    import tensorflow as tf
    _orig_sep = tf.keras.layers.SeparableConv2D
    class _SepCompat(_orig_sep):
        def __init__(self, *a, **k):
            if 'kernel_initializer' in k:
                k.setdefault('pointwise_initializer', k.pop('kernel_initializer'))
            if 'kernel_regularizer' in k:
                k.setdefault('pointwise_regularizer', k.pop('kernel_regularizer'))
            super().__init__(*a, **k)
    tf.keras.layers.SeparableConv2D = _SepCompat
except Exception as e:
    print('SHIM_SKIP', e)
# ---- end shim ----
'''
s = s + SHIM
compile(s, p, 'exec')
open(p, 'w', encoding='utf-8').write(s)
print('SHIM_ADDED')
