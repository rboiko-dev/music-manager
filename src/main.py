import uvicorn
from fastapi import FastAPI
from src.endpoints.search_endpoints import router as search_router
from src.dependencies import init_dependencies

app = FastAPI()
app.include_router(search_router)
init_dependencies()

if __name__ == '__main__':
    init_dependencies()
    uvicorn.run(app)
