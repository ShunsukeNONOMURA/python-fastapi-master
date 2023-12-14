from fastapi import FastAPI
from mangum import Mangum

from views import *

app = FastAPI()

app.include_router(health_view.router)
app.include_router(user_view.router)

handler = Mangum(app)

# invoke debug 用
# def handler_debug(event, context):
#     print(event)
#     print(context)
#     # if event.get("resource") != '/{proxy+}':
#     #     # proxy+ 由来ではない場合何もしない
#     #     return
    
#     # default
#     asgi_handler = Mangum(app)
#     response = asgi_handler(event, context) # Call the instance with the event arguments
    
#     return response
# handler = handler_debug