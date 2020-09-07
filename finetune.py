from gensim.models import Word2Vec     
import gensim.downloader as api

print("[ INFO ] loading pretrained model's words")
w2v_googlenews = api.load('word2vec-google-news-300')
model = Word2Vec(size=300, min_count=1)

print('[ INFO ] loading data...')
with open('data/tokenized_content.txt', 'r', encoding='utf-8') as f:
    data = f.read().split('\n')
sentence = [line.split(' ') for line in data]

print('[ INFO ] building our vocabulary...')
model.build_vocab(sentence)
total_examples = model.corpus_count

print('[ INFO ] building pretrained-vocabulary...')
model.build_vocab([list(w2v_googlenews.vocab.keys())], update=True)
print('[ INFO ] loading pretrained model...')
model.intersect_word2vec_format("model/GoogleNews-vectors-negative300.bin", binary=True)

print('[ INFO ] training...')
model.train(sentence, total_examples=total_examples, epochs=model.iter)

output_path = 'model/model'
print(f'[ INFO ] saving model to {output_path}')
model.save(output_path)
