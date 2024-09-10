from fastapi import BackgroundTasks
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel

class EmailSchema(BaseModel):
    email: EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME = "username",
    MAIL_PASSWORD = "**********",
    MAIL_FROM = "test@email.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "mail server",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def simple_send(email: EmailSchema) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


async def send_in_background(
    background_tasks: BackgroundTasks,
    email: EmailSchema
    ) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=email.dict().get("email"),
        body="Simple background task",
        subtype=MessageType.plain)

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message,message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})