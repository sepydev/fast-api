from fastapi import FastAPI, APIRouter, status


app = FastAPI(
    title='Accounts API',
    openapi_url="/openapi.json",
)

api_router = APIRouter()


@api_router.get("/", status_code=status.HTTP_200_OK)
def root() -> dict:
    return {
        "msg": "Hellow world"
    }


app.include_router(api_router)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="debug")
