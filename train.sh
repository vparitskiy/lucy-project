python train.py --model_name_or_path 'satouV1' \
  --do_train \
  --do_eval \
  --do_predict \
  --learning_rate '3e-4' \
  --num_train_epochs 1 \
  --source_lang 'ja' \
  --target_lang 'en' \
  --pad_to_max_length True \
  --max_eval_samples 5000 \
  --max_predict_samples 5000 \
  --source_prefix "" \
  --dataset_path 'datasets/satou-big' \
  --per_device_train_batch_size=8 \
  --output_dir 'train/satouV2/' \
  --save_steps=10000 \
  --evaluation_strategy "steps" \
  --logging_strategy "steps" \
  --logging_steps=10000 \
  --predict_with_generate \
  --report_to "tensorboard" \
  --overwrite_output_dir False \
  --num_beams 4 \
  --use_fast_tokenizer False \
  --optim 'adafactor' \
  --preprocessing_num_workers 8 \
  --bf16 \
  #--tf32 \
  #--fp16 \


#  --gradient_accumulation_steps=64 \

# --gradient_checkpointing=True \
# --max_train_samples 10000
# --do_predict \
# --dataset_config_name 'en-ja' \