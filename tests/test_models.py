def test_as_dict(app):
    from backend.models import db

    class TestModel(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        foo = db.Column(db.Integer())
        bar = db.Column(db.Text())

    t = TestModel(foo=5, bar='baz')
    # t is not commited, so id is not yet determined
    assert t.as_dict() == {'foo': 5, 'bar': 'baz', 'id': None}
