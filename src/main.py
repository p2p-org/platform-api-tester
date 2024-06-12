import asyncio
import json
import yaml
import os
import logging
from dotenv import load_dotenv
from cosmos import CosmosAPI
from ethereum import EthereumAPI
from polkadot import PolkadotAPI
from polygon import PolygonAPI
from solana import SolanaAPI
from celestia import CelestiaAPI
from data import DataAPI
from server import create_app
from metrics import Metrics
from aiohttp import web

load_dotenv()


async def run_tests(config, metrics):
    logging.info('Testing started')
    results = []

    while True:
        try:
            for environment_name, environment_url in config['environments'].items():
                api_key = os.getenv(f'{environment_name.upper()}_API_KEY')
                for service_name, service_config in config['services'].items():
                    for zone_name, zone_config in service_config.get('zones', {}).items():
                        logging.info(f'Testing {environment_name}/{service_name}/{zone_name}')

                        url = f"{environment_url}{service_config['path']}{zone_config.get('path', '')}"
                        if service_name == 'cosmos_api':
                            api = CosmosAPI(url, api_key, config['request_timeout'])
                        elif service_name == 'polkadot_api':
                            api = PolkadotAPI(url, api_key, config['request_timeout'])
                        elif service_name == 'solana_api':
                            api = SolanaAPI(url, api_key, config['request_timeout'])
                        elif service_name == 'celestia_api':
                            api = CelestiaAPI(url, api_key, config['request_timeout'])
                        elif service_name == 'polygon_api':
                            api = PolygonAPI(url, api_key, config['request_timeout'])
                        elif service_name == 'ethereum_api':
                            api = EthereumAPI(url, api_key, config['request_timeout'])
                        elif service_name == 'data_api':
                            api = DataAPI(url, api_key, config['request_timeout'])
                        else:
                            logging.warning(f'Unknown service: {service_name}. Skipping.')
                            continue

                        for method_name, method_config in zone_config.get('methods', {}).items():

                            if not hasattr(api, method_name):
                                logging.warning(f'Method {method_name} not found in {service_name}. Skipping.')
                            else:
                                method = getattr(api, method_name)
                                logging.info(f'Calling method {method_name}, {method_config}')
                                result = await method(method_config)

                                result.update({
                                    'environment': environment_name,
                                    'service': service_name,
                                    'zone': zone_name,
                                    'method': method_name
                                })

                                service_status = result['service_status']
                                logging.info(f'Service status: {"up" if service_status == 1 else "down"}')
                                results.append(result)

                        await api.close()

            for result in results:
                #logging.debug(json.dumps(result, indent=2))
                metrics.update_metrics(result)

            results.clear()

            await asyncio.sleep(config['test_interval'])

        except Exception as e:
            logging.error(f'Error occurred during testing: {str(e.__repr__())}')
            await asyncio.sleep(config['test_interval'])


def setup_logging(debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


async def main():
    with open('config/config.yaml', 'r') as file:
        config_text = file.read()
        print(config_text)

    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        print(config)

    setup_logging(config.get('debug', False))

    app = await create_app()
    metrics = Metrics()
    app['metrics'] = metrics

    asyncio.create_task(run_tests(config, metrics))
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass

    await runner.cleanup()


if __name__ == '__main__':
    asyncio.run(main())
