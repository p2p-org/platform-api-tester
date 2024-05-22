from base_api import BaseAPI

class PolkadotAPI(BaseAPI):
    async def bond(self, method_config):
        result = await self.call_method(method_config)
        return result

    async def unbond(self, method_config):
        result = await self.call_method(method_config)
        return result

    async def broadcast(self, method_config):
        result = await self.call_method(method_config)
        return result