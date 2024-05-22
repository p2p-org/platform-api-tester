from base_api import BaseAPI

class PolygonAPI(BaseAPI):
    async def approve(self, method_config):
        result = await self.call_method(method_config)
        return result

    async def send(self, method_config):
        result = await self.call_method(method_config)
        return result