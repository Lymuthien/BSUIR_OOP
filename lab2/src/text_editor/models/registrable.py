class Registrable(object):
    _registry: dict[str: type['Registrable']] = {}

    @classmethod
    def registry(cls) -> dict[str: type['Registrable']]:
        return cls._registry

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__.lower()] = cls
