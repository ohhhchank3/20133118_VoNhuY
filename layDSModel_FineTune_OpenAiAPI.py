import openai

def main():
    # Set your OpenAI API key
    api_key = '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'
    openai.api_key = api_key
    # List all models
    models = openai.Model.list()
    # Extract only the "id" values and create a list
    model_ids = [d["id"] for d in models.data if d["id"].startswith("ft:gpt")]
    return model_ids



