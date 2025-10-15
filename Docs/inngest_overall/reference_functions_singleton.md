#### On this page

- [Ensure exclusive execution of a function](\docs\reference\functions\singleton#ensure-exclusive-execution-of-a-function)
- [Configuration](\docs\reference\functions\singleton#configuration)

References [TypeScript SDK](\docs\reference\typescript)

# Ensure exclusive execution of a function

Ensure that only a single run of a function ( *or a set of specific functions, based on specific event properties* ) is running at a time.

See the [Singleton Functions guide](\docs\guides\singleton) for more information about how this feature works.

Copy Copied

```
export default inngest .createFunction (
{
id : "data-sync" ,
singleton : {
key : "event.data.user_id" ,
mode : "skip" ,
} ,
} ,
{ event : "data-sync.start" } ,
async ({ event }) => {
// This function will be skipped if another run of the same function is already running for the same user
}
);
```

## [Configuration](\docs\reference\functions\singleton#configuration)

- Name `singleton` Type object Required optional Description Options to configure exclusive execution of a function. Properties