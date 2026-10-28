import json

d = json.load(open('/tmp/tf.json'))
rd = d['info'].get('requires_dist') or []
for x in rd:
    if 'nvidia' in x.lower() or 'cuda' in x.lower():
        print(x)
