#### On this page

- [Writing expressions](\docs\guides\writing-expressions#writing-expressions)
- [Types of Expressions](\docs\guides\writing-expressions#types-of-expressions)
- [Variables](\docs\guides\writing-expressions#variables)
- [Examples](\docs\guides\writing-expressions#examples)
- [Boolean Expressions](\docs\guides\writing-expressions#boolean-expressions)
- [Value Expressions](\docs\guides\writing-expressions#value-expressions)
- [Tips](\docs\guides\writing-expressions#tips)
- [Testing out expressions](\docs\guides\writing-expressions#testing-out-expressions)

Features [Events &amp; Triggers](\docs\features\events-triggers)

# Writing expressions

Expressions are used in a number of ways for configuring your functions. They are used for:

- Defining keys based on event properties for [concurrency](\docs\functions\concurrency) , [rate limiting](\docs\reference\functions\rate-limit) , [debounce](\docs\reference\functions\debounce) , or [idempotency](\docs\guides\handling-idempotency)
- Conditionally matching events for [wait for event](\docs\reference\functions\step-wait-for-event) , [cancellation](\docs\guides\cancel-running-functions) , or the [function trigger's](\docs\reference\functions\create#trigger) [`if`](\docs\reference\functions\create#trigger) [option](\docs\reference\functions\create#trigger)
- Returning values for function [run priority](\docs\reference\functions\run-priority)

All expressions are defined using the [Common Expression Language (CEL)](https://github.com/google/cel-go) . CEL offers simple, fast, non-turing complete expressions. It allows Inngest to evaluate millions of expressions for all users at scale.

## [Types of Expressions](\docs\guides\writing-expressions#types-of-expressions)

Within the scope of Inngest, expressions should evaluate to either a boolean or a value:

- **Booleans** - Any expression used for conditional matching should return a boolean value. These are used in wait for event, cancellation, and the function trigger's `if` option.
- **Values** - Other expressions can return any value which might be used as keys (for example, concurrency, rate limit, debounce or [idempotency keys](\docs\guides\handling-idempotency) ) or a dynamic value (for example, run priority).

## [Variables](\docs\guides\writing-expressions#variables)

- `event` refers to the event that triggered the function run, in every case.
- `async` refers to a new event in `step.waitForEvent` and [cancellation](\docs\guides\cancel-running-functions) . It's the incoming event which is matched asynchronously. This is only present when matching new events in a function run.

## [Examples](\docs\guides\writing-expressions#examples)

Most expressions are given the `event` payload object as the input. Expressions that match additional events (for example, wait for event, cancellation) will also have the `async` object for the matched event payload. To learn more, consult this [reference of all the operators available in CEL](https://github.com/google/cel-spec/blob/master/doc/langdef.md#list-of-standard-definitions) .

### [Boolean Expressions](\docs\guides\writing-expressions#boolean-expressions)

Copy Copied

```
// Match a field to a string
"event.data.billingPlan == 'enterprise'"

// Number comparison
"event.data.amount > 1000"

// Combining multiple conditions
"event.data.billingPlan == 'enterprise' && event.data.amount > 1000"
"event.data.billingPlan != 'pro' || event.data.amount < 300"

// Compare the function trigger with an inbound event (for wait for event or cancellation)
"event.data.userId == async.data.userId"

// Alternatively, you can use JavaScript string interpolation for wait for event
` ${ userId } == async.data.userId` // => "user_1234 == async.data.userId"
```

### [Value Expressions](\docs\guides\writing-expressions#value-expressions)

### [Keys](\docs\guides\writing-expressions#keys)

Copy Copied

```
// Use the user's id as a concurrency key
"event.data.id" // => "1234"

// Concatenate two strings together to create a unique key
`event.data.userId + "-" + event.type` // => "user_1234-signup"
```

### [Dynamic Values](\docs\guides\writing-expressions#dynamic-values)

Copy Copied

```
// Return a 0 priority if the billing plan is enterprise, otherwise return 1800
`event.data.billingPlan == 'enterprise' ? 0 : 1800`

// Return a value based on multiple conditions
`event.data.billingPlan == 'enterprise' && event.data.requestNumber < 10 ? 0 : 1800`
```

## [Tips](\docs\guides\writing-expressions#tips)

- Use `+` to concatenate strings
- Use `==` for equality checks
- You can use single `'` or double quotes `"` for strings, but we recommend sticking with one for code consistency
- When working with the TypeScript SDK, write expressions within backticks ``` to use quotes in your expression or use JavaScript's string interpolation.
- Use ternary operators to return default values
- When using the or operator ( `||` ), CEL will always return a boolean. This is different from JavaScript, where the or operator returns the value of the statement left of the operator if truthy. Use the ternary operator ( `?` ) instead of `||` for conditional returns.

Please note that while CEL supports a wide range of helpers and macros, Inngest only supports a subset of these to ensure a high level of performance and reliability.

## [Testing out expressions](\docs\guides\writing-expressions#testing-out-expressions)

You can test out expressions on [Undistro's CEL Playground](https://playcel.undistro.io/) . It's a great way to quickly test out more complex expressions, especially with conditional returns.