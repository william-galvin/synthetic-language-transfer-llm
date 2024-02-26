  python finetune.py \
    --output_dir="outputs/frisian/" \
    --model_type=gpt2 \
    --model_name_or_path=gpt2 \
    --save_total_limit=2 \
    --do_train \
    --train_data_file="data/fry_news_2020_100K/clean_fry_news_2020_100K-sentences.txt" \
    --per_gpu_train_batch_size=1 \
    --overwrite_output_dir \
    --overwrite_cache \
    --block_size 512 \
    --tokenizer tokenizers/frisian