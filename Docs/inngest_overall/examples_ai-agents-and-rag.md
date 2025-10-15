#### On this page

- [AI Agents and RAG](\docs\examples\ai-agents-and-rag#ai-agents-and-rag)
- [Quick Snippet](\docs\examples\ai-agents-and-rag#quick-snippet)
- [App examples](\docs\examples\ai-agents-and-rag#app-examples)
- [Resources](\docs\examples\ai-agents-and-rag#resources)
- [Related concepts](\docs\examples\ai-agents-and-rag#related-concepts)

[Examples](\docs\examples)

# AI Agents and RAG

Inngest offers tools to support the development of AI-powered applications. Whether you're building AI agents, automating tasks, or orchestrating and managing AI workflows, Inngest provides features that accommodate various needs and requirements, such as concurrency, debouncing, or throttling (see ["Related Concepts"](\docs\examples\ai-agents-and-rag#related-concepts) ).

## [Quick Snippet](\docs\examples\ai-agents-and-rag#quick-snippet)

Below is an example of a RAG workflow (from this [example app](https://github.com/inngest/inngest-demo-app/) ). This asynchronous Inngest function summarizes content via GPT-4 by following these steps:

- Query a vector database for relevant content.
- Retrieve a transcript from an S3 file.
- Combine the transcript and queried content to generate a summary using GPT-4.
- Save the summary to a database and sends a notification to the client.

The function uses [Inngest steps](\docs\learn\inngest-steps) to guarantee automatic retries on failure.

### ./inngest/functions.ts

Copy Copied

```
export const summarizeContent = inngest .createFunction (
{ name : 'Summarize content via GPT-4' , id : 'summarize-content' } ,
{ event : 'ai/summarize.content' } ,
async ({ event , step , attempt }) => {
const results = await step .run ( 'query-vectordb' , async () => {
return {
matches : [
{
id : 'vec3' ,
score : 0 ,
values : [ 0.3 , 0.3 , 0.3 , 0.3 , 0.3 , 0.3 , 0.3 , 0.3 ] ,
text : casual .sentences ( 3 ) ,
} ,
{
id : 'vec4' ,
score : 0.0799999237 ,
values : [ 0.4 , 0.4 , 0.4 , 0.4 , 0.4 , 0.4 , 0.4 , 0.4 ] ,
text : casual .sentences ( 3 ) ,
} ,
{
id : 'vec2' ,
score : 0.0800000429 ,
values : [ 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.2 , 0.2 ] ,
text : casual .sentences ( 3 ) ,
} ,
] ,
namespace : 'ns1' ,
usage : { readUnits : 6 } ,
};
});

const transcript = await step .run ( 'read-s3-file' , async () => {
return casual .sentences ( 10 );
});

// We can globally share throttle limited functions like this using invoke
const completion = await step .invoke ( 'generate-summary-via-gpt-4' , {
function : chatCompletion ,
data : {
messages : [
{
role : 'system' ,
content :
'You are a helpful assistant that summaries content for product launches.' ,
} ,
{
role : 'user' ,
content : `Question: Summarize my content: \n ${ transcript } . \nInformation: ${ results .matches
.map ((m) => m .text)
.join ( '. ' ) } ` ,
} ,
] ,
} ,
});
// You might use the response like this:
const summary = completion .choices[ 0 ]. message .content;

await step .run ( 'save-to-db' , async () => {
return casual .uuid;
});

await step .run ( 'websocket-push-to-client' , async () => {
return casual .uuid;
});
return { success : true , summaryId : casual .uuid };
}
);
```

## [App examples](\docs\examples\ai-agents-and-rag#app-examples)

Here are apps that use Inngest to power AI workflows:

### Integrate AI agents with Inngest

AI-powered task automation in Next.js using OpenAI and Inngest. Enhance productivity with automated workflows.

Technology used : Next.js, OpenAI Explore : [Code](https://github.com/joelhooks/inngest-partykit-nextjs-openai) | [Demo](https://www.loom.com/share/c43aa34205854096bcec0a96e7ba5634?sid=839b1adc-ad39-4540-9995-88967f2b6da9) Made by : [Joel Hooks](https://twitter.com/jhooks)

### PCXI starter

A boilerplate project for the PCXI stack featuring an OpenAI call

Technology used : Next.js, OpenAI, Xata, Prisma, Clerk Explore : [Code](https://github.com/inngest/next-pxci-starter) Made by : Inngest Team

## [Resources](\docs\examples\ai-agents-and-rag#resources)

Check the resources below to learn more about working with AI using Inngest:

### [Blog: "AI in production: Managing capacity with flow control"](\blog\ai-in-production-managing-capacity-with-flow-control)

[Learn how to manage AI capacity in production using Inngest's flow control techniques, including throttling, concurrency, debouncing, and prioritization, to optimize performance and cost-efficiency.](\blog\ai-in-production-managing-capacity-with-flow-control)

### [Podcast: "Building Production Workflows for AI Applications"](https://a16z.com/podcast/building-production-workflows-for-ai-applications/)

[Tony Holdstock-Brown and Yoko Li discuss the reality and complexity of running AI agents and other multistep AI workflows in production.](https://a16z.com/podcast/building-production-workflows-for-ai-applications/)

### [Talk: "Automate All of Your Customer Interactions with AI in Next.js"](https://www.youtube.com/watch?v=EoFI_Bmzb4g)

[Joel Hooks discusses managing long-running processes like generative AI to automate customer interactions effectively.](https://www.youtube.com/watch?v=EoFI_Bmzb4g)

### [Blog: "Semi-Autonomous AI Agents and Collaborative Multiplayer Asynchronous Workflows"](\blog\semi-autonomous-ai-agents)

[Build an AI agent that reads from Linear issues, returns relevant issues based on queries, and allows actions on those issues.](\blog\semi-autonomous-ai-agents)

### [Video: "Chaining Prompts The Easy Way - Using Inngest Serverless Jobs with OpenAI"](https://www.youtube.com/watch?v=PCq6DozV-mY)

[Doug Silkstone demonstrates how to chain together prompts and get content in next to no time at all.](https://www.youtube.com/watch?v=PCq6DozV-mY)

## [Related concepts](\docs\examples\ai-agents-and-rag#related-concepts)

- [Concurrency](\docs\guides\concurrency) : control the number of steps executing code at any one time.
- [Debouncing](\docs\guides\debounce) : delay function execution until a series of events are no longer received.
- [Prioritization](\docs\guides\priority) : dynamically execute some runs ahead or behind others based on any data.
- [Rate limiting](\docs\guides\rate-limiting) : limit on how many function runs can start within a time period.
- [Steps](\docs\reference\functions\step-run) : individual tasks within a function that can be executed independently with a guaranteed retrial.
- [Throttling](\docs\guides\throttling) : specify how many function runs can start within a time period.