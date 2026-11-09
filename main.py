from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      #允许访问的源
    allow_credentials=True,  #允许携带Cookie
    allow_methods=["*"],     #允许所有请求方法
    allow_headers=["*"]      #允许所有请求头
)
# 引入新闻路由
app.include_router(news.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
