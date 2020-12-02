import venusian

# app.router.add_route('*', '/api_info', api_info.ApiInfoController, name='api_info')


def resource(resource_uri: str, prefix: str = ''):
    def wrapper(cls):
        def callback(scanner, name, ob):
            url = prefix + resource_uri
            scanner.api.add_route("*", url, cls, name=name)

        venusian.attach(cls, callback)
        return cls
    return wrapper
