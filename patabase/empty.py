class Database(object):
    def __init__(self, user: str, password: str, database: str, host: str = 'localhost', port=0):
        assert user
        assert password
        assert database
        assert host
        assert port

        raise ImportError('Database package is not installed')
