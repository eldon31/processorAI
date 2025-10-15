#### On this page

- [Cleanup after function cancellation](\docs\examples\cleanup-after-function-cancellation#cleanup-after-function-cancellation)
- [Quick snippet](\docs\examples\cleanup-after-function-cancellation#quick-snippet)
- [More context](\docs\examples\cleanup-after-function-cancellation#more-context)

[Examples](\docs\examples)

# Cleanup after function cancellation

When function runs are cancelled, you may want to perform some sort of post-cancellation code. This example will use the [`inngest/function.cancelled`](\docs\reference\system-events\inngest-function-cancelled) system event.

Whether your function run is cancelled via [`cancelOn`](\docs\features\inngest-functions\cancellation\cancel-on-events) [event](\docs\features\inngest-functions\cancellation\cancel-on-events) , [REST API](\docs\guides\cancel-running-functions) or [bulk cancellation](\docs\platform\manage\bulk-cancellation) , this method will work the same.

## [Quick snippet](\docs\examples\cleanup-after-function-cancellation#quick-snippet)

Here is an Inngest function and a corresponding function that will be run whenever the original function is cancelled. This uses the function trigger's `if` parameter to filter the `inngest/function.cancelled` event to only be triggered for the original function.

Copy Copied

```
const inngest = new Inngest ({ id : "newsletter-app" });

// This is our "import" function that will get cancelled
export const importAllContacts = inngest .createFunction (
{
id : "import-all-contacts" ,
cancelOn : [{ event : "contacts/import.cancelled" , if : "async.data.importId == event.data.importId" }]
} ,
{ event : "contacts/import.requested" } ,
async ({ event , step  }) => {
// This is a long running function
}
)

// This function will be run only when the matching function_id has a run that is cancelled
export const cleanupCancelledImport = inngest .createFunction (
{
name : "Cleanup cancelled import" ,
id : "cleanup-cancelled-import"
} ,
{
event : "inngest/function.cancelled" ,
// The function ID is a hyphenated slug of the App ID w/ the functions" id
if : "event.data.function_id == 'newsletter-app-import-all-contacts'"
} ,
async ({ event , step , logger }) => {
// This code will execute after your function is cancelled

// The event that triggered our original function run is passed nested in our event payload
const originalTriggeringEvent = event . data .event;
logger .info ( `Import was cancelled: ${ originalTriggeringEvent . data .importId } ` )
}
);
```

An example cancellation event payload:

Copy Copied

```
{
"name" : "inngest/function.cancelled" ,
"data" : {
"error" : {
"error" : "function cancelled" ,
"message" : "function cancelled" ,
"name" : "Error"
} ,
"event" : {
"data" : {
"importId" : "bdce1b1b-6e3a-43e6-84c2-2deb559cdde6"
} ,
"id" : "01JDJK451Y9KFGE5TTM2FHDEDN" ,
"name" : "contacts/import.requested" ,
"ts" : 1732558407003 ,
"user" : {}
} ,
"events" : [
{
"data" : {
"importId" : "bdce1b1b-6e3a-43e6-84c2-2deb559cdde6"
} ,
"id" : "01JDJK451Y9KFGE5TTM2FHDEDN" ,
"name" : "contacts/import.requested" ,
"ts" : 1732558407003 ,
"user" : {}
}
] ,
"function_id" : "newsletter-app-import-all-contacts" ,
"run_id" : "01JDJKGTGDVV4DTXHY6XYB7BKK"
} ,
"id" : "01JDJKH1S5P2YER8PKXPZJ1YZJ" ,
"ts" : 1732570023717
}
```

## [More context](\docs\examples\cleanup-after-function-cancellation#more-context)

Check the resources below to learn more about building email sequences with Inngest.

### [Reference: inngest/function.cancelled system event](\docs\reference\system-events\inngest-function-cancelled)

[Learn more about the system event.](\docs\reference\system-events\inngest-function-cancelled)

### [Guide: Function cancellation](\docs\features\inngest-functions\cancellation)

[Learn about the different ways to cancel a function run.](\docs\features\inngest-functions\cancellation)