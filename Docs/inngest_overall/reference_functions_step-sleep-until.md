#### On this page

- [Sleep until step.sleepUntil()](\docs\reference\functions\step-sleep-until#sleep-until-step-sleep-until)
- [step.sleepUntil(id, datetime): Promise](\docs\reference\functions\step-sleep-until#step-sleep-until-id-datetime-promise)

References [TypeScript SDK](\docs\reference\typescript) [Steps](\docs\reference\functions\step-run)

# Sleep until step.sleepUntil()

## [step.sleepUntil(id, datetime): Promise](\docs\reference\functions\step-sleep-until#step-sleep-until-id-datetime-promise)

- Name `id` Type string Required required Description The ID of the step. This will be what appears in your function's logs and is used to memoize step state across function versions.
- Name `datetime` Type Date | string | Temporal.Instant | Temporal.ZonedDateTime Required required Description The datetime at which to continue execution of your function. This can be:

v3 v2

Copy Copied

```
// Sleep until the new year
await step .sleepUntil ( "happy-new-year" , "2024-01-01" );

// Sleep until September ends
await step .sleepUntil ( "wake-me-up" , "2023-09-30T11:59:59" );

// Sleep until the end of the this week
const date = dayjs () .endOf ( "week" ) .toDate ();
await step .sleepUntil ( "wait-for-end-of-the-week" , date);

// Sleep until tea time in London
const teaTime = Temporal . ZonedDateTime .from ( "2025-05-01T16:00:00+01:00[Europe/London]" );
await step .sleepUntil ( "british-tea-time" , teaTime);

// Sleep until the end of the day
const now = Temporal . Now .instant ();
const endOfDay = now .round ({ smallestUnit : "day" , roundingMode : "ceil" });
await step .sleepUntil ( "done-for-today" , endOfDay);
```

`step.sleepUntil()` must be called using `await` or some other Promise handler to ensure your function sleeps correctly.