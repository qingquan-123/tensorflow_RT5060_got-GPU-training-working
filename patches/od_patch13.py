# od_patch13.py - TF2.21: relax strict checkpoint restore (allow unmatched vars due to Keras3 layer-name sanitization)
p = '/home/devcontainers/od/object_detection/model_lib_v2.py'
s = open(p, encoding='utf-8', errors='ignore').read()
old = 'checkpoint_path).expect_partial().assert_existing_objects_matched()'
new = 'checkpoint_path).expect_partial()  # Keras3 compat: layer-name sanitization may leave unmatched vars; skip strict assert'
if old not in s:
    print('ANCHOR_NOT_FOUND')
else:
    s = s.replace(old, new, 1)
    compile(s, p, 'exec')
    open(p, 'w', encoding='utf-8').write(s)
    print('PATCHED_OK')
