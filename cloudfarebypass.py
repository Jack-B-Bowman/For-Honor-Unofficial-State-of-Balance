import json, requests

url = 'http://falcon.proxyrotator.com:51337/'

params = dict(
    apiKey='FTPoXxC6253AUzrat4vNK87hfMbm9Hpe'
)

resp = requests.get(url=url, params=params)
data = json.loads(resp.text)
print(data)