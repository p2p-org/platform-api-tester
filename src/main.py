import asyncio
import json
import yaml
import os
import logging
from dotenv import load_dotenv
from cosmos import CosmosAPI
from polkadot import PolkadotAPI
from solana import SolanaAPI
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
                        else:
                            logging.warning(f'Unknown service: {service_name}. Skipping.')
                            continue

                        for method_name, method_config in zone_config.get('methods', {}).items():
                            result = await api.call_method(method_name, method_config)
                            result['environment'] = environment_name
                            result['service'] = service_name
                            result['zone'] = zone_name
                            result['method'] = method_name
                            results.append(result)

                        await api.close()

            for result in results:
                logging.debug(json.dumps(result, indent=2))
                metrics.update_metrics(result)

            results.clear()

            await asyncio.sleep(config['test_interval'])

        except Exception as e:
            logging.error(f'Error occurred during testing: {str(e)}')
            await asyncio.sleep(config['test_interval'])

def setup_logging(debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

async def main():
    with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

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