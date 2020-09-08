from gensim.models import Word2Vec

print('[ INFO ] loading model...')
model = Word2Vec.load('model/model')
print('[ INFO ] evaluating...')
accuracy = model.wv.evaluate_word_analogies('./data/questions-words.txt')

print(accuracy)
