#### On this page

- [Signing keys](\docs\platform\signing-keys#signing-keys)
- [Configuring the signing key](\docs\platform\signing-keys#configuring-the-signing-key)
- [Local development](\docs\platform\signing-keys#local-development)
- [Rotation](\docs\platform\signing-keys#rotation)
- [Vercel integration](\docs\platform\signing-keys#vercel-integration)
- [Signing keys and branch environments](\docs\platform\signing-keys#signing-keys-and-branch-environments)
- [Further reading](\docs\platform\signing-keys#further-reading)

Platform [Deployment](\docs\platform\deployment)

# Signing keys

Inngest uses signing keys to secure communication between Inngest and your servers. The signing key is a *secret* pre-shared key unique to each [environment](\docs\platform\environments) . The signing key adds the following security features:

- **Serve endpoint authentication** - All requests sent to your server are signed with the signing key, ensuring that they originate from Inngest. Inngest SDKs reject all requests that are not authenticated with the signing key.
- **API authentication** - Requests sent to the Inngest API are signed with the signing key, ensuring that they originate from your server. The Inngest API rejects all requests that are not authenticated with the signing key. For example, when syncing functions with Inngest, the SDK sends function configuration to Inngest's API with the signing key as a bearer token.
- **Replay attack prevention** - Requests are signed with a timestamp embedded, and old requests are rejected, even if the requests are authenticated correctly.

🔐 **Signing keys are secrets and you should take precautions to ensure that they are kept secure** . Avoid storing them in source control.

You can find your signing key within each environment's [Signing Key tab](https://app.inngest.com/env/production/manage/signing-key) .

## [Configuring the signing key](\docs\platform\signing-keys#configuring-the-signing-key)

You can set the signing key in your SDK by setting the `INNGEST_SIGNING_KEY` environment variable. Alternatively, you can pass the signing key as an argument when creating the SDK client, but we recommend never hardcoding the signing key in your code.

Additionally, you'll set the `INNGEST_SIGNING_KEY_FALLBACK` environment variable to ensure zero downtime when rotating your signing key. Read more about that [below](\docs\platform\signing-keys#rotation) .

## [Local development](\docs\platform\signing-keys#local-development)

Signing keys should be omitted when using the Inngest [Dev Server](\docs\local-development) . To simplify local development and testing, the Dev Server doesn't require a signing key.

Each language SDK attempts to detect if your application is running in production or development mode. If you're running in development mode, the SDK will automatically disable signature verification. To force development mode, set `INNGEST_DEV=1` in your environment. This is useful when running in an automated testing environment.

## [Rotation](\docs\platform\signing-keys#rotation)

Signing keys can be rotated to mitigate the risk of a compromised key. We recommend rotating your signing keys periodically or whenever you believe they may have been exposed.

Inngest supports zero downtime signing key rotation if your SDK version meets the minimum version:

| Language   | Minimum Version   |
|------------|-------------------|
| Go         | 0.7.2             |
| Python     | 0.3.9             |
| TypeScript | 3.18.0            |

You can still rotate your signing key if you use an older SDK version, but you will experience downtime.

To begin the rotation process, navigate to the [Signing Key tab](https://app.inngest.com/env/production/manage/signing-key) in the Inngest dashboard. Click the "Create new signing key" button and then follow the instructions in the **Rotate key** section.

🤔 **Why do I need a "fallback" signing key?**

As requests are signed with the current signing key, your code must have both the current and the new signing key available to verify requests during the rotation. To ensure there is zero downtime, the SDKs will retry authentication failures with the fallback key.

### [Vercel integration](\docs\platform\signing-keys#vercel-integration)

To rotate signing keys for Vercel projects, you must manually update the `INNGEST_SIGNING_KEY` environment variable in your Vercel project.

During initial setup, the Vercel integration automatically sets this key, but the integration ***will not*** automatically rotate the key for you. You must follow the manual process as guided within the Inngest dashboard.

## [Signing keys and branch environments](\docs\platform\signing-keys#signing-keys-and-branch-environments)

All [branch environments](\docs\platform\environments#configuring-branch-environments) within your account share a signing key. This enables you to set a single environment variable for preview environments in platforms like [Vercel](\docs\deploy\vercel) or [Netlify](\docs\deploy\netlify) and each platform can dynamically specify the correct branch environment through secondary environment variables.

## [Further reading](\docs\platform\signing-keys#further-reading)

- [TypeScript SDK serve reference](\docs\reference\serve#signingKey)
- [Python SDK client reference](\docs\reference\python\client\overview#signing_key)