from rest_lx.rest import LxClient

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyIjp7ImlkIjozNzY0NCwiaXBfYWRkcmVzcyI6IjEwLjIwLjExLjM0IiwiY2lkIjoyNTU4MjkyMDE0LCJtcGlkIjozODMwNDM2NTI1LCJhY2NvdW50X2lkIjo0MjAxMCwiaXNfdHJhZGVyIjp0cnVlLCJpc19tcF9hZG1pbiI6dHJ1ZSwiaXNfYXVkaXRvciI6ZmFsc2UsImlzX2VjcCI6ZmFsc2V9LCJleHAiOjE2NjY1NDg5OTcsImp0aSI6ImU1MjZkNmY5ZjljNDNmZGVkMWI4NDlhZmQxNjFkMDYwMzU4YTI1ZmEzMjlmNjA2YmMyYjk1ZGUyODAzNGIyY2YzYTNiZmRkZjcwZGY4Yjg1In0.ksPv3UT03rsK3hwO78N6Zo7_uX9o4eGmlBvYTiCVAgbscl_UL_kzaw9bHm3i6XVELCZNMe6N4Gktiom_tspz3w"  # TODO: Put API key here

# Init REST client
client = LxClient(api_key=api_key)
print(client.list_transactions())
# list active day-ahead-swap contracts
options = client.list_contracts({
    'active': True,
    'derivative_type': 'options_contract',
})

# grab ETH options contract ID
data = options['data']
eth_option = filter(lambda data: data['underlying_asset'] == 'ETH', data)
contract_id = next(eth_option)['id']
print(f"ETH Option contract_id: {contract_id}")

# retrieve your position for BTC day-ahead-swap contract (requires authentication)
position = client.retrieve_contract_position(contract_id)
print(f"ETH option position: {position}")

# place bid for BTC next-day swap
lx_buy = {
    'order_type': 'limit',
    'contract_id': contract_id,
    'is_ask': False,
    'swap_purpose': 'undisclosed',
    'size': 1,
    'price': 100,  # $1 (100 cents)
    'volatile': True
}
order = client.create_order(**lx_buy)

# cancel placed order
message_id = order['data']['mid']  # order ID
print('order',message_id,'placed')
position = client.retrieve_contract_position(contract_id)
print(f"ETH option position: {position}")
client.cancel_single_order(message_id=message_id, contract_id=contract_id)