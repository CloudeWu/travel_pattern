#!/bin/sh

training_data='data/all_unhyphened_sent.txt'
eval_file='data/questions-words.txt'

for dim in 300; do
    for e in 1 5 10 15 20 ; do
        echo "python train.py -i ${training_data} -o models/model_${dim}_${e}iter -e ${e} -d ${dim} --evaluate ${eval_file}"
        python train.py -i ${training_data} -o models/model_${dim}_${e}iter -e ${e} -d ${dim} --evaluate ${eval_file} 
    done
done
