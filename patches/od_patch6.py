# od_patch6.py - Keras3/TF2.21: restore control_flow_ops.case (removed in TF 2.16+) via tf.cond chain
p = '/home/devcontainers/od/object_detection/__init__.py'
s = open(p, encoding='utf-8', errors='ignore').read()

ADD = '''

# ---- TF2.21 compat: restore control_flow_ops.case (removed in TF 2.16+, used by tf_slim decoder) ----
try:
    import tensorflow as tf
    from tensorflow.python.ops import control_flow_ops as _cfo
    if not hasattr(_cfo, 'case'):
        def _case(pred_fn_pairs, default=None, exclusive=True):
            fn = default
            for pred, f in reversed(list(pred_fn_pairs)):
                fn = lambda p=pred, f=f, fn=fn: tf.cond(p, f, fn)
            return fn()
        _cfo.case = _case
except Exception as e:
    print('CASE_SHIM_SKIP', e)
# ---- end case shim ----
'''
s = s + ADD
compile(s, p, 'exec')
open(p, 'w', encoding='utf-8').write(s)
print('CASE_SHIM_ADDED')
