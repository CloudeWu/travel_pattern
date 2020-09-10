from gensim.models import Word2Vec, KeyedVectors
from train import loss_record, log_epoch

if __name__ == '__main__':
    def parse_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('input', help='input Word2Vec model')
        parser.add_argument('output', nargs='?', help='output name')
        return parser.parse_args()
    args = parse_args()

    model_path, output_path = args.input, args.output
    if not output_path:
        import os.path
        output_path = os.path.join(os.path.split(model_path)[0], 'vector.kv')

    print('[ INFO ] loading model...')
    model = Word2Vec.load(model_path)
    print(f'[ INFO ] storing vectors to {output_path}...')
    model.wv.save(output_path)

