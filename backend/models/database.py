from flask_sqlalchemy import SQLAlchemy, Model


class BaseModel(Model):
    '''Customized base class of the flask_sqlalchemy model class'''

    def as_dict(self):
        ''' Transform this model instance into a dict '''
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
        }


db = SQLAlchemy(model_class=BaseModel)
