class Adapter:
    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def get_all(cls):
        raise NotImplementedError()

    @classmethod
    def get(cls, identifier):
        raise NotImplementedError()

    @classmethod
    def get_by_attr(cls, attr, value):
        raise NotImplementedError()

    @classmethod
    def delete(cls, identifier):
        raise NotImplementedError()

    @classmethod
    def save(cls, obj):
        raise NotImplementedError()

    @classmethod
    def filter(cls, **kwargs):
        raise NotImplementedError()
