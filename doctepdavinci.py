import random

import requests


def random_number():
    return random.randint(1, 3)

def is_valid_api_key(api_key):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {"role": "user", "content": "Hello"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

    return False

def main():
    # Đọc dữ liệu từ tệp
    with open('daivinci.txt', 'r') as file:
        lines = file.readlines()

    # Lấy một số ngẫu nhiên để chọn dòng từ tệp
    random_value = random_number()
    index_to_check = random_value % len(lines)
    desired_line = lines[index_to_check].strip()

    # Chia các giá trị trong dòng
    values = desired_line.split(',')

    # Kiểm tra tính hợp lệ của API key
    if is_valid_api_key(values[0]) and is_valid_api_key(values[1]):
        print("API keys hợp lệ")
    else:
        print("Ít nhất một API key không hợp lệ, xóa dòng")

        # Xóa dòng không hợp lệ khỏi tệp
        # lines.pop(index_to_check)

        # Ghi lại nội dung của tệp
        # with open('apiKey.txt', 'w') as file_write:
        #     file_write.writelines(lines)

    # Trả về cả hai giá trị
    return values[0], values[1]


