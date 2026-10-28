# od_patch11.py - Keras3: call FPN generator via .call() to bypass __call__ positional-tensor-only check
p = '/home/devcontainers/od/object_detection/models/ssd_mobilenet_v2_fpn_keras_feature_extractor.py'
s = open(p, encoding='utf-8', errors='ignore').read()
old = '    fpn_features = self._fpn_features_generator(fpn_input_image_features)'
new = '    fpn_features = self._fpn_features_generator.call(fpn_input_image_features)  # Keras3: __call__ rejects list arg (key, tensor) pairs'
if old not in s:
    print('ANCHOR_NOT_FOUND')
else:
    s = s.replace(old, new, 1)
    compile(s, p, 'exec')
    open(p, 'w', encoding='utf-8').write(s)
    print('PATCHED_OK')
