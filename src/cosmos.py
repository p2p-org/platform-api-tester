from base_api import BaseAPI

class CosmosAPI(BaseAPI):
    async def stake(self, params):
        payload = {
            'stashAccountAddress': params['stashAccountAddress'],
            'amount': params['amount']
        }
        return await self.call_method('stake', payload)

    async def unstake(self, params):
        payload = {
            'stashAccountAddress': params['stashAccountAddress'],
            'amount': params['amount']
        }
        return await self.call_method('unstake', payload)

    async def broadcast(self, signed_transaction):
        payload = {
            'signedTransaction': signed_transaction
        }
        return await self.call_method('broadcast', payload)