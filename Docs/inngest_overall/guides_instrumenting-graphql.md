#### On this page

- [Instrumenting GraphQL](\docs\guides\instrumenting-graphql#instrumenting-graph-ql)
- [Getting Started](\docs\guides\instrumenting-graphql#getting-started)
- [Usage example](\docs\guides\instrumenting-graphql#usage-example)
- [Output events](\docs\guides\instrumenting-graphql#output-events)
- [Reacting to events](\docs\guides\instrumenting-graphql#reacting-to-events)

# Instrumenting GraphQL

When building with GraphQL, you can give your event-driven application a kick-start by instrumenting every query and mutation, sending events when one is successfully executed.

We can do this using an [Envelop](https://envelop.dev/) plugin, `useInngest` , for [GraphQL Yoga](https://the-guild.dev/graphql/yoga-server) and servers or frameworks powered by Yoga, such as [RedwoodJS](https://www.redwoodjs.com/) .

By instrumenting with the `useInngest` plugin:

- Get an immediate set of events to react to that automatically grows with your GraphQL API.
- No changes to your existing resolvers are ever needed.
- Utilise fine-grained control over what events are sent such as operations (queries, mutations, or subscriptions), introspection events, when GraphQL errors occur, if result data should be included, type and schema coordinate denylists, and more.
- Automatically capture context such as user data.

## [Getting Started](\docs\guides\instrumenting-graphql#getting-started)

Copy Copied

```
npm install envelop-plugin-inngest # or yarn add
```

### [Usage example](\docs\guides\instrumenting-graphql#usage-example)

Using `useInngest` just requires that you have an Inngest client (see the [Quick start](\docs\getting-started\nextjs-quick-start) ) set up with an appropriate event key (see [Creating an event key](https://www.inngest.com/docs/events/creating-an-event-key) ).

Here's a single-file example of how to add the plugin.

Copy Copied

```
import { useInngest } from "envelop-plugin-inngest" ;
import { createSchema , createYoga } from "graphql-yoga" ;
import { Inngest } from "inngest" ;

const inngest = new Inngest ({ id : "my-app" });

// Provide your schema
const yoga = createYoga ({
schema : createSchema ({
typeDefs : /* GraphQL */ `
type Query {
greetings: String!
}
` ,
resolvers : {
Query : {
greetings : () => "Hello World!" ,
} ,
} ,
}) ,

// Add the plugin to the server. RedwoodJS users can use the
// `extraPlugins` option instead.
plugins : [ useInngest ({ inngestClient : inngest })] ,
});

// Start the server and explore http://localhost:4000/graphql
const server = createServer (yoga);

server .listen ( 4000 , () => {
console .info ( "Server is running on http://localhost:4000/graphql" );
});
```

### [Output events](\docs\guides\instrumenting-graphql#output-events)

Once the plugin is installed, an event will be sent for all successful GraphQL operations, resulting in a ready-to-use set of events that you can react to immediately.

Here's an example event sent from a mutation to create a new item in a user's cart:

Copy Copied

```
{
"name" : "graphql/create-cart-item.mutation" ,
"data" : {
"identifiers" : [
{
"id" : 27 ,
"typename" : "CartItem"
}
] ,
"operation" : {
"id" : "create-cart-item" ,
"name" : "CreateCartItem" ,
"type" : "mutation"
} ,
"result" : {
"data" : {
"createCartItem" : {
"id" : 27 ,
"productId" : "123"
}
}
} ,
"types" : [
"CartItem"
] ,
"variables" : {}
} ,
"id" : "01GXXAQ1M0A1SFVGEHACRF4K1C"
}
```

### [Reacting to events](\docs\guides\instrumenting-graphql#reacting-to-events)

We can react to this event by creating a new Inngest function with the event as the trigger.

Copy Copied

```
inngest .createFunction (
{ id : "send-cart-alert" } ,
{ event : "graphql/create-cart-item.mutation" } ,
async ({ event }) => {
await sendSlackMessage (
"#marketing" ,
`Someone added product # ${ event . data .identifiers[ 0 ].id } to their cart!`
);
}
);
```

For more info on how to customize the events sent check out the [envelop-plugin-inngest](https://github.com/inngest/envelop-plugin-inngest) repository, or see [Writing functions](https://www.inngest.com/docs/functions) to learn how to react to these events in different ways.