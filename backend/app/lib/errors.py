# custom error class
class HTTPError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "HTTPError - {}".format(*self.args)

class UnAuthError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "UnAuthError - {}".format(*self.args)
    
class MathFlexOperationError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "MathFlex Operational Error - {}".format(*self.args)