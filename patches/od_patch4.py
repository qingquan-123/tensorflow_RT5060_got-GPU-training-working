# od_patch4.py - Keras3: move kernel_*->pointwise_* conversion out of the if block (fires always)
p = '/home/devcontainers/od/object_detection/predictors/heads/keras_box_head.py'
s = open(p, encoding='utf-8', errors='ignore').read()
old = '''      if self._apply_conv_hyperparams_to_heads:
        kwargs['depthwise_regularizer'] = kwargs['kernel_regularizer']
        kwargs['depthwise_initializer'] = kwargs['kernel_initializer']
        kwargs['pointwise_regularizer'] = kwargs['kernel_regularizer']
        kwargs['pointwise_initializer'] = kwargs['kernel_initializer']
        kwargs.pop('kernel_regularizer', None)
        kwargs.pop('kernel_initializer', None)'''
new = '''      kwargs['pointwise_regularizer'] = kwargs.get('kernel_regularizer')
      kwargs['pointwise_initializer'] = kwargs.get('kernel_initializer')
      kwargs.pop('kernel_regularizer', None)
      kwargs.pop('kernel_initializer', None)'''
if old not in s:
    print('ANCHOR_NOT_FOUND')
else:
    s = s.replace(old, new, 1)
    compile(s, p, 'exec')
    open(p, 'w', encoding='utf-8').write(s)
    print('PATCHED_OK')
