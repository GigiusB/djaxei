class ImportException(Exception):
    def __init__(self, cause, worksheet=None, *args):
        super(ImportException, self).__init__(*args)
        self.worksheet = worksheet
        self.cause = cause

    def __str__(self):
        if hasattr(self.cause, 'reference'):
            msg = "[%s:%s] %s: %s" % (self.worksheet, self.cause.reference, self.cause.__class__.__name__, str(self.cause))
        else:
            msg = "[%s] %s: %s" % (self.worksheet, self.cause.__class__.__name__, str(self.cause))
        return msg

