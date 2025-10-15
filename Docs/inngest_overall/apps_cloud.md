#### On this page

- [Syncing an Inngest App](\docs\apps\cloud#syncing-an-inngest-app)
- [Sync a new app in Inngest Cloud](\docs\apps\cloud#sync-a-new-app-in-inngest-cloud)
- [Manually](\docs\apps\cloud#manually)
- [Automatically using an integration](\docs\apps\cloud#automatically-using-an-integration)
- [Curl command](\docs\apps\cloud#curl-command)
- [How and when to resync an app](\docs\apps\cloud#how-and-when-to-resync-an-app)
- [When to resync Vercel apps manually](\docs\apps\cloud#when-to-resync-vercel-apps-manually)
- [How to resync manually](\docs\apps\cloud#how-to-resync-manually)
- [Troubleshooting](\docs\apps\cloud#troubleshooting)

Platform [Deployment](\docs\platform\deployment)

# Syncing an Inngest App

After deploying your code to a hosting platform, it is time to go to production and inform Inngest about your apps and functions. Check what [Inngest Apps](\docs\apps) are if you haven't done it yet.

## [Sync a new app in Inngest Cloud](\docs\apps\cloud#sync-a-new-app-in-inngest-cloud)

You can synchronize your app with Inngest using three methods:

- Manually;
- Automatically using an integration;
- With a curl command.

### [Manually](\docs\apps\cloud#manually)

1. Select your environment (for example, "Production") in Inngest Cloud and navigate to the Apps page. You'll find a button named "Sync App" or "Sync New App", depending on whether you already have synced apps.

Inngest Cloud screen with sync App button when you have no apps synced yet

<!-- image -->

Inngest Cloud screen with sync new app button when you have apps synced

<!-- image -->

2. Provide the location of your app by pasting the URL of your project's `serve()` endpoint and click on "Sync App".

Sync New App form where you paste your project's serve endpoint to inform Inngest about the location of your app

<!-- image -->

3. Your app is now synced with Inngest. 🎉

Inngest Cloud screen with apps

<!-- image -->

### [Automatically using an integration](\docs\apps\cloud#automatically-using-an-integration)

[Learn how to install our official Vercel integration](\docs\deploy\vercel?ref=docs-app) [Learn how to install our official Netlify integration](\docs\deploy\netlify?ref=docs-app)

### [Curl command](\docs\apps\cloud#curl-command)

Use the curl command to sync from your machine or automate the process within a CI/CD pipeline.

Send a PUT request to your application's serve endpoint using the following command:

Copy Copied

```
curl -X PUT https:// < your-ap p > .com/api/inngest
```

Before syncing with Inngest, ensure that the latest version of your code is live on your platform. This is because some platforms have rolling deploys that take seconds or minutes until the latest version of your code is live.

This is especially important when setting up your own automated process.

## [How and when to resync an app](\docs\apps\cloud#how-and-when-to-resync-an-app)

To ensure that your functions are up to date, you need to resync your app with Inngest whenever you deploy new function configurations to your hosted platform.

If you are syncing your app through an integration, this process is automatically handled for you.

### [When to resync Vercel apps manually](\docs\apps\cloud#when-to-resync-vercel-apps-manually)

We recommend using our official Vercel integration, since the syncing process is automatic.

You will want to resync a Vercel app manually if:

- There was an error in the automatic syncing process (such as a network error)
- You chose not to install the Vercel integration and synced the app manually

If you have the Vercel integration and resync the app manually, the next time you deploy code to Vercel, the app will still be automatically resynced.

[Vercel generates a unique URL for each deployment](https://vercel.com/docs/deployments/generated-urls) . Please confirm that you are using the correct URL if you choose a deployment's generated URL instead of a static domain for your app.

### [How to resync manually](\docs\apps\cloud#how-to-resync-manually)

1. Navigate to the app you want to resync. You will find a "Resync" button at the top-right corner of the page.

Inngest Cloud screen with resync app button

<!-- image -->

2. You will see a confirmation modal. Click on "Resync App".

Inngest Cloud screen with resync app modal

<!-- image -->

If your app location changes, enable the "Override" switch and edit the URL before clicking on "Resync App". Please ensure that the app ID is the same, otherwise Inngest will consider it a new app white resyncing.

Inngest Cloud screen with resync app modal displaying an edited URL

<!-- image -->

## [Troubleshooting](\docs\apps\cloud#troubleshooting)

Why is my app syncing to the wrong environment?

- Apps are synced to one environment. The [**`INNGEST_SIGNING_KEY`**](\docs\platform\signing-keys) ensures that your app is synced within the correct Inngest environment. Verify that you assigned your signing key to the right `INNGEST_SIGNING_KEY` environment variable in your hosting provider or **`.env`** file locally.

Why do I have duplicated apps?

- Each app ID is considered a persistent identifier. [Since the app ID is determined by the ID passed to the serve handler from the Inngest client](\docs\apps#apps-in-sdk) , changing that ID will result in Inngest not recognizing the app ID during the next sync. As a result, Inngest will create a new app.

Why is my sync inside unattached syncs?

- Failures in automatic syncs may not be immediately visible. In such cases, an unattached sync (a sync without an app) containing the failure message is created.

Why don't I see my sync in the sync list?

If you're experiencing difficulties with syncing and cannot locate your sync in the sync list, consider the following scenarios:

1. **Different App ID:**

- If you resync the app after modifying the [app ID](\docs\reference\client\create) , a new app is created, not a new sync within the existing app.
- Solution: Confirm the creation of a new app when changing the app ID.

2. **Syncing Errors:**

- *Manual Syncs and Manual Resyncs:*
    - Sync failures during manual operations are immediately displayed, preventing the creation of a new sync. The image below shows an example of an error while manually syncing:
    Inngest Cloud screen with app error while syncing

<!-- image -->
    - Solution: Review the displayed error message and address the syncing issue accordingly.
Inngest Cloud screen with app error while syncing

<!-- image -->
- *Automatic Syncs (such as Vercel Integration):*
    - Failures in automatic syncs may not be immediately visible. In such cases, an unattached sync (a sync without an app) containing the failure message is created.
    Inngest Cloud screen with app sync error

<!-- image -->
    - Solution: Check for unattached syncs and address the issues outlined in the failure message. The image below shows the location of unattached syncs in Inngest Cloud:
    Inngest Cloud screen with unattached syncs

<!-- image -->
Inngest Cloud screen with app sync error

<!-- image -->
Inngest Cloud screen with unattached syncs

<!-- image -->