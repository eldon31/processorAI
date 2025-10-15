#### On this page

- [Send events](\docs\reference\python\client\send#send-events)
- [send](\docs\reference\python\client\send#send)
- [send\_sync](\docs\reference\python\client\send#send-sync)

References [Python SDK](\docs\reference\python)

# Send events

💡️ This guide is for sending events from *outside* an Inngest function. To send events within an Inngest function, refer to the [step.send\_event](\docs\reference\python\steps\send-event) guide.

Sends 1 or more events to the Inngest server. Returns a list of the event IDs.

Copy Copied

```
import inngest

inngest_client = inngest . Inngest (app_id = "my_app" )

# Call the `send` method if you're using async/await
ids = await inngest_client . send (
inngest. Event (name = "my_event" , data = { "msg" : "Hello!" })
)

# Call the `send_sync` method if you aren't using async/await
ids = inngest_client . send_sync (
inngest. Event (name = "my_event" , data = { "msg" : "Hello!" })
)

# Can pass a list of events
ids = await inngest_client . send (
[
inngest. Event (name = "my_event" , data = { "msg" : "Hello!" }),
inngest. Event (name = "my_other_event" , data = { "name" : "Alice" }),
]
)
```

## [send](\docs\reference\python\client\send#send)

Only for async/await code.

- Name `events` Type Event | list[Event] Required required Description 1 or more events to send. Properties

## [send\_sync](\docs\reference\python\client\send#send-sync)

Blocks the thread. If you're using async/await then use `send` instead.

Arguments are the same as `send` .