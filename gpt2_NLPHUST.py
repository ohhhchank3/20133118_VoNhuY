import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def generate_text(prompt):
    tokenizer = GPT2Tokenizer.from_pretrained('NlpHUST/gpt2-vietnamese')
    model = GPT2LMHeadModel.from_pretrained('NlpHUST/gpt2-vietnamese')
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    max_length = 200
    sample_outputs = model.generate(input_ids, pad_token_id=tokenizer.eos_token_id,
                                    do_sample=True,
                                    max_length=max_length,
                                    min_length=max_length,
                                    top_k=40,
                                    num_beams=5,
                                    early_stopping=True,
                                    no_repeat_ngram_size=2,
                                    num_return_sequences=3)
    # Chỉ trả về bản ghi cuối cùng
    generated_text = tokenizer.decode(sample_outputs[-1].tolist())
    return generated_text
