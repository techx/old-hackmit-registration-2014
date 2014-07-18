# -------------------------------------------------
# Error Handling for Database Errors
# -------------------------------------------------
class DatabaseError(Exception):

    message = "Something went wrong! :( Please try again."
    status_code = 500 # Generic internal server error

    def __init__(self, message=None, status_code=None):
        # Don't allow payload, they shouldn't know about db internals
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        return rv
