import requests

def get_assistant_response(question):
    url = "http://localhost:8005/v1/chat/completions"
    # Prepare the JSON body
    json_body = {
        "messages": [
            {"content": "You are a helpful assistant.", "role": "system"},
            {"content": question, "role": "user"}
        ]
    }
    # Send POST request
    response = requests.post(url, json=json_body)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        response_data = response.json()
        # Extract and return the assistant's response
        if "choices" in response_data and response_data["choices"]:
            return response_data["choices"][0]["message"]["content"]
        else:
            return "No response from the assistant."
    else:
        return f"Request failed with status code: {response.status_code}"



