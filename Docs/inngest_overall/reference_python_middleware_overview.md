#### On this page

- [Middleware](\docs\reference\python\middleware\overview#middleware)
- [Examples](\docs\reference\python\middleware\overview#examples)

References [Python SDK](\docs\reference\python)

# Middleware v0.3.0+

Middleware allows you to run code at various points in an Inngest function's lifecycle. This is useful for adding custom behavior to your functions, like error reporting and end-to-end encryption.

Copy Copied

```
class MyMiddleware ( inngest . Middleware ):
async def before_send_events ( self , events : list [ inngest . Event ] ) -> None :
print ( f "Sending { len (events) } events" )

async def after_send_events ( self , result : inngest . SendEventsResult) -> None :
print ( "Done sending events" )

inngest_client = inngest . Inngest (
app_id = "my_app" ,
middleware = [MyMiddleware],
)
```

## [Examples](\docs\reference\python\middleware\overview#examples)

- [End-to-end encryption](https://github.com/inngest/inngest-py/tree/main/pkg/inngest_encryption)
- [Sentry](https://github.com/inngest/inngest-py/blob/main/pkg/inngest/inngest/experimental/sentry_middleware.py)