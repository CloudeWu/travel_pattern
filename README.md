READ ME
=============

Files
-------------
### server/

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

#### train_all.sh

Script to run train.py with all parameter-list at once.  
Current parameter:  
 - #iter

#### eval_all.sh

Script to run evaluate.py with all models at once.  

#### train.py
Finetune or train a word2vec model with custom input data.
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

#### evaluate.py
Evaluate word2vec model with question dataset.  
If the output_dir is specified, the eval result will be written to output_dir/accuracy.  
sample: python evaluate.py -o model/mymodel model/mymodel/model data/questions-words.txt
```
usage: evaluate.py [-h] [-o OUTPUT] input eval_file

positional arguments:
  input                       target model
  eval_file                   evaluation data

optional arguments:
  -h, --help                  show this help message and exit
  -o OUTPUT, --output OUTPUT  folder to store output
```


#### finetune.py
Sample code to finetune on GoogleNews pretrained model.

#### testmodel.py
Sample code to evaluate model accuracy.


### process_bundles[.py|.ipynb]

All bundle processing methods


### extract_bundles[.py|.ipynb]

Extract all lexical bundles from LB_longlyplanet.json


### playground.ipynb

Notebook for all testing trash.  
Things here are all messed-up and odd and dangerous and better not to be executed without brains.  
Black magic is dangerous. You know it, right?
