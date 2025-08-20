from app.modules.database_module.dao.generic_dao import GenericDao


class DatabaseManager:
    def __init__(self):
        self._register_dao_methods(GenericDao)

    def _register_dao_methods(self, dao_class: object) -> None:
        for dao in dao_class.__dict__:
            if callable(getattr(dao_class, dao)) and not dao.startswith("__"):
                setattr(self, dao, getattr(dao_class, dao))
