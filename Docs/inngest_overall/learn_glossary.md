#### On this page

- [Glossary](\docs\learn\glossary#glossary)
- [Batching](\docs\learn\glossary#batching)
- [Concurrency Management](\docs\learn\glossary#concurrency-management)
- [Debouncing](\docs\learn\glossary#debouncing)
- [Durable Execution](\docs\learn\glossary#durable-execution)
- [Fan-out Function](\docs\learn\glossary#fan-out-function)
- [Flow Control](\docs\learn\glossary#flow-control)
- [Function Replay](\docs\learn\glossary#function-replay)
- [Idempotency](\docs\learn\glossary#idempotency)
- [Inngest App](\docs\learn\glossary#inngest-app)
- [Inngest Client](\docs\learn\glossary#inngest-client)
- [Inngest Cloud](\docs\learn\glossary#inngest-cloud)
- [Inngest Dev Server](\docs\learn\glossary#inngest-dev-server)
- [Inngest Event](\docs\learn\glossary#inngest-event)
- [Inngest Function](\docs\learn\glossary#inngest-function)
- [Inngest Step](\docs\learn\glossary#inngest-step)
- [Priority](\docs\learn\glossary#priority)
- [Rate Limiting](\docs\learn\glossary#rate-limiting)
- [SDK](\docs\learn\glossary#sdk)
- [Step Memoization](\docs\learn\glossary#step-memoization)
- [Throttling](\docs\learn\glossary#throttling)
- [Next Steps](\docs\learn\glossary#next-steps)

# Glossary

This glossary serves as a quick reference for key terminology used in Inngest's documentation. The terms are organized alphabetically.

## [Batching](\docs\learn\glossary#batching)

Batching is one of the methods offered by Inngest's [Flow Control](\docs\learn\glossary#flow-control) . It allows you to process multiple events in a single batch function to improve efficiency and reduce system load. By handling high volumes of data in batches, you can optimize performance, minimize processing time, and reduce costs associated with handling individual events separately. Read more about [Batching](https://www.inngest.com/docs/guides/batching) .

## [Concurrency Management](\docs\learn\glossary#concurrency-management)

Concurrency management is one of the methods offered by Inngest's [Flow Control](\docs\learn\glossary#flow-control) . It involves controlling the number of [steps](\docs\learn\glossary#inngest-step) executing simultaneously within a [function](\docs\learn\glossary#inngest-function) . It prevents system overload by limiting how many processes run at once, which can be set at various levels such as globally, per-function, or per-user. This ensures efficient resource use and system stability, especially under high load conditions. Read more about [Concurrency Management](\docs\guides\concurrency) .

## [Debouncing](\docs\learn\glossary#debouncing)

Debouncing is one of the methods offered by Inngest's [Flow Control](\docs\learn\glossary#flow-control) . It prevents a [function](\docs\learn\glossary#inngest-function) from being executed multiple times in rapid succession by ensuring it is only triggered after a specified period of inactivity. This technique helps to eliminate redundant function executions caused by quick, repeated events, thereby optimizing performance and reducing unnecessary load on the system. It is particularly useful for managing user input events and other high-frequency triggers. Read more about [Debouncing](\docs\guides\debounce) .

## [Durable Execution](\docs\learn\glossary#durable-execution)

Durable Execution ensures that functions are fault-tolerant and resilient by handling failures and interruptions gracefully. It uses automatic retries and state persistence to allow [functions](\docs\learn\glossary#inngest-function) to continue running from the point of failure, even if issues like network failures or timeouts occur. This approach enhances the reliability and robustness of applications, making them capable of managing even complex and long-running workflows. Read more about [Durable Execution](\docs\learn\how-functions-are-executed) .

## [Fan-out Function](\docs\learn\glossary#fan-out-function)

A fan-out function (also known as "fan-out job") in Inngest is designed to trigger multiple [functions](\docs\learn\glossary#inngest-function) simultaneously from a single [event](\docs\learn\glossary#inngest-event) . This is particularly useful when an event needs to cause several different processes to run in parallel, such as sending notifications, updating databases, or performing various checks. Fan-out functions enhance the efficiency and responsiveness of your application by allowing concurrent execution of tasks, thereby reducing overall processing time and enabling complex workflows. Read more about [Fan-out Functions](\docs\guides\fan-out-jobs) .

## [Flow Control](\docs\learn\glossary#flow-control)

Flow control in Inngest encompasses rate, throughput, priority, timing, and conditions of how functions are executed in regard to events. It helps optimize the performance and reliability of workflows by preventing bottlenecks and managing the execution order of tasks with tools like [steps](\docs\learn\glossary#inngest-step) . Read more about [Flow Control](\docs\guides\flow-control) .

## [Function Replay](\docs\learn\glossary#function-replay)

Function replay allows developers to rerun failed functions from any point in their execution history. This is useful for debugging and correcting errors without needing to manually re-trigger events, thus maintaining workflow integrity and minimizing downtime. Read more about [Function Replay](\docs\platform\replay) .

## [Idempotency](\docs\learn\glossary#idempotency)

Idempotency is one of the methods offered by Inngest's [Flow Control](\docs\learn\glossary#flow-control) . It guarantees that multiple identical requests have the same effect as a single request, preventing unintended side effects from repeated executions. By handling idempotency, you can avoid issues such as duplicate transactions or repeated actions, ensuring that your workflows remain accurate and dependable. Read more about [Handling idempotency](\docs\guides\handling-idempotency) .

## [Inngest App](\docs\learn\glossary#inngest-app)

Inngest apps are higher-level constructs that group multiple [functions](\docs\learn\glossary#inngest-function) and configurations under a single entity. An Inngest app can consist of various functions that work together to handle complex workflows and business logic. This abstraction helps in organizing and managing related functions and their configurations efficiently within the Inngest platform. Read more about [Inngest Apps](\docs\apps\cloud) .

## [Inngest Client](\docs\learn\glossary#inngest-client)

The Inngest client is a component that interacts with the Inngest platform. It is used to define and manage [functions](\docs\learn\glossary#inngest-function) , send [events](\docs\learn\glossary#inngest-event) , and configure various aspects of the Inngest environment. The client serves as the main interface for developers to integrate Inngest's capabilities into their applications, providing methods to create functions, handle events, and more. Read more about [Inngest Client](\docs\reference\client\create) .

## [Inngest Cloud](\docs\learn\glossary#inngest-cloud)

Inngest Cloud (also referred to as "Inngest UI" or inngest.com) is the managed service for running and managing your [Inngest functions](\docs\learn\glossary#inngest-function) . It comes with multiple environments for developing, testing, and production. Inngest Cloud handles tasks like state management, retries, and scalability, allowing you to focus on building your application logic. Read more about [Inngest Cloud](\docs\platform\environments) .

## [Inngest Dev Server](\docs\learn\glossary#inngest-dev-server)

The Inngest Dev Server provides a local development environment that mirrors the production setup. It allows developers to test and debug their [functions](\docs\learn\glossary#inngest-function) locally, ensuring that code behaves as expected before deployment. This tool significantly enhances the development experience by offering real-time feedback and simplifying local testing. Read more about [Inngest Dev Server](\docs\local-development) .

## [Inngest Event](\docs\learn\glossary#inngest-event)

An event is a trigger that initiates the execution of a [function](\docs\learn\glossary#inngest-function) . Events can be generated from various sources, such as user actions or external services (third party webhooks or API requests). Each event carries data that functions use to perform their tasks. Inngest supports handling these events seamlessly. Read more about [Events](\docs\events) .

## [Inngest Function](\docs\learn\glossary#inngest-function)

Inngest functions are the fundamental building blocks of the Inngest platform,

which enable developers to run reliable background logic, from background jobs to complex workflows. They provide robust tools for retrying, scheduling, and coordinating complex sequences of operations. They are composed of

[steps](\docs\learn\glossary#inngest-step) that can run independently and be retried in case of failure. Inngest functions are powered by [Durable Execution](\docs\learn\glossary#durable-execution) , ensuring reliability and fault tolerance, and can be deployed on any platform, including serverless environments. Read more about [Inngest Functions](\docs\learn\inngest-functions) .

## [Inngest Step](\docs\learn\glossary#inngest-step)

In Inngest, a "step" represents a discrete, independently retriable unit of work within a [function](\docs\learn\glossary#inngest-function) . Steps enable complex workflows by breaking down a function into smaller, manageable blocks, allowing for automatic retries and state persistence. This approach ensures that even if a step fails, only that task is retried, not the entire function. Read more about [Inngest Steps](\docs\learn\inngest-steps) .

## [Priority](\docs\learn\glossary#priority)

Priority is one of the methods offered by Inngest's [Flow Control](\docs\learn\glossary#flow-control) . It allows you to assign different priority levels to [functions](\docs\learn\glossary#inngest-function) , ensuring that critical tasks are executed before less important ones. By setting priorities, you can manage the order of execution, improving the responsiveness and efficiency of your workflows. This feature is essential for optimizing resource allocation and ensuring that high-priority operations are handled promptly. Read more about [Priority](\docs\guides\priority) .

## [Rate Limiting](\docs\learn\glossary#rate-limiting)

Rate limiting is one of the methods offered by Inngest's [Flow Control](\docs\learn\glossary#flow-control) . It controls the frequency of [function](\docs\learn\glossary#inngest-function) executions over a specified period to prevent overloading the system. It helps manage API calls and other resources by setting limits on how many requests or processes can occur within a given timeframe, ensuring system stability and fair usage. Read more about [Rate Limiting](\docs\guides\rate-limiting) .

## [SDK](\docs\learn\glossary#sdk)

The Software Development Kit (SDK) is a collection of tools, libraries, and documentation that allows developers to easily integrate and utilize Inngest's features within their applications. The SDK simplifies the process of creating, managing, and executing functions, handling events, and configuring workflows. It supports multiple programming languages and environments, ensuring broad compatibility and ease of use. Currently, Inngest offers SDKs for TypeScript, Python, and Go. Read more about [Inngest SDKs](\docs\reference) .

## [Step Memoization](\docs\learn\glossary#step-memoization)

Step memoization in Inngest refers to the technique of storing the results of steps so they do not need to be re-executed if already completed. This optimization enhances performance and reliability by preventing redundant computations and ensuring that each step's result is consistently available for subsequent operations. Read more about [Step Memoization](\docs\learn\how-functions-are-executed#secondary-executions-memoization-of-steps) .

## [Throttling](\docs\learn\glossary#throttling)

Throttling is one of the methods offered by Inngest's [Flow Control](\docs\learn\glossary#flow-control) . It controls the rate at which [functions](\docs\learn\glossary#inngest-function) are executed to prevent system overload. By setting limits on the number of executions within a specific timeframe, throttling ensures that resources are used efficiently and helps maintain the stability and performance of your application. It can be configured on a per-user or per-function basis, allowing for flexible and precise control over execution rates. Read more about [Throttling](\docs\guides\throttling) .

## [Next Steps](\docs\learn\glossary#next-steps)

- Explore Inngest through our [Quick Start](\docs\getting-started\nextjs-quick-start?ref=docs-glossary) .
- Learn about [Inngest Functions](\docs\learn\inngest-functions) .
- Learn about [Inngest Steps](\docs\learn\inngest-steps) .
- Understand how [Inngest functions are executed](\docs\learn\how-functions-are-executed) .