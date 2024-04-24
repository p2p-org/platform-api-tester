from base_network import BaseNetwork

class Solana(BaseNetwork):
    def __init__(self, api_key, base_url, network_name, blockchain_env, api_env):
        base_url = f"{base_url}/solana/{'testnet' if blockchain_env == 'testnet' else 'mainnet-beta'}"
        super().__init__(api_key, base_url, network_name, blockchain_env, api_env)

    async def stake(self, params):
        url = f'{self.base_url}/staking/stake'
        payload = {
            'feePayer': params['feePayer'],
            'fromPublicKey': params['fromPublicKey'],
            'stakeAuthority': params.get('stakeAuthority', params['fromPublicKey']),
            'withdrawAuthority': params.get('withdrawAuthority', params['fromPublicKey']),
            'amount': params['amount']
        }
        response = await self.make_request(url, 'POST', payload)
        return self.parse_response(response, 'stake')