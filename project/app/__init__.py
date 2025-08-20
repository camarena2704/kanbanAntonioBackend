class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def get_instance(cls, target_cls, *args, **kwargs):

        if target_cls not in cls._instances:
            cls._instances[target_cls] = target_cls(*args, **kwargs)
        return cls._instances[target_cls]
