from typing import Optional, Tuple
import httpx
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

from infrastructure import etherscan_cache
from classes.etherscan import ApiError, GetBlockResponse

api_key: Optional[str] = None

async def get_block_async(start: str, end: str) -> list[str]:
    etherscan_url = f"https://api.etherscan.io/api?module=block&action=getblocknobytime" \
                    f"&closest=before&apikey={api_key}"
    (utc_start_date, utc_end_date) = validate_input(start, end)
    result_list: list[str] = []
    utc_date = utc_start_date
    while utc_date <= utc_end_date:
        if block := etherscan_cache.get_cache(utc_date):
            pass
        else:
            async with httpx.AsyncClient() as client:
                resp = await client.get(etherscan_url + f"&timestamp={int(utc_date.timestamp())}")
                resp.raise_for_status()
                if resp.status_code != 200:
                    raise ApiError(status_code=resp.status_code, error_msg=resp.text)
                if not resp.json() or resp.json()['message'] != "OK":
                    error = f"GET error: {etherscan_url} {resp.text}"
                    raise ApiError(status_code=400, error_msg=error)
            data = resp.json()
            block = GetBlockResponse(status=data['status'], message=data['message'], result=data['result'])
            etherscan_cache.set_cache(utc_date, block)

        result_list.append(f"{utc_date.strftime('%Y-%m-%d')} {block.result}")
        utc_date = utc_date + relativedelta(days=1)
    return result_list

def validate_input(start: str, end: str) -> Tuple[datetime, datetime]:
    try:
        (hour, minute, second, millisecond) = (23, 59, 59, 0)
        (year, month, day) = tuple(map(int, start.split('-')))
        utc_start_date = datetime(year, month, day, hour, minute, second, millisecond, pytz.UTC)
        (year, month, day) = tuple(map(int, end.split('-')))
        utc_end_date = datetime(year, month, day, hour, minute, second, millisecond, pytz.UTC)
        return utc_start_date, utc_end_date
    except Exception as e:
        raise ApiError(status_code=400, error_msg=str(e) + f":start:{start} end={end}")
