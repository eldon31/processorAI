#### On this page

- [Managing concurrency](\docs\functions\concurrency#managing-concurrency)
- [Configuration](\docs\functions\concurrency#configuration)

References [TypeScript SDK](\docs\reference\typescript)

# Managing concurrency

Limit the number of concurrently running steps for your function with the [`concurrency`](\docs\reference\functions\create#configuration) configuration options. Setting an optional `key` parameter limits the concurrency for each unique value of the expression.

[Read our concurrency guide for more information on concurrency, including how it works and any limits](\docs\guides\concurrency) .

Simple Multiple keys

Copy Copied

```
export default inngest .createFunction (
{
id : "sync-contacts" ,
concurrency : {
limit : 10 ,
} ,
}
// ...
);
```

Setting `concurrency` limits are very useful for:

- Handling API rate limits - Limit concurrency to stay within the rate limit quotas that are allowed by a given third party API.
- Limiting database operations or connections
- Preventing one of your user's accounts from consuming too many resources (see `key` )

Alternatively, if you want to limit the number of times that your function runs in a given period, [the](\docs\reference\functions\rate-limit) [`rateLimit`](\docs\reference\functions\rate-limit) [option](\docs\reference\functions\rate-limit) may be better for your use case.

## [Configuration](\docs\functions\concurrency#configuration)

- Name `concurrency` Type number | object | [object, object] Required optional Description Options to configure concurrency. Specifying a `number` is a shorthand to set the `limit` property. Properties

The current concurrency option controls the number of concurrent *steps* that can be running at any one time.

Because a single function run can contain multiple steps, it's possible that more functions than the concurrency limit are triggered, but only the set number of steps will ever be running.