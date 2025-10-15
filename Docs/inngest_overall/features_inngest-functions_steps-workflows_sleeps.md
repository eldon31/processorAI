#### On this page

- [Sleeps](\docs\features\inngest-functions\steps-workflows\sleeps#sleeps)
- [How Sleeps work](\docs\features\inngest-functions\steps-workflows\sleeps#how-sleeps-work)
- [Pausing an execution for a given time](\docs\features\inngest-functions\steps-workflows\sleeps#pausing-an-execution-for-a-given-time)
- [Pausing an execution until a given date](\docs\features\inngest-functions\steps-workflows\sleeps#pausing-an-execution-until-a-given-date)

Features [Inngest Functions](\docs\features\inngest-functions) [Steps &amp; Workflows](\docs\features\inngest-functions\steps-workflows)

# Sleeps

Two step methods, `step.sleep` and `step.sleepUntil` , are available to pause the execution of your function for a specific amount of time. Your function can sleep for seconds, minutes, or days, up to a maximum of one year (seven days for account on our [free tier](\pricing?ref=docs-sleeps) ).

Using sleep methods can avoid the need to run multiple cron jobs or use additional queues. For example, Sleeps enable you to create a user onboarding workflow that sequences multiple actions in time: first send a welcome email, then send a tutorial each day for a week.

## [How Sleeps work](\docs\features\inngest-functions\steps-workflows\sleeps#how-sleeps-work)

`step.sleep` and `step.sleepUntil` tell Inngest to resume execution of your function at a future time. Your code doesn't need to be running during the sleep interval, allowing sleeps to be used in any environment, even serverless platforms.

A Function paused by a sleeping Step doesn't affect your account capacity; i.e. it does not count against your plan's concurrency limit. A sleeping Function doesn't count against any [concurrency policy](\docs\guides\concurrency) you've set on the function, either.

TypeScript Go Python

## [Pausing an execution for a given time](\docs\features\inngest-functions\steps-workflows\sleeps#pausing-an-execution-for-a-given-time)

Use `step.sleep()` to pause the execution of your function for a specific amount of time.

Copy Copied

```
export default inngest .createFunction (
{ id : "send-delayed-email" } ,
{ event : "app/user.signup" } ,
async ({ event , step }) => {
await step .sleep ( "wait-a-couple-of-days" , "2d" );
// Do something else
}
);
```

Check out the [`step.sleep()`](\docs\reference\functions\step-sleep) [TypeScript reference.](\docs\reference\functions\step-sleep)

## [Pausing an execution until a given date](\docs\features\inngest-functions\steps-workflows\sleeps#pausing-an-execution-until-a-given-date)

Use `step.sleepUntil()` to pause the execution of your function until a specific date time.

Copy Copied

```
export default inngest .createFunction (
{ id : "send-scheduled-reminder" } ,
{ event : "app/reminder.scheduled" } ,
async ({ event , step }) => {
const date = new Date ( event . data .remind_at);
await step .sleepUntil ( "wait-for-scheduled-reminder" , date);
// Do something else
}
);
```

Check out the [`step.sleepUntil()`](\docs\reference\functions\step-sleep-until) [TypeScript reference.](\docs\reference\functions\step-sleep-until)

**Sleeps and trace/log history**

You may notice that Inngest Cloud's Function Runs view doesn't show function runs that use sleeps longer than your [Inngest plan's](\pricing?ref=docs-sleeps) trace &amp; log history limit, even though the functions are still sleeping and will continue to run as expected. **This is a known limitation** in our current dashboard and we're working to improve it.

In the meantime:

- Rest assured that your sleeping functions *are* still sleeping and will resume as scheduled, even if they're not visible in the Function Runs list.
- Given a function run's ID, you can inspect its status using Inngest Cloud's Quick Search feature (Ctrl-K or ⌘K) or the [REST API](https://api-docs.inngest.com/docs/inngest-api/) .