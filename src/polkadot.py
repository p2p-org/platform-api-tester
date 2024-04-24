from base_api import BaseAPI

class PolkadotAPI(BaseAPI):
    async def stake(self, params):
        payload = {
            'stashAccountAddress': params['stashAccountAddress'],
            'rewardDestinationType': params['rewardDestinationType'],
            'rewardDestination': params['rewardDestination'],
            'amount': params['amount']
        }
        return await self.call_method('stake', payload)

    async def broadcast(self, signed_transaction):
        payload = {
            'signedTransaction': signed_transaction
        }
        return await self.call_method('broadcast', payload)