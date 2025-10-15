This page documents the event handling system in the Inngest Python SDK. Events are a fundamental component that enable event-driven architectures by serving as messages that trigger function execution and carry data between systems. For information about defining functions that respond to events, see [Functions](#3.2).

## Event Structure and Lifecycle

Events in Inngest have a defined structure and follow a lifecycle from creation to function execution.

```mermaid
classDiagram
    class Event {
        name: str
        data: dict
        id: Optional[str]
        ts: Optional[int]
        to_dict()
    }
    
    note for Event "Core fields of an Inngest event"
```

Sources: [pkg/inngest/inngest/_internal/client_lib/client.py:424-475]()

Each event contains:

- `name`: Event type identifier (e.g., "app/user.created")
- `data`: JSON-serializable payload containing event information
- `id`: Optional unique identifier (auto-generated if not provided)
- `ts`: Optional timestamp in milliseconds (defaults to current time)

## Sending Events

The Inngest client provides both synchronous and asynchronous methods for sending events to trigger functions.

```mermaid
sequenceDiagram
    participant App as "Application"
    participant Client as "Inngest Client"
    participant API as "Inngest Event API"
    
    App->>Client: "send(Event(...))" or "send_sync(Event(...))"
    Client->>Client: "Validate events"
    Client->>Client: "Apply middleware transformations"
    Client->>API: "HTTP POST to /e/{event_key}"
    API-->>Client: "Return response with event IDs"
    Client-->>App: "Return list of event IDs"
```

Sources: [pkg/inngest/inngest/_internal/client_lib/client.py:424-475](), [pkg/inngest/inngest/_internal/client_lib/client.py:476-522]()

### Sending Events Programmatically

There are two primary methods for sending events:

#### Asynchronous API

```python