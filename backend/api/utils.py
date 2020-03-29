from flask_restful import abort


def all_as_dict(query):
    '''Return a list of dicts for all rows in query'''
    return [row.as_dict() for row in query]


def get_or_404(model, id_):
    '''return with 404 if there is no instance of a given model with id `id_`'''
    result = model.query.get(id_)
    if result is None:
        abort(404, message=f'{model.__name__} with id {id_} does not exist')
    else:
        return result
