#### On this page

- [Inngest client](\docs\reference\python\client\overview#inngest-client)
- [Configuration](\docs\reference\python\client\overview#configuration)

References [Python SDK](\docs\reference\python)

# Inngest client

The Inngest client is used to configure your application and send events outside of Inngest functions.

Copy Copied

```
import inngest

inngest_client = inngest . Inngest (
app_id = "flask_example" ,
)
```

## [Configuration](\docs\reference\python\client\overview#configuration)

- Name `api_base_url` Type str Required optional Description Override the default base URL for our REST API ( `https://api.inngest.com/` ). See also the [`INNGEST_EVENT_API_BASE_URL`](\docs\reference\python\overview\env-vars#inngest-event-api-base-url) environment variable.
- Name `app_id` Type str Required required Description A unique identifier for your application. We recommend a hyphenated slug.
- Name `env` Type str Required optional Description The environment name. Required only when using [Branch Environments](\docs\platform\environments) .
- Name `event_api_base_url` Type str Required optional Description Override the default base URL for sending events ( `https://inn.gs/` ). See also the [`INNGEST_EVENT_API_BASE_URL`](\docs\reference\python\overview\env-vars#inngest-event-api-base-url) environment variable.
- Name `event_key` Type str Required optional Description An Inngest event key. Alternatively, set the [`INNGEST_EVENT_KEY`](\docs\reference\python\overview\env-vars#inngest-event-key) environment variable.
- Name `is_production` Type bool Required optional Description Whether the SDK should run in [production mode](\docs\reference\python\overview\prod-mode) . See also the [`INNGEST_DEV`](\docs\reference\python\overview\env-vars#inngest-dev) environment variable.
- Name `logger` Type logging.Logger | logging.LoggerAdapter Required optional Description A logger object derived from `logging.Logger` or `logging.LoggerAdapter` . Defaults to using `logging.getLogger(__name__)` if not provided.
- Name `middleware` Type list Required optional Version experimental Description A list of middleware to add to the client. Read more in our [middleware docs](\docs\reference\python\middleware\overview) .
- Name `signing_key` Type str Required optional Description The Inngest signing key. Alternatively, set the [`INNGEST_SIGNING_KEY`](\docs\reference\python\overview\env-vars#inngest-signing-key) environment variable.