from pydantic import BaseModel

class GetBlockResponse(BaseModel):
    status: int
    message: str
    result: int

class ApiError(Exception):
    def __init__(self, error_msg: str, status_code: int):
        super().__init__(error_msg)
        self.status_code = status_code
        self.error_msg = error_msg

class EtherscanError(Exception):
    def __init__(self, error_msg: str, status_code: int):
        super().__init__(error_msg)
        self.status_code = status_code
        self.error_msg = error_msg

