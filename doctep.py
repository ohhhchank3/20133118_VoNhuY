import random

import requests


def random_number():
    # Trả về một số ngẫu nhiên từ 1 đến 7
    return random.randint(1, 6)

def is_valid_api_key(api_key):
    url = "https://api.openai.com/v1/chat/completions"
    api_key1= api_key

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": "Hello"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
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
    # Sử dụng hàm để lấy một số ngẫu nhiên và in ra màn hình
    random_value = random_number()

    with open('apiKey.txt', 'r') as file:
        # Đọc nội dung của tệp
        lines = file.readlines()

        # Trích xuất thông tin từ dòng cụ thể
        index_to_check = random_value % len(lines)  # Tránh lỗi nếu random_value lớn hơn số dòng
        desired_line = lines[index_to_check].strip()

        # Kiểm tra tính hợp lệ của API key
        if is_valid_api_key(desired_line):
            print("API key hợp lệ")
        else:
            print("API key không hợp lệ, xóa dòng")

            # Xóa dòng không hợp lệ khỏi tệp
            #lines.pop(index_to_check)

            # Ghi lại nội dung của tệp
            with open('apiKey.txt', 'w') as file_write:
                file_write.writelines(lines)

    return desired_line  # Trả về giá trị của API key

