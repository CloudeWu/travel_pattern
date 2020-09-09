#!/bin/sh

eval_file='data/questions-words.txt'

for dim in 300; do
	for e in 5 10 15 20 ; do
        echo "python evaluate.py -o models/finetuned_${dim}_${e}iter models/finetuned_${dim}_${e}iter/model ${eval_file}"
		python evaluate.py -o models/finetuned_${dim}_${e}iter models/finetuned_${dim}_${e}iter/model ${eval_file}
    done
done
