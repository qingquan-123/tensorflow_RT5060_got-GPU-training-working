# od_patch3.py - Keras3: SeparableConv2D rejects leftover kernel_* kwargs (copied to pointwise_*)
p = '/home/devcontainers/od/object_detection/predictors/heads/keras_box_head.py'
s = open(p, encoding='utf-8', errors='ignore').read()
old = '''        kwargs['pointwise_regularizer'] = kwargs['kernel_regularizer']
        kwargs['pointwise_initializer'] = kwargs['kernel_initializer']
      self._box_encoder_layers.append('''
new = '''        kwargs['pointwise_regularizer'] = kwargs['kernel_regularizer']
        kwargs['pointwise_initializer'] = kwargs['kernel_initializer']
        kwargs.pop('kernel_regularizer', None)
        kwargs.pop('kernel_initializer', None)
      self._box_encoder_layers.append('''
if old not in s:
    print('ANCHOR_NOT_FOUND')
else:
    s = s.replace(old, new, 1)
    compile(s, p, 'exec')
    open(p, 'w', encoding='utf-8').write(s)
    print('PATCHED_OK')
