import asyncio
import socketio
import uvicorn

from quart import Quart
from quart_cors import cors

CORS_ALLOWED_ORIGINS = "*"


class QuartSIO:
    def __init__(self) -> None:
        self._sio = socketio.AsyncServer(
            async_mode="asgi", cors_allowed_origins=CORS_ALLOWED_ORIGINS
        )
        self._quart_app = Quart(__name__)
        self._quart_app = cors(self._quart_app, allow_origin=CORS_ALLOWED_ORIGINS)
        self._sio_app = socketio.ASGIApp(self._sio, self._quart_app)
        self.route = self._quart_app.route
        self.on = self._sio.on
        self.emit = self._sio.emit

    async def _run(self, host: str, port: int):
        try:
            uvconfig = uvicorn.Config(self._sio_app, host=host, port=port)
            server = uvicorn.Server(config=uvconfig)
            await server.serve()
        except KeyboardInterrupt:
            print("Shutting down")
        finally:
            print("Bye!")

    def run(self, host: str, port: int):
        asyncio.run(self._run(host, port))


app = QuartSIO()


@app.route("/")
async def index():
    return "Hello, world!"


@app.on("connect")
async def on_connect(sid, environ):
    print("Connected")


@app.on("disconnect")
async def on_disconnect(sid):
    print("Disconnected")


@app.on("*")
async def on_message(message, sid, *args):
    print("Message:", message, args)
    await app.emit("echo", message)


if __name__ == "__main__":
    app.run("localhost", 3000)
