import requests


def get_iam_token():
	headers = {
	    'Content-Type': 'application/x-www-form-urlencoded',
	}

	data = '{"yandexPassportOauthToken":"y0_AgAAAAA3hobLAATuwQAAAAEGW6ZGAAD4-7rTv_lMuZSQBSHXrPZaY3qEYg"}'

	response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', headers=headers, data=data)
	return response.json()


print(get_iam_token())