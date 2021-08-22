import requests
import argparse
from datetime import datetime

def get_base_url():
    parser = argparse.ArgumentParser(description='Test this Flask api')
    parser.add_argument(
        'url',
        metavar='-u',
        type=str,
        nargs='?',
        help='the host url to test',
        default='http://127.0.0.1:5000/'
        )

    base_url = parser.parse_args().url

    if base_url[-1] == '/':
        base_url = base_url[:-1]
    if base_url[:4] != 'http':
        raise parser.error('is the url http:// or https:// ?')
    
    return base_url

def test(url, method, response_code, json=None):
    print(f'Testing URL: {url}')
    
    switch = {
        'get' : requests.get,
        'put' : requests.put,
        'post' : requests.post,
        'patch' : requests.patch,
        'delete' : requests.delete
    }

    r = switch[method](url, json=json)

    print(f'Desired Code: {response_code}')
    print(f'Actual Code: {r.status_code}')

    if r.status_code == response_code:
        print('Success!\n')
    else:
        print('Failed!\n')
        raise Exception(f'{url} provided the wrong response:\n{r}')
    
    return r.json()


# The basic request URL - http://127.0.0.1 by default
base_url = get_base_url()


# Get all transactions
print('Get all transactions\n')
all_transactions = test(base_url+f'/transaction', 'get', 200) # Correct request
print(f'All transactions: {[t["id"] for t in all_transactions]}')
print()

# Get all buyers
print('Get all buyers\n')
all_buyers =test(base_url+f'/buyer', 'get', 200) # Correct request
print(f'All buyers: {[b["id"] for b in all_buyers]}')
print()

# Get all posters
print('Get all posters\n')
all_posters = test(base_url+f'/poster', 'get', 200) # Correct request
print(f'All posters: {[p["id"] for p in all_posters]}')
print()

# Get all responses
print('Get all responses\n')
all_responses = test(base_url+f'/response', 'get', 200) # Correct request
print(f'All responses: {[r["id"] for r in all_responses]}')
print()

transaction = all_transactions[0]
transaction_id = transaction['id']
buyer_id = transaction['buyer_id']
poster_id = transaction['posters'][0]

# Get transaction
print(f"Get transaction {transaction_id}\n")
r = test(base_url+f"/transaction/{transaction_id}", 'get', 200) # Correct request
print()

# Get buyer
print(f"Get buyer {buyer_id}\n")
r = test(base_url+f"/buyer/{buyer_id}", 'get', 200) # Correct request
print()

# Get poster
print(f"Get poster {poster_id}\n")
r = test(base_url+f"/poster/{poster_id}", 'get', 200) # Correct request
print()

print('All good, G!')