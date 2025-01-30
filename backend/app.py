from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.auth import *
from backend.models.user import User
from backend.routes.transaction import router as TransactionRouter
from backend.routes.user import router as UserRouter

app = FastAPI()
# app = FastAPI(dependencies=[Depends(get_current_user)],)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

templates = Jinja2Templates(directory="frontend/templates")

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# async def start_database():
#     await initiate_database()

# token_listener = JWTBearer()

@app.get("/", tags=["Root"], response_class=HTMLResponse)
# @check_roles(["admin"])
# def read_root():
def read_root(request: Request):
# def read_root(request: Request, current_user: User=Depends(get_current_user)):
# def read_root(get_current_user:User = Depends(get_current_user)):
    # print("current_user", current_user)
    # print("current_user", current_user['_id'])
    # print(type(current_user))
    # print("get_current_user", get_current_user)
    # return {"message": "Welcome to this fantastic app!"}
    return templates.TemplateResponse(request=request, name="index.html", context={})
    # return templates.TemplateResponse(request=request, name="index.html", context={"current_user": current_user})


app.include_router(UserRouter, tags=["User"], prefix="/user")
# app.include_router(UserRouter, tags=["User"], prefix="/user", dependencies=[Depends(get_current_user)])
app.include_router(TransactionRouter, tags=["Transaction"], prefix="/transaction")
# app.include_router(TransactionRouter, tags=["Transaction"], prefix="/transaction", dependencies=[Depends(token_listener)])
