# This is a sample Python script.
import requests
import sys
import hashlib


def req_api_data(first5_char):
    api = 'https://api.pwnedpasswords.com/range/' + first5_char
    res = requests.get(api)
    # print(res)
    if res.status_code != 200:
        raise RuntimeError('Response Error')
    return res.text


def get_pw_and_count(res, hash_tocheck):
    for line in res.splitlines():
        hashes, count = line.split(':')
        if hashes == hash_tocheck:
            return count
    return 0


def check_passwords(passwords):
    for pw in passwords:
        hash_pw = hashlib.sha1(pw.encode('utf-8')).hexdigest()
        first5_char, to_check = hash_pw[:5].upper(), hash_pw[5:].upper()
        response = req_api_data(first5_char)
        leaked_count = get_pw_and_count(response, to_check)
        if leaked_count == 0:
            print(f'Your password "{pw}" has never been breached. Congrats!')
        else:
            print(f'Your password "{pw}" has been breached for {leaked_count} times..')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    check_passwords(sys.argv[1:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
