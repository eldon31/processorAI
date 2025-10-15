#### On this page

- [Middleware](\docs\features\middleware#middleware)
- [Middleware SDKs support](\docs\features\middleware#middleware-sdks-support)
- [Middleware lifecycle](\docs\features\middleware#middleware-lifecycle)

Features

# Middleware

Middleware allows your code to run at various points in an Inngest client's lifecycle, such as during a function's execution or when sending an event.

This can be used for a wide range of uses:

## [Custom observability](\docs\features\middleware\create)

[Add custom logging, tracing or helpers to your Inngest Functions.](\docs\features\middleware\create)

## [Dependency Injection](\docs\features\middleware\dependency-injection)

[Provide shared client instances (ex, OpenAI) to your Inngest Functions.](\docs\features\middleware\dependency-injection)

## [Encryption Middleware](\docs\features\middleware\encryption-middleware)

[End-to-end encryption for events, step output, and function output.](\docs\features\middleware\encryption-middleware)

## [Sentry Middleware](\docs\features\middleware\sentry-middleware)

[Quickly setup Sentry for your Inngest Functions.](\docs\features\middleware\sentry-middleware)

## [Middleware SDKs support](\docs\features\middleware#middleware-sdks-support)

Middleware are available in the [TypeScript SDK](\docs\reference\middleware\typescript) v2.0.0+ and [Python SDK](\docs\reference\python\middleware\lifecycle) v0.3.0+ .

Support in the Go SDK in planned.

## [Middleware lifecycle](\docs\features\middleware#middleware-lifecycle)

Middleware can be registered at the Inngest clients or functions level.

Adding middleware contributes to an overall "stack" of middleware. If you register multiple middlewares, the SDK will group and run hooks for each middleware in the following order:

1. Middleware registered on the **client** , in descending order
2. Middleware registered on the **function** , in descending order

For example:

TypeScript Python

Copy Copied

```
const inngest = new Inngest ({
id : "my-app" ,
middleware : [
logMiddleware , // This is executed first
errorMiddleware , // This is executed second
] ,
});

inngest .createFunction (
{
id : "example" ,
middleware : [
dbSetupMiddleware , // This is executed third
datadogMiddleware , // This is executed fourth
] ,
} ,
{ event : "test" } ,
async () => {
// ...
}
);
```

Learn more about the Middleware hooks and their execution order in ["Creating a Middleware"](\docs\features\middleware\create) .