#### On this page

- [Sentry Middleware](\docs\features\middleware\sentry-middleware#sentry-middleware)
- [Installation](\docs\features\middleware\sentry-middleware#installation)

Features [Middleware](\docs\features\middleware)

# Sentry Middleware

Using the Sentry middleware is useful to:

- Capture exceptions for reporting
- Add tracing to each function run
- Include useful context for each exception and trace like function ID and event names

## [Installation](\docs\features\middleware\sentry-middleware#installation)

TypeScript (v3.0.0+) Python (v0.3.0+)

Install the [`@inngest/middleware-sentry`](https://www.npmjs.com/package/@inngest/middleware-sentry) [package](https://www.npmjs.com/package/@inngest/middleware-sentry) and configure it as follows:

Copy Copied

```
import * as Sentry from "@sentry/node" ;
import { Inngest } from "inngest" ;
import { sentryMiddleware } from "@inngest/middleware-sentry" ;

// Initialize Sentry as usual wherever is appropriate
Sentry .init ( ... );

const inngest = new Inngest ({
id : "my-app" ,
middleware : [ sentryMiddleware ()] ,
});
```

Requires inngest@&gt;=3.0.0 and @sentry/*@&gt;=8.0.0`.