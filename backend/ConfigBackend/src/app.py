from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domains.policies.router import router as policies_router
from src.exceptions import BaseAppException

app = FastAPI()

app.include_router(policies_router)


@app.exception_handler(Exception)
async def app_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'error': str(exc)},
    )


@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': exc.error},
    )


@app.get('/health')
def health():
    return {'message': 'healthy'}
