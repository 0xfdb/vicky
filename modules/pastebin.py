import requests

dev_key = "redacted"
username = "redacted"
password = "redacted"
header = {"Content-Type": "application/json; charset=utf8"}
privatepaste = 1 #limits for this are confusing http://192.184.83.59/SPG%20All/pastebin.com/faq.html#11a

def pastebin(pastedata):
	params = {"api_option": "paste", "api_user_key": "", "api_paste_private": privatepaste, "api_dev_key": dev_key, "api_paste_expire_date": "10M", "api_paste_format": "php", "api_paste_code": pastedata}
	req = requests.post("http://pastebin.com/api/api_post.php", data=params)
	return req.text
