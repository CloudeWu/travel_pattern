from gensim.models import Word2Vec
import os

from train import log_epoch, loss_record

def test_accuracy(model_path, eval_file, output_dir):
    print(f'[ INFO ] loading model: {model_path}...')
    model = Word2Vec.load(model_path)

    print('[ INFO ] start evaluation.')
    result = model.wv.evaluate_word_analogies(eval_file)

    print(f'\nAccuracy: {result[0]}')
    if output_dir:
        output_file = os.path.join(output_dir, 'accuracy')
        print(f'[ INFO ] eval result is saved to {output_file}')
        with open(output_file, 'w+') as f:
            f.write(f"{result[0]}\n")    # write accuracy
            f.write(str(result[1]))      # write evaluation log

if __name__ == '__main__':
    def parse_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('input', type=str, help='target model')
        parser.add_argument('eval_file', type=str, help='evaluation data')
        parser.add_argument('-o', '--output', type=str, help='folder to store output')
        return parser.parse_args()
    args = parse_args()

    print()
    print('Get Setting: ')
    print(f'  + input model: {args.input}')
    print(f'  + evaluate file: {args.eval_file}')
    print(f'  + output dir: {args.output}')
    print()

    test_accuracy(args.input, args.eval_file, args.output)
