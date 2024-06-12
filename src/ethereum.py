from base_api import BaseAPI

class EthereumAPI(BaseAPI):
    async def validator_status(self, method_config):
        result = await self.call_method(method_config)
        return result
