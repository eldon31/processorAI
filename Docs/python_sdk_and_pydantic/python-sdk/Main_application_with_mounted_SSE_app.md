main_app = Starlette(routes=[
    Mount("/api/v1", app=sse_app)
])