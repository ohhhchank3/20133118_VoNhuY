import requests


def main(message_content,model):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiIyMDEzMzExOEBzdHVkZW50LmhjbXV0ZS5lZHUudm4iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJwb2lkIjoib3JnLWhjSzRMdFR1OHFzVE9uSjJFZmExNklWaiIsInVzZXJfaWQiOiJ1c2VyLWpEeFYyTEtic3hPWU5CRjQ0V1RZaWpXdyJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTc3MDEzMzgzNTQwMjgxNjY5MjciLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzAzODk1NjE2LCJleHAiOjE3MDQ3NTk2MTYsImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIG9mZmxpbmVfYWNjZXNzIn0.GaCtrjkbYAP1lzydeYKSxeF93BEQp-kZAw0jtGS77udRiL24diFBHq5XG7ZwZgT7EkiDXhQ46UVS7lBncnwQYgt_Y7-QfjqAUQumVANxQK8d7uLD4n9kXfx-DISUxVhXI93Hkp4b5vCQ_15dWw-pzveg1IANca7VjufTkR6lTk0YtAtxYuIGcelA2e027Q6AieuJCbM-LFfstZzVxeaSFv09oruzHY9QZEdPrsBPQxDwSSX6Y1XgQGYusd7cgcbEsV8HWtEe_hLFNBzeXkpge_5a-y0fiAiCh6FrD7n5dxp0-zfUhG7HBKEI0dGW9UJ5B4wiBbpisa0Uj2mTWuZqoA',
        'Content-Type': 'application/json',
    }
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": message_content
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    result_json = response.json()
# Kiểm tra xem 'choices' có tồn tại trong result_json hay không
    if 'choices' in result_json:
        # Lấy nội dung từ đối tượng JSON
        content = result_json['choices'][0]['message']['content']
        return content
    else:
        return "Không có dữ liệu phản hồi từ OpenAI API"
    


