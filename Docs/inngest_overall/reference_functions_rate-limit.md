#### On this page

- [Rate limit function execution](\docs\reference\functions\rate-limit#rate-limit-function-execution)
- [Configuration](\docs\reference\functions\rate-limit#configuration)
- [Examples](\docs\reference\functions\rate-limit#examples)
- [Limiting synchronization triggered by webhook events](\docs\reference\functions\rate-limit#limiting-synchronization-triggered-by-webhook-events)
- [Send at most one email for multiple alerts over an hour](\docs\reference\functions\rate-limit#send-at-most-one-email-for-multiple-alerts-over-an-hour)

References [TypeScript SDK](\docs\reference\typescript)

# Rate limit function execution

Set a *hard limit* on how many function runs can start within a time period. Events that exceed the rate limit are *skipped* and do not trigger functions to start.

See the [Rate Limiting guide](\docs\guides\rate-limiting) for more information about how this feature works.

Copy Copied

```
export default inngest .createFunction (
{
id : "synchronize-data" ,
rateLimit : {
key : "event.data.company_id" ,
limit : 1 ,
period : "4h" ,
} ,
} ,
{ event : "intercom/company.updated" } ,
async ({ event , step }) => {
// This function will be rate limited
// It will only run 1 once per 4 hours for a given event payload with matching company_id
}
);
```

## [Configuration](\docs\reference\functions\rate-limit#configuration)

- Name `rateLimit` Type object Required optional Description Options to configure how to rate limit function execution Properties

## [Examples](\docs\reference\functions\rate-limit#examples)

### [Limiting synchronization triggered by webhook events](\docs\reference\functions\rate-limit#limiting-synchronization-triggered-by-webhook-events)

In this example, we use events from the Intercom webhook. The webhook can be overly chatty and send multiple `intercom/company.updated` events in a short time window. We also only really care to sync the user's data from Intercom no more than 4 times per day, so we set our limit to `6h` :

Copy Copied

```
/** Example event payload:
{
name: "intercom/company.updated",
data: {
company_id: "123456789",
company_name: "Acme, Inc."
}
}
*/
export default inngest .createFunction (
{
id : "synchronize-data" ,
rateLimit : {
key : "event.data.company_id" ,
limit : 1 ,
period : "4h" ,
} ,
} ,
{ event : "intercom/company.updated" } ,
async ({ event , step }) => {
const company = await step .run (
"fetch-latest-company-data-from-intercom" ,
async () => {
return await client . companies .find ({
companyId : event . data .company_id ,
});
}
);

await step .run ( "update-company-data-in-database" , async () => {
return await database . companies .upsert ({ id : company .id } , company);
});
}
);
```

### [Send at most one email for multiple alerts over an hour](\docs\reference\functions\rate-limit#send-at-most-one-email-for-multiple-alerts-over-an-hour)

When there is an issue in your system, you may want to send your user an email notification, but don't want to spam them. The issue may repeat several times within the span of few minutes, but the user really just needs one email. You can

Copy Copied

```
/** Example event payload:
{
name: "service/check.failed",
data: {
incident_id: "01HB9PWHZ4CZJYRAGEY60XEHCZ",
issue: "HTTP uptime check failed at 2023-09-26T21:23:51.515631317Z",
user_id: "user_aW5uZ2VzdF9pc19mdWNraW5nX2F3ZXNvbWU=",
service_name: "api",
service_id: "01HB9Q2EFBYG2B7X8VCD6JVRFH"
},
user: {
external_id: "user_aW5uZ2VzdF9pc19mdWNraW5nX2F3ZXNvbWU=",
email: "user @example .com"
}
}
*/
export default inngest .createFunction (
{
id : "send-check-failed-notification" ,
rateLimit : {
// Don't send duplicate emails to the same user for the same service over 1 hour
key : `event.data.user_id + "-" + event.data.service_id` ,
limit : 1 ,
period : "1h" ,
} ,
} ,
{ event : "service/check.failed" } ,
async ({ event , step }) => {
await step .run ( "send-alert-email" , async () => {
return await resend . emails .send ({
from : "notifications@myco.com" ,
to : event . user .email ,
subject : `ALERT: ${ event . data .issue } ` ,
text : `Dear user, ...` ,
});
});
}
);
```