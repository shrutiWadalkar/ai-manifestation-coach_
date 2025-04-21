import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import load_dataset

def fine_tune_mistral(base_model="mistralai/Mistral-7B-v0.1", dataset_path="your_dataset.json"):
    # Load model with QLoRA
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        load_in_4bit=True,
        device_map="auto",
        torch_dtype=torch.float16
    )
    
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Setup LoRA
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, lora_config)
    
    # Load dataset (customize for your LOA content)
    dataset = load_dataset("json", data_files=dataset_path)["train"]
    
    # Training setup
    training_args = TrainingArguments(
        output_dir="./mistral-7b-loa",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-5,
        num_train_epochs=3,
        logging_dir="./logs",
        save_strategy="epoch",
        fp16=True
    )
    
    # Train (you'll need to customize the data collator)
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer
    )
    trainer.train()
    
    # Save adapter
    model.save_pretrained("./mistral-7b-loa-adapter")