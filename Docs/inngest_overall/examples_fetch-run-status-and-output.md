#### On this page

- [Fetch run status and output](\docs\examples\fetch-run-status-and-output#fetch-run-status-and-output)
- [Quick Snippet](\docs\examples\fetch-run-status-and-output#quick-snippet)
- [Triggering the function](\docs\examples\fetch-run-status-and-output#triggering-the-function)
- [Fetching triggered function status and output](\docs\examples\fetch-run-status-and-output#fetching-triggered-function-status-and-output)
- [Putting it all together](\docs\examples\fetch-run-status-and-output#putting-it-all-together)
- [More context](\docs\examples\fetch-run-status-and-output#more-context)
- [Related concepts](\docs\examples\fetch-run-status-and-output#related-concepts)

[Examples](\docs\examples)

# Fetch run status and output

Inngest provides a way to fetch the status and output of a function run using [the REST API](https://api-docs.inngest.com/docs/inngest-api/1j9i5603g5768-introduction) . This is useful when:

- You want to check the status or output of a given run.
- You want to display the status of a function run in your application, for example, in a user dashboard.

This page provides a quick example of how to fetch the status and output of a function run using the Inngest API.

## [Quick Snippet](\docs\examples\fetch-run-status-and-output#quick-snippet)

Here is a basic function that processes a CSV file and returns the number of items processed:

Copy Copied

```
const processCSV = inngest .createFunction (
{ id : "process-csv-upload" } ,
{ event : "imports/csv.uploaded" } ,
async ({ event , step }) => {
// CSV processing logic omitted for the sake of the example
return {
status : "success" ,
processedItems : results . length ,
failedItems : failures . length ,
}
}
);
```

### [Triggering the function](\docs\examples\fetch-run-status-and-output#triggering-the-function)

To trigger this function, you will send an event `"imports/csv.uploaded"` using `inngest.send()` with whatever payload data you need. The `inngest.send()` function returns an array of Event IDs that you will use to fetch the status and output of the function run.

Copy Copied

```
const { ids } = await inngest .send ({
name : "imports/csv.uploaded" ,
data : {
file : "http://s3.amazonaws.com/acme-uploads/user_0xp3wqz7vumcvajt/JVLO6YWS42IXEIGO.csv" ,
userId : "user_0xp3wqz7vumcvajt" ,
} ,
});
// ids = ["01HWAVEB858VPPX47Z65GR6P6R"]
```

### [Fetching triggered function status and output](\docs\examples\fetch-run-status-and-output#fetching-triggered-function-status-and-output)

Using the REST API, we can use the Event ID to fetch all runs triggered by that event using the [event's runs endpoint](https://api-docs.inngest.com/docs/inngest-api/yoyeen3mu7wj0-list-event-function-runs) :

Copy Copied

```
https://api.inngest.com/v1/events/01HWAVEB858VPPX47Z65GR6P6R/runs
```

To query this, we can use a simple `fetch` request using our signing key to authenticate with the API. Here, we'll wrap this in a re-usable function:

Copy Copied

```
async function getRuns (eventId) {
const response = await fetch ( `https://api.inngest.com/v1/events/ ${ eventId } /runs` , {
headers : {
Authorization : `Bearer ${ process . env . INNGEST_SIGNING_KEY } ` ,
} ,
});
const json = await response .json ();
return json .data;
}
```

We can now use the Event ID to fetch the status and output of the function run. The `getRuns` function will return an array of runs as events can trigger multiple runs via [fan-out](\docs\guides\fan-out-jobs) . We'll consider that this event only triggers a single function:

Copy Copied

```
const runs = await getRuns ( "01HWAVEB858VPPX47Z65GR6P6R" );
console .log (runs[ 0 ]);
/*
{
run_id: '01HWAVJ8ASQ5C3FXV32JS9DV9Q',
run_started_at: '2024-04-25T14:46:45.337Z',
function_id: '6219fa64-9f58-41b6-95ec-a45c7172fa1e',
function_version: 12,
environment_id: '6219fa64-9f58-41b6-95ec-a45c7172fa1e',
event_id: '01HWAVEB858VPPX47Z65GR6P6R',
status: 'Completed',
ended_at: '2024-04-25T14:46:46.896Z',
output: {
status: "success",
processedItems: 98,
failedItems: 2,
}
}
*/
```

If we want to trigger the function then immediately await it's output in the same code, we can wrap our `getRuns` to poll until the status is `Completed` :

Copy Copied

```
async function getRunOutput (eventId) {
let runs = await getRuns (eventId);
while (runs[ 0 ].status !== "Completed" ) {
await new Promise ((resolve) => setTimeout (resolve , 1000 ));
runs = await getRuns (eventId);
if (runs[ 0 ].status === "Failed" || runs[ 0 ].status === "Cancelled" ) {
throw new Error ( `Function run ${ runs[ 0 ].status } ` );
}
}
return runs[ 0 ];
}
```

### [Putting it all together](\docs\examples\fetch-run-status-and-output#putting-it-all-together)

Brining this all together, we can now trigger the function and await the output:

Copy Copied

```
const { ids } = await inngest .send ({
name : "imports/csv.uploaded" ,
data : {
file : "http://s3.amazonaws.com/acme-uploads/user_0xp3wqz7vumcvajt/JVLO6YWS42IXEIGO.csv" ,
userId : "user_0xp3wqz7vumcvajt" ,
} ,
});

const run = await getRunOutput (ids[ 0 ]);
console .log ( run .output);
/*
{
status: "success",
processedItems: 98,
failedItems: 2,
}
*/
```

## [More context](\docs\examples\fetch-run-status-and-output#more-context)

Check the resources below to learn more about working with the Inngest REST API.

### [Reference: REST API: List event function runs](https://api-docs.inngest.com/docs/inngest-api/yoyeen3mu7wj0-list-event-function-runs)

[Return all runs triggered by an event.](https://api-docs.inngest.com/docs/inngest-api/yoyeen3mu7wj0-list-event-function-runs)

## [Related concepts](\docs\examples\fetch-run-status-and-output#related-concepts)

- [Fan-out jobs](\docs\guides\fan-out-jobs)