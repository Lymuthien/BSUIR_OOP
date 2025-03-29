from ..models.registrable import Registrable

class GenericFactory(object):
    @staticmethod
    def create(data: dict):
        object_type = data['type'].lower()
        object_class = Registrable.registry().get(object_type)
        if object_class:
            return object_class()
        else:
            raise ValueError(f'Unknown component: {object_type}')


