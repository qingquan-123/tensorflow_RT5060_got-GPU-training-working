# od_patch_all_estimator.py - patch every OD API module importing removed tf.compat.v1.estimator (safe: compile-verified)
import glob, os

STUB = '''try:
    from tensorflow.compat.v1 import estimator as tf_estimator
except ImportError:
    class _EstimatorStub:
        def __getattr__(self, name):
            return _EstimatorStub()
        def __call__(self, *a, **k):
            return _EstimatorStub()
    tf_estimator = _EstimatorStub()'''

root = '/home/devcontainers/od/object_detection'
patched = []
failed = []
for f in glob.glob(root + '/**/*.py', recursive=True):
    s = open(f, encoding='utf-8', errors='ignore').read()
    old = 'from tensorflow.compat.v1 import estimator as tf_estimator'
    if old in s:
        s2 = s.replace(old, STUB, 1)
        try:
            compile(s2, f, 'exec')
        except SyntaxError as e:
            failed.append((os.path.basename(f), str(e)))
            continue
        open(f, 'w', encoding='utf-8').write(s2)
        patched.append(f)
print('PATCHED:', len(patched), 'FAILED:', len(failed))
for name, err in failed:
    print('FAILED_FILE:', name, err)
