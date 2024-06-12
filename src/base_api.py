import aiohttp
import logging
import time
from urllib.parse import urlencode

class BaseAPI:
    def __init__(self, base_url, api_key, request_timeout):
        self.base_url = base_url
        self.api_key = api_key
        self.request_timeout = request_timeout
        self.connector = aiohttp.TCPConnector(verify_ssl=False)
        self.session = aiohttp.ClientSession(
            headers={'Authorization': f'Bearer {self.api_key}', 'accept': 'application/json'}, connector=self.connector)

    async def call_method(self, method_config):
        url = f"{self.base_url}{method_config['path']}"
        params = method_config.get('params', {})
        method = method_config.get('method', 'POST').upper()

        start_time = time.time()
        logging.info(f'Sending request: {method} {url}')
        logging.debug(f'Headers: {self.session._default_headers}')
        logging.debug(f'Request payload: {params}' if method == 'POST' else f'Request params: {params}')

        try:
            if method == 'POST':
                async with self.session.post(url, json=params, timeout=self.request_timeout) as response:
                    return await self._handle_response(response, start_time)
            elif method == 'GET':
                full_url = f"{url}?{urlencode(params)}" if params else url
                logging.debug(f'Request URL: {full_url}')
                async with self.session.get(full_url, timeout=self.request_timeout) as response:
                    return await self._handle_response(response, start_time)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        except Exception as e:
            logging.error(f'Error calling API: {str(e)}')
            return {
                'url': url,
                'http_response_code': 555,
                'execution_duration': time.time() - start_time,
                'response': {'error': str(e)}
            }

    async def _handle_response(self, response, start_time):
        end_time = time.time()
        execution_time = end_time - start_time
        http_response_code = response.status
        response_text = await response.text()
        logging.info(f'Received response with HTTP status code: {http_response_code}')
        logging.debug(f'Response text: {response_text}')
        logging.info(f'Request took {execution_time:.3f} seconds')

        try:
            result = await response.json()
        except aiohttp.ContentTypeError as e:
            logging.error(f'Error parsing JSON response: {str(e)}, response text: {response_text}')
            result = {'error': str(e), 'response_text': response_text}

        result.update({
            'url': str(response.url),
            'http_response_code': http_response_code,
            'execution_duration': execution_time,
            'service_status': 1 if http_response_code in [200, 201] else 0,
        })

        return result

    async def close(self):
        await self.session.close()
        await self.connector.close()
