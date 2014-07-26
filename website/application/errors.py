# -------------------------------------------------
# Error Handling for Database Errors
# -------------------------------------------------

class ServerError(Exception):
    message = "Something went wrong! :( Please try again."
    status_code = 500

    def __init__(self, message=None, status_code=None, payload=None):
        super(ServerError, self).__init__()
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload=payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

class BadDataError(ServerError):
    message = "Your data is bad and you should feel bad."
    status_code = 403
