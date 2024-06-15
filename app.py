from flask import Flask, jsonify, request
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

# ANSI color codes for colored output
G = '\x1b[1;32m'  # Green
E = '\x1b[1;31m'  # Red
F = '\x1b[2;32m'  # Dim Green
X = '\x1b[1;33m'  # Yellow

total_money = 0
Good = 0
Bad = 0

def process_account(email, password):
    global total_money, Good, Bad
    headers = {
        'authority': 'faucetearner.org',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://faucetearner.org',
        'referer': 'https://faucetearner.org/login.php',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'act': 'login',
    }

    json_data = {
        'email': email,
        'password': password,
    }

    try:
        response = requests.post('https://faucetearner.org/api.php', params=params, headers=headers, json=json_data, timeout=10)
        if "Login successful" in response.text:
            Mahos = response.cookies.get_dict()
            print(f'{G}Good Login for {email}')
            Money(Mahos)
        elif "wrong username or password" in response.text:
            print(f'{E}Bad Login for {email}')
        else:
            print(f'{X}Error for {email}')
    except requests.exceptions.RequestException as e:
        print(f'{X}Error for {email}: {str(e)}')

def Money(cookies):
    global total_money, Good, Bad
    while True:
        time.sleep(5)
        headers = {
            'authority': 'faucetearner.org',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
            'origin': 'https://faucetearner.org',
            'referer': 'https://faucetearner.org/faucet.php',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'act': 'faucet',
        }

        try:
            rr = requests.post('https://faucetearner.org/api.php', params=params, cookies=cookies, headers=headers, timeout=10).text

            if 'Congratulations on receiving' in rr:
                Good += 1
                json_data = json.loads(rr)
                message = json_data.get("message", "")
                start_index = message.find(">") + 1
                end_index = message.find(" ", start_index)
                balance = message[start_index:end_index]
                total_money += float(balance)
                print(f"{F}Done {balance} XRP£. Total money: {total_money}")
            elif 'You have already claimed, please wait for the next wave!' in rr:
                Bad += 1
                print(f'{E}Bad Claim with this account.')
            else:
                print(f'{X}Error')
        except requests.exceptions.RequestException as e:
            print(f'{X}Error: {str(e)}')

def run_accounts(emails, passwords):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_account, email, password) for email, password in zip(emails, passwords)]
        for future in as_completed(futures):
            pass  # Handle results if needed

# Flask route
@app.route('/')
def hello_world():
    return 'Hello from Koyeb'

# Flask route for checking total money
@app.route('/total_money')
def get_total_money():
    return jsonify({'total_money': total_money})

# Flask route for checking good logins
@app.route('/good_logins')
def get_good_logins():
    return jsonify({'good_logins': Good})

# Flask route for checking bad logins
@app.route('/bad_logins')
def get_bad_logins():
    return jsonify({'bad_logins': Bad})

if __name__ == "__main__":
    # List of emails and passwords
    emails = ['imadser', 'imadser001']
    passwords = ['imad2468', 'imad2468']

    # Start the Flask application
    app.run()
