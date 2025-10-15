#### On this page

- [Prisma Pulse: Trigger Functions from database changes](\docs\features\events-triggers\prisma-pulse#prisma-pulse-trigger-functions-from-database-changes)
- [Setup Prisma Pulse](\docs\features\events-triggers\prisma-pulse#setup-prisma-pulse)
- [Setup and deploying the Inngest Pulse Router](\docs\features\events-triggers\prisma-pulse#setup-and-deploying-the-inngest-pulse-router)
- [Configuring the watched tables](\docs\features\events-triggers\prisma-pulse#configuring-the-watched-tables)
- [Deploying the Inngest Pulse Router](\docs\features\events-triggers\prisma-pulse#deploying-the-inngest-pulse-router)
- [Trigger a Function from a database event](\docs\features\events-triggers\prisma-pulse#trigger-a-function-from-a-database-event)

Features [Events &amp; Triggers](\docs\features\events-triggers)

# Prisma Pulse: Trigger Functions from database changes

Prisma Pulse integrates with Inngest, transforming database changes into Inngest Events.

Connecting Prisma Pulse to your database will trigger a new row in the `users` table, creating a `db/user.created` event that can trigger Inngest Functions ( *for example, a user onboarding email sequence* ).

## [Setup Prisma Pulse](\docs\features\events-triggers\prisma-pulse#setup-prisma-pulse)

Using Prisma Pulse requires some configuration changes on both your Prisma Data Platform account and database.

Please refer to the [Prisma Pulse documentation to enable it](https://www.prisma.io/docs/pulse/getting-started#1-enable-pulse-in-the-platform-console) .

## [Setup and deploying the Inngest Pulse Router](\docs\features\events-triggers\prisma-pulse#setup-and-deploying-the-inngest-pulse-router)

Once Prisma Pulse enabled on your account, you'll have to deploy a Inngest Pulse Router, responsible for translating Prisma Pulse events into

Inngest events.

The following command will generate for you the Inngest Pulse Router in your application:

Copy Copied

```
npx try-prisma -t pulse/inngest-router
```

### [Configuring the watched tables](\docs\features\events-triggers\prisma-pulse#configuring-the-watched-tables)

The list of watched tables should be configured in the `src/index.ts` file by updating the following list:

### src/index.ts

Copy Copied

```
// Here configure each prisma model to stream changes from
const PRISMA_MODELS = [ 'notification' , 'user' ];
```

### [Deploying the Inngest Pulse Router](\docs\features\events-triggers\prisma-pulse#deploying-the-inngest-pulse-router)

The Inngest Pulse Router is a Node.js program opening a websocket connection with the Prisma Pulse API.

The following environment variables are required:

- DATABASE\_URL
- [PULSE\_API\_KEY](https://www.prisma.io/docs/pulse/getting-started#14-generate-an-api-key)
- [INNGEST\_EVENT\_KEY](\docs\events\creating-an-event-key)
- [INNGEST\_SIGNING\_KEY](\docs\platform\signing-keys)

Due to its long-lived nature, the Inngest Pulse Router needs to be deployed on a Cloud Provider such as Railway.

**Using Prisma Pulse with Serverless**

The Inngest Pulse Router can also be deployed on Serverless by leveraging the [Delivery Guarantees](https://www.prisma.io/blog/prisma-pulse-introducing-delivery-guarantees-for-database-change-events) of Pulse events.

By passing a `name` to your `prisma.model.stream({ name: "inngest-router" })` , Prisma Pulse will keep track of received events and only send the new ones (since the last connection).

We can leverage this mechanism by creating a Inngest Functions trigger by a CRON schedule and running on a Serverless Function. The Inngest Function will run every 15min and collect the first 100 updates before finishing.

## [Trigger a Function from a database event](\docs\features\events-triggers\prisma-pulse#trigger-a-function-from-a-database-event)

Once your Inngest Pulse Router deployed, Inngest events matching your database changes will be triggered.

All events follow the following format: `"db/<table>.<action>"` with `<action>` part of:

- create
- update
- delete

The events sent by the Inngest Pulse Router contains the changed data, as described [in this API Reference](https://www.prisma.io/docs/pulse/api-reference#pulsecreateeventuser) .

Here is an example of a onboarding workflow followed upon each new account creation:

### app/inngest/functions.ts

Copy Copied

```
import { inngest } from "./client" ;
import { sendEmail } from "@/lib/email"

export const handleNewUser = inngest .createFunction (
{ id : "handle-new-user" } ,
{ event : "db/user.create" } ,
async ({ event , step }) => {
// This object includes the entire record that changed
const pulseEvent = event .data;

await step .run ( "send-welcome-email" , async () => {
// Send welcome email
await sendEmail ({
template : "welcome" ,
to : pulseEvent . created .email ,
});
});

await step .sleep ( "wait-before-tips" , "3d" );

await step .run ( "send-new-user-tips-email" , async () => {
// Follow up with some helpful tips
await sendEmail ({
template : "new-user-tips" ,
to : pulseEvent . created .email ,
});
});
} ,
);
```

**Best practice**

A Function run performing a database change might trigger a Prisma Pulse event that will run the Function again.

We recommend using `"db/*"` events in combination with a `if:` filter to avoid any infinite loop of Function runs triggered.