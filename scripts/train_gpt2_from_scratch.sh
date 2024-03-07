#!/bin/sh
# TODO for Ben: Rewrite all of the commands below for training from scratch.

for n in 1 2 5 9 10 25 50 75 99; do
  python scripts/finetune.py \
    --output_dir="outputs/frisian_$n/" \
    --model_type=gpt2 \
    --model_name_or_path=gpt2 \
    --save_total_limit=2 \
    --do_train \
    --num_train_epochs=1 \
    --do_eval \
    --train_data_file="data/fry_news_2020_100K/training_${n}k_clean_fry_news_2020_100K-sentences.txt" \
    --eval_data_file="data/fry_news_2020_100K/validation_1k_clean_fry_news_2020_100K-sentences.txt" \
    --per_gpu_train_batch_size=1 \
    --overwrite_output_dir \
    --overwrite_cache \
    --block_size 512 \
    --tokenizer tokenizers/frisian \
    --overwrite_output_dir \
    --overwrite_cache \
    --logging_steps 400 \
    --save_steps 400 \
    > outputs/frisian_$n.log 2>&1
done

for n in 1 2 5 9 10 25 50 75 100 150 199; do
  python scripts/finetune.py \
    --output_dir="outputs/occitan_$n/" \
    --model_type=gpt2 \
    --model_name_or_path=gpt2 \
    --save_total_limit=2 \
    --do_train \
    --num_train_epochs=1 \
    --do_eval \
    --train_data_file="data/oci_community_2023/training_${n}k_clean_oci_community_2023-sentences.txt" \
    --eval_data_file="data/oci_community_2023/validation_1k_clean_oci_community_2023-sentences.txt" \
    --per_gpu_train_batch_size=1 \
    --overwrite_output_dir \
    --overwrite_cache \
    --block_size 512 \
    --tokenizer tokenizers/occitan \
    --overwrite_output_dir \
    --overwrite_cache \
    --logging_steps 400 \
    --save_steps 400 \
    > outputs/occitan_$n.log 2>&1
done

for n in 1 2 5 9; do
  python scripts/finetune.py \
    --output_dir="outputs/yoruba_$n/" \
    --model_type=gpt2 \
    --model_name_or_path=gpt2 \
    --save_total_limit=2 \
    --do_train \
    --num_train_epochs=1 \
    --do_eval \
    --train_data_file="data/yor_community_2017/training_${n}k_clean_yor_community_2017-sentences.txt" \
    --eval_data_file="data/yor_community_2017/validation_1k_clean_yor_community_2017-sentences.txt" \
    --per_gpu_train_batch_size=1 \
    --overwrite_output_dir \
    --overwrite_cache \
    --block_size 512 \
    --tokenizer tokenizers/yoruba \
    --overwrite_output_dir \
    --overwrite_cache \
    --logging_steps 400 \
    --save_steps 400 \
    > outputs/yoruba_$n.log 2>&1
done
