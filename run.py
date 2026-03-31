import asyncio
import uvicorn

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    config = uvicorn.Config(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        loop="asyncio"
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())