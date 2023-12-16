import requests


def main(content):
    url = "https://open-ai21.p.rapidapi.com/conversationmpt"

    payload = {
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "web_access": False
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "da4f58fd3dmsh5fd25e06985af08p102a61jsnb7edb73d0d25",
        "X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()['result']

