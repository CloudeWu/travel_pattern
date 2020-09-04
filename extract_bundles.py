import json

with open('LB_lonelyplanet.json', 'r') as f:
    data = json.load(f)

all_lb = set()
for key, val in data.items():
    for lb in val:
        all_lb.add(lb[0])

# save file
with open('bundles.txt', 'w+') as f:
    for lb in sorted(all_lb):
        f.write(lb+'\n')