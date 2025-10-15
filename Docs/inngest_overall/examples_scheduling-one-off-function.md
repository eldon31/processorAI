#### On this page

- [Scheduling a one-off function](\docs\examples\scheduling-one-off-function#scheduling-a-one-off-function)
- [Quick Snippet](\docs\examples\scheduling-one-off-function#quick-snippet)
- [Triggering the function with a timestamp](\docs\examples\scheduling-one-off-function#triggering-the-function-with-a-timestamp)
- [Alternatives](\docs\examples\scheduling-one-off-function#alternatives)
- [More context](\docs\examples\scheduling-one-off-function#more-context)
- [Related concepts](\docs\examples\scheduling-one-off-function#related-concepts)

[Examples](\docs\examples)

# Scheduling a one-off function

Inngest provides a way to delay a function run to a specific time in the future. This is useful when:

- You want to schedule work in the future based on user input.
- You want to slightly delay execution of a non-urgent function for a few seconds or minutes.

This page provides a quick example of how to delay a function run to a specific time in the future using the [event payload's](\docs\events#event-payload-format) `ts` field.

## [Quick Snippet](\docs\examples\scheduling-one-off-function#quick-snippet)

Here is a basic function that sends a reminder to a user at a given email.

Copy Copied

```
const sendReminder = inngest .createFunction (
{ id : "send-reminder" } ,
{ event : "notifications/reminder.scheduled" } ,
async ({ event , step }) => {
const { user , message } = event .data;

const { id } = await emailApi .send ({
to : user .email ,
subject : "Reminder for your upcoming event" ,
body : message ,
});

return { id }
}
);
```

### [Triggering the function with a timestamp](\docs\examples\scheduling-one-off-function#triggering-the-function-with-a-timestamp)

To trigger this function, you will send an event `"notifications/reminder.scheduled"` using `inngest.send()` with the necessary data. The `ts` field in the [event payload](\docs\events#event-payload-format) should be set to the Unix timestamp of the time you want the function to run. For example, to schedule a reminder for 5 minutes in the future:

Copy Copied

```
await inngest .send ({
name : "notifications/reminder.scheduled" ,
data : {
user : { email : "johnny.utah@fbi.gov" }
message: "Don't forget to catch the wave at 3pm" ,
} ,
// Include the timestamp for 5 minutes in the future:
ts : Date .now () + 5 * 60 * 1000 ,
});
```

⚠️ Providing a timestamp in the event only applies for starting function runs. Functions waiting for a matching event will immediately resume, regardless of the timestamp.

### [Alternatives](\docs\examples\scheduling-one-off-function#alternatives)

Depending on your use case, you may want to consider using [scheduled functions (cron jobs)](\docs\guides\scheduled-functions) for scheduling periodic work or use [`step.sleepUntil()`](\docs\reference\functions\step-sleep-until) to add mid-function delays for a layer time.

## [More context](\docs\examples\scheduling-one-off-function#more-context)

Check the resources below to learn more about scheduling functions with Inngest.

### [Guide: Sending events](\docs\events)

[Learn how to send events to trigger functions in Inngest.](\docs\events)

## [Related concepts](\docs\examples\scheduling-one-off-function#related-concepts)

- [Scheduled functions (cron jobs)](\docs\guides\scheduled-functions)
- [step.sleepUntil()](\docs\reference\functions\step-sleep-until)