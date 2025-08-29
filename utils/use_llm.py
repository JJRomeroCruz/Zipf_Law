from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

local_path = "models"

tokenizer = GPT2Tokenizer.from_pretrained(local_path, local_files_only=True)
model = GPT2LMHeadModel.from_pretrained(local_path, local_files_only=True)

tokenizer.pad_token = tokenizer.eos_token

#input = tokenizer.encode("Había una vez un niño llamado ", return_tensors="pt", padding=True, truncation=True)
input = tokenizer("Había una vez un niño llamado ", return_tensors="pt", padding=True, truncation=True)

output = model.generate(
    input["input_ids"],
    attention_mask=input["attention_mask"], 
    max_length=100, 
    do_sample=True,
    top_k=50, 
    top_p=0.95,
    temperature=0.9,
    pad_token_id=tokenizer.eos_token_id
)

print(tokenizer.decode(output[0], skip_special_tokens=True))

