This page documents the network-related types in Pydantic, which provide specialized validation and handling for network data formats such as URLs, email addresses, IP addresses, and database connection strings. These types help ensure that network-related data is properly validated and structured for use in your applications.

## Core Network Types Overview

Pydantic offers several categories of network types that handle different types of network-related data:

```mermaid
graph TD
    subgraph "Pydantic Network Types"
        urlTypes["URL Types"] 
        dsnTypes["Database DSN Types"]
        emailTypes["Email Types"]
        ipTypes["IP Address Types"]
    end
    
    urlTypes --> baseUrl["BaseUrl Classes"]
    urlTypes --> httpUrl["HttpUrl"]
    urlTypes --> wsUrl["WebsocketUrl"]
    urlTypes --> fileUrl["FileUrl"]
    urlTypes --> ftpUrl["FtpUrl"]
    
    dsnTypes --> postgresDsn["PostgresDsn"]
    dsnTypes --> redisDsn["RedisDsn"]
    dsnTypes --> mongoDsn["MongoDsn"]
    dsnTypes --> otherDsn["Other DSNs"]
    
    emailTypes --> emailStr["EmailStr"]
    emailTypes --> nameEmail["NameEmail"]
    
    ipTypes --> ipv4["IPv4 Types"]
    ipTypes --> ipv6["IPv6 Types"]
    ipTypes --> ipvAny["IPv4/IPv6 Union Types"]
```

Sources: [pydantic/networks.py:1-67]()(showing exported types), [pydantic/__init__.py:120-144]()

## URL Types Architecture

URL types in Pydantic are built on a hierarchical architecture with two base classes: `_BaseUrl` for single-host URLs and `_BaseMultiHostUrl` for URLs that can contain multiple hosts (commonly used in database connection strings).

```mermaid
graph TD
    subgraph "Base Implementation"
        _BaseUrl["_BaseUrl"] -->|wraps| CoreUrl["pydantic_core.Url"]
        _BaseMultiHostUrl["_BaseMultiHostUrl"] -->|wraps| CoreMultiUrl["pydantic_core.MultiHostUrl"]
    end
    
    subgraph "Single Host URL Types"
        AnyUrl["AnyUrl"] -->|inherits| _BaseUrl
        HttpUrl["HttpUrl"] -->|inherits| AnyUrl
        AnyHttpUrl["AnyHttpUrl"] -->|inherits| AnyUrl
        FileUrl["FileUrl"] -->|inherits| AnyUrl
        FtpUrl["FtpUrl"] -->|inherits| AnyUrl
        WebsocketUrl["WebsocketUrl"] -->|inherits| AnyUrl
        AnyWebsocketUrl["AnyWebsocketUrl"] -->|inherits| AnyUrl
    end
    
    subgraph "Multi-Host URL Types"
        PostgresDsn["PostgresDsn"] -->|inherits| _BaseMultiHostUrl
        MySQLDsn["MySQLDsn"] -->|inherits| _BaseMultiHostUrl
        RedisDsn["RedisDsn"] -->|inherits| _BaseMultiHostUrl
        MongoDsn["MongoDsn"] -->|inherits| _BaseMultiHostUrl
        KafkaDsn["KafkaDsn"] -->|inherits| _BaseMultiHostUrl
        OtherDsns["Other DSNs..."] -->|inherits| _BaseMultiHostUrl
    end
    
    subgraph "Customization"
        UrlConstraints["UrlConstraints"] -.->|configures| _BaseUrl
        UrlConstraints -.->|configures| _BaseMultiHostUrl
    end
```

Sources: [pydantic/networks.py:70-532]()

## Common URL Types

Pydantic provides several specialized URL types for different protocols:

| Type | Description | Constraints |
|------|-------------|------------|
| `AnyUrl` | Base type for all URLs | Any scheme allowed, TLD and host not required |
| `HttpUrl` | HTTP/HTTPS URLs | Only http/https schemes, max length 2083 |
| `AnyHttpUrl` | HTTP/HTTPS URLs with fewer constraints | Only http/https schemes |
| `FileUrl` | File URLs | Only file scheme |
| `FtpUrl` | FTP URLs | Only ftp scheme |
| `WebsocketUrl` | WebSocket URLs | Only ws/wss schemes, max length 2083 |
| `AnyWebsocketUrl` | WebSocket URLs with fewer constraints | Only ws/wss schemes |

Sources: [pydantic/networks.py:534-688]()

### URL Components and Properties

All URL types provide access to standard URL components:

```python