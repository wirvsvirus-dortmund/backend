import flask.json
from datetime import date, datetime


class JSONEncoder(flask.json.JSONEncoder):
    '''
    Custom json encoder that
    * Converts datetimes to ISO 8601 format
    '''
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()

        return super().default(o)
