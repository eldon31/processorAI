#### On this page

- [Errors &amp; Retries](\docs\guides\error-handling#errors-and-retries)
- [Types of failure](\docs\guides\error-handling#types-of-failure)
- [Failures, Retries and Idempotency](\docs\guides\error-handling#failures-retries-and-idempotency)

Features [Inngest Functions](\docs\features\inngest-functions)

# Errors &amp; Retries

Inngest Functions are designed to handle errors or exceptions gracefully and will automatically retry after an error or exception. This adds an immediate layer of durability to your code, ensuring it survives transient issues like network timeouts, outages, or database locks.

Inngest Functions come with:

## [Automatic Retries](\docs\features\inngest-functions\error-retries\retries)

[Configurable with a custom retry policies to suit your specific use case.](\docs\features\inngest-functions\error-retries\retries)

## [Failure handlers](\docs\features\inngest-functions\error-retries\failure-handlers)

[Utilize callbacks to handle all failing retries.](\docs\features\inngest-functions\error-retries\failure-handlers)

## [Rollbacks support](\docs\features\inngest-functions\error-retries\rollbacks)

[Each step within a function can have its own retry logic and be handled individually.](\docs\features\inngest-functions\error-retries\rollbacks)

## [Types of failure](\docs\guides\error-handling#types-of-failure)

Inngest helps you handle both **errors** and **failures** , which are defined differently.

An **error** causes a step to retry. Exhausting all retry attempts will cause that step to **fail** , which means the step will never be attempted again this run.

A **failed** step can be handled with native language features such as `try` / `catch` , but unhandled errors will cause the function to **fail** , meaning the run is marked as "Failed" in the Inngest UI and all future executions are cancelled.

See how to handle step failure by [performing rollbacks](\docs\features\inngest-functions\error-retries\rollbacks) .

## [Failures, Retries and Idempotency](\docs\guides\error-handling#failures-retries-and-idempotency)

Re-running a step upon error requires its code to be idempotent, which means that running the same code multiple times won't have any side effect.

For example, a step inserting a new user to the database is not idempotent while a step [upserting a user](https://www.cockroachlabs.com/blog/sql-upsert/) is.

Learn how to write idempotent steps that can be retried safely by reading ["Handling idempotency"](\docs\guides\handling-idempotency) .