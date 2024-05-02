import os
from prometheus_client import Gauge, Histogram, CollectorRegistry, generate_latest

class Metrics:
    def __init__(self):
        self.registry = CollectorRegistry()

        metrics_prefix = os.getenv('METRICS_PREFIX', 'platform_api_tester_')

        self.request_status = Gauge(
            f'{metrics_prefix}request_status',
            'Request status',
            ['environment', 'service', 'zone', 'method', 'status'],
            registry=self.registry
        )

        self.request_duration = Histogram(
            f'{metrics_prefix}request_duration',
            'Latency in seconds',
            ['environment', 'service', 'zone', 'method'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, float('inf')],
            registry=self.registry
        )

        self.http_response_codes = Gauge(
            f'{metrics_prefix}http_response_codes',
            'HTTP response codes',
            ['environment', 'service', 'zone', 'method', 'code'],
            registry=self.registry
        )

    def update_metrics(self, result):
        environment = result['environment']
        service = result['service']
        zone = result['zone']
        method = result['method']
        status = 'ok' if str(result['status_code']).startswith('2') else 'fail'
        latency = result['execution_duration']
        http_code = str(result['status_code'])

        self.request_status.labels(environment=environment, service=service, zone=zone, method=method, status=status).set(1)
        self.request_duration.labels(environment=environment, service=service, zone=zone, method=method).observe(latency)
        self.http_response_codes.labels(environment=environment, service=service, zone=zone, method=method, code=http_code).inc()

    def get_metrics(self):
        return generate_latest(self.registry)

    def generate_metrics(self):
        return generate_latest(self.registry)