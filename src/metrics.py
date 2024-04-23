from prometheus_client import Gauge, Histogram, CollectorRegistry, generate_latest

class Metrics:
    def __init__(self):
        self.registry = CollectorRegistry()

        self.request_status = Gauge(
            'request_status',
            'Request status',
            ['network', 'environment', 'method', 'status'],
            registry=self.registry
        )

        self.request_duration = Histogram(
            'request_duration_seconds',
            'Request duration in seconds',
            ['network', 'environment', 'method'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, float('inf')],
            registry=self.registry
        )

    def update_metrics(self, result):
        network = result['network']
        environment = result['environment']
        method = result['method']
        status = result['result']
        duration = result['execution_duration']

        self.request_status.labels(network=network, environment=environment, method=method, status=status).set(
            1 if status == 'ok' else 0)
        self.request_duration.labels(network=network, environment=environment, method=method).observe(duration)


    def generate_metrics(self):
        return generate_latest(self.registry)