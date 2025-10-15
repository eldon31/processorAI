#### On this page

- [Sleep step.sleep()](\docs\reference\functions\step-sleep#sleep-step-sleep)
- [step.sleep(id, duration): Promise](\docs\reference\functions\step-sleep#step-sleep-id-duration-promise)

References [TypeScript SDK](\docs\reference\typescript) [Steps](\docs\reference\functions\step-run)

# Sleep step.sleep()

## [step.sleep(id, duration): Promise](\docs\reference\functions\step-sleep#step-sleep-id-duration-promise)

- Name `id` Type string Required required Description The ID of the step. This will be what appears in your function's logs and is used to memoize step state across function versions.
- Name `duration` Type number | string | Temporal.Duration Required required Description The duration of time to sleep:

v3 v2

Copy Copied

```
// Sleep for 30 minutes
const thirtyMins = Temporal . Duration .from ({ minutes : 30 });
await step .sleep ( "wait-with-temporal" , thirtyMins);

await step .sleep ( "wait-with-string" , "30m" );
await step .sleep ( "wait-with-string-alt" , "30 minutes" );
await step .sleep ( "wait-with-ms" , 30 * 60 * 1000 );
```

`step.sleep()` must be called using `await` or some other Promise handler to ensure your function sleeps correctly.