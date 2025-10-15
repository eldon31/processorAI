unicode_host()   # Get the host as a unicode string (decode punycode)
query_params()   # Get query parameters as list of key-value pairs
unicode_string() # Get the full URL as a unicode string
encoded_string() # Get the encoded URL string (same as str())
```

Sources: [pydantic/networks.py:124-226](), [pydantic/networks.py:351-426]()

### Usage Example

```python
from pydantic import BaseModel, HttpUrl

class WebResource(BaseModel):
    url: HttpUrl

# Valid HTTP URL
resource = WebResource(url="https://example.com/api/resource?id=123")

# Access URL components
print(resource.url.host)       # "example.com"
print(resource.url.path)       # "/api/resource"
print(resource.url.port)       # 443 (default for HTTPS)
print(resource.url.query)      # "id=123"
print(resource.url.scheme)     # "https"
```

Sources: [tests/test_networks.py:115-119](), [tests/test_networks.py:173-194]()

## Database Connection Strings (DSNs)

Pydantic provides specialized types for validating and handling database connection strings (Data Source Names or DSNs), which are URLs that specify how to connect to a database.

### Supported DSN Types

| Type | Description | Allowed Schemes |
|------|-------------|-----------------|
| `PostgresDsn` | PostgreSQL connections | postgres, postgresql, postgresql+asyncpg, etc. |
| `CockroachDsn` | CockroachDB connections | cockroachdb, cockroachdb+psycopg2, etc. |
| `MySQLDsn` | MySQL connections | mysql, mysql+mysqlconnector, mysql+pymysql, etc. |
| `MariaDBDsn` | MariaDB connections | mariadb, mariadb+mariadbconnector, etc. |
| `ClickHouseDsn` | ClickHouse connections | clickhouse, clickhouse+http, etc. |
| `SnowflakeDsn` | Snowflake connections | snowflake |
| `MongoDsn` | MongoDB connections | mongodb |
| `RedisDsn` | Redis connections | redis, rediss |
| `AmqpDsn` | AMQP (RabbitMQ) connections | amqp, amqps |
| `KafkaDsn` | Kafka connections | kafka |
| `NatsDsn` | NATS connections | nats, tls, ws |

Sources: [pydantic/networks.py:690-826]()

### DSN Example

```python
from pydantic import BaseModel, PostgresDsn, RedisDsn

class AppConfig(BaseModel):
    database_url: PostgresDsn
    cache_url: RedisDsn