#### On this page

- [Cancel on](\docs\reference\typescript\functions\cancel-on#cancel-on)
- [How to use cancelOn](\docs\reference\typescript\functions\cancel-on#how-to-use-cancel-on)
- [Configuration](\docs\reference\typescript\functions\cancel-on#configuration)
- [Examples](\docs\reference\typescript\functions\cancel-on#examples)
- [With a timeout window](\docs\reference\typescript\functions\cancel-on#with-a-timeout-window)

References [TypeScript SDK](\docs\reference\typescript)

# Cancel on

Stop the execution of a running function when a specific event is received using `cancelOn` .

Copy Copied

```
inngest .createFunction (
{
id : "sync-contacts" ,
cancelOn : [
{
event : "app/user.deleted" ,
// ensure the async (future) event's userId matches the trigger userId
if : "async.data.userId == event.data.userId" ,
} ,
] ,
}
// ...
);
```

Using `cancelOn` is very useful for handling scenarios where a long-running function should be terminated early due to changes elsewhere in your system.

The API for this is similar to the [`step.waitForEvent()`](\docs\guides\multi-step-functions#wait-for-event) tool, allowing you to specify the incoming event and different methods for matching pieces of data within.

## [How to use cancelOn](\docs\reference\typescript\functions\cancel-on#how-to-use-cancel-on)

The most common use case for cancellation is to cancel a function's execution if a specific field in the incoming event matches the same field in the triggering event. For example, you might want to cancel a sync event for a user if that user is deleted. For this, you need to specify a `match` [expression](\docs\guides\writing-expressions) . Let's look at an example function and two events.

This function specifies it will `cancelOn` the `"app/user.deleted"` event only when it and the original `"app/user.created"` event have the same `data.userId` value:

Copy Copied

```
inngest .createFunction (
{
id : "sync-contacts" ,
cancelOn : [
{
event : "app/user.deleted" ,
// ensure the async (future) event's userId matches the trigger userId
if : "async.data.userId == event.data.userId" ,
} ,
] ,
} ,
{ event : "app/user.created" } ,
// ...
);
```

For the given function, this is an example of an event that would trigger the function:

Copy Copied

```
{
"name" : "app/user.created" ,
"data" : {
"userId" : "123" ,
"name" : "John Doe"
}
}
```

And this is an example of an event that would cancel the function as it and the original event have the same `data.userId` value of `"123"` :

Copy Copied

```
{
"name" : "app/user.deleted" ,
"data" : {
"userId" : "123"
}
}
```

Match expressions can be simple equalities or be more complex. Read [our guide to writing expressions](\docs\guides\writing-expressions) for more info.

Functions are cancelled *between steps* , meaning that if there is a `step.run` currently executing, it will finish before the function is cancelled.

Inngest does this to ensure that steps are treated like atomic operations and each step either completes or does not run at all.

## [Configuration](\docs\reference\typescript\functions\cancel-on#configuration)

- Name `cancelOn` Type array of objects Required optional Description Define events that can be used to cancel a running or sleeping function Properties

## [Examples](\docs\reference\typescript\functions\cancel-on#examples)

### [With a timeout window](\docs\reference\typescript\functions\cancel-on#with-a-timeout-window)

Cancel a function's execution if a matching event is received within a given amount of time from the function being triggered.

v3 v2

Copy Copied

```
inngest .createFunction (
{
id : "sync-contacts" ,
cancelOn : [{ event : "app/user.deleted" , match : "data.userId" , timeout : "1h" }] ,
}
// ...
);
```

This is useful when you want to limit the time window for cancellation, ensuring that the function will continue to execute if no matching event is received within the specified time frame.