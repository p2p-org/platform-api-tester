import asyncio
import json
import yaml
import os
import logging
from dotenv import load_dotenv
from cosmos import Cosmos
from polkadot import Polkadot
from server import create_app
from metrics import Metrics
from aiohttp import web

load_dotenv()

async def run_tests(config, metrics):
    logging.info('Testing started')
    results = []

    while True:
        try:
            for network_name, network_config in config['networks'].items():
                for environment, methods in network_config.items():
                    base_url = config['environments'][environment]
                    api_key = os.getenv(f'{environment.upper()}_API_KEY')
                    logging.info(f'Testing network: {network_name}, environment: {environment}')

                    if network_name == 'cosmos':
                        network = Cosmos(api_key, base_url, network_name, environment)
                    elif network_name == 'polkadot':
                        network = Polkadot(api_key, base_url, network_name, environment)
                    else:
                        continue

                    for method, params in methods.items():
                        if method == 'stake':
                            result = await network.stake(params)
                        elif method == 'unstake':
                            result = await network.unstake(params)
                        elif method == 'broadcast':
                            result = await network.broadcast(params['signedTransaction'])
                        else:
                            continue

                        results.append(result)

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
    metrics = app['metrics']

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