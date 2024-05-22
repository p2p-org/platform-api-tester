from base_api import BaseAPI

class CosmosAPI(BaseAPI):
    async def stake(self, method_config):
        result = await self.call_method(method_config)
        service_status = 0

        if result['http_response_code'] in [200, 201] and result.get('error') is None:
            response = result.get('result', {})
            if (
                isinstance(response.get('amount'), (int, float)) and response['amount'] > 0 and
                isinstance(response.get('validatorAddress'), str) and len(response['validatorAddress']) > 0 and
                isinstance(response.get('stashAccountAddress'), str) and len(response['stashAccountAddress']) > 0
            ):
                service_status = 1

        result['service_status'] = service_status
        return result

    async def unstake(self, method_config):
        result = await self.call_method(method_config)
        return result

    async def broadcast(self, method_config):
        result = await self.call_method(method_config)
        return result