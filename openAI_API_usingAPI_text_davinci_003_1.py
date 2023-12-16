import openai

model_engine = "text-davinci-003"
def main(prompt1, maxtoken,key,id):
    api_key = key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Openai-Organization":id
    }
    openai.api_key = api_key
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt1,
        temperature=0.6,
        n=1,
        stop=None,
        max_tokens=maxtoken,
        headers=headers  # Thêm headers vào yêu cầu API
    )
    return response['choices'][0]['text']


