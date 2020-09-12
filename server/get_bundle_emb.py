import os
import numpy as np
import torch
from infersent import InferSent

### SET PARAMENTERS HERE ###
W2V_PATH = os.path.join(os.getenv('HOME'), 'fastText', 'crawl-300d-2M.vec')     # check your model location, plz
MODEL_PATH = 'encoder/infersent2.pkl'                                           # check your model location, plz
BATCH_SIZE = 64
EMB_DIM = 300
LSTM_DIM = 2048
POOL_TYPE = 'max'       # max / mean
DPOUT_MODEL = 0.0
MODEL_VER = 2
params_model = {'bsize': BATCH_SIZE, 
                'word_emb_dim': EMB_DIM, 
                'enc_lstm_dim': LSTM_DIM,
                'pool_type': POOL_TYPE, 
                'dpout_model': DPOUT_MODEL, 
                'version': MODEL_VER}

DEBUG_MODE = False

# utility functions #
def log_args(args):
    print()
    print("Get setting: ")
    print(f"  + bundle input: {args.input}")
    print(f"  + inferSent model: {args.model}")
    print(f"  + word embeddings: {args.emb_dir}")
    print(f"  + output dir: {args.output_dir}")
    print(f"  + batch size: {args.batch_size}")
    print(f"  + debug mode: {'on' if args.debug else 'off'}")
    print()
    return

def log(content, tag='LOG', verbose=DEBUG_MODE):
    if verbose:
        print(f'[ {tag} ] {content}')

def ensure_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        log('dir already exists. Original contents may be overwritten.')

def load_model(model_path, config, w2v_path=None):
    # load model
    model = InferSent(config)
    model.load_state_dict(torch.load(model_path))
    # model = model.cuda()   # GPU
    # model.set_w2v_path(w2v_path)
    # model.build_vocab(sentences)
    return model

def get_word_emb(path):
    if not os.path.exists(path):
        return None
    return np.load(path)

# @param bundles: list of bundle
# @ret: all bundle embedding's np array
def get_embeddings(bundles, emb_dir):
    # load beginning-of-sent and end-of-sent embedding
    emb_bos = np.load(os.path.join(emb_dir, 'bos.npy'))
    emb_eos = np.load(os.path.join(emb_dir, 'eos.npy'))
    
    # extract embeddings
    max_len = 0
    embeddings, lengths, bundle_list, fail_list = [], [], [], []
    for bundle in bundles:
        words = bundle.split(' ')
        emb = []
        
        emb.append(emb_bos)
        for w in words:
            emb_path = os.path.join(emb_dir, w + '.npy')
            emb.append(get_word_emb(emb_path))
        emb.append(emb_eos)
        
        if any(e is None for e in emb):
            fail_list.append(bundle)
            continue
            
        # store info
        embeddings.append(emb)
        lengths.append(len(emb))
        bundle_list.append(bundle)
        max_len = len(emb) if len(emb) > max_len else max_len
    
    # generate batches
    batches = np.zeros((max_len, len(embeddings), embeddings[0][0].shape[0]))
    for i in range(len(embeddings)):
        for j in range(len(embeddings[i])):
            batches[j][i][:] = embeddings[i][j]
    return batches, np.array(lengths), bundle_list, fail_list

def get_phrase_embeddings(bundle_path, model_path, emb_dir, out_dir, batch_size=64, debugging=False):
    log('getting bundles...', verbose=debugging)
    with open(bundle_path, 'r') as f:
        bundles = f.read().split('\n')[:-1]
    log(f'{len(bundles)} bundles loaded', verbose=debugging)

    log('extracting word embedding...', verbose=debugging)
    embeddings, lengths, bundle_list, fail_list = get_embeddings(bundles, emb_dir)
    log('finished.')
    log(f'#bundles: {len(bundle_list)}', 'INFO', True)
    
    log(f'loading model...', verbose=True)
    config = params_model
    model = load_model(model_path, config)
    log(f'loaded', verbose=debugging)

    log('generating bundle embedding...', verbose=True)
    phrase_embs = []
    for idx in range(0, embeddings.shape[1], batch_size):
        batch = torch.FloatTensor(embeddings[:,idx:idx+batch_size, :])
        length = lengths[idx:idx+batch_size]
        with torch.no_grad():
            emb = model.forward((batch, length)).data.cpu().numpy()
        phrase_embs.append(emb)
    phrase_embs = np.vstack(phrase_embs)

    log(f'writing output to {out_dir}...', verbose=True)
    ensure_exists(out_dir)
    for (bundle, emb) in zip(bundle_list, phrase_embs):
        out_path = os.path.join(out_dir, bundle.replace(' ', '_'))
        np.save(out_path, emb)
    log('finished', verbose=debugging)

if __name__ == '__main__':
    def parse_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('input', help="path to bundle files")
        parser.add_argument('model', help="path to InferSent model")
        parser.add_argument('emb_dir', help="path to word embeddings")
        parser.add_argument('-o', '--output-dir', default="bundle_emb", help="where to save bundle embeddings")
        parser.add_argument('-b', '--batch-size', type=int, default=64, help="batch size")
        parser.add_argument('-d', '--debug', action='store_true', help="debug mode")
        return parser.parse_args()
    args = parse_args()
   
    log_args(args)

    get_phrase_embeddings(args.input, args.model, args.emb_dir, args.output_dir)
