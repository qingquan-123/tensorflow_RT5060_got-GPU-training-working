# od_patch2.py - patch WSL OD API copy: mock removed tf.compat.v1.estimator (serving-export only)
p = '/home/devcontainers/od/object_detection/inputs.py'
s = open(p, encoding='utf-8').read()
old = 'from tensorflow.compat.v1 import estimator as tf_estimator'
new = '''try:
    from tensorflow.compat.v1 import estimator as tf_estimator
except ImportError:
    # TF 2.16+ removed tf.compat.v1.estimator; only used for serving export (unused in training)
    class _ExportStub:
        def ServingInputReceiver(self, *a, **k):
            raise NotImplementedError('serving export not supported in this env')
    class _EstimatorStub:
        export = _ExportStub()
    tf_estimator = _EstimatorStub()'''
if old not in s:
    print('ANCHOR_NOT_FOUND')
else:
    s = s.replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(s)
    print('PATCHED_OK')
