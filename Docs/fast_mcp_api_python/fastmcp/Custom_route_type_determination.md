def custom_route_mapper(route: HTTPRoute, mcp_type: MCPType) -> MCPType | None:
    if "/admin" in route.path:
        return MCPType.EXCLUDE
    return mcp_type