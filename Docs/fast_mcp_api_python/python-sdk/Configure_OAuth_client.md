client_metadata = OAuthClientMetadata(
    client_name="My MCP Client",
    client_uri=AnyHttpUrl("https://myapp.example.com"),
    redirect_uris=[AnyUrl("http://localhost:3030/callback")],
    scope="read write"
)