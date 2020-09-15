READ ME
=============
TOC:
 * [Server files](#On-Server)
 * [Other scripts](#Others)

On Server
-------------

Files on server: joaw@jedi:~/projects/travel_pattern  
Folder structure:
```
 server/
   |- data/         : all training and evaluating data file
   |- models/       : all pretrained and finetuned model
   |- ...           : scripts
```
Data Download:
 * data/questions-words.txt: Google's evaluation dataset. You can extract it from [Google's source code](https://storage.googleapis.com/google-code-archive-source/v2/code.google.com/word2vec/source-archive.zip)  
 * models/GoogleNews-vectors-negative300.bin: Google's pretrained model. You can download it [here](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing)

### train_all.sh

Script to run train.py with all parameter-list at once.  
Current parameter:  
 - #iter

### eval_all.sh

Script to run do_gensim_evaluate.py with all models at once.  

### train.py
Finetune or train a word2vec model with custom input data.
 * If output is specified, model and losses will be saved to `output/model` and `output/loss`, respectively.  
 * If pretrained is specified, model will load pretrained model first, and continueing training with input data.(w/o freezing)  
 * If eval is specified, model do eval with provided question file and write result to `output/accuracy`.  
```
usage: train.py [-h] -i INPUT [-o OUTPUT] [-e EPOCH] [-d DIM] [-p [PRETRAINED]] [-eval EVALUATE]

optional arguments:
  -h, --help                  show this help message and exit
  -i INPUT, --input INPUT
                              training data
  -o OUTPUT, --output OUTPUT
                              folder to store output
  -e EPOCH, --epoch EPOCH
                              #iter
  -d DIM, --dim DIM           embedding dimension
  -p [PRETRAINED], --pretrained [PRETRAINED]
                              pretrained model path
  -eval EVALUATE, --evaluate EVALUATE
                              evaluation data
```
#### Output
If the output_dir is specified, three files will be written into that folder:
```
Model
 |- model       model file
 |- loss        loss information during training
 |- accuracy    evaluation result. (only if eval is specified)
```
 * loss: One epoch per line. format: `[epoch idx]\t[loss]`
 * accuracy: Two line in the file. First line is the final accuracy. Second line is all details about every test result.

### do_gensim_evaluate.py
Use gensim evaluate_word_analogies() function to evaluate word2vec model with question dataset.  
If the output_dir is specified, the eval result will be written to output_dir/accuracy.  
sample: python evaluate.py -o model/mymodel model/mymodel/model data/questions-words.txt
```
usage: do_gensim_evaluate.py [-h] [-o OUTPUT] input eval_file

positional arguments:
  input                       target model
  eval_file                   evaluation data

optional arguments:
  -h, --help                  show this help message and exit
  -o OUTPUT, --output OUTPUT  folder to store output
```

### extract_word_emb.py
Extract all bundles' word embedding.  
Output will be binary files named [word].npy. You can load it with `np.load('[word].npy')`  
```
usage: extract_word_emb.py [-h] [-d] model input output

positional arguments:
  model        input kv model
  input        bundles for extracting bundles
  output       where to store output (default = embeddings/)
```

### get_bundle_emb[.py|.ipynb]
User InferSent to encode word embeddings into bundle embedding.  
Output will be binary files named `[bundles_with_words].npy`.   
Usage example: `python get_bundle_emb.py -o bundle_embs -b 64 data/bundles_all.txt encoder/infersent2.pkl word_embs`  
You can download InferSent pretrained model [here](https://github.com/facebookresearch/InferSent)
```
usage: get_bundle_emb.py [-h] [-o OUTPUT_DIR] [-b BATCH_SIZE] [-d] input model emb_dir

positional arguments:
  input                 path to bundle files
  model                 path to InferSent model
  emb_dir               path to word embeddings

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        where to save bundle embeddings
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        batch size
  -d, --debug           debug mode
```

### pipeline.py
A concatenated script to get word embedding and generate bundle embeddings at once.  
Usage example:
 * Only one bundle: `python pipeline.py -w2v models/finetuned_300_10iter/vectors.kv -if encoders/infersent2.pkl -wd word_embs -bd bundle_embs 'ask for a'`
 * Get all bundles in file: `python pipeline.py -w2v models/finetuned_300_10iter/vectors.kv -if encoders/infersent2.pkl -wd word_embs -bd bundle_embs data/bundles_all.txt`
```
usage: pipeline.py [-h] [-w2v WORD2VEC_MODEL] [-if INFERSENT_MODEL]
                   [-wd WORD_EMBEDDING] [-bd BUNDLE_EMBEDDING] [-v VERBOSE]
                   input

positional arguments:
  input                 bundles for extracting bundles

optional arguments:
  -h, --help            show this help message and exit
  -w2v WORD2VEC_MODEL, --word2vec-model WORD2VEC_MODEL
                        word2vec's kv model
  -if INFERSENT_MODEL, --infersent-model INFERSENT_MODEL
                        infersent's pkl model
  -wd WORD_EMBEDDING, --word-embedding WORD_EMBEDDING
                        word embedding folder
  -bd BUNDLE_EMBEDDING, --bundle-embedding BUNDLE_EMBEDDING
                        bundle embedding folder
  -v VERBOSE, --verbose VERBOSE
                        verbose level. 0=only error, 3=debugging
```

### check_similarity[.py|.ipynb]
Get load pharse embeddings and find the most similar vectors.  
 * check_similarity.ipynb contains cherry-picked result  
 * check_similarity.py can check similarity on the fly. Usage: `python check_similarity.py bundle_emb`
```
usage: check_similarity.py [-h] [-n N] folders [folders ...]

positional arguments:
  folders     embedding folders

optional arguments:
  -h, --help  show this help message and exit
  -n N        how many similar bundles to show
```


### finetune.py
Sample code to finetune on GoogleNews pretrained model.

### testmodel.py
Sample code to evaluate model accuracy.


Others
-------------------
Other local testing or processing file not on server.

### process_bundles[.py|.ipynb]
All bundle processing methods

### extract_bundles[.py|.ipynb]
Extract all lexical bundles from LB_longlyplanet.json

### playground.ipynb
Notebook for all testing trash.  
Things here are all messed-up and odd and dangerous and better not to be executed without brains. Black magic is dangerous. You know it, right?
