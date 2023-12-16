import openai

model_engine = "text-davinci-003"
def main(prompt1, maxtoken, key, id,temp,stop):
    api_key = key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Openai-Organization": id
    }
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt1,
            temperature=temp,
            n=1,
            stop=stop,
            max_tokens=maxtoken,
            headers=headers  # Thêm headers vào yêu cầu API
        )
        return response['choices'][0]['text']
    except openai.error.OpenAIError as e:
        # Xử lý lỗi từ OpenAI API
        error_message = f"OpenAI API error: {e}"
        print(error_message)
        return error_message
    except Exception as e:
        # Xử lý các ngoại lệ khác
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return error_message


