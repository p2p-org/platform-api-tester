import os
from prometheus_client import Gauge, Histogram, CollectorRegistry, generate_latest

class Metrics:
    def __init__(self):
        self.registry = CollectorRegistry()

        metrics_prefix = os.getenv('METRICS_PREFIX', 'platform_api_tester_')

        self.request_status = Gauge(
            f'{metrics_prefix}request_status',
            'Request status',
            ['network', 'blockchain_env', 'api_env', 'method', 'status'],
            registry=self.registry
        )

        self.request_duration = Histogram(
            f'{metrics_prefix}request_duration',
            'Request duration in seconds',
            ['network', 'blockchain_env', 'api_env', 'method'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, float('inf')],
            registry=self.registry
        )

        self.http_response_codes = Gauge(
            f'{metrics_prefix}http_response_codes',
            'HTTP response codes',
            ['network', 'blockchain_env', 'api_env', 'method', 'code'],
            registry=self.registry
        )

    def update_metrics(self, result):
        network = result['network']
        blockchain_env = result['blockchain_env']
        api_env = result['api_env']
        method = result['method']
        status = result['result']
        duration = result['execution_duration']
        http_code = str(result['http_response_code'])

        self.request_status.labels(network=network, blockchain_env=blockchain_env, api_env=api_env, method=method, status=status).set(
            1 if status == 'ok' else 0)
        self.request_duration.labels(network=network, blockchain_env=blockchain_env, api_env=api_env, method=method).observe(duration)
        self.http_response_codes.labels(network=network, blockchain_env=blockchain_env, api_env=api_env, method=method, code=http_code).inc()

    def generate_metrics(self):
        return generate_latest(self.registry)