import bcrypt
from pyramid.httpexceptions import HTTPFound



USERS = {}
GROUPS = {}

def check_password(pw, hashed_pw):

    expected_hash = hashed_pw.decode('utf8').encode('utf8')
    return bcrypt.checkpw(pw.encode('utf8'), expected_hash)


def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])


def forbidden(request):
    if request.authenticated_userid is None:
        url = request.route_url('login')
    else:
        url = request.route_url('forbidden')
    return HTTPFound(location=url)

def load_user_accounts(settings):
    pass
#    with model.SecurityModel(settings) as db:
#        accounts = db.get_accounts()

#    for a in accounts:
#        USERS[a['username']] = a['password'].tobytes()
#        GROUPS[a['username']] = a['groups'][1:-1].split(',')



