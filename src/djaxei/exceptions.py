class ImportException(Exception):
    def __init__(self, cause, worksheet=None, *args):
        super(ImportException, self).__init__(*args)
        self.worksheet = worksheet
        self.cause = cause

    def __str__(self):
        return "[%s]%s: %s" % (self.worksheet, self.cause.__class__.__name__, str(self.cause))

