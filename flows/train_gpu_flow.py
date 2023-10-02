from metaflow import step, FlowSpec, kubernetes

MY_IMAGE = "eddieob/torch-transformers-datasets:1"

class HFTestFlow(FlowSpec):

    @step
    def start(self):
        print("Starting")
        self.next(self.train)

    @kubernetes(cpu=4, gpu=1, memory=16000, image=MY_IMAGE)
    @step
    def train(self):

        import os
        import sys
        import torch

        from datasets import load_dataset
        dataset = load_dataset("imdb")

        print(os.popen("nvidia-smi").read())
        print(os.popen("nvcc --version").read())
        print('__Python VERSION:', sys.version)
        print('__pyTorch VERSION:', torch.__version__)
        print('__CUDA VERSION')
        print('__CUDNN VERSION:', torch.backends.cudnn.version())
        print('__Number CUDA Devices:', torch.cuda.device_count())
        print('__Devices')
        print('Active CUDA Device: GPU', torch.cuda.current_device())
        print('Available devices ', torch.cuda.device_count())
        print('Current cuda device ', torch.cuda.current_device())
 
        print(f"GPU count: {torch.cuda.device_count()}")
        assert torch.cuda.is_available()

        from transformers import AutoTokenizer, Trainer, TrainingArguments, AutoModelForSequenceClassification, DataCollatorWithPadding
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

        tokenized_data = dataset.map(lambda examples: self.tokenizer(examples["text"], truncation=True), batched=True)
        data_collator = DataCollatorWithPadding(tokenizer=self.tokenizer)

        self.training_args = TrainingArguments(
            output_dir="imdb-model",
            learning_rate=2e-5,
            per_device_train_batch_size=16,
            per_device_eval_batch_size=16,
            num_train_epochs=2,
            weight_decay=0.01,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            push_to_hub=False,
        )

        trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=tokenized_data["train"],
            eval_dataset=tokenized_data["test"],
            data_collator=data_collator,
            tokenizer=self.tokenizer,
        )

        trainer.train()
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    HFTestFlow()