from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from time import time
import os

## SETTINGS ##
# TRAINING_DATA = 'data/all_unhyphened_sent.txt'
# EVALUATING_DATA = 'data/questions-words.txt'
# MODEL_PATH = 'model/w2v'

# EMB_DIM = 200
# EPOCHS = 20

def ensure_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)

def load_file(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        data = f.read()
    return data

def preprocessing(data):
    ''' seperete sentences by '\n' and remove redudent spaces '''
    lines = data.split('\n')
    sentences = [[token for token in line.split(' ') if token != ''] for line in lines]
    return sentences

class loss_record(CallbackAny2Vec):
    '''Callback to record loss after each epoch.'''
    def __init__(self, loss_record = [], logging=False):
        self.epoch = 0
        self.logging= logging
        self.total_loss = 0
        self.record = loss_record

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss() - self.total_loss
        self.record.append(loss)
        self.total_loss = model.get_latest_training_loss()
        if self.logging:
            print('Loss after epoch {:3d}: {:10.3f}'.format(self.epoch, loss))
        self.epoch += 1

class log_epoch(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 0
        self.epoch_start_time = None

    def on_epoch_begin(self, model):
        print(f'[ INFO ] Epoch {self.epoch} start...')
        self.epoch_start_time = time()

    def on_epoch_end(self, model):
        train_time = time() - self.epoch_start_time
        print(f'[ INFO ] Epoch {self.epoch} end. Time eplapse: {train_time}')
        self.epoch += 1

def train(input_file, output_dir, epoch, dim, eval_file):
    # preprocessing
    print('[ INFO ] data processing...')
    training_data = load_file(input_file)
    training_data = preprocessing(training_data)

    # training
    losses = []
    print('[ INFO ] training start.')
    model = Word2Vec(training_data,
                      size = dim,
                      iter = epoch,
                      compute_loss = True,
                      callbacks=[log_epoch(), loss_record(losses, True)])
    print('[ INFO ] finished')

    # evaluating
    print('[ INFO ] evaluating...')
    result = model.wv.evaluate_word_analogies(eval_file)
    print(f'[ INFO ] evaluating finished. Accuracy = {result[0]}')

    # save model
    print(f'[ INFO ] saving data to {output_dir} ...')
    ensure_exist(output_dir)
    model.save(os.path.join(output_dir, 'model'))
    with open(os.path.join(output_dir, 'loss'), 'w+') as f:
        for idx, loss in enumerate(losses):
            f.write(f"{idx}\t{loss}\n")
    with open(os.path.join(output_dir, 'accuracy'), 'w+') as f:
        f.write(f"{result[0]}\n")
        f.write(str(result[1]))

if __name__ == '__main__':
    def parse_args():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input', type=str, help='training data')
        parser.add_argument('-o', '--output', type=str, help='folder to store output')
        parser.add_argument('-e', '--epoch', type=int, default=5,help='#iter')
        parser.add_argument('-d', '--dim', type=int, default=300, help='embedding dimension')
        parser.add_argument('--evaluate', type=str, default='data/questions-words.txt', help='evaluation data')
        return parser.parse_args()
    args = parse_args()

    print()
    print('Get Setting: ')
    print(f'  + input: {args.input}')
    print(f'  + output: {args.output}')
    print(f'  + epoch: {args.epoch}')
    print(f'  + dimension: {args.dim}')
    print(f'  + evaluate file: {args.evaluate}')
    print()

    train(args.input, args.output, args.epoch, args.dim, args.evaluate)
    print('finish')
