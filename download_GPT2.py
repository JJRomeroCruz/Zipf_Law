from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2"
save_path = "./models"

# download the model
tokenizer = GPT2Tokenizer.from_pretrained(model_name, cache_dir="./models")
model = GPT2LMHeadModel.from_pretrained(model_name, cache_dir="./models")


tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)