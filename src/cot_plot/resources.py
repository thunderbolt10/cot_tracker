from pyramid.security import Allow, Everyone


class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit'),
               (Allow, 'group:admin', 'admin')]

    def __init__(self, request):
        pass