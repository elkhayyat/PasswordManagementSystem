from abc import ABC


class BaseModelFilter(ABC):

    def __init__(self):
        self.model = self.get_model()
        self.main_queryset = self.get_main_queryset()
        self.query_params = {}
        self.data = self.execute()

    def get_model(self):
        return self.model

    def get_main_queryset(self):
        return self.model.objects.all()

    def execute(self):
        return self._filter(self.main_queryset)

    def add_filter(self, key, value):
        self.query_params[key] = value

    def _filter(self, data):
        for key, value in self.query_params.items():
            if value is not None:
                data = data.filter(**{key: value})
        return data
