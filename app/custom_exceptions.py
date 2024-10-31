class FacebookAPIError(Exception):
    """Exception raised for errors in the Facebook API."""
    pass

class APIError(Exception):
    """General API error."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
