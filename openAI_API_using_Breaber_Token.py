import requests


def main(message_content,model):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiIyMDEzMzExOEBzdHVkZW50LmhjbXV0ZS5lZHUudm4iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJwb2lkIjoib3JnLWhjSzRMdFR1OHFzVE9uSjJFZmExNklWaiIsInVzZXJfaWQiOiJ1c2VyLWpEeFYyTEtic3hPWU5CRjQ0V1RZaWpXdyJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTc3MDEzMzgzNTQwMjgxNjY5MjciLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzAyMDkwNTU5LCJleHAiOjE3MDI5NTQ1NTksImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb3JnYW5pemF0aW9uLndyaXRlIG9mZmxpbmVfYWNjZXNzIn0.eOJDRX-L7kI1Km8C2t8kQyXrvNrRMerAAXSEO618EyupY1E_6sJo3obbZjHLdYO2CHLi9M56xtOi90oMgFb01zySabFx6NwerTb_1RJWPPq1ptNlKQ6aY8h3Ex1E31JTluzLrxRStfxzwDT66ZkVE-Lvn5BY5CWEfPYZ2gLga_lrPvMW4rquK12EEF-QSnYjb8E266X_33_KRdmzZOTgmUuyuAzrWDlcNQYtWFmMLSIHSUV1xzpgiTRAeM91V6jpl0qZgsTl44UiG3FVwY_I0SskfTuxql-uxhxoaCHpoy3yzPtK48kUsRWGvEDu-J_A4nAqrGDaJ0ewADqYahQvQQ',
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
    


