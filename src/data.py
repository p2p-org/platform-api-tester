from base_api import BaseAPI

class DataAPI(BaseAPI):
    async def validator_state(self, method_config):
        result = await self.call_method(method_config)
        return result

    async def exit_queue(self, method_config):
        result = await self.call_method(method_config)
        return result
