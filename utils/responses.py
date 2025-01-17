from rest_framework.response import Response


class SuccessAPIResponse(Response):
    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        super().__init__(data, status, template_name, headers, exception, content_type)
        self.data = {
            "status": "success",
            "data": data
        }


class ErrorAPIResponse(Response):
    def __init__(self, data=None, status=None, template_name=None, headers=None, exception=False, content_type=None):
        super().__init__(data, status, template_name, headers, exception, content_type)
        self.data = {
            "status": "error",
            "data": data
        }
