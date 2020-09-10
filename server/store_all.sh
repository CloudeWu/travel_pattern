#!/bin/sh

for dim in 300; do
	for e in 5 10 15 20 ; do
        echo "python store_ky.py models/finetuned_${dim}_${e}iter/model"
		python store_ky.py models/finetuned_${dim}_${e}iter/model
    done
done
