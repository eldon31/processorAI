#### On this page

- [Bulk Cancellation](\docs\guides\cancel-running-functions#bulk-cancellation)
- [Bulk cancel via the REST API](\docs\guides\cancel-running-functions#bulk-cancel-via-the-rest-api)

Features [Inngest Functions](\docs\features\inngest-functions) [Cancellation](\docs\features\inngest-functions\cancellation)

# Bulk Cancellation

With Inngest, your functions can be running or paused for long periods of time. You may have function with hundreds of steps, or you may be using [`step.sleep`](\docs\reference\functions\step-sleep) , [`step.sleepUntil`](\docs\reference\functions\step-sleep-until) , or [`step.waitForEvent`](\docs\reference\functions\step-wait-for-event) . Sometimes, things happen in your system that make it no longer necessary to complete running the function, which is when cancelling is necessary.

Inngest provides both a Bulk Cancellation API and UI. The Bulk Cancellation API offers more flexibility with the support of event expression matching

while the

[Bulk Cancellation UI](\docs\platform\manage\bulk-cancellation) , available from the Platform, provides a quick way to cancel unwanted Function runs.

## [Bulk cancel via the REST API](\docs\guides\cancel-running-functions#bulk-cancel-via-the-rest-api)

You can also cancel functions in bulk via the [REST API](https://api-docs.inngest.com/docs/inngest-api) . This is useful if you have a large number of functions within a specific range that you need to cancel.

With the `POST /cancellations` endpoint, you can cancel functions by specifying the `app_id` , `function_id` , and a `started_after` and `started_before` timestamp range. You can also optionally specify an `if` statement to only cancel functions that match a [given expression](\docs\guides\writing-expressions) .

POST api.inngest.com/v1/cancellations

Copy Copied

```
curl -X POST https://api.inngest.com/v1/cancellations \
-H 'Authorization: Bearer signkey-prod-<YOUR-SIGNING-KEY>' \
-H 'Content-Type: application/json' \
--data '{
"app_id": "acme-app",
"function_id": "schedule-reminder",
"started_after": "2024-01-21T18:23:12.000Z",
"started_before": "2024-01-22T14:22:42.130Z",
"if": "event.data.userId == ' user_o9235hf84hf '"
}'
```

When successful, the response will be returned with the cancellation ID and the cancellation job data:

### Response

Copy Copied

```
{
"id" : "01HMRMPE5ZQ4AMNJ3S2N79QGRZ" ,
"environment_id" : "e03843e1-d2df-419e-9b7b-678b03f7398f" ,
"function_id" : "schedule-reminder" ,
"started_after" : "2024-01-21T18:23:12.000Z" ,
"started_before" : "2024-01-22T14:22:42.130Z" ,
"if" : "event.data.userId == 'user_o9235hf84hf'"
}
```

To learn more, read the full [REST API reference](https://api-docs.inngest.com/docs/inngest-api) .