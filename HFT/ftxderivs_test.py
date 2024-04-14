import json
import pandas as pd
import requests

def get_ftx_data():
	key = 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyIjp7ImlkIjozNzY0NCwiaXBfYWRkcmVzcyI6IjEwLjIwLjExLjM0IiwiY2lkIjoyNTU4MjkyMDE0LCJtcGlkIjozODMwNDM2NTI1LCJhY2NvdW50X2lkIjo0MjAxMCwiaXNfdHJhZGVyIjp0cnVlLCJpc19tcF9hZG1pbiI6dHJ1ZSwiaXNfYXVkaXRvciI6ZmFsc2UsImlzX2VjcCI6ZmFsc2V9LCJleHAiOjE2NjY1NDg5OTcsImp0aSI6ImU1MjZkNmY5ZjljNDNmZGVkMWI4NDlhZmQxNjFkMDYwMzU4YTI1ZmEzMjlmNjA2YmMyYjk1ZGUyODAzNGIyY2YzYTNiZmRkZjcwZGY4Yjg1In0.ksPv3UT03rsK3hwO78N6Zo7_uX9o4eGmlBvYTiCVAgbscl_UL_kzaw9bHm3i6XVELCZNMe6N4Gktiom_tspz3w'

	url = "https://api.ledgerx.com/trading/contracts?"
	active = "active=true"
	contract = ""#"&contract_type=call"
	derivative = "&derivative_type=options_contract"
	before = "&before_ts=2022-10-28T00%3A00"
	asset = "&asset=ETH"
	limit = ""#&limit=10"
	total = url+active+contract+derivative+before+asset+limit

	headers = {"accept": "application/json","Authorization": key}

	response = requests.get(total, headers=headers)
	rj = json.loads(response.text)
	num_results = int(rj['meta']['total_count'])

	ids = [rj['data'][i]['id'] for i in range(num_results)]

	label = list()
	expiry = list()
	strike = list()
	is_call = list()
	bid = list()
	ask = list()
	last = list()
	timestamp = list()

	for j in range(len(ids)):
		
		contract_link = "https://api.ledgerx.com/trading/contracts/"+str(ids[j])+"/ticker"
		contract_response = requests.get(contract_link, headers=headers)
		contract_json = json.loads(contract_response.text)

		label.append(rj['data'][j]['label'])
		expiry.append(pd.to_datetime(rj['data'][j]['date_expires']))
		strike.append(int(rj['data'][j]['strike_price'])/100)
		is_call.append(bool(rj['data'][j]['is_call']))
		bid.append(float(contract_json['data']['bid'])/100)
		ask.append(float(contract_json['data']['ask'])/100)
		try:
			last.append(float(contract_json['data']['last_trade']['price'])/100)
			timestamp.append(pd.to_datetime(contract_json['data']['last_trade']['time']))
		except:
			last.append(0.0)
			timestamp.append(pd.to_datetime(0))
		

	ftx_options = pd.DataFrame(
					{'contract':label,
					'expiry':expiry,
					'strike':strike,
					'is_call':is_call,
					'bid':bid,
					'ask':ask,
					'last':last,
					'timestamp':timestamp},
					index=range(len(ids))
					)

	return ftx_options


print(get_ftx_data())


