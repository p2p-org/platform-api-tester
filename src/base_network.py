import aiohttp
import logging
import time
import json

class BaseNetwork:
    def __init__(self, api_key, base_url, network_name, environment):
        self.api_key = api_key
        self.base_url = base_url
        self.network_name = network_name
        self.environment = environment
        self.headers = {'Authorization': f'Bearer {self.api_key}'}

    async def make_request(self, url, method, payload=None):
        start_time = time.time()
        logging.info(f'Sending request: {method} {url}')
        logging.debug(f'Request payload: {payload}')

        connector = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            try:
                async with session.request(method, url, headers=self.headers, json=payload) as response:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    http_response_code = response.status
                    logging.info(f'Received response with HTTP status code: {http_response_code}')

                    response_text = await response.text()
                    logging.debug(f'Response text: {response_text}')
                    logging.info(f'Request took {execution_time:.3f} seconds')

                    return {
                        'network': self.network_name,
                        'environment': self.environment,
                        'url': url,
                        'execution_timestamp': start_time,
                        'execution_duration': execution_time,
                        'http_response_code': http_response_code,
                        'response_text': response_text
                    }
            except aiohttp.ClientError as e:
                logging.error(f'Request error: {str(e)}')
                return None

    def parse_response(self, response, method_name):
        if response is None:
            return {
                'network': self.network_name,
                'environment': self.environment,
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
            'environment': response['environment'],
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

                """
                if 'result' in json_response:
                    result_data = json_response['result']
                    if method_name == 'stake' or method_name == 'bond':
                        result['comment'] = f"Staked/Bonded {result_data.get('amount', '')} {result_data.get('currency', '')}"
                    elif method_name == 'unstake':
                        result['comment'] = f"Unstaked {result_data.get('amount', '')} {result_data.get('currency', '')}"
                    elif method_name == 'broadcast':
                        result['comment'] = f"Transaction hash: {result_data.get('transactionData', {}).get('messageHash', '')}"
                """

        except json.JSONDecodeError:
            result['result'] = 'fail'
            result['comment'] = 'Failed to parse JSON response'
        except KeyError:
            result['result'] = 'fail'
            result['comment'] = 'Missing expected fields in response'

        return result