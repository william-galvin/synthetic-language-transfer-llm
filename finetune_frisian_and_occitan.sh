for n in 10 25 50 75 99; do 
  python finetune.py \
    --output_dir="outputs/frisian_$n/" \
    --model_type=gpt2 \
    --model_name_or_path=gpt2 \
    --save_total_limit=2 \
    --do_train \
    --num_train_epochs=1 \
    --do_eval \
    --train_data_file="data/fry_news_2020_100K/fry_news_training_${n}k-sentences.txt" \
    --eval_data_file="data/fry_news_2020_100K/fry_news_validation_1k-sentences.txt" \
    --per_gpu_train_batch_size=1 \
    --overwrite_output_dir \
    --overwrite_cache \
    --block_size 512 \
    --tokenizer tokenizers/frisian \
    --overwrite_output_dir \
    --overwrite_cache \
    > outputs/frisian_$n.log 2>&1
done

for n in 10 25 50 75 100 150 199; do 
  python finetune.py \
    --output_dir="outputs/occitan_$n/" \
    --model_type=gpt2 \
    --model_name_or_path=gpt2 \
    --save_total_limit=2 \
    --do_train \
    --num_train_epochs=1 \
    --do_eval \
    --train_data_file="data/oci_community_2023/oci_community_training_${n}k-sentences.txt" \
    --eval_data_file="data/oci_community_2023/oci_community_validation_1k-sentences.txt" \
    --per_gpu_train_batch_size=1 \
    --overwrite_output_dir \
    --overwrite_cache \
    --block_size 512 \
    --tokenizer tokenizers/occitan \
    --overwrite_output_dir \
    --overwrite_cache \
    > outputs/occitan_$n.log 2>&1
done
