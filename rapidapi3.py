import requests


def get_chatbot_response(message):
    url = "https://lemurbot.p.rapidapi.com/chat"

    payload = {
        "bot": "dilly",
        "client": "d531e3bd-b6c3-4f3f-bb58-a6632cbed5e2",
        "message": message
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "744560b352msh56a291550432aeep1c01d7jsn9226c469da4c",
        "X-RapidAPI-Host": "lemurbot.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.ok:
        data = response.json()
        if 'data' in data and 'conversation' in data['data']:
            output_from_bot = data['data']['conversation']['output']
            return output_from_bot
        else:
            return "Unable to extract 'output' from the response."
    else:
        return f"Request failed with status code: {response.status_code}"


