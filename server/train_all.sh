#!/bin/sh

training_data='data/all_hyphened_sent.txt'
eval_file='data/questions-words.txt'
pretrain_model='models/GoogleNews-vectors-negative300.bin'

for window in 3 4 5; do
	for dim in 300; do
		for e in 1 5 10 15 20 ; do
    	    echo "python train.py -i ${training_data} -o models/finetuned_${dim}_${e}iter -e ${e} -d ${dim} -p ${pretrain_model}"
       		python train.py -i ${training_data} -o models/hyphened/finetuned_${dim}d_w${window}_${e}iter -e ${e} -d ${dim} -w window -p ${pretrain_model} 
    	done
	done
done
