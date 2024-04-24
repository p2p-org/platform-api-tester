from base_api import BaseAPI

class SolanaAPI(BaseAPI):
    async def stake(self, params):
        payload = {
            'feePayer': params['feePayer'],
            'fromPublicKey': params['fromPublicKey'],
            'stakeAuthority': params.get('stakeAuthority', params['fromPublicKey']),
            'withdrawAuthority': params.get('withdrawAuthority', params['fromPublicKey']),
            'amount': params['amount']
        }
        return await self.call_method('stake', payload)