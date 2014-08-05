from ..errors import ServerError

# -------------------------------------------------
# Error Handling for Authentication Errors
# -------------------------------------------------
class AuthenticationError(ServerError):
    status_code = 403 # Not 401 because WWW-Authenticate header won't work well
