#### On this page

- [ESLint Plugin](\docs\sdk\eslint#es-lint-plugin)
- [Getting started](\docs\sdk\eslint#getting-started)
- [Rules](\docs\sdk\eslint#rules)
- [@inngest/await-inngest-send](\docs\sdk\eslint#inngest-await-inngest-send)
- [@inngest/no-nested-steps](\docs\sdk\eslint#inngest-no-nested-steps)
- [@inngest/no-variable-mutation-in-step](\docs\sdk\eslint#inngest-no-variable-mutation-in-step)

References [TypeScript SDK](\docs\reference\typescript) [Using the SDK](\docs\sdk\environment-variables)

# ESLint Plugin

An ESLint plugin is available at [@inngest/eslint-plugin](https://www.npmjs.com/package/@inngest/eslint-plugin) , providing rules to enforce best practices when writing Inngest functions.

## [Getting started](\docs\sdk\eslint#getting-started)

Install the package using whichever package manager you'd prefer as a [dev dependency](https://docs.npmjs.com/cli/v10/configuring-npm/package-json#devdependencies) .

Copy Copied

```
npm install -D @inngest/eslint-plugin
```

Add the plugin to your ESLint configuration file with the recommended config.

Copy Copied

```
{
"plugins" : [ "@inngest" ] ,
"extends" : [ "plugin:@inngest/recommended" ]
}
```

You can also manually configure each rule instead of using the `plugin:@inngest/recommend` config.

Copy Copied

```
{
"plugins" : [ "@inngest" ] ,
"rules" : {
"@inngest/await-inngest-send" : "warn"
}
}
```

See below for a list of all rules available to configure.

## [Rules](\docs\sdk\eslint#rules)

- [@inngest/await-inngest-send](\docs\sdk\eslint#inngest-await-inngest-send)
- [@inngest/no-nested-steps](\docs\sdk\eslint#inngest-no-nested-steps)
- [@inngest/no-variable-mutation-in-step](\docs\sdk\eslint#inngest-no-variable-mutation-in-step)

### [@inngest/await-inngest-send](\docs\sdk\eslint#inngest-await-inngest-send)

You should use `await` or `return` before `inngest.send().

Copy Copied

```
"@inngest/await-inngest-send" : "warn" // recommended
```

In serverless environments, it's common that runtimes are forcibly killed once a request handler has resolved, meaning any pending promises that are not performed before that handler ends may be cancelled.

Copy Copied

```
// ❌ Bad
inngest .send ({ name : "some.event" });
```

Copy Copied

```
// ✅ Good
await inngest .send ({ name : "some.event" });
```

### [When not to use it](\docs\sdk\eslint#when-not-to-use-it)

There are cases where you have deeper control of the runtime or when you'll safely `await` the send at a later time, in which case it's okay to turn this rule off.

### [@inngest/no-nested-steps](\docs\sdk\eslint#inngest-no-nested-steps)

Use of `step.*` within a `step.run()` function is not allowed.

Copy Copied

```
"@inngest/no-nested-steps" : "error" // recommended
```

Nesting `step.run()` calls is not supported and will result in an error at runtime. If your steps are nested, they're probably reliant on each other in some way. If this is the case, extract them into a separate function that runs them in sequence instead.

Copy Copied

```
// ❌ Bad
await step .run ( "a" , async () => {
const someValue = "..." ;
await step .run ( "b" , () => {
return use (someValue);
});
});
```

Copy Copied

```
// ✅ Good
const aThenB = async () => {
const someValue = await step .run ( "a" , async () => {
return "..." ;
});

return step .run ( "b" , async () => {
return use (someValue);
});
};

await aThenB ();
```

### [@inngest/no-variable-mutation-in-step](\docs\sdk\eslint#inngest-no-variable-mutation-in-step)

Do not mutate variables inside `step.run()` , return the result instead.

Copy Copied

```
"@inngest/no-variable-mutation-in-step" : "error" // recommended
```

Inngest executes your function multiple times over the course of a single run, memoizing state as it goes. This means that code within calls to `step.run()` is not called on every execution.

This can be confusing if you're using steps to update variables within the function's closure, like so:

Copy Copied

```
// ❌ Bad
// THIS IS WRONG!  step.run only runs once and is skipped for future
// steps, so userID will not be defined.
let userId;

// Do NOT do this!  Instead, return data from step.run.
await step .run ( "get-user" , async () => {
userId = await getRandomUserId ();
});

console .log (userId); // undefined
```

Instead, make sure that any variables needed for the overall function are *returned* from calls to `step.run()` .

Copy Copied

```
// ✅ Good
// This is the right way to set variables within step.run :)
const userId = await step .run ( "get-user" , () => getRandomUserId ());

console .log (userId); // 123
```