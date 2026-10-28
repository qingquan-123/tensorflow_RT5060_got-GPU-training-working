# od_patch12.py - Keras3: sanitize layer names containing '/' (Keras3 forbids '/')
p = '/home/devcontainers/od/object_detection/__init__.py'
s = open(p, encoding='utf-8', errors='ignore').read()
anchor = "# ---- end tfkbp shim ----"
patch = anchor + """

# ---- Keras3 compat: sanitize layer 'name' containing '/' (Keras3 rejects '/') ----
try:
    import keras as _keras_san
    _orig_layer_init = _keras_san.layers.Layer.__init__
    def _sanitized_layer_init(self, *a, **k):
        if k.get('name') and isinstance(k['name'], str) and '/' in k['name']:
            k['name'] = k['name'].replace('/', '_')
        return _orig_layer_init(self, *a, **k)
    _keras_san.layers.Layer.__init__ = _sanitized_layer_init
    import tensorflow as _tf_san
    if hasattr(_tf_san.keras, 'layers'):
        _tf_orig_layer_init = _tf_san.keras.layers.Layer.__init__
        def _tf_sanitized_layer_init(self, *a, **k):
            if k.get('name') and isinstance(k['name'], str) and '/' in k['name']:
                k['name'] = k['name'].replace('/', '_')
            return _tf_orig_layer_init(self, *a, **k)
        _tf_san.keras.layers.Layer.__init__ = _tf_sanitized_layer_init
except Exception as e:
    print('NAME_SAN_SHIM_SKIP', e)
# ---- end name sanitizer shim ----
"""
if anchor not in s:
    print('ANCHOR_NOT_FOUND')
else:
    s = s.replace(anchor, patch, 1)
    compile(s, p, 'exec')
    open(p, 'w', encoding='utf-8').write(s)
    print('PATCHED_OK')
