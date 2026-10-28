# od_patch1.py - patch WSL OD API copy for Keras 3 compat (SyncBatchNormalization)
p = '/home/devcontainers/od/object_detection/core/freezable_sync_batch_norm.py'
s = open(p, encoding='utf-8').read()
anchor = 'import tensorflow as tf'
shim = '''import tensorflow as tf

# ---- Keras3 compat shim (OD API expects tf.keras.layers.experimental.SyncBatchNormalization) ----
try:
    _sync_bn = tf.keras.layers.experimental.SyncBatchNormalization
except (AttributeError, TypeError):
    import keras as _keras
    class _SyncBNCompat(_keras.layers.BatchNormalization):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault('synchronized', True)
            super().__init__(*args, **kwargs)
    class _ExpCompat:
        SyncBatchNormalization = _SyncBNCompat
    tf.keras.layers.experimental = _ExpCompat()
# ---- end shim ----
'''
if anchor not in s:
    print('ANCHOR_NOT_FOUND')
else:
    s = s.replace(anchor, shim, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('PATCHED_OK')
