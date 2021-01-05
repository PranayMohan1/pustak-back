from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter


class PustakRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        self._extended_routers = []
        return super(PustakRouter, self).__init__(*args, **kwargs)

    def extend(self, url_prefix, router):
        self._extended_routers.append((url_prefix, router))

    def get_urls(self):
        urls = super(PustakRouter, self).get_urls()

        urls.extend([self.get_router_url(prefix, router) for prefix, router in self._extended_routers])
        return urls

    def get_router_url(self, prefix, router):
        if isinstance(router, tuple):
            return url(r'%s/' % prefix, router)

        return url(r'%s/' % prefix, include(router.urls))
