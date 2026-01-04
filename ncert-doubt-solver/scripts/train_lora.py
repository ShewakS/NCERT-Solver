import argparse
import transformers
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType

def train_lora(
    base_model_name: str, 
    data_path: str, 
    output_dir: str = "./finetuned_model",
    epochs: int = 3
):
    print(f"Starting Finetuning for {base_model_name} on {data_path}...")
    
    # Load model and tokenizer
    # For T5/Seq2Seq
    model = transformers.AutoModelForSeq2SeqLM.from_pretrained(base_model_name)
    tokenizer = transformers.AutoTokenizer.from_pretrained(base_model_name)
    
    # LoRA Configuration
    peft_config = LoraConfig(
        task_type=TaskType.SEQ_2_SEQ_LM, 
        inference_mode=False, 
        r=8, 
        lora_alpha=32, 
        lora_dropout=0.1
    )
    
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()
    
    # Load dataset
    # Expecting a JSONL file with {"input": "...", "output": "..."}
    try:
        dataset = load_dataset('json', data_files=data_path)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    def preprocess_function(examples):
        inputs = examples["input"]
        targets = examples["output"]
        model_inputs = tokenizer(inputs, max_length=512, truncation=True)
        labels = tokenizer(targets, max_length=512, truncation=True)
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_datasets = dataset.map(preprocess_function, batched=True)
    
    # Training Arguments
    training_args = transformers.TrainingArguments(
        output_dir=output_dir,
        learning_rate=1e-3,
        per_device_train_batch_size=4,
        num_train_epochs=epochs,
        save_steps=1000,
        save_total_limit=2,
        logging_steps=100,
    )
    
    trainer = transformers.Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
    )
    
    try:
        trainer.train()
        model.save_pretrained(output_dir)
        print(f"Finetuning complete. Model saved to {output_dir}")
    except Exception as e:
        print(f"Training failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="google/flan-t5-base", help="Base model")
    parser.add_argument("--data", type=str, required=True, help="Path to training data (jsonl)")
    args = parser.parse_args()
    
    train_lora(args.model, args.data)
