#### On this page

- [Function run priority](\docs\reference\functions\run-priority#function-run-priority)
- [Configuration](\docs\reference\functions\run-priority#configuration)

References [TypeScript SDK](\docs\reference\typescript)

# Function run priority v3.2.1+

You can prioritize specific function runs above other runs **within the same function** .

See the [Priority guide](\docs\guides\priority) for more information about how this feature works.

Copy Copied

```
export default inngest .createFunction (
{
id : "ai-generate-summary" ,
priority : {
// For enterprise accounts, a given function run will be prioritized
// ahead of functions that were enqueued up to 120 seconds ago.
// For all other accounts, the function will run with no priority.
run : "event.data.account_type == 'enterprise' ? 120 : 0" ,
} ,
} ,
{ event : "ai/summary.requested" } ,
async ({ event , step }) => {
// This function will be prioritized based on the account type
}
);
```

## [Configuration](\docs\reference\functions\run-priority#configuration)

- Name `priority` Type object Required optional Description Options to configure how to prioritize functions Properties

Return values outside of your account's range (by default, -600 to 600) will automatically be clipped

to your max bounds.

An invalid expression will evaluate to 0, as in "no priority".