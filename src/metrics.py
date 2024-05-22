import os
from prometheus_client import Gauge, Histogram, CollectorRegistry, generate_latest

class Metrics:
    def __init__(self):
        self.registry = CollectorRegistry()

        metrics_prefix = os.getenv('METRICS_PREFIX', 'platform_api_tester_')

        self.request_status = Gauge(
            f'{metrics_prefix}request_status',
            'Request status',
            ['environment', 'service', 'zone', 'method'],
            registry=self.registry
        )

        self.request_latency = Gauge(
            f'{metrics_prefix}request_duration',
            'Latency in seconds',
            ['environment', 'service', 'zone', 'method'],
            registry=self.registry
        )

        self.http_response_codes = Gauge(
            f'{metrics_prefix}http_response_codes',
            'HTTP response codes',
            ['environment', 'service', 'zone', 'method', 'http_code'],
            registry=self.registry
        )

    def update_metrics(self, result):
        environment = result['environment']
        service = result['service']
        zone = result['zone']
        method = result['method']
        service_status = result['service_status']
        latency = result['execution_duration']
        http_code = result['http_response_code']

        self.request_status.labels(environment=environment, service=service, zone=zone, method=method).set(service_status)
        self.request_latency.labels(environment=environment, service=service, zone=zone, method=method).set(latency)
        self.http_response_codes.labels(environment=environment, service=service, zone=zone, method=method, http_code=http_code).inc()

    def get_metrics(self):
        return generate_latest(self.registry)

    def generate_metrics(self):
        return generate_latest(self.registry)