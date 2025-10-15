#### On this page

- [Modal](\docs\reference\python\guides\modal#modal)
- [Setting up your development environment](\docs\reference\python\guides\modal#setting-up-your-development-environment)
- [Creating a tunnel](\docs\reference\python\guides\modal#creating-a-tunnel)
- [Creating and deploying a FastAPI app](\docs\reference\python\guides\modal#creating-and-deploying-a-fast-api-app)
- [Syncing with the Dev Server](\docs\reference\python\guides\modal#syncing-with-the-dev-server)
- [Deploying to production](\docs\reference\python\guides\modal#deploying-to-production)

References [Python SDK](\docs\reference\python) [Guides](\docs\reference\python\guides\testing)

# Modal

This guide will help you use setup an Inngest app in [Modal](https://modal.com/) , a platform for building and deploying serverless Python applications.

## [Setting up your development environment](\docs\reference\python\guides\modal#setting-up-your-development-environment)

This section will help you setup your development environment. You'll have an Inngest Dev Server running locally and a FastAPI app running in Modal.

### [Creating a tunnel](\docs\reference\python\guides\modal#creating-a-tunnel)

Since we need bidirectional communication between the Dev Server and your app, you'll also need a tunnel to allow your app to reach your locally-running Dev Server. We recommend using [ngrok](https://ngrok.com/) for this.

Copy Copied

```
# Tunnel to the Dev Server's port
ngrok http 8288
```

This should output a public URL that can reach port `8288` on your machine. The URL can be found in the `Forwarding` part of ngrok's output:

Copy Copied

```
Forwarding    https://23ef-173-10-53-121.ngrok-free.app -> http://localhost:8288
```

### [Creating and deploying a FastAPI app](\docs\reference\python\guides\modal#creating-and-deploying-a-fast-api-app)

Create an `.env` file that contains the tunnel URL:

Copy Copied

```
INNGEST_DEV=https://23ef-173-10-53-121.ngrok-free.app
```

Create a dependency file that Modal will use to install dependencies. For this guide, we'll use `requirements.txt` :

Copy Copied

```
fastapi==0.115.0
inngest==0.4.12
python-dotenv==1.0.1
```

Create a `main.py` file that contains your FastAPI app:

Copy Copied

```
import os

from dotenv import load_dotenv
from fastapi import FastAPI
import inngest
import inngest . fast_api
import modal

load_dotenv ()

app = modal . App ( "test-fast-api" )

# Load all environment variables that start with "INNGEST_"
env : dict [ str , str ] = {}
for k , v , in os . environ . items ():
if k . startswith ( "INNGEST_" ):
env [ k ] = v

image = (
modal . Image . debian_slim ()
. pip_install_from_requirements ( "requirements.txt" )
. env (env)
)

fast_api_app = FastAPI ()

# Create an Inngest client
inngest_client = inngest . Inngest (app_id = "fast_api_example" )

# Create an Inngest function
@inngest_client . create_function (
fn_id = "my-fn" ,
trigger = inngest. TriggerEvent (event = "my-event" ),
)
async def fn ( ctx : inngest . Context) -> str :
print (ctx.event)
return "done"

# Serve the Inngest endpoint (its path is /api/inngest)
inngest . fast_api . serve (fast_api_app, inngest_client, [fn])

@app . function (image = image)
@modal . asgi_app ()
def fastapi_app ():
return fast_api_app
```

Deploy your app to Modal:

Copy Copied

```
modal deploy main.py
```

Your terminal should show the deployed app's URL:

Copy Copied

```
└── 🔨 Created web function fastapi_app =>
    https://test-fast-api-fastapi-app.modal.run
```

To test whether the deploy worked, send a request to the Inngest endpoint (note that we added the `/api/inngest` to the Modal URL). It should output JSON similar to the following:

Copy Copied

```
$ curl https://test-fast-api-fastapi-app.modal.run/api/inngest
{ "schema_version" : "2024-05-24" , "authentication_succeeded" : null, "function_count" : 1 , "has_event_key" : false , "has_signing_key" : false , "has_signing_key_fallback" : false , "mode" : "dev" }
```

### [Syncing with the Dev Server](\docs\reference\python\guides\modal#syncing-with-the-dev-server)

Start the Dev Server, specifying the FastAPI app's Inngest endpoint:

Copy Copied

```
npx inngest-cli@latest dev -u https://test-fast-api-fastapi-app.modal.run/api/inngest --no-discovery
```

In your browser, navigate to `http://127.0.0.1:8288/apps` . Your app should be successfully synced.

## [Deploying to production](\docs\reference\python\guides\modal#deploying-to-production)

A production Inngest app is very similar to an development app. The only difference is with environment variables:

- `INNGEST_DEV` must not be set. Alternatively, you can set it to `0` .
- `INNGEST_EVENT_KEY` must be set. Its value can be found on the [event keys page](https://app.inngest.com/env/production/manage/keys) .
- `INNGEST_SIGNING_KEY` must be set. Its value can be found on the [signing key page](https://app.inngest.com/env/production/manage/signing-key) .

Once your app is deployed with these environment variables, you can sync it on our [new app page](https://app.inngest.com/env/production/apps/sync-new) .

For more information about syncing, please see our [docs](\docs\apps\cloud) .