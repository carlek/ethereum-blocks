from typing import Optional
from datetime import datetime
from classes.etherscan import GetBlockResponse
__cache = {}

def get_cache(date: datetime) -> Optional[GetBlockResponse]:
    block: GetBlockResponse = __cache.get(date)
    if not block:
        return None
    return block


def set_cache(date: datetime, block: GetBlockResponse):
    __cache[date] = block
