from gensim.models import KeyedVectors
import numpy as np
import argparse
import os

def log(content):
    if args.debug:
        print(f'[ DEBUG ] {content}')

parser = argparse.ArgumentParser()
parser.add_argument('model', help="input kv model")
parser.add_argument('input', help="bundles for extracting bundles")
parser.add_argument('output', default="embeddings", help="where to store output (default = embeddings/)")
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

model_path, in_file, out_dir = args.model, args.input, args.output

# load input data
with open(in_file, 'r') as f:
    bundles = f.read().split('\n')
log(f'{len(bundles)} bundles loaded.')

log(f'loading model {model_path}...')
wv = KeyedVectors.load(model_path)

log(f'extracting embeddings...')
log(f'  + output folder: {out_dir}')
print()

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

total_words = set()
failures = []
for bundle in bundles:
    words = bundle.split(' ')
    try:
        for w in words:
            if w not in total_words:
                emb = wv[w]
                np.save(os.path.join(out_dir, w), emb)
                total_words.add(w)
                
    except:
        failures.append((bundle, w))
        continue

with open(os.path.join(out_dir, 'log'), 'w+') as f:
    f.write(f'Fail cases: {len(failures)}\n')
    for fail in failures:
        f.write(f'{str(fail)}\n')

log(f'finished. #words: {len(total_words)}, #failures: {failures}')

