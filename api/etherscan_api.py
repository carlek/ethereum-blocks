
import fastapi

from classes.etherscan import ApiError
from services import etherscan_service

router = fastapi.APIRouter()

@router.get('/blocks/')
async def get_blocks(start: str, end: str):
    try:
        return await etherscan_service.get_block_async(start, end)
    except ApiError as e:
        return fastapi.Response(content=e.error_msg, status_code=e.status_code)
    except Exception as x:
        return fastapi.Response(content=str(x), status_code=500)
