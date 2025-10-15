#### On this page

- [Fan-out (one-to-many)](\docs\guides\fan-out-jobs#fan-out-one-to-many)
- [How to fan-out to multiple functions](\docs\guides\fan-out-jobs#how-to-fan-out-to-multiple-functions)
- [Further reading](\docs\guides\fan-out-jobs#further-reading)

Features [Events &amp; Triggers](\docs\features\events-triggers)

# Fan-out (one-to-many)

The fan-out pattern enables you to send a single event and trigger multiple functions in parallel (one-to-many). The key benefits of this approach are:

- **Reliability** : Logic from each function runs independently, meaning an issue with one function will not affect the other(s).
- **Performance** : As functions area run in parallel, all of the work will execute faster than running in sequence.

A use case for fan-out is, for example, when a user signs up for your product. In this scenario, you may want to:

1. Send a welcome email
2. Start a trial in Stripe
3. Add the user to your CRM
4. Add the user's email to your mailing list

The fan-out pattern is also useful in distributed systems where a single event is consumed by functions running in different applications.

## [How to fan-out to multiple functions](\docs\guides\fan-out-jobs#how-to-fan-out-to-multiple-functions)

TypeScript Go Python

Since Inngest is powered by events, implementing fan-out is as straightforward as defining multiple functions that use the same event trigger. Let's take the above example of user signup and implement it in Inngest.

First, set up a `/signup` route handler to send an event to Inngest when a user signs up:

### app/routes/signup/route.ts

Copy Copied

```
import { inngest } from '../inngest/client' ;

export async function POST (request : Request ) {
// NOTE - this code is simplified for the of the example:
const { email , password } = await request .json ();
const user = await createUser ({ email , password });
await createSession ( user .id);

// Send an event to Inngest
await inngest .send ({
name : 'app/user.signup' ,
data : {
user : {
id : user .id ,
email : user .email ,
} ,
} ,
});

redirect ( 'https://myapp.com/dashboard' );
}
```

Now, with this event, any function using `"app/user.signup"` as its event trigger will be automatically invoked.

Next, define two functions: `sendWelcomeEmail` and `startStripeTrial` . As you can see below, both functions use the same event trigger, but perform different work.

### inngest/functions.ts

Copy Copied

```
const sendWelcomeEmail = inngest .createFunction (
{ id : 'send-welcome-email' } ,
{ event : 'app/user.signup' } ,
async ({ event , step }) => {
await step .run ( 'send-email' , async () => {
await sendEmail ({ email : event . data . user .email , template : 'welcome' );
});
}
)

const startStripeTrial = inngest .createFunction (
{ id : 'start-stripe-trial' } ,
{ event : 'app/user.signup' } ,
async ({ event }) => {
const customer = await step .run ( 'create-customer' , async () => {
return await stripe . customers .create ({ email : event . data . user .email });
});
await step .run ( 'create-subscription' , async () => {
return await stripe . subscriptions .create ({
customer : customer .id ,
items : [{ price : 'price_1MowQULkdIwHu7ixraBm864M' }] ,
trial_period_days : 14 ,
});
});
}
)
```

You've now successfully implemented fan-out in our application. Each function will run independently and in parallel. If one function fails, the others will not be disrupted.

Other benefits of fan-out include:

- **Bulk Replay** : If a third-party API goes down for a period of time (for example, your email provider), you can use [Replay](\docs\platform\replay) to selectively re-run all functions that failed, without having to re-run all sign-up flow functions.
- **Testing** : Each function can be tested in isolation, without having to run the entire sign-up flow.
- **New features or refactors** : As each function is independent, you can add new functions or refactor existing ones without having to edit unrelated code.
- **Trigger functions in different codebases** : If you have multiple codebases, even using different programming languages (for example [Python](\docs\reference\python) or [Go](https://pkg.go.dev/github.com/inngest/inngestgo) ), you can trigger functions in both codebases from a single event.

## [Further reading](\docs\guides\fan-out-jobs#further-reading)

- [Sending events](\docs\events)
- [Invoking functions from within functions](\docs\guides\invoking-functions-directly)
- [Sending events from functions](\docs\guides\sending-events-from-functions)