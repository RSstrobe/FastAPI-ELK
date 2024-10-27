from fastapi import HTTPException, status


class NumberIsAlreadyExist(HTTPException):
    def __init__(self, phone_number: str, status_code=status.HTTP_409_CONFLICT):
        self.detail = f'Number {phone_number!r} is already exist'
        self.status_code = status_code


class NumberDoesNotExist(HTTPException):
    def __init__(self, phone_number: str, status_code=status.HTTP_404_NOT_FOUND):
        self.detail = f'Number {phone_number!r} does not exist'
        self.status_code = status_code
