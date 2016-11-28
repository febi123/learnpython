class Predictgender(object):
    def __init__(self, **kwargs):
        for field in ('nama', 'suku'):
            setattr(self, field, kwargs.get(field, None))
class Predictgenderresult(object):
    def __init__(self, **kwargs):
        for field in ('nama', 'suku', 'jk', 'prob'):
            setattr(self, field, kwargs.get(field, None))