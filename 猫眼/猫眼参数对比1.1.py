import execjs
import requests
import os
from cmap import build_mapping, decrypt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open("猫眼_code.js", "r", encoding="utf-8") as f:
    js_code = f.read()
ctx = execjs.compile(js_code)

cookies = {
    '_ga': 'GA1.1.610928589.1790198425',
    '_lxsdk_cuid': '1a0d0242425c8-0f704622b11fd68-26061951-240000-1a0d0242425c8',
    '_lxsdk': '970F4840B79411F19702A1876DDA39B603B9C352F1AD4412AC5977A696FEAE22',
    'WEBDFPID': '2yyw47xwz0475y41z14yv24w4xvzz4vw8z9w9757036679584817wz9v-1790284824737-1790198423738EQMEEAUfd79fef3d01d5e9aadc18ccd4d0c95071743',
    'utm_source_rg': 'AM%255eZ9a90%25138%25Qkk5bS359xbSokbK9KbkvQb5b3v99bv5y9l5lSoSxzaaSloybyKS59lv',
    '_ga_WN80P4PSY7': 'GS2.1.s1790198424$o1$g1$t1790198736$j15$l0$h0',
    '_lx_utm': 'utm_source%3DBaidu%26utm_medium%3Dorganic',
    '_lxsdk_s': '1a0d0242426-2bd-254-b68%7C%7C39',
}

url = "https://piaofang.maoyan.com/i/api/encrypt/dashboard-ajax/movie?showDate=20260924&movieId=&orderType=0&yodaReady=h5&csecplatform=4&csecversion=4.3.0"

sign_headers = {
    "Accept": "application/json, text/plain, */*",
    "M-APPKEY": "fe_com.sankuai.movie.fe.ipro",
    "uid": "86a7cabae1a5a584c9dbc6973a9d490dd8084ed0",
    "uuid": "1a0d0242425c8-0f704622b11fd68-26061951-240000-1a0d0242425c8",
    "channelid": "40009",
    "m-traceid": "-3696672313376002060",
}

mtgsig = ctx.call("getMtgSig", url, "GET", None, sign_headers)
# print("mtgsig =", mtgsig)

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'channelid': '40009',
    'm-appkey': 'fe_com.sankuai.movie.fe.ipro',
    'm-traceid': '-3696672313376002060',
    'mtgsig': mtgsig,
    'priority': 'u=1, i',
    'referer': 'https://piaofang.maoyan.com/i/dashboard/movie',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'uid': '86a7cabae1a5a584c9dbc6973a9d490dd8084ed0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'uuid': '1a0d0242425c8-0f704622b11fd68-26061951-240000-1a0d0242425c8',
}

font_headers = {
    'Origin': 'https://piaofang.maoyan.com',
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://piaofang.maoyan.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
}

response = requests.get(url, cookies=cookies, headers=headers)
data=response.json()
url=data['fontStyle'].split('url("')[-1].replace('");}','')
font_url="https:"+url

woff_path=os.path.join(BASE_DIR,"猫眼.woff")
resp=requests.get(font_url,headers=font_headers)
with open("猫眼.woff",'wb')as f:
    f.write(resp.content)

#调用外部模块生成映射
mapping=build_mapping(woff_path)
# print(f"\n[+] 映射表: {mapping}")

#解密字体
def decrypt_obj(obj):
    if isinstance(obj, str):
        return decrypt(obj, mapping)
    if isinstance(obj, dict):
        return {k: decrypt_obj(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [decrypt_obj(x) for x in obj]
    return obj
decrypted=decrypt_obj(data)

# ========== 6. 打印结果 ==========
print("\n=== splitBoxSplitUnit 解密 ===")
for movie in decrypted["movieList"]["list"]:
    name = movie["movieInfo"]["movieName"]
    split = movie.get("splitBoxSplitUnit") or {}
    num = split.get("num", "")
    unit = split.get("unit", "")
    print(f"{name:35s} {num}{unit}")


