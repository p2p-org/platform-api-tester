import aiohttp
import logging
import time

class BaseAPI:
    def __init__(self, base_url, api_key, request_timeout):
        self.base_url = base_url
        self.api_key = api_key
        self.request_timeout = request_timeout
        self.connector = aiohttp.TCPConnector(verify_ssl=False)
        self.session = aiohttp.ClientSession(headers={'Authorization': f'Bearer {self.api_key}'}, connector=self.connector)

    async def call_method(self, method_name, method_config):
        url = f"{self.base_url}{method_config['path']}"
        params = method_config.get('params', {})

        start_time = time.time()
        logging.info(f'Sending request: POST {url}')
        logging.debug(f'Request payload: {params}')

        try:
            async with self.session.post(url, json=params, timeout=self.request_timeout) as response:
                end_time = time.time()
                execution_time = end_time - start_time
                http_response_code = response.status
                logging.info(f'Received response with HTTP status code: {http_response_code}')

                response_text = await response.text()
                logging.debug(f'Response text: {response_text}')
                logging.info(f'Request took {execution_time:.3f} seconds')

                try:
                    result = await response.json()
                except aiohttp.ContentTypeError as e:
                    logging.error(f'Error parsing JSON response: {str(e)}, response text: {response_text}')
                    result = {'error': str(e), 'response_text': response_text}

                return {
                    'url': str(response.url),
                    'status_code': http_response_code,
                    'execution_duration': execution_time,
                    'response': result
                }
        except Exception as e:
            logging.error(f'Error calling method {method_name}: {str(e)}')
            return {
                'url': url,
                'status_code': 555,
                'execution_duration': time.time() - start_time,
                'response': {'error': str(e)}
            }

    async def close(self):
        await self.session.close()
        await self.connector.close()