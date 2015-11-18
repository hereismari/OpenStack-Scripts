
class UtilKeystone():

    def __init__(self, connection):
        self.connection = connection

    def getTokenRef(self, user, key, project_name):

        print 'Getting token ref...'
        token_ref = self.connection.tokens.authenticate(username=user,
                                         tenant_name=project_name,
                                         password=key)
        print 'Success!'
        return token_ref
