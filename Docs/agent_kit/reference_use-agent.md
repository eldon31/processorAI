##### Introduction

- [Introduction](\reference\introduction)

##### Agent

- [createAgent](\reference\create-agent)
- [createTool](\reference\create-tool)

##### Network

- [createNetwork](\reference\create-network)
- [createState](\reference\state)
- [Router](\reference\network-router)

##### Models

- [OpenAI Model](\reference\model-openai)
- [Anthropic Model](\reference\model-anthropic)
- [Gemini Model](\reference\model-gemini)
- [Grok Model](\reference\model-grok)

##### Streaming

- [useAgent](\reference\use-agent)

close

On this page

- [Configuration](#configuration)
- [Identity &amp; Connection](#identity-%26-connection)
- [Initial State](#initial-state)
- [Data Fetching &amp; Caching](#data-fetching-%26-caching)
- [Callbacks](#callbacks)
- [Behavior](#behavior)
- [Return Values](#return-values)
- [Core Agent State](#core-agent-state)
- [Core Actions](#core-actions)
- [Thread Management State](#thread-management-state)
- [Thread Management Actions](#thread-management-actions)
- [Advanced Actions](#advanced-actions)

Streaming

# useAgent

React hook for building real-time, multi-threaded AI applications

The `useAgent` hook is the core of the `@inngest/use-agent` package. It's a comprehensive, client-side hook for React that manages real-time, multi-threaded conversations with an AgentKit network. It encapsulates the entire lifecycle of agent interactions, including sending messages, receiving streaming events, handling out-of-order event sequences, and managing connection state.

Copy Ask AI

```
import { useAgent , AgentProvider } from '@inngest/use-agent' ;

function App () {
return (
< AgentProvider userId = "user-123" >
< ChatComponent />
</ AgentProvider >
);
}

function ChatComponent () {
const { messages , sendMessage , status , currentThreadId , switchToThread } = useAgent ();

// UI to switch threads and display messages...

return < ChatUI messages = { messages } onSend = { sendMessage } status = { status } /> ;
}
```

## [ Configuration](#configuration)

The `useAgent` hook accepts a configuration object with the following properties.

### [ Identity &amp; Connection](#identity-%26-connection)

[](#param-user-id) userId string A unique identifier for the current user. This is used for personalizing agent interactions and routing real-time events. If not provided, it will be inherited from the `AgentProvider` .

[](#param-channel-key) channelKey string A key for targeting subscriptions, enabling collaborative sessions. If not provided, it defaults to the `userId` .

[](#param-transport) transport IClientTransport An optional transport instance to override the default HTTP transport provided by `AgentProvider` . This allows you to customize how the hook communicates with your backend.

### [ Initial State](#initial-state)

[](#param-initial-thread-id) initialThreadId string The ID of the conversation thread to load when the hook is first mounted.

[](#param-state) state () =&gt; TState A function that returns the current client-side UI state. This state is captured and sent with each user message, allowing agents to have context about what the user is seeing. It can also be used to restore the UI when revisiting a message.

### [ Data Fetching &amp; Caching](#data-fetching-%26-caching)

[](#param-fetch-threads) fetchThreads function A function to fetch a paginated list of conversation threads for the user. If not provided, the hook uses the default transport method.

[](#param-fetch-history) fetchHistory function A function to fetch the message history for a specific thread. If not provided, the hook uses the default transport method.

[](#param-threads-page-size) threadsPageSize number default: "20" The number of threads to fetch per page in pagination requests.

### [ Callbacks](#callbacks)

[](#param-on-event) onEvent (event, meta) =&gt; void A low-level callback invoked for every real-time event processed by the hook. This is useful for building custom UI that reacts to specific agent activities, like showing a "thinking" indicator when a `run.started` event is received.

[](#param-on-stream-ended) onStreamEnded (args) =&gt; void A callback fired when a terminal stream event ( `stream.ended` or `run.completed` ) is received for a thread, indicating the agent has finished its turn.

[](#param-on-tool-result) onToolResult (result) =&gt; void A strongly-typed callback that fires when a tool call completes and returns its final output. This is useful for observing or reacting to the data returned by agents' tools.

[](#param-on-state-rehydrate) onStateRehydrate (state, messageId) =&gt; void A callback invoked when `rehydrateMessageState` is called. It receives the client state that was captured when the original message was sent, allowing you to restore the UI to its previous state.

[](#param-on-thread-not-found) onThreadNotFound (threadId) =&gt; void A callback that is triggered if `switchToThread` is called with a `threadId` that cannot be found.

### [ Behavior](#behavior)

[](#param-debug) debug boolean default: "false" Enables detailed logging to the console for debugging the hook's internal state and event flow.

[](#param-require-provider) requireProvider boolean default: "false" If `true` , the hook will throw an error if it's not used within an `AgentProvider` . When `false` , it creates a local fallback instance.

[](#param-enable-thread-validation) enableThreadValidation boolean default: "true" If `true` , the hook will automatically re-fetch a thread's history if it detects a mismatch between the local message count and the server's message count, ensuring data consistency.

## [ Return Values](#return-values)

The `useAgent` hook returns an object containing state and actions to manage conversations.

### [ Core Agent State](#core-agent-state)

[](#param-messages) messages ConversationMessage[] An array of messages for the currently active thread. Each message contains structured parts that are updated in real-time as events are received.

[](#param-status) status AgentStatus The current activity status of the agent for the active thread. Possible values are: `"ready"` , `"submitted"` , `"streaming"` , or `"error"` .

[](#param-error) error AgentError An object containing details about the last error that occurred. It's `undefined` if there is no error.

[](#param-clear-error) clearError () =&gt; void A function to clear the current error state.

[](#param-is-connected) isConnected boolean Returns `true` if the client is currently connected to the real-time event stream.

### [ Core Actions](#core-actions)

[](#param-send-message) sendMessage (message, options) =&gt; Promise&lt;void&gt; Sends a message to the currently active thread.

[](#param-cancel) cancel () =&gt; Promise&lt;void&gt; Sends a request to the backend to cancel the current agent run for the active thread.

[](#param-approve-tool-call) approveToolCall (toolCallId, reason) =&gt; Promise&lt;void&gt; Approves a tool call that is awaiting human-in-the-loop (HITL) confirmation.

[](#param-deny-tool-call) denyToolCall (toolCallId, reason) =&gt; Promise&lt;void&gt; Denies a tool call that is awaiting human-in-the-loop (HITL) confirmation.

### [ Thread Management State](#thread-management-state)

[](#param-threads) threads Thread[] An array of all conversation threads loaded for the user.

[](#param-current-thread-id) currentThreadId string | null The ID of the currently active thread.

[](#param-threads-loading) threadsLoading boolean `true` while the initial list of threads is being fetched.

[](#param-threads-has-more) threadsHasMore boolean `true` if there are more pages of threads to be loaded.

[](#param-threads-error) threadsError string | null Contains an error message if fetching threads failed.

[](#param-is-loading-initial-thread) isLoadingInitialThread boolean `true` only while the selected thread's history has not yet been loaded.

### [ Thread Management Actions](#thread-management-actions)

[](#param-switch-to-thread) switchToThread (threadId) =&gt; Promise&lt;void&gt; Switches the active conversation to a different thread, loading its history.

[](#param-set-current-thread-id) setCurrentThreadId (threadId) =&gt; void Immediately changes the `currentThreadId` without fetching history. Useful for optimistic UI updates before `switchToThread` completes.

[](#param-create-new-thread) createNewThread () =&gt; string Creates a new, empty thread locally and returns its generated UUID.

[](#param-delete-thread) deleteThread (threadId) =&gt; Promise&lt;void&gt; Deletes a thread from the backend and removes it from the local state.

[](#param-load-more-threads) loadMoreThreads () =&gt; Promise&lt;void&gt; Fetches the next page of threads.

[](#param-refresh-threads) refreshThreads () =&gt; Promise&lt;void&gt; Refetches the first page of threads to get the latest list.

### [ Advanced Actions](#advanced-actions)

[](#param-send-message-to-thread) sendMessageToThread (threadId, message, options) =&gt; Promise&lt;void&gt; Sends a message to a specific thread, which may not be the currently active one.

[](#param-load-thread-history) loadThreadHistory (threadId) =&gt; Promise&lt;ConversationMessage[]&gt; Manually fetches the message history for a specific thread.

[](#param-clear-thread-messages) clearThreadMessages (threadId) =&gt; void Clears all messages from a specific thread's local state.

[](#param-replace-thread-messages) replaceThreadMessages (threadId, messages) =&gt; void Replaces all messages in a specific thread's local state. Useful for manually populating history.

[](#param-rehydrate-message-state) rehydrateMessageState (messageId) =&gt; void Triggers the `onStateRehydrate` callback with the client state associated with a specific message. Useful for UI features like "edit message" where you need to restore the UI to how it was when the message was sent.

[Grok Model Previous](\reference\model-grok)

⌘ I

Assistant Responses are generated using AI and may contain mistakes.