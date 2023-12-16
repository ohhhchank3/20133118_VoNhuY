import json
import http.client
import requests

def main(question):
    # Send request to chatbot
    conn_bot = http.client.HTTPSConnection("harley-the-chatbot.p.rapidapi.com")

    payload_bot = {
        "client": "",
        "bot": "harley",
        "message": question
    }

    headers_bot = {
        'content-type': "application/json",
        'Accept': "application/json",
        'X-RapidAPI-Key': "744560b352msh56a291550432aeep1c01d7jsn9226c469da4c",
        'X-RapidAPI-Host': "harley-the-chatbot.p.rapidapi.com"
    }

    conn_bot.request("POST", "/talk/bot", json.dumps(payload_bot), headers_bot)

    res_bot = conn_bot.getresponse()
    data_bot = res_bot.read().decode("utf-8")

    # Parse JSON response from chatbot
    response_data_bot = json.loads(data_bot)

    # Extract and print the 'output' field from chatbot response
    if 'data' in response_data_bot and 'conversation' in response_data_bot['data']:
        output_from_bot = response_data_bot['data']['conversation']['output']

        # Use the result from chatbot to translate with the translation API
        url = "https://microsoft-translator-text.p.rapidapi.com/translate"

        querystring = {
            "to": "vi",
            "api-version": "3.0",
            "profanityAction": "NoAction",
            "textType": "plain"
        }

        payload = [{"Text": output_from_bot}]

        headers = {
            'content-type': "application/json",
            'X-RapidAPI-Key': "744560b352msh56a291550432aeep1c01d7jsn9226c469da4c",
            'X-RapidAPI-Host': "microsoft-translator-text.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers, params=querystring)

        if response.ok:
            data = response.json()
            if isinstance(data, list) and 'translations' in data[0] and isinstance(data[0]['translations'], list):
                translated_text = data[0]['translations'][0]['text']
                return translated_text
            else:
                return "Unable to extract 'text' from the translation response."
        else:
            return "Translation request failed with status code:", response.status_code
    else:
        return "Output field not found in the chatbot response."

