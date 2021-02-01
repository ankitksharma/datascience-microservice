import falcon
import json
from src.logger import logging
logger = logging.getLogger(__name__)


def make_response(res, data, status):
    res.body = json.dumps(data, indent=2, ensure_ascii=False)
    res.status = status
    res.append_header('Access-Control-Allow-Origin', '*')


class StaticResource(object):
    @classmethod
    def on_get(cls, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.body = "<h1 style='color:red'>Data Science MicroService</h1>"


class UpdateResource(object):
    @classmethod
    def on_get(cls, req, resp):
        """Handles GET requests"""
        # Return note for particular ID
        if req.get_param("id"):
            resp.body = json.dumps({"result": "we got:" + req.get_param("id")})
            make_response(resp, resp.body, falcon.HTTP_200)
        else:
            resp.body = "Service to host data science project"

    @classmethod
    def on_post(cls, req, resp):
        """Handles POST requests"""
        try:
            raw_json = req.stream.read()
            logger.info(f'RECEIVED: {raw_json}')
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)

        try:
            result = json.loads(raw_json)
            logger.info(result['text'])
            resp.body = json.dumps({"result": 'Successfully inserted: ' + result['text']})
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Invalid JSON', "Could not decode the request body. The ''JSON was incorrect.")


def handle_404(req, resp):
    data = {
        'status': '404 - Not Found'
    }
    status = falcon.HTTP_404
    make_response(resp, data, status)


def get_app():
    api = falcon.API()
    api.add_route('/', StaticResource())
    api.add_route('/update', UpdateResource())
    api.add_sink(handle_404, '')
    return api
