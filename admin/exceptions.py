class InputValidationError(ValueError):
    """Невалидные данные в инпутере"""
    def __init__(self, msg: str, code: str = None):
        self.msg = msg
