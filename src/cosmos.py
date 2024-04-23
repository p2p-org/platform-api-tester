from src.base_network import BaseNetwork

class Cosmos(BaseNetwork):
    def __init__(self, api_key, base_url, network_name, environment):
        base_url = f"{base_url}/cosmos/theta-testnet-001" if environment == "testnet" else f"{base_url}/cosmos/cosmoshub-4"
        super().__init__(api_key, base_url, network_name, environment)

    async def stake(self, params):
        url = f'{self.base_url}/staking/stake'
        payload = {
            'stashAccountAddress': params['stashAccountAddress'],
            'amount': params['amount']
        }
        response = await self.make_request(url, 'POST', payload)
        return self.parse_response(response, 'stake')

    async def unstake(self, params):
        url = f'{self.base_url}/staking/unstake'
        payload = {
            'stashAccountAddress': params['stashAccountAddress'],
            'amount': params['amount']
        }
        response = await self.make_request(url, 'POST', payload)
        return self.parse_response(response, 'unstake')

    async def broadcast(self, signed_transaction):
        url = f'{self.base_url}/transaction/send'
        payload = {
            'signedTransaction': signed_transaction
        }
        response = await self.make_request(url, 'POST', payload)
        return self.parse_response(response, 'broadcast')