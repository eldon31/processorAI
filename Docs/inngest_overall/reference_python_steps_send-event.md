#### On this page

- [Send event](\docs\reference\python\steps\send-event#send-event)
- [Arguments](\docs\reference\python\steps\send-event#arguments)
- [Examples](\docs\reference\python\steps\send-event#examples)

References [Python SDK](\docs\reference\python) [Steps](\docs\reference\python\steps\invoke)

# Send event

💡️ This guide is for sending events from *inside* an Inngest function. To send events outside an Inngest function, refer to the [client event sending](\docs\reference\python\client\send) guide.

Sends 1 or more events to the Inngest server. Returns a list of the event IDs.

## [Arguments](\docs\reference\python\steps\send-event#arguments)

- Name `step_id` Type str Required required Description Step ID. Should be unique within the function.
- Name `events` Type Event | list[Event] Required required Description 1 or more events to send. Properties

## [Examples](\docs\reference\python\steps\send-event#examples)

Copy Copied

```
@inngest_client . create_function (
fn_id = "my_function" ,
trigger = inngest. TriggerEvent (event = "app/my_function" ),
)
async def fn ( ctx : inngest . Context) -> list [ str ] :
return await ctx . step . send_event ( "send" , inngest. Event (name = "foo" ))
```