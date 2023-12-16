import requests

def main(messages, model, apikey):
    url = "https://api.openai.com/v1/chat/completions"
    api_key = apikey

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": messages}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Nếu có lỗi trong response, nó sẽ ném ra một ngoại lệ
        result_json = response.json()
        # Lấy nội dung từ đối tượng JSON
        content = result_json['choices'][0]['message']['content']
        return content
    except requests.exceptions.RequestException as e:
        content = f"Request failed: {e}"
        return content
    except Exception as e:
        # Xử lý các ngoại lệ khác
        content = f"An unexpected error occurred: {e}"
        return content



