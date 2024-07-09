export WANDB_DISABLED=true

CUDA_VISIBLE_DEVICES=0 \
    python run_summarization_baseline.py \
    --model_name_or_path  "google-t5/t5-small" \
    --do_train \
    --do_eval \
    --train_file ./dataset/train_3000/first_3000_train_qfid.csv \
    --validation_file ./dataset/train_3000//first_300_val_qfid.csv \
    --test_file ./dataset/train_3000/first_300_test_qfid.csv \
    --source_prefix "summarize: " \
    --text_column reference \
    --summary_column target \
    --output_dir ./test \
    --auto_find_batch_size \
    --num_train_epochs=1 \
    --predict_with_generate \
    --save_strategy epoch \
    --evaluation_strategy epoch \
    --load_best_model_at_end \
    --save_total_limit=1 \
    --metric_for_best_model=eval_rouge2 \
    --greater_is_better True \
    --max_source_length 1024 \
    --max_target_length 512 \
    --generation_max_length 512 \
    --num_beams 4 \
    --overwrite_output_dir \
    
