from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.domains.policies.router import router as policies_router
from src.exceptions import BaseAppException

app = FastAPI(
    title='[Decision Engine] ConfigBackend',
    description='Backend service for managing and storing decision policies in a no-code environment.',
    version='1.0.0',
    contact={'name': 'Matheus', 'email': 'mbatista.sarti@gmail.com'},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

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
