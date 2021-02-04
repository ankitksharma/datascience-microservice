import json

import falcon

from src.heart_rate import segmented_average


class CalculateHeartRate(object):
    @classmethod
    def on_post(cls, req, resp):
        try:
            raw_json = req.stream.read()
            body = json.loads(raw_json)
            data_stream = body["data_stream"]
            fps = body["fps"]

            if len(data_stream) > 0 and fps > 0:
                print(f'{len(data_stream)}, fps: {fps}')
                bpm = segmented_average.calc_bpm(data_stream, fps)
                resp.body = json.dumps({"bpm": bpm})
                return
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)
