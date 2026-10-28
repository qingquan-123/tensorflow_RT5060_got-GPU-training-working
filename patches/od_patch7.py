# od_patch7.py - restore BOTH cond and case on tensorflow.python.ops.control_flow_ops
p = '/home/devcontainers/od/object_detection/__init__.py'
s = open(p, encoding='utf-8', errors='ignore').read()

NEW = '''

# ---- TF2.21 compat: restore control_flow_ops.cond/case (removed in TF 2.16+, used by tf_slim) ----
try:
    import tensorflow as tf
    from tensorflow.python.ops import control_flow_ops as _cfo
    if not hasattr(_cfo, 'cond'):
        _cfo.cond = tf.cond
    if not hasattr(_cfo, 'case'):
        def _case(pred_fn_pairs, default=None, exclusive=True):
            fn = default
            for pred, f in reversed(list(pred_fn_pairs)):
                fn = lambda p=pred, f=f, fn=fn: _cfo.cond(p, f, fn)
            return fn()
        _cfo.case = _case
except Exception as e:
    print('CFO_SHIM_SKIP', e)
# ---- end case shim ----
'''

import re
pat = re.compile(r"\n# ---- TF2\.21 compat: restore control_flow_ops\.case.*?# ---- end case shim ----\n", re.S)
s2, n = pat.subn('\n' + NEW, s, count=1)
print('REPLACED:', n)
compile(s2, p, 'exec')
open(p, 'w', encoding='utf-8').write(s2)
print('CFO_SHIM_UPDATED')
