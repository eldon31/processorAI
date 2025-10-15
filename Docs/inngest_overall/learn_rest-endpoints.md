#### On this page

- [Functions in REST Endpoints](\docs\learn\rest-endpoints#functions-in-rest-endpoints)
- [Quick start](\docs\learn\rest-endpoints#quick-start)
- [How it works](\docs\learn\rest-endpoints#how-it-works)
- [Switching REST Endpoints from sync to async](\docs\learn\rest-endpoints#switching-rest-endpoints-from-sync-to-async)
- [SDK Support](\docs\learn\rest-endpoints#sdk-support)
- [Developer Preview](\docs\learn\rest-endpoints#developer-preview)
- [Limitations](\docs\learn\rest-endpoints#limitations)
- [Roadmap](\docs\learn\rest-endpoints#roadmap)
- [Coming soon](\docs\learn\rest-endpoints#coming-soon)
- [Roadmap](\docs\learn\rest-endpoints#roadmap-2)

Features [Inngest Functions](\docs\features\inngest-functions)

# Functions in REST Endpoints

The latest versions of Inngest SDKs allow you to use steps directly within REST endpoints, allowing you to build resumable, durable workflows in any existing endpoint, triggered by your users.

REST Endpoint support is currently in developer preview. Some details including APIs are still subject to change during this period. Read more about the [developer preview here](\docs\learn\rest-endpoints#developer-preview) .

[SDK Support](\docs\learn\rest-endpoints#sdk-support) is currently being worked on, including all common frameworks.

REST Endpoint support allows you to:

- Build APIs with full observability and tracing support
- Quickly build complex durable workflows
- Work in your existing codebase, without learning new systems
- Deploy anywhere your code currently runs
- Execute functions with low latency

## [Quick start](\docs\learn\rest-endpoints#quick-start)

In order to start using steps within your API endpoints, you must first set up middleware to intercept HTTP requests.

Go

Copy Copied

```
import (
"context"

"github.com/inngest/inngestgo/step"
"github.com/inngest/inngestgo/stephttp"
)

func setuphttp () {
// provider adds inngest support to http handlers
provider := stephttp. Setup (stephttp.SetupOpts{
Domain: "api.example.com" , // add your api domain here.
})

// provider allows you to wrap individual http handlers via `provider.servehttp`,
// and provides stdlib-compatible middleware via `provider.middleware`
http. HandleFunc ( "/users" , provider. ServeHTTP (handleUsers))

// or, via middleware with, for example, chi:
r := chi. NewRouter ()
r. Use (provider.Middleware)
r. Get ( "/users" , handleUsers)
}
```

Once you've added the middleware, you can configure functions and execute steps within REST endpoints directly:

Copy Copied

```
import (
"context"

"github.com/inngest/inngestgo/step"
"github.com/inngest/inngestgo/stephttp"
)

func handleUsers (w http.ResponseWriter, r * http.Request) {
ctx := r. Context ()

stephttp. Configure (ctx, stephttp.FnOpts{
// Configure the function ID, removing IDs from the URL:
ID: "/users/{id}"
})

// Step 1: Authenticate (with full observability)
auth, err := step. Run (ctx, "authenticate" , func (ctx context.Context) ( * AuthResult, error ) {
// You can chain steps as usual...
return nil , nil
})
if err != nil {
http. Error (w, "Authentication failed" , http.StatusUnauthorized)
return
}
// ...
}
```

## [How it works](\docs\learn\rest-endpoints#how-it-works)

REST Support works by applying middleware that tracks each HTTP request to your API endpoints.  This is the lifecycle of a REST API:

1. Set up the Inngest request manager, which tracks runs of functions
2. Execute the REST Endpoint as usual
3. Track all steps, such as `step.run`
4. If the function finishes, send the step information, input, and output to Inngest for observability
5. If a step errors or any async step is used (eg. `step.waitForEvent` ), send the step information to Inngest and switch the API endpoint from sync to async.
    - Issue a redirect (which awaits the function's results) or custom HTTP response on async switching.

### [Switching REST Endpoints from sync to async](\docs\learn\rest-endpoints#switching-rest-endpoints-from-sync-to-async)

When a step errors, or you use an async step (such as `step.sleep` or `step.waitForEvent` ), Inngest must resume your API endpoint at some point in the future.  This means

that your REST endpoint switches from being synchronous (sync) to asynchronous (finishing in the background).

To handle this, Inngest provides two ways for you to switch to background execution of your API endpoints, automatically without extra code:

1. *Redirection* : By default, we redirect the caller of the API to an endpoint that blocks and waits for the function result. This is seamless, and works across all REST methods
2. *Custom repsonse* : For each function you can override the async response handler to write any response to your users

## [SDK Support](\docs\learn\rest-endpoints#sdk-support)

Steps in REST Endpoints is currently supported in the following SDKs:

| SDK        | Support     | Version    |
|------------|-------------|------------|
| TypeScript | In Progress | -          |
| Golang     | ✅          | >= v0.14.0 |
| Python     | In progress | -          |

## [Developer Preview](\docs\learn\rest-endpoints#developer-preview)

REST Endpoint support is available as a developer preview. During this period:

- This feature is **widely available** for all Inngest accounts.
- Some details including APIs and SDKs are subject to change based on user feedback.
- As we improve support for steps in REST endpoints, some unknown issues may be uncovered during the preview

Read the [release phases](\docs\release-phases) for more details.

## [Limitations](\docs\learn\rest-endpoints#limitations)

Because REST endpoints are initialized by your own users instead of Inngest, there are several key considerations and differences to know:

- [Flow control](\docs\guides\flow-control) is not available (See "Coming soon")
- Redirects currently wait for up to 5 minutes for the function to finish in the background

## [Roadmap](\docs\learn\rest-endpoints#roadmap)

REST Endpoint support is rapidly being improved, with full support of Inngest planned:

### [Coming soon](\docs\learn\rest-endpoints#coming-soon)

- Full flow control support
- End-to-end encryption across REST-based functions
- Wider support for GraphQL

### [Roadmap](\docs\learn\rest-endpoints#roadmap-2)

- `step.defer` , for executing small steps in the background once results have been sent to users