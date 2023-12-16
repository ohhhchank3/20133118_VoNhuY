import json
import re

import requests


def extract_content_from_chunk(chunk):
    # Sử dụng regex để trích xuất thông tin content từ chunk
    content_match = re.search(r'"content":"(.*?)"', chunk)
    if content_match:
        return content_match.group(1)
    return ""

def extract_content(response_text):
    # Tách các chunks dựa trên dấu xuống dòng
    chunks = response_text.split("\n\n")

    # Lấy thông tin content từ mỗi chunk và kết hợp chúng lại
    contents = [extract_content_from_chunk(chunk) for chunk in chunks]

    # Ghép các giá trị lại với nhau và cách nhau bằng khoảng trắng
    result = ' '.join(contents)

    return result

def get_chat_completion(message,model,temperature,presence,frequency,chat_token,top_p):
    url = "https://chat.eqing.tech/api/openai/v1/chat/completions"
    headers = {
       "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6ImQ4STRQOFppVVRWV25NaUwiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzAwODc4MjA4LCJpYXQiOjE3MDAyNzM0MDgsImlzcyI6Imh0dHBzOi8vYmpiZHNkd2F0dmlheGR1eWxyZHEuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6ImEzNDExYTI1LTAxZDctNDJlNS05ODAxLTU0YmE0MTMyMTRlOSIsImVtYWlsIjoidm9uaHV5NTExMjAwMkBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImdpdGh1YiIsInByb3ZpZGVycyI6WyJnaXRodWIiXX0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vYXZhdGFycy5naXRodWJ1c2VyY29udGVudC5jb20vdS85NDk2NDA5Nj92PTQiLCJlbWFpbCI6InZvbmh1eTUxMTIwMDJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vYXBpLmdpdGh1Yi5jb20iLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6Im9oaGhjaGFuazMiLCJwcm92aWRlcl9pZCI6Ijk0OTY0MDk2Iiwic3ViIjoiOTQ5NjQwOTYiLCJ1c2VyX25hbWUiOiJvaGhoY2hhbmszIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoib2F1dGgiLCJ0aW1lc3RhbXAiOjE3MDAxNDY5MjV9XSwic2Vzc2lvbl9pZCI6IjU4NzY2Mjc0LTI0OGEtNGNiMi1hMzE2LTk5MjZkZjVhYjk1ZCJ9.NYnaAD-U67XjTAZGQL2qNozpamF-xg58674LMwyNcJ4"
}

    payload = {
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": True,
        "model": model,
        "temperature": temperature,
        "presence_penalty": presence,
        "frequency_penalty": frequency,
        "top_p": top_p,
        "chat_token": chat_token
    }

    response = requests.post(url, json=payload, headers=headers)


    # Lấy thông tin content từ response
    result = extract_content(response.text)

    return result

def get_chat_completion1(message,model):
    url = "https://chat.eqing.tech/api/openai/v1/chat/completions"
    headers = {
       "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6ImQ4STRQOFppVVRWV25NaUwiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzAwODc4MjA4LCJpYXQiOjE3MDAyNzM0MDgsImlzcyI6Imh0dHBzOi8vYmpiZHNkd2F0dmlheGR1eWxyZHEuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6ImEzNDExYTI1LTAxZDctNDJlNS05ODAxLTU0YmE0MTMyMTRlOSIsImVtYWlsIjoidm9uaHV5NTExMjAwMkBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImdpdGh1YiIsInByb3ZpZGVycyI6WyJnaXRodWIiXX0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vYXZhdGFycy5naXRodWJ1c2VyY29udGVudC5jb20vdS85NDk2NDA5Nj92PTQiLCJlbWFpbCI6InZvbmh1eTUxMTIwMDJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vYXBpLmdpdGh1Yi5jb20iLCJwaG9uZV92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6Im9oaGhjaGFuazMiLCJwcm92aWRlcl9pZCI6Ijk0OTY0MDk2Iiwic3ViIjoiOTQ5NjQwOTYiLCJ1c2VyX25hbWUiOiJvaGhoY2hhbmszIn0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoib2F1dGgiLCJ0aW1lc3RhbXAiOjE3MDAxNDY5MjV9XSwic2Vzc2lvbl9pZCI6IjU4NzY2Mjc0LTI0OGEtNGNiMi1hMzE2LTk5MjZkZjVhYjk1ZCJ9.NYnaAD-U67XjTAZGQL2qNozpamF-xg58674LMwyNcJ4"
}

    payload = {
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": True,
        "model": model,
        "temperature": 0.5,
        "presence_penalty": 0.5,
        "frequency_penalty": 0,
        "top_p": 1,
        "chat_token": 125
    }

    response = requests.post(url, json=payload, headers=headers)

    try:
        response_dict = json.loads(response.text)
        return response_dict
    except json.JSONDecodeError:
        return {"error": "Failed to decode response as JSON."}
# Sử dụng hàm với một message bất kỳ




