from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def summarize_text(input_sentence):
    tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base-vietnews-summarization")
    model = AutoModelForSeq2SeqLM.from_pretrained("VietAI/vit5-base-vietnews-summarization")
    sentence = input_sentence + "</s>"
    encoding = tokenizer(sentence, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]
    outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        max_length=256,
        early_stopping=True
    )
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return summary

