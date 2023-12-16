import requests

def main(messages,model,apikey):
    url = "https://api.openai.com/v1/chat/completions"
    api_key = apikey  # Thay thế bằng API key thực tế của bạn

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
    response = requests.post(url, headers=headers, json=data)
    result_json = response.json()
    # Lấy nội dung từ đối tượng JSON
    content = result_json['choices'][0]['message']['content']
    return content



