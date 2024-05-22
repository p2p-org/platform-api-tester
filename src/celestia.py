from base_api import BaseAPI

class CelestiaAPI(BaseAPI):
    async def stake(self, method_config):
        result = await self.call_method(method_config)
        return result

    async def unstake(self, method_config):
        result = await self.call_method(method_config)
        return result

    async def send(self, method_config):
        result = await self.call_method(method_config)
        return result