#### On this page

- [Vercel](\docs\deploy\vercel#vercel)
- [Hosting Inngest functions on Vercel](\docs\deploy\vercel#hosting-inngest-functions-on-vercel)
- [Choose the Next.js App Router or Pages Router:](\docs\deploy\vercel#choose-the-next-js-app-router-or-pages-router)
- [Deploying to Vercel](\docs\deploy\vercel#deploying-to-vercel)
- [Bypassing Deployment Protection](\docs\deploy\vercel#bypassing-deployment-protection)
- [Configure protection bypass](\docs\deploy\vercel#configure-protection-bypass)
- [Multiple apps in one single Vercel project](\docs\deploy\vercel#multiple-apps-in-one-single-vercel-project)
- [Manually syncing apps](\docs\deploy\vercel#manually-syncing-apps)

Platform [Deployment](\docs\platform\deployment) [Cloud Providers](\docs\deploy\vercel)

# Vercel

Inngest enables you to host your functions on Vercel using their [serverless functions platform](https://vercel.com/docs/concepts/functions/serverless-functions) . This allows you to deploy your Inngest functions right alongside your existing website and API functions running on Vercel.

Inngest will call your functions securely via HTTP request on-demand, whether triggered by an event or on a schedule in the case of cron jobs.

## [Hosting Inngest functions on Vercel](\docs\deploy\vercel#hosting-inngest-functions-on-vercel)

After you've written your functions using [Next.js](\docs\learn\serving-inngest-functions?ref=docs-deploy-vercel#framework-next-js) or Vercel's [Express-like](\docs\learn\serving-inngest-functions?ref=docs-deploy-vercel#framework-express) functions within your project, you need to serve them via the `serve` handler. Using the `serve` handler, create a Vercel/Next.js function at the `/api/inngest` endpoint. Here's an example in a Next.js app:

## [Choose the Next.js App Router or Pages Router:](\docs\deploy\vercel#choose-the-next-js-app-router-or-pages-router)

Next.js - App Router Next.js - Pages Router

Copy Copied

```
import { serve } from "inngest/next" ;
import { client } from "../../inngest/client" ;
import { firstFunction , anotherFunction } from "../../inngest/functions" ;

export const { GET , POST , PUT } = serve ({
client : client ,
functions : [
firstFunction ,
anotherFunction
]
});
```

## [Deploying to Vercel](\docs\deploy\vercel#deploying-to-vercel)

Installing [Inngest's official Vercel integration](https://vercel.com/integrations/inngest) does 3 things:

1. Automatically sets the required [`INNGEST_SIGNING_KEY`](\docs\sdk\environment-variables#inngest-signing-key) environment variable to securely communicate with Inngest's API ( [docs](\docs\platform\signing-keys) ).
2. Automatically sets the [`INNGEST_EVENT_KEY`](\docs\sdk\environment-variables#inngest-event-key) environment variable to enable your application to send events ( [docs](\docs\events\creating-an-event-key) ).
3. Automatically syncs your app to Inngest every time you deploy updated code to Vercel - no need to change your existing workflow!

[Install the Inngest Vercel integration](https://app.inngest.com/settings/integrations/vercel/connect)

To enable communication between Inngest and your code, you need to either [disable Deployment Protection](https://vercel.com/docs/security/deployment-protection#configuring-deployment-protection) or, if you're on Vercel's Pro plan, configure protection bypass:

## [Bypassing Deployment Protection](\docs\deploy\vercel#bypassing-deployment-protection)

If you have Vercel's [Deployment Protection feature](https://vercel.com/docs/security/deployment-protection) enabled, *by default* , Inngest may not be able to communicate with your application. This may depend on what configuration you have set:

- **"Standard protection"** or **"All deployments"** - This affects Inngest production and [branch environments](\docs\platform\environments) .
- **"Only preview deployments"** - This affects [branch environments](\docs\platform\environments) .

To work around this, you can either:

1. Disable deployment protection
2. Configure protection bypass ( *Protection bypass may or may not be available depending on your pricing plan* )

### [Configure protection bypass](\docs\deploy\vercel#configure-protection-bypass)

To enable this, you will need to leverage Vercel's " [Protection Bypass for Automation](https://vercel.com/docs/deployment-protection/methods-to-bypass-deployment-protection/protection-bypass-automation) " feature. Here's how to set it up:

1. Enable "Protection Bypass for Automation" on your Vercel project
2. Copy your secret
3. Go to [the Vercel integration settings page in the Inngest dashboard](https://app.inngest.com/settings/integrations/vercel)
4. For each project that you would like to enable this for, add the secret in the "Deployment protection key" input. Inngest will now use this parameter to communicate with your application to bypass the deployment protection.

A Vercel protection bypass secret added in the Inngest dashboard

<!-- image -->

5. Trigger a re-deploy of your preview environment(s) (this resyncs your app to Inngest)

## [Multiple apps in one single Vercel project](\docs\deploy\vercel#multiple-apps-in-one-single-vercel-project)

You can pass multiple paths by adding their path information to each Vercel project in the Vercel Integration's settings page.

Add new path information button in the Inngest dashboard

<!-- image -->

You can also add paths to separate functions within the same app for bundle size issues or for running certain functions on the edge runtime for streaming.

## [Manually syncing apps](\docs\deploy\vercel#manually-syncing-apps)

While we strongly recommend our Vercel integration, you can still use Inngest by manually telling Inngest that you've deployed updated functions. You can sync your app [via the Inngest UI](\docs\apps\cloud#sync-a-new-app-in-inngest-cloud) or [via our API with a curl request](\docs\apps\cloud#curl-command) .