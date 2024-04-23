from src.base_network import BaseNetwork

class Polkadot(BaseNetwork):
    def __init__(self, api_key, base_url, network_name, environment):
        base_url = f"{base_url}/polkadot/westend" if environment == "testnet" else f"{base_url}/polkadot/mainnet"
        super().__init__(api_key, base_url, network_name, environment)

    async def stake(self, params):
        url = f'{self.base_url}/staking/bond'
        payload = {
            'stashAccountAddress': params['stashAccountAddress'],
            'rewardDestinationType': params['rewardDestinationType'],
            'rewardDestination': params['rewardDestination'],
            'amount': params['amount']
        }
        response = await self.make_request(url, 'POST', payload)
        return self.parse_response(response, 'stake')

    async def broadcast(self, signed_transaction):
        url = f'{self.base_url}/tx/send'
        payload = {
            'signedTransaction': signed_transaction
        }
        response = await self.make_request(url, 'POST', payload)
        return self.parse_response(response, 'broadcast')