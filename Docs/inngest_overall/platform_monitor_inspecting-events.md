#### On this page

- [Inspecting an Event](\docs\platform\monitor\inspecting-events#inspecting-an-event)
- [Accessing Events](\docs\platform\monitor\inspecting-events#accessing-events)
- [Searching Events](\docs\platform\monitor\inspecting-events#searching-events)
- [Searchable properties](\docs\platform\monitor\inspecting-events#searchable-properties)

Platform [Monitor](\docs\platform\monitor\insights)

# Inspecting an Event

The Event details will provide all the information to understand how this event was received, which data it contained and the tools to reproduce it locally.

## [Accessing Events](\docs\platform\monitor\inspecting-events#accessing-events)

Events across all application of the currently [selected environment](\docs\platform\environments) are accessible via the "Events" page in the left side navigation.

The Events list features the last events received.

<!-- image -->

*Events can be filtered using a time filter.*

Accessing the events of a specific Event Type is achieved via the "Event Types" menu.

## [Searching Events](\docs\platform\monitor\inspecting-events#searching-events)

Advanced filters are available using a [CEL expression](\docs\guides\writing-expressions) . The search feature is available by clicking on the "Show search" button.

The events list features an advance search feature that filters results using a CEL query.

<!-- image -->

### [Searchable properties](\docs\platform\monitor\inspecting-events#searchable-properties)

Only basic search operators and the `event` variable are available for now:

| Field name   | Type           | Operators                                                                       |
|--------------|----------------|---------------------------------------------------------------------------------|
| event.id     | string         | ``` == ```  ``` != ```  ,                                                       |
| event.name   | string         | ``` == ```  ``` != ```  ,                                                       |
| event.ts     | int64          | ``` == ```  ``` != ```  ``` > ```  ``` >= ```  ``` < ```  ``` <= ```  , , , , , |
| event.v      | string         | ``` == ```  ``` != ```  ,                                                       |
| event.data   | map[string]any | ``` == ```  ``` != ```  ``` > ```  ``` >= ```  ``` < ```  ``` <= ```  , , , , , |

A few examples of valid search queries are `event.data.hello == "world"` and `event.name != "billing"` . [Learn more about how expressions are used in Inngest.](\docs\guides\writing-expressions)

You can combine multiple search queries using the `&&` operator or `||` operator. Adding a new line is the equivalent of using the `&&` operator.