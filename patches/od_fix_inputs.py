# od_fix_inputs.py - repair inputs.py double-patch pollution
import re

p = '/home/devcontainers/od/object_detection/inputs.py'
s = open(p, encoding='utf-8', errors='ignore').read()

CLEAN = '''try:
    from tensorflow.compat.v1 import estimator as tf_estimator
except ImportError:
    class _EstimatorStub:
        def __getattr__(self, name):
            return _EstimatorStub()
        def __call__(self, *a, **k):
            return _EstimatorStub()
    tf_estimator = _EstimatorStub()'''

# from first 'try:' after the tf import up to 'tf_estimator = _EstimatorStub()'
pat = re.compile(r'try:\n.*?tf_estimator = _EstimatorStub\(\)', re.S)
s2, n = pat.subn(CLEAN, s, count=1)
print('REPLACED:', n)
if n == 1:
    compile(s2, p, 'exec')
    open(p, 'w', encoding='utf-8').write(s2)
    print('FIXED_OK')
