from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from os import getenv
import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
app = Flask(__name__)
CORS(app)
JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')
metrics = GunicornInternalPrometheusMetrics(app)
metrics.info('app_info', 'Trial Service', version='1.0')
def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            'local_agent': {
                'reporting_host': JAEGER_HOST
            }
        },
        service_name=service,
    )
    return config.initialize_tracer()
tracer = init_tracer('trial')
@app.route('/')
def homepage():
    with tracer.start_span('get-python-jobs') as span:
        homepages = []
        res = requests.get(
            'https://jobs.github.com/positions.json?description=python')
        if res.status_code != 200:
            span.set_tag('error', 400)
            homepages.append('ERROR')
        else:
            span.set_tag('jobs-count', len(res.json()))
            for result in res.json():
                if result['company'] is not None:
                    span_text = result['company']
                else:
                    span_text = 'ERROR'
                with tracer.start_span(span_text, child_of=span) as site_span:
                    print('Getting website for %s' % span_text)
                    try:
                        homepages.append(requests.get(result['company_url']))
                    except:
                        print('Unable to get site for %s' % span_text)
    return jsonify(homepages)
if __name__ == "__main__":
    app.run(debug=True,)
