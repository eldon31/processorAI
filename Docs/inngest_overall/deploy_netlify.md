#### On this page

- [Netlify](\docs\deploy\netlify#netlify)
- [Setup](\docs\deploy\netlify#setup)
- [Configuration](\docs\deploy\netlify#configuration)

Platform [Deployment](\docs\platform\deployment) [Cloud Providers](\docs\deploy\vercel)

# Netlify

We provide a Netlify build plugin, [netlify-plugin-inngest](https://www.npmjs.com/package/netlify-plugin-inngest) , that allows you to automatically sync any found apps whenever your site is deployed to Netlify.

## [Setup](\docs\deploy\netlify#setup)

1. Install `netlify-plugin-inngest` as a dev dependency:

Copy Copied

```
npm install --save-dev netlify-plugin-inngest
# or
yarn add --dev netlify-plugin-inngest
```

2. Create or edit a `netlify.toml` file at the root of your project with the following:

Copy Copied

```
[[plugins]]
package = "netlify-plugin-inngest"
```

Done! 🥳 Whenever your site is deployed, your app hosted at `/api/inngest` will be synced.

## [Configuration](\docs\deploy\netlify#configuration)

If you want to use a URL that isn't your "primary" Netlify domain, or your functions are served at a different path, provide either `host` , `path` , or both as inputs in the same file:

Copy Copied

```
[[plugins]]
package = "netlify-plugin-inngest"

[plugins.inputs]
host = "https://my-specific-domain.com"
path = "/api/inngest"
```