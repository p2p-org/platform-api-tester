import aiohttp
import logging
import time
import json
import asyncio


class BaseNetwork:
    def __init__(self, api_key, base_url, network_name, blockchain_env, api_env, request_timeout=60):
        self.api_key = api_key
        self.base_url = base_url
        self.network_name = network_name
        self.blockchain_env = blockchain_env
        self.api_env = api_env
        self.headers = {'Authorization': f'Bearer {self.api_key}'}
        self.request_timeout = request_timeout

    async def make_request(self, url, method, payload=None):
        start_time = time.time()
        logging.info(f'Sending {method} {url}')
        logging.debug(f'Request payload: {payload}')

        connector = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            try:
                async with session.request(method, url, headers=self.headers, json=payload, timeout=self.request_timeout) as response:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    http_response_code = response.status
                    logging.info(f'Received response with HTTP {http_response_code} in {execution_time:.3f} seconds')

                    response_text = await response.text()
                    logging.debug(f'Response text: {response_text}')

                    return {
                        'network': self.network_name,
                        'blockchain_env': self.blockchain_env,
                        'api_env': self.api_env,
                        'url': url,
                        'execution_timestamp': start_time,
                        'execution_duration': execution_time,
                        'http_response_code': http_response_code,
                        'response_text': response_text
                    }
            except asyncio.TimeoutError:
                end_time = time.time()
                execution_time = end_time - start_time
                logging.error(f'Request timed out after {execution_time:.3f} seconds')
                return {
                    'network': self.network_name,
                    'blockchain_env': self.blockchain_env,
                    'api_env': self.api_env,
                    'url': url,
                    'execution_timestamp': start_time,
                    'execution_duration': self.request_timeout,
                    'http_response_code': 408,
                    'response_text': ''
                }
            except aiohttp.ClientError as e:
                logging.error(f'Request error: {str(e)}')
                return None

    def parse_response(self, response, method_name):
        if response is None:
            return {
                'network': self.network_name,
                'blockchain_env': self.blockchain_env,
                'api_env': self.api_env,
                'url': None,
                'method': method_name,
                'execution_timestamp': None,
                'execution_duration': None,
                'http_response_code': None,
                'result': 'fail',
                'comment': 'Request error'
            }

        result = {
            'network': response['network'],
            'blockchain_env': response['blockchain_env'],
            'api_env': response['api_env'],
            'url': response['url'],
            'method': method_name,
            'execution_timestamp': response['execution_timestamp'],
            'execution_duration': response['execution_duration'],
            'http_response_code': response['http_response_code'],
            'result': 'ok' if response['http_response_code'] // 100 == 2 else 'fail',
            'comment': ''
        }

        try:
            json_response = json.loads(response['response_text'])
            if json_response.get('error') is not None:
                result['result'] = 'fail'
                result['comment'] = json_response['error'].get('message', str(json_response['error']))
            else:
                result['result'] = 'ok'
                result['comment'] = 'Success'

        except json.JSONDecodeError:
            result['result'] = 'fail'
            result['comment'] = 'Failed to parse JSON response'
        except KeyError:
            result['result'] = 'fail'
            result['comment'] = 'Missing expected fields in response'

        return result