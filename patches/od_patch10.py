# od_patch10.py - Keras3: drop unsupported layers= kwarg in MobileNetV2 call (OD API _LayersOverride mechanism removed in Keras3)
p = '/home/devcontainers/od/object_detection/models/keras_models/mobilenet_v2.py'
s = open(p, encoding='utf-8', errors='ignore').read()
old = '''  return tf.keras.applications.MobileNetV2(alpha=alpha,
                                           layers=layers_override,
                                           **kwargs)'''
new = '''  # Keras3: applications.MobileNetV2 has no 'layers' kwarg (OD API _LayersOverride is a Keras2 mechanism).
  # Fallback to standard Keras3 MobileNetV2; custom conv/BN hyperparams (momentum/L2) not applied (known degradation).
  return tf.keras.applications.MobileNetV2(alpha=alpha,
                                           **kwargs)'''
if old not in s:
    print('ANCHOR_NOT_FOUND')
else:
    s = s.replace(old, new, 1)
    compile(s, p, 'exec')
    open(p, 'w', encoding='utf-8').write(s)
    print('PATCHED_OK')
