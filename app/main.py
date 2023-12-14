from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

from views import *
app.include_router(health_view.router)
app.include_router(user_view.router)

handler = Mangum(app)