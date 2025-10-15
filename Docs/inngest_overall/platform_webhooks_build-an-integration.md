#### On this page

- [Webhook intents: Building a webhook integration](\docs\platform\webhooks\build-an-integration#webhook-intents-building-a-webhook-integration)
- [What is a webhook intent?](\docs\platform\webhooks\build-an-integration#what-is-a-webhook-intent)
- [Creating a webhook intent](\docs\platform\webhooks\build-an-integration#creating-a-webhook-intent)
- [How it works](\docs\platform\webhooks\build-an-integration#how-it-works)
- [Default webhook transform](\docs\platform\webhooks\build-an-integration#default-webhook-transform)

# Webhook intents: Building a webhook integration

**Webhook intents** is a feature that enables any webhook provider to build an integration with Inngest.

## [What is a webhook intent?](\docs\platform\webhooks\build-an-integration#what-is-a-webhook-intent)

A webhook intent is a simple URL that providers can redirect their users to for Inngest users to approve and create a new webhook URL. The intent redirects the user back to the provided redirect URL with the new webhook URL as a query parameter.

## [Creating a webhook intent](\docs\platform\webhooks\build-an-integration#creating-a-webhook-intent)

The base webhook intent URL is:

Copy Copied

```
https://app.inngest.com/intent/create-webhook
```

To customize the intent, use the following query params:

- Name `name` Type string Required required Description The name of the webhook intent. This will be used to identify the webhook in the user's Inngest environment and create a slug prefix for all events received from this webhook.
- Name `redirect_uri` Type string Required required Description The URL to redirect the user back to after they approve the webhook intent. This URL will receive a `url` query param with the full URL of the webhook intent which can be stored on your end as the webhook target URL.

A full example URL would look like this:

Copy Copied

```
https://app.inngest.com/intent/create-webhook?name=AcmeApp&redirect_uri=https%3A%2F%2Fapi.example.com%2Fwebhook%2Fcallback
```

## [How it works](\docs\platform\webhooks\build-an-integration#how-it-works)

1

In your application, create a button that opens the webhook intent URL either in the same tab or in a pop up window (ex. via `window.open` ).

Example: Open in pop up window

Copy Copied

```
window .open ( "https://app.inngest.com/intent/create-webhook?name=AcmeApp&redirect_uri=https%3A%2F%2Fapi.example.com%2Fwebhook%2Fcallback" , "_blank" , "popup=true,height=640,width=680" )
```

2

The user will be sent to the intent page where they can approve the webhook intent. If they are not logged in, they will be prompted to login.

Webhook intent page

<!-- image -->

3

When approved, Inngest will create a new webhook URL with the slugified name as an event prefix and the [default transform function](\docs\platform\webhooks\build-an-integration#default-webhook-transform) will be used to transform incoming webhook payloads into [the Inngest event format](\docs\features\events-triggers\event-format) .

4

The user will be redirected back to the original application's `redirect_uri` with the new webhook URL as a query parameter ( `url` ). You can save this URL to your database and use it as the webhook target URL for your application. The user will begin seeing events from your application in Inngest immediately.

Copy Copied

```
https://api.example.com/webhook/callback?url=https%3A%2F%2Finn.gs%2Fe%2F9VFPYIh8dKJmt7ERkNytXlQEvc_WtX0YgZCErRB5qPd4OUx7t7lUyl333ynly8Mo5-OjRKZ1oWPDhWZq24Y6Qw
```

## [Default webhook transform](\docs\platform\webhooks\build-an-integration#default-webhook-transform)

Inngest webhooks support [transform functions](\docs\platform\webhooks#defining-a-transform-function) which are used to transform incoming webhook payload JSON body into [the Inngest event format](\docs\features\events-triggers\event-format) . The webhook intent creates a default transform automatically that supports the most common webhook payloads.

Copy Copied

```
function transform (evt , headers = {} , queryParams = {} , raw = "" ) {
return {
// This was created by the <Provider name> integration.
// Edit this to customize the event name and payload.
name : `<provider-name-slug>/ ${ evt .type || evt .name || evt .event_type || "webhook.received" } ` ,
data : evt .data || evt ,
};
};
```

If you're a developer and you'd like to request new functionality please [contact us](mailto:hello@inngest.com?subject=Webhook%20intent%20feature%20request) .