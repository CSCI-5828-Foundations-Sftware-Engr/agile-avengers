class PayException(Exception):
    def __init__(self, message="Connection to internal systems Failed"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

    pass
