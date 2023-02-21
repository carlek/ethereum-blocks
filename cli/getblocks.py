from datetime import datetime
from dateutil.relativedelta import relativedelta
from classes.etherscan import EtherscanError, GetBlockResponse
import pytz
import httpx
import click

etherscan_api_key = "valid api key from etherscan.io"
etherscan_url = f"https://api.etherscan.io/api?module=block&action=getblocknobytime" \
                f"&closest=before&apikey={etherscan_api_key}"


def call_etherscan_getblock(url: str) -> GetBlockResponse:
    with httpx.Client() as client:
        resp = client.get(url)
        resp.raise_for_status()
        if not resp.json():
            error = f"Something went wrong: {url}"
            raise EtherscanError(status_code=404, error_msg=error)
    data = resp.json()
    return GetBlockResponse(status=data['status'], message=data['message'], result=data['result'])

def get_blocks(utc_start_date: datetime, utc_end_date: datetime) -> list[str]:
    utc_date = utc_start_date
    print(f"utc_start_date={utc_start_date}, utc_end_date={utc_end_date}")
    res: list[str] = []
    while utc_date <= utc_end_date:
        timestamp = int(utc_date.timestamp())
        block: GetBlockResponse = call_etherscan_getblock(etherscan_url + f"&timestamp={timestamp}")
        res.append(f"{utc_date.strftime('%Y-%m-%d')} {block.result}")
        utc_date = utc_date + relativedelta(days=1)
    return res

@click.command()
@click.option('--start-date', type=str, default='2021-12-30', help='Start date =YYYY-MM-DD')
@click.option('--end-date', type=str, default='2021-12-31', help='End date =YYYY-MM-DD')
def get_blocks_cmd(start_date: str, end_date: str, time: tuple = (23, 59, 59, 0)):
    """ Simple program that prints last block id for date range (inclusive) """
    (hour, minute, second, millisecond) = time
    (year, month, day) = tuple(map(int, start_date.split('-')))
    utc_start_date = datetime(year, month, day, hour, minute, second, millisecond, pytz.UTC)
    (year, month, day) = tuple(map(int, end_date.split('-')))
    utc_end_date = datetime(year, month, day, hour, minute, second, millisecond, pytz.UTC)
    res = get_blocks(utc_start_date, utc_end_date)
    for r in res:
        click.echo(r)


if __name__ == '__main__':
    get_blocks_cmd()
