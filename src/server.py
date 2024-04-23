from aiohttp import web
from metrics import Metrics

async def metrics_handler(request):
    metrics = request.app['metrics']
    return web.Response(body=metrics.generate_metrics(), content_type='text/plain')

async def create_app():
    app = web.Application()
    app['metrics'] = Metrics()
    app.add_routes([web.get('/metrics', metrics_handler)])
    return app
