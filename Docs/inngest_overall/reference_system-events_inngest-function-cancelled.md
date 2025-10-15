#### On this page

- [inngest/function.cancelled](\docs\reference\system-events\inngest-function-cancelled#inngest-function-cancelled)
- [The event payload](\docs\reference\system-events\inngest-function-cancelled#the-event-payload)
- [Related resources](\docs\reference\system-events\inngest-function-cancelled#related-resources)

References [System events](\docs\reference\system-events\inngest-function-failed)

# inngest/function.cancelled

The `inngest/function.cancelled` event is sent whenever any single function is cancelled in your [Inngest environment](\docs\platform\environments) . The event will be sent if the event is cancelled via [`cancelOn`](\docs\features\inngest-functions\cancellation\cancel-on-events) [event](\docs\features\inngest-functions\cancellation\cancel-on-events) , [function timeouts](\docs\features\inngest-functions\cancellation\cancel-on-timeouts) , [REST API](\docs\guides\cancel-running-functions) or [bulk cancellation](\docs\platform\manage\bulk-cancellation) .

This event can be used to handle cleanup or similar for a single function or handle some sort of tracking function cancellations in some external system like Datadog.

You can write a function that uses the `"inngest/function.cancelled"` event with the optional `if` parameter to filter to specifically handle a single function by `function_id` .

## [The event payload](\docs\reference\system-events\inngest-function-cancelled#the-event-payload)

- Name `name` Type string: "inngest/function.cancelled" Description The `inngest/` event prefix is reserved for system events in each environment.
- Name `data` Type object Description The event payload data. Properties
- Name `ts` Type number Description The timestamp integer in milliseconds at which the cancellation occurred.

### Example payload

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
"content" : "Yost LLC explicabo eos" ,
"transcript" : "s3://product-ideas/carber-vac-release.txt" ,
"userId" : "bdce1b1b-6e3a-43e6-84c2-2deb559cdde6"
} ,
"id" : "01JDJK451Y9KFGE5TTM2FHDEDN" ,
"name" : "integrations/export.requested" ,
"ts" : 1732558407003 ,
"user" : {}
} ,
"events" : [
{
"data" : {
"content" : "Yost LLC explicabo eos" ,
"transcript" : "s3://product-ideas/carber-vac-release.txt" ,
"userId" : "bdce1b1b-6e3a-43e6-84c2-2deb559cdde6"
} ,
"id" : "01JDJK451Y9KFGE5TTM2FHDEDN" ,
"name" : "integrations/export.requested" ,
"ts" : 1732558407003
}
] ,
"function_id" : "demo-app-export" ,
"run_id" : "01JDJKGTGDVV4DTXHY6XYB7BKK"
} ,
"id" : "01JDJKH1S5P2YER8PKXPZJ1YZJ" ,
"ts" : 1732570023717
}
```

## [Related resources](\docs\reference\system-events\inngest-function-cancelled#related-resources)

- [Example: Cleanup after function cancellation](\docs\examples\cleanup-after-function-cancellation)