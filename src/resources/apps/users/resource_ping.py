from rubix_http.resource import RubixResource


class AppPing(RubixResource):
    @classmethod
    def get(cls):
        return {'message': "We are up!"}
