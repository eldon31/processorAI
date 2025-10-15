print(config.database_url.scheme)   # "postgresql"
print(config.database_url.path)     # "/mydb"
print(config.cache_url.port)        # 6379
```

Sources: [tests/test_networks.py:482-494](), [tests/test_networks.py:700-731]()

### Multi-Host Support

Some DSN types support connecting to multiple hosts, which is useful for database clusters:

```python
from pydantic import BaseModel, PostgresDsn

class DbConfig(BaseModel):
    cluster_url: PostgresDsn

# Connect to multiple database servers
config = DbConfig(
    cluster_url="postgres://user:pass@host1.db.net:4321,host2.db.net:6432/app"
)

# Access hosts as a list of dictionaries
hosts = config.cluster_url.hosts()
# [
#   {'username': 'user', 'password': 'pass', 'host': 'host1.db.net', 'port': 4321},
#   {'username': None, 'password': None, 'host': 'host2.db.net', 'port': 6432}
# ]
```

Sources: [pydantic/networks.py:389-406](), [tests/test_networks.py:628-647]()

## Email Validation Types

Pydantic provides specialized types for validating email addresses. These types depend on the optional `email_validator` package.

```mermaid
graph TD
    subgraph "Email Types Structure"
        EmailStr["EmailStr"] -->|validates| EmailAddress["Email Address"]
        NameEmail["NameEmail"] -->|validates| DisplayAndEmail["Display Name + Email"]
        NameEmail -->|has| name["name: str"]
        NameEmail -->|has| email["email: EmailStr"]
    end
    
    subgraph "Dependencies"
        EmailValidator["email_validator Library"]
        validate_email["validate_email()"] 
    end
    
    EmailStr -.->|uses| EmailValidator
    NameEmail -.->|uses| EmailValidator
    validate_email -.->|uses| EmailValidator
```

Sources: [pydantic/networks.py:31-39]()

### Email Types Example

```python
from pydantic import BaseModel, EmailStr, NameEmail

class User(BaseModel):
    email: EmailStr
    contact: NameEmail

# Valid user
user = User(
    email="john@example.com",
    contact="John Doe <john@example.com>"
)

print(user.email)          # "john@example.com"
print(user.contact.name)   # "John Doe"
print(user.contact.email)  # "john@example.com"
```

Note: If the `email_validator` package is not installed, an error will be raised when these types are used.

## IP Address Types

Pydantic provides types for validating IP addresses, network interfaces, and networks.

```mermaid
graph TD
    subgraph "Standard Library"
        StdLib["ipaddress Module"]
    end
    
    subgraph "IP Address Types"
        IPvAnyAddress["IPvAnyAddress"] -->|union of| IPv4Address["IPv4Address"]
        IPvAnyAddress -->|union of| IPv6Address["IPv6Address"]
        
        IPvAnyInterface["IPvAnyInterface"] -->|union of| IPv4Interface["IPv4Interface"]
        IPvAnyInterface -->|union of| IPv6Interface["IPv6Interface"]
        
        IPvAnyNetwork["IPvAnyNetwork"] -->|union of| IPv4Network["IPv4Network"]
        IPvAnyNetwork -->|union of| IPv6Network["IPv6Network"]
    end
    
    StdLib -.->|provides| IPv4Address
    StdLib -.->|provides| IPv6Address
    StdLib -.->|provides| IPv4Interface
    StdLib -.->|provides| IPv6Interface
    StdLib -.->|provides| IPv4Network
    StdLib -.->|provides| IPv6Network
```

These types leverage Python's standard `ipaddress` module and provide proper validation during model instantiation.

### IP Address Types Categories

| Type | Description | Example |
|------|-------------|---------|
| `IPvAnyAddress` | Either IPv4 or IPv6 address | "192.168.1.1" or "::1" |
| `IPvAnyInterface` | IP interface with network information | "192.168.1.1/24" |
| `IPvAnyNetwork` | IP network | "192.168.0.0/24" |

Sources: [pydantic/networks.py:52-54]()

## Customization with UrlConstraints

The `UrlConstraints` class allows you to customize URL validation with specific constraints.

```python
from typing import Annotated
from pydantic import BaseModel, Url, UrlConstraints

# Create a custom URL type for a specific API
ApiUrl = Annotated[Url, UrlConstraints(
    allowed_schemes=['https'],
    host_required=True,
    default_path='/api/v1'
)]

class ApiConfig(BaseModel):
    endpoint: ApiUrl

# Valid configuration with default path
config = ApiConfig(endpoint="https://api.example.com")
print(config.endpoint)  # "https://api.example.com/api/v1"
```

### UrlConstraints Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `max_length` | Maximum URL length | `None` |
| `allowed_schemes` | List of allowed schemes | `None` |
| `host_required` | Whether host is required | `None` |
| `default_host` | Default host if none provided | `None` |
| `default_port` | Default port if none provided | `None` |
| `default_path` | Default path if none provided | `None` |

Sources: [pydantic/networks.py:70-120](), [tests/test_networks.py:823-841]()

## Implementation Details

### URL Validation Process

URL validation and processing in Pydantic follows these steps:

1. Parse the URL string into components
2. Validate the scheme against allowed schemes
3. Apply length constraints
4. Convert international domain names to punycode
5. Apply default values for missing components
6. Construct a validated URL object with accessible properties

### International Domain Name Support

Pydantic's URL types support internationalized domain names (IDNs) by automatically converting them to punycode:

```python
from pydantic import BaseModel, HttpUrl

class Site(BaseModel):
    url: HttpUrl