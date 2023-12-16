import requests


def get_bingchat_response(question):
    url = "https://edgegpt-api.p.rapidapi.com/bingchat"
    bing_u_cookie = "1-caaY5H9zd3XQcChQ5TDpVmVdvqNS7tUVglEVvgcNDsSY7NOP2na62E9YfedNgPA-d8Y_5AB_Y0NdF2tYeIUZCa1wtzyJOemk9X2hE9KPQAFntG6LznGTo3WbqRrQDH3nUcrcTGsG-raZB9hU6IfCudo9euRHaPkfQVNX7fKzxePelj_9-SCRN2Vw9oAKzjKULL9_FW75dtR403rf_E9yQ"
    payload = {
        "question": question,
        "bing_u_cookie": bing_u_cookie,
        "conversation_style": "balanced"
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "744560b352msh56a291550432aeep1c01d7jsn9226c469da4c",
        "X-RapidAPI-Host": "edgegpt-api.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()['response']['text']


