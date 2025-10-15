#### On this page

- [Production mode](\docs\reference\python\overview\prod-mode#production-mode)
- [How to opt-out](\docs\reference\python\overview\prod-mode#how-to-opt-out)

References [Python SDK](\docs\reference\python)

# Production mode

When the SDK is in production mode it will try to connect to Inngest Cloud instead of the Inngest Dev Server. Production mode is opt-out for security reasons.

## [How to opt-out](\docs\reference\python\overview\prod-mode#how-to-opt-out)

You'll want to disable production mode whenever you're using the Inngest Dev Server. This is typically during local development and CI. Production mode can be disabled in 2 ways:

1. Set the `INNGEST_DEV` environment variable to `1` .
2. Set the `Inngest` 's `is_production` constructor argument to `false` .

Using the `INNGEST_DEV` environment variable is the recommended way to disable production mode. But make sure that it isn't set in production!

`Inngest` 's `is_production` constructor argument is useful for disabling production mode based on whatever logic you want. For example, you could control it using the `FLASK_ENV` environment variable:

Copy Copied

```
import inngest

inngest . Inngest (
app_id = "my_flask_app" ,
is_production = os.environ. get ( "FLASK_ENV" ) == "production" ,
)
```