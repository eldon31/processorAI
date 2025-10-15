#### On this page

- [Go SDK migration guide: v0.8 to v0.11](\docs\reference\go\migrations\v0.8-to-v0.11#go-sdk-migration-guide-v0-8-to-v0-11)
- [Input](\docs\reference\go\migrations\v0.8-to-v0.11#input)
- [GenericEvent](\docs\reference\go\migrations\v0.8-to-v0.11#generic-event)

References [Go SDK](https://pkg.go.dev/github.com/inngest/inngestgo) [Migrations](\docs\reference\go\migrations\v0.8-to-v0.11)

# Go SDK migration guide: v0.8 to v0.11

This guide will help you migrate your Inngest Go SDK from v0.8 to v0.11 by providing a summary of the breaking changes.

## [Input](\docs\reference\go\migrations\v0.8-to-v0.11#input)

The `Input` type now accepts the event data type as a generic parameter. Previously, it accepted the `GenericEvent` type.

Copy Copied

```
type MyEventData struct {
Message string `json:"message"`
}

_, err := inngestgo. CreateFunction (
client,
inngestgo.FunctionOpts{ID: "my-fn" },
inngestgo. EventTrigger ( "my-event" , nil ),
func (
ctx context.Context,
input inngestgo.Input[MyEventData],
) (any, error ) {
fmt. Println (input.Event.Data.Message)
return nil , nil
},
)
```

## [GenericEvent](\docs\reference\go\migrations\v0.8-to-v0.11#generic-event)

The `GenericEvent` type no longer accepts the event user type as a generic parameter.

Copy Copied

```
type MyEventData struct {
Message string `json:"message"`
}

type MyEvent = inngestgo.GenericEvent[MyEventData]
```