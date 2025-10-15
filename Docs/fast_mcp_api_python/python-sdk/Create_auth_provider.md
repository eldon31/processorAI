auth_provider = OAuthClientProvider(
    server_url="https://api.example.com/v1/mcp",
    client_metadata=client_metadata,
    storage=my_token_storage,
    redirect_handler=my_redirect_handler,
    callback_handler=my_callback_handler
)