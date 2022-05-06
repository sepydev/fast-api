from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from accounts import api as accounts_api
from database import create_db_and_tables  # noqa
from settings import *  # noqa

app = FastAPI(
    title='Modular app with SQLModel and Alembic ',
    description='Created by Mohammad Rezazadeh',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts_api.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app="main:app", host='0.0.0.0', port=8080, reload=True)
