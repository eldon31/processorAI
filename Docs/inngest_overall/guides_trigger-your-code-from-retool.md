#### On this page

- [Trigger your code from Retool](\docs\guides\trigger-your-code-from-retool#trigger-your-code-from-retool)
- [The problem](\docs\guides\trigger-your-code-from-retool#the-problem)
- [The plan](\docs\guides\trigger-your-code-from-retool#the-plan)
- [Sending an event from Retool](\docs\guides\trigger-your-code-from-retool#sending-an-event-from-retool)
- [Writing our Inngest function](\docs\guides\trigger-your-code-from-retool#writing-our-inngest-function)
- [Serving our function](\docs\guides\trigger-your-code-from-retool#serving-our-function)
- [Deploying your function](\docs\guides\trigger-your-code-from-retool#deploying-your-function)
- [Bringing it all together](\docs\guides\trigger-your-code-from-retool#bringing-it-all-together)
- [Over to you](\docs\guides\trigger-your-code-from-retool#over-to-you)

Features [Inngest Functions](\docs\features\inngest-functions) [Steps &amp; Workflows](\docs\features\inngest-functions\steps-workflows)

# Trigger your code from Retool

Internal tools are a pain to build and maintain. Fortunately, [Retool](https://retool.com/) has helped tons of companies reduce the burden. Retool primarily focuses on building dashboards and forms and it integrates well with several databases and cloud APIs.

Often though, there are actions that your support or customer success team needs to perform that are too complex for Retool built-in features. You may have even written some of necessary code in your application, but you can't easily run it from Retool.

## [The problem](\docs\guides\trigger-your-code-from-retool#the-problem)

Let's say you have an integration built in your application and you backend code imports a bunch of data from that third party. The third party API or your backend may have went down for a few hours and you may have missing data for certain user. When someone reaches out to support, you may need to re-run that import script to backfill the missing data.

We're going to walk through how you can do this so your team can trigger important scripts right from your Retool app. This guide assumes you have a basic experience building forms with Retool ( *If you don't, check out* [*this great guide*](https://docs.retool.com/docs/create-forms-using-form-component) ).

## [The plan](\docs\guides\trigger-your-code-from-retool#the-plan)

The goal is to enable your team to trigger a script anytime they click a button in Retool. To achieve this we will:

1. Create a Retool button that sends an event to Inngest
2. Write an Inngest function that uses our existing script
3. Configure that function to run when our event is received
4. See how it works end to end

## [Sending an event from Retool](\docs\guides\trigger-your-code-from-retool#sending-an-event-from-retool)

To send data from Retool, we'll need to set up a " [Resource](https://docs.retool.com/docs/resources) " first. On your Resources tab in Retool, click "Create New" then select "Resource." Then select "Rest API." Now jump over to the Inngest Cloud dashboard and [create a new Event Key in the Inngest dashboard](\docs\events\creating-an-event-key) . Copy your brand new key and in the Retool dashboard, prefix your key with the Inngest Event API URL and path: `https://inn.gs/e/`

Copy Copied

```
https://inn.gs/e/<INNGEST-EVENT-KEY>
```

Your new resource will look like this. When it does, click "Create resource."

Inngest Retool resource screenshot

<!-- image -->

Now, let's head to the Retool app that you want to add the button form to. Let's say you have already built out the following form called `runBackfillForm` with a single input called `userId` and a submit button:

Retool form screenshot

<!-- image -->

Next, create a new "Resource query" from the "Code" panel at the bottom left (use the + button). Let's name our new query `sendBackfillRequested` and select our new "Inngest" resource from the drop down. Update the "Action type" to a `POST` request. In the "Body" section, we need add the data that we want to send to Inngest. Inngest events require a name and some data as JSON. It's useful to prefix your event names to group them, here we'll call our event `"retool/backfill.requested"` and we'll pass the user id from the form and for future auditing purposes, the email of the current Retool user on your team:

Copy Copied

```
{ "user_id" : "{{runBackfillForm.data.userId}}" , "agent_id" : "{{current_user.email}}" }
```

At the end, your resource query will look like this. Let's save it then click "Run" to test it.

Retool resource query screenshot

<!-- image -->

In the Inngest Cloud dashboard's "Events" tab, you should see a brand new `retool/backfill.requested` event. Click on the event and you should be able to select the payload that we just sent.

Inngest Cloud dashboard view event payload

<!-- image -->

Now that we've verified the data is sent over to Inngest, you can attach the resource query as an event handler to the submit button. Select the "Default" interaction type and click "+ Add" to select our resource query `sendBackfillRequested` . For fun, you can add an `isFetching` to show loading.

Retool form submit button event handler

<!-- image -->

We're halfway there - with this in place any agent from our team can trigger this event as needed.

## [Writing our Inngest function](\docs\guides\trigger-your-code-from-retool#writing-our-inngest-function)

Using [the Inngest SDK](\features\sdk?ref=retool-guide) you can define your Inngest function and it's event trigger in one file. We'll create a directory called `inngest` in our project root:

Copy Copied

```
mkdir -p inngest
```

Now we'll create a file in this directory for our function - `runBackfillForUser.js` . This will be our Inngest function which will import our existing backfill code, use the `user_id` from the event payload to run that code, and return a http status code in our response to tell Inngest [if it should be retried or not](\docs\functions\retries?ref=retool-guide) .

runBackfillForUser.ts client.ts

Copy Copied

```
import { runBackfillForUser } from "../lib/backfill-scripts" ;
import { inngest } from "./client" ;

export default inngest .createFunction (
{ id : "run-backfill-for-user" } , // The name displayed in the Inngest dashboard
{ event : "retool/backfill.requested" } , // The event triggger
async ({ event }) => {
const result = await runBackfillForUser ( event . data .user_id);

return {
status : result .ok ? 200 : 500 ,
message : `Ran backfill for user ${ event . data .user_id } ` ,
};
}
);
```

That's our function - now, we just need to serve our function.

### [Serving our function](\docs\guides\trigger-your-code-from-retool#serving-our-function)

You need to serve your function to enable Inngest to remotely and securely invoke your function via HTTP.

For this guide, we'll explain how to do this with an existing [Express.js](https://expressjs.com/) application. Inngest's default [`serve()`](\docs\reference\serve) handler can be imported and passed to Express.js' `app.use` or `router.use` . You can get your Inngest signing key from [the Inngest dashboard](https://app.inngest.com/env/production/manage/signing-key) .

Copy Copied

```
import { serve } from "inngest/express"
import runBackfillForUser from "../inngest/runBackfillForUser"

app .use ( "/api/inngest" , serve ( "My API" , process . env . INNGEST_SIGNING_KEY , [
runBackfillForUser ,
]))
// your existing routes...
app .get ( "/api/whatever" , ... )
app .post ( "/api/something_else" , ... )
```

## [Deploying your function](\docs\guides\trigger-your-code-from-retool#deploying-your-function)

By serving your functions via HTTP, you don't need to deploy your code to Inngest Cloud or set up a new deployment process. After you deploy your code, you need to visit the Inngest dashboard to sync your app. This allows Inngest to discover and remotely execute your functions.

👉 You can read how to do this in [our Working with apps guide](\docs\apps\cloud) .

After syncing your app, your new function should appear in the Functions tab of the Inngest Cloud dashboard:

Inngest Cloud dashboard view deployed function

<!-- image -->

## [Bringing it all together](\docs\guides\trigger-your-code-from-retool#bringing-it-all-together)

Now that our code is pushed to production and we've set the secrets that we need, let's test it end to end.

Retool submit form

<!-- image -->

And a few seconds later in the Inngest cloud dashboard:

Inngest cloud dashboard view function output

<!-- image -->

Fantastic. We've now used our Retool form to trigger a backfill script on-demand with no infrastructure required to setup. Every time your support team needs to trigger this script, they can do it and ensure your users are happy.

## [Over to you](\docs\guides\trigger-your-code-from-retool#over-to-you)

You now know how to get some existing code from your application shipped to Inngest and triggered right from Retool with a full audit trail of who triggered it, for what user and full logs. There was no need to set up a more complex infrastructure with a queue or new endpoint on your production API - Just push your code to Inngest and send an event from Retool - done and dusted.