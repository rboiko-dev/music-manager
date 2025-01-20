from fastapi import APIRouter

from src.dependencies import search_core
from src.dto.endpoints_dto.search_endpoints_dto import SearchDTO

router = APIRouter(prefix='/search')


@router.get('/{query}', status_code=200)
async def search_by_query(query: str) -> SearchDTO:
    result = await search_core.search(query)
    return SearchDTO(tracks=result)
