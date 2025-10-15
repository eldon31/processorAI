#### On this page

- [Inngest Dev Server](\docs\dev-server#inngest-dev-server)
- [Connecting apps to the Dev Server](\docs\dev-server#connecting-apps-to-the-dev-server)
- [How functions are loaded by the Dev Server](\docs\dev-server#how-functions-are-loaded-by-the-dev-server)
- [Testing functions](\docs\dev-server#testing-functions)
- [Invoke via UI](\docs\dev-server#invoke-via-ui)
- [Sending events to the Dev Server](\docs\dev-server#sending-events-to-the-dev-server)
- [Configuration file](\docs\dev-server#configuration-file)
- [Inngest SDK debug endpoint](\docs\dev-server#inngest-sdk-debug-endpoint)
- [Auto-discovery](\docs\dev-server#auto-discovery)
- [Flags](\docs\dev-server#flags)

Features [Local Development](\docs\local-development)

# Inngest Dev Server

The Inngest dev server is an [open source](https://github.com/inngest/inngest) environment that:

1. Runs a fast, in-memory version of Inngest on your machine
2. Provides a browser interface for sending events and viewing events and function runs

Dev Server Demo

<!-- image -->

You can start the dev server with a single command. The dev server will attempt to find an Inngest `serve` API endpoint by scanning ports and endpoints that are commonly used for this purpose (See " [Auto-discovery](\docs\dev-server#auto-discovery) "). Alternatively, you can specify the URL of the `serve` endpoint:

npx (npm) Docker

Copy Copied

```
npx inngest-cli@latest dev
# You can specify the URL of your development `serve` API endpoint
npx inngest-cli@latest dev -u http://localhost: 3000 /api/inngest
```

You can now open the dev server's browser interface on [`http://localhost:8288`](http://localhost:8288/) . For more information about developing with Docker, see the [Docker guide](\docs\guides\development-with-docker) .

### [Connecting apps to the Dev Server](\docs\dev-server#connecting-apps-to-the-dev-server)

There are two ways to connect apps to the Dev Server:

1. **Automatically** : The Dev Server will attempt to "auto-discover" apps running on common ports and endpoints (See " [Auto-discovery](\docs\dev-server#auto-discovery) ").
2. **Manually** : You scan explicitly add the URL of the app to the Dev Server using one of the following options:
    - Using the CLI `-u` param (ex. `npx inngest-cli@latest dev -u http://localhost:3000/api/inngest` )
    - Adding the URL in the Dev Server Apps page. You can edit the URL or delete a manually added app at any point in time
    - Using the `inngest.json` (or similar) configuration file (See " [Configuration file](\docs\dev-server#configuration-file) ")

Dev Server demo manually syncing an app

<!-- image -->

The dev server does "auto-discovery" which scans popular ports and endpoints like `/api/inngest` and `/.netlify/functions/inngest` . **If you would like to disable auto-discovery, pass the** **`--no-discovery`** **flag to the** **`dev`** **command** . Learn more about [this below](\docs\dev-server#auto-discovery)

### [How functions are loaded by the Dev Server](\docs\dev-server#how-functions-are-loaded-by-the-dev-server)

The dev server polls your app locally for any new or changed functions. Then as events are sent, the dev server calls your functions directly, just as Inngest would do in production over the public internet.

<!-- image -->

## [Testing functions](\docs\dev-server#testing-functions)

### [Invoke via UI](\docs\dev-server#invoke-via-ui)

From the Functions tab, you can quickly test any function by click the "Invoke" button and providing the data for your payload in the modal that pops up there. This is the easiest way to directly call a specific function:

<!-- image -->

### [Sending events to the Dev Server](\docs\dev-server#sending-events-to-the-dev-server)

There are different ways that you can send events to the dev server when testing locally:

1. Using the Inngest SDK
2. Using the "Test Event" button in the Dev Server's interface
3. Via HTTP request (e.g. curl)

### [Using the Inngest SDK](\docs\dev-server#using-the-inngest-sdk)

When using the Inngest SDK locally, it tries to detect if the dev server is running on your machine. If it's running, the event will be sent there.

Node.js Python Go

Copy Copied

```
import { Inngest } from "inngest" ;

const inngest = new Inngest ({ id : "my_app" });
await inngest .send ({
name : "user.avatar.uploaded" ,
data : { url : "https://a-bucket.s3.us-west-2.amazonaws.com/..." } ,
});
```

**Note** - During local development, you can use a dummy value for your [`INNGEST_EVENT_KEY`](\docs\sdk\environment-variables#inngest-event-key?ref=local-development) environment variable. The dev server does not validate keys locally.

### [Using the "Test Event" button](\docs\dev-server#using-the-test-event-button)

The dev server's interface also has a "Test Event" button on the top right that enables you to enter any JSON event payload and send it manually. This is useful for testing out different variants of event payloads with your functions.

<!-- image -->

### [Via HTTP request](\docs\dev-server#via-http-request)

All events are sent to Inngest using a simple HTTP API with a JSON body. Here is an example of a curl request to the local dev server's `/e/<EVENT_KEY>` endpoint running on the default port of `8228` using a dummy event key of `123` :

Copy Copied

```
curl -X POST -v "http://localhost:8288/e/123" \
-d '{
"name": "user.avatar.uploaded",
"data": { "url": "https://a-bucket.s3.us-west-2.amazonaws.com/..." }
}'
```

💡 Since you can send events via HTTP, this means you can send events with any programming language or from your favorite testing tools like Postman.

## [Configuration file](\docs\dev-server#configuration-file)

When using lots of configuration options or specifying multiple `-u` flags for a project, you can choose to configure the CLI via `inngest.json` configuration file. The `dev` command will start in your current directory and walk up directories until it finds a file. `yaml` , `yml` , `toml` , or `properties` file formats and extensions are also supported. You can list all options with `dev --help` . Here is an example file specifying two app urls and the `no-discovery` option:

inngest.json inngest.yaml

Copy Copied

```
{
"sdk-url" : [
"http://localhost:3000/api/inngest" ,
"http://localhost:3030/api/inngest"
] ,
"no-discovery" : true
}
```

## [Inngest SDK debug endpoint](\docs\dev-server#inngest-sdk-debug-endpoint)

The [SDK's](\docs\learn\serving-inngest-functions) [`serve`](\docs\learn\serving-inngest-functions) [API endpoint](\docs\learn\serving-inngest-functions) will return some diagnostic information for your server configuration when sending a `GET` request. You can do this via `curl` command or by opening the URL in the browser.

Here is an example of a curl request to an Inngest app running at `http://localhost:3000/api/inngest` :

Copy Copied

```
$ curl -s http://localhost: 3000 /api/inngest | jq
{
"message" : "Inngest endpoint configured correctly." ,
"hasEventKey" : false ,
"hasSigningKey" : false ,
"functionsFound" : 1
}
```

## [Auto-discovery](\docs\dev-server#auto-discovery)

The dev server will automatically detect and connect to apps running on common ports and endpoints. You can disable auto-discovery by passing the `--no-discovery` flag to the `dev` command:

Copy Copied

```
npx inngest-cli@latest dev --no-discovery -u http://localhost: 3000 /api/inngest
```

Common endpoints Common ports

Copy Copied

```
/api/inngest
/x/inngest
/.netlify/functions/inngest
/.redwood/functions/inngest
```

## [Flags](\docs\dev-server#flags)

`inngest-cli dev` command supports the following flags:

| Long form      | Short form   | Type    | Default value                     | Description                           |
|----------------|--------------|---------|-----------------------------------|---------------------------------------|
| --config       | -            | string  | -                                 | Path to an Inngest configuration file |
| --help         | -h           | -       | -                                 | Output the help information           |
| --host         | -            | string  | http://localhost                  | Inngest server host                   |
| --no-discovery | -            | boolean | false                             | Disable app auto-discovery            |
| --no-poll      | -            | boolean | false                             | Disable polling of apps for updates   |
| --port         | -p           | int     | 8288                              | Inngest server port                   |
| --sdk-url      | -u           | strings | http://localhost:3000/api/inngest | App serve URLs to sync                |