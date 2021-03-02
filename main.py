import requests

url = "http://10.5.0.219/light/test_bulb/turn_on"

headers = {
    'authorization': "Digest username=\"admin\", realm=\"asyncesp\", nonce=\"\", uri=\"/light/test_bulb/turn_on?r=255&g=0&b=0&brightness=255\", qop=auth, nc=, cnonce=\"\", response=\"2858d15a99bb1659a04056065b7c7c3f\", opaque=\"\"",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "117c6d7f-9a33-9ee8-1cab-deae9bf7be08"
    }

querystring = {"r":"0","g":"255","b":"0","brightness":"255"}

response = requests.request("POST", url, headers=headers, params=querystring)

print(response.text)

input("placeholder")