#### On this page

- [Run](\docs\reference\functions\step-run#run)
- [step.run(id, handler): Promise](\docs\reference\functions\step-run#step-run-id-handler-promise)
- [How to call step.run()](\docs\reference\functions\step-run#how-to-call-step-run)
- [Return values and serialization](\docs\reference\functions\step-run#return-values-and-serialization)
- [Usage limits](\docs\reference\functions\step-run#usage-limits)

References [TypeScript SDK](\docs\reference\typescript) [Steps](\docs\reference\functions\step-run)

# Run

Use `step.run()` to run synchronous or asynchronous code as a retriable step in your function. `step.run()` returns a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) that resolves with the return value of your handler function.

Copy Copied

```
export default inngest .createFunction (
{ id : "import-product-images" } ,
{ event : "shop/product.imported" } ,
async ({ event , step }) => {
const uploadedImageURLs = await step .run ( "copy-images-to-s3" , async () => {
return copyAllImagesToS3 ( event . data .imageURLs);
});
}
);
```

## [step.run(id, handler): Promise](\docs\reference\functions\step-run#step-run-id-handler-promise)

- Name `id` Type string Required required Description The ID of the step. This will be what appears in your function's logs and is used to memoize step state across function versions.
- Name `handler` Type function Required required Description The function that code that you want to run and automatically retry for this step. Functions can be: Throwing errors within the handler function will trigger the step to be retried ( [reference](\docs\functions\retries) ).

Copy Copied

```
// Steps can have async handlers
const result = await step .run ( "get-api-data" , async () => {
// Steps should return data used in other steps
return fetch ( "..." ) .json ();
});

// Steps can have synchronous handlers
const data = await step .run ( "transform" , () => {
return transformData (result);
});

// Returning data is optional
await step .run ( "insert-data" , async () => {
db .insert (data);
});
```

## [How to call step.run()](\docs\reference\functions\step-run#how-to-call-step-run)

As `step.run()` returns a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) , you will need to handle it like any other Promise in JavaScript. Here are some ways you can use `step.run()` in your code:

Copy Copied

```
// Use the "await" keyword to wait for the promise to fulfil
await step .run ( "create-user" , () => { /* ... */ });
const user = await step .run ( "create-user" , () => { /* ... */ });

// Use `then` (or similar)
step .run ( "create-user" , () => { /* ... */ })
.then ((user) => {
// do something else
});

// Use with a Promise helper function to run in parallel
Promise .all ([
step .run ( "create-subscription" , () => { /* ... */ }) ,
step .run ( "add-to-crm" , () => { /* ... */ }) ,
step .run ( "send-welcome-email" , () => { /* ... */ }) ,
]);
```

## [Return values and serialization](\docs\reference\functions\step-run#return-values-and-serialization)

All data returned from `step.run` is serialized as JSON. This is done to enable the SDK to return a valid serialized response to the Inngest service.

Copy Copied

```
const output = await step .run ( "create-user" , () => {
return { id : new ObjectId () , createdAt : new Date () };
});
/*
{
"id": "647731d1759aa55be43b975d",
"createdAt": "2023-05-31T11:39:18.097Z"
}
*/
```

## [Usage limits](\docs\reference\functions\step-run#usage-limits)

See [usage limits](\docs\usage-limits\inngest#functions) for more details.