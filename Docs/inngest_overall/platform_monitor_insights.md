#### On this page

- [Insights](\docs\platform\monitor\insights#insights)
- [Overview](\docs\platform\monitor\insights#overview)
- [Getting Started](\docs\platform\monitor\insights#getting-started)
- [SQL Editor](\docs\platform\monitor\insights#sql-editor)
- [Available Columns](\docs\platform\monitor\insights#available-columns)
- [Data Retention](\docs\platform\monitor\insights#data-retention)
- [Result Limits](\docs\platform\monitor\insights#result-limits)
- [SQL Support](\docs\platform\monitor\insights#sql-support)
- [Supported Functions](\docs\platform\monitor\insights#supported-functions)
- [Aggregate Functions](\docs\platform\monitor\insights#aggregate-functions)
- [SQL Syntax Limitations](\docs\platform\monitor\insights#sql-syntax-limitations)
- [Working with Event Data](\docs\platform\monitor\insights#working-with-event-data)
- [Event-Specific Schema](\docs\platform\monitor\insights#event-specific-schema)
- [Example Queries](\docs\platform\monitor\insights#example-queries)
- [Saved Queries](\docs\platform\monitor\insights#saved-queries)
- [Roadmap](\docs\platform\monitor\insights#roadmap)
- [Coming Soon](\docs\platform\monitor\insights#coming-soon)
- [Future Enhancements](\docs\platform\monitor\insights#future-enhancements)
- [Need Help?](\docs\platform\monitor\insights#need-help)

Platform [Monitor](\docs\platform\monitor\insights)

# Insights

Inngest Insights allows you to query and analyze your event data using SQL directly within the Inngest platform. Every event sent to Inngest contains valuable information, and Insights gives you the power to extract meaningful patterns and analytics from that data.

Insights support is currently in Public Beta. Some details including SQL syntax and feature availability are still subject to change during this period. Read more about the [Public Beta release phase here](\docs\release-phases#public-beta) and the [roadmap here](\docs\platform\monitor\insights#roadmap) .

## [Overview](\docs\platform\monitor\insights#overview)

Insights provides an in-app SQL editor and query interface where you can:

- Query event data using familiar SQL syntax
- Save and reuse common queries
- Analyze patterns in your event triggers
- Extract business intelligence from your workflows

Currently, you can **only query events** . Support for querying function runs will be added in future releases.

## [Getting Started](\docs\platform\monitor\insights#getting-started)

Access Insights through the Inngest dashboard by clicking on the "Insights" tab in the left navigation.

Getting Started Dashboard View

<!-- image -->

We have several pre-built query templates to help you get started exploring your data.

Getting Started Templates View

<!-- image -->

## [SQL Editor](\docs\platform\monitor\insights#sql-editor)

The Insights interface includes a full-featured SQL editor where you can:

- Write and execute SQL queries against your event data
- Save frequently used queries for later access
- View query results in an organized table format
- Access query history and templates from the sidebar

Sql Editor View

<!-- image -->

### [Available Columns](\docs\platform\monitor\insights#available-columns)

When querying events, you have access to the following columns:

| Column   | Type                | Description                                                                                           |
|----------|---------------------|-------------------------------------------------------------------------------------------------------|
| id       | String              | Unique identifier for the event                                                                       |
| name     | String              | The name/type of the event                                                                            |
| data     | JSON                | The event payload data - users can send any JSON structure here                                       |
| ts       | Unix timestamp (ms) | [reference](https://www.unixtimestamp.com/)  Unix timestamp in milliseconds when the event occurred - |
| v        | String              | Event format version                                                                                  |

For more details on the event format, see the [Inngest Event Format documentation](\docs\features\events-triggers\event-format) .

### [Data Retention](\docs\platform\monitor\insights#data-retention)

Refer to [pricing plans](\pricing) for data retention limits.

### [Result Limits](\docs\platform\monitor\insights#result-limits)

- Current page limit: **1000 rows**
- Future updates will support larger result sets through async data exports

## [SQL Support](\docs\platform\monitor\insights#sql-support)

Insights is built on ClickHouse, which provides powerful SQL capabilities with some differences from traditional SQL databases.

Sql Editor View

<!-- image -->

### [Supported Functions](\docs\platform\monitor\insights#supported-functions)

### [Arithmetic Functions](\docs\platform\monitor\insights#arithmetic-functions)

Basic mathematical operations and calculations. [View ClickHouse arithmetic functions documentation](https://clickhouse.com/docs/sql-reference/functions/arithmetic-functions)

### [String Functions](\docs\platform\monitor\insights#string-functions)

String manipulation and search capabilities.

- [String search functions](https://clickhouse.com/docs/sql-reference/functions/string-search-functions)
- [String manipulation functions](https://clickhouse.com/docs/sql-reference/functions/string-functions)

### [JSON Functions](\docs\platform\monitor\insights#json-functions)

Essential for working with `events.data` payloads. [View ClickHouse JSON functions documentation](https://clickhouse.com/docs/sql-reference/functions/json-functions)

### [Date/Time Functions](\docs\platform\monitor\insights#date-time-functions)

For analyzing event timing and patterns. [View ClickHouse date/time functions documentation](https://clickhouse.com/docs/sql-reference/functions/date-time-functions)

### [Other Supported Function Categories](\docs\platform\monitor\insights#other-supported-function-categories)

- [Logical functions](https://clickhouse.com/docs/sql-reference/functions/logical-functions)
- [Rounding functions](https://clickhouse.com/docs/sql-reference/functions/rounding-functions)
- [Type conversion functions](https://clickhouse.com/docs/sql-reference/functions/type-conversion-functions)
- [Functions for nulls](https://clickhouse.com/docs/sql-reference/functions/functions-for-nulls)
- [ULID functions](https://clickhouse.com/docs/sql-reference/functions/ulid-functions)

### [Aggregate Functions](\docs\platform\monitor\insights#aggregate-functions)

The following aggregate functions are supported:

| Function      | Description                                                                                                              |
|---------------|--------------------------------------------------------------------------------------------------------------------------|
| ARRAY_AGG()   | [Aggregates values into an array](https://clickhouse.com/docs/sql-reference/aggregate-functions/reference/grouparray)  * |
| AVG()         | Calculates average                                                                                                       |
| COUNT()       | Counts rows                                                                                                              |
| MAX()         | Finds maximum value                                                                                                      |
| MIN()         | Finds minimum value                                                                                                      |
| STDDEV_POP()  | Population standard deviation                                                                                            |
| STDDEV_SAMP() | Sample standard deviation                                                                                                |
| SUM()         | Calculates sum                                                                                                           |
| VAR_POP()     | Population variance                                                                                                      |
| VAR_SAMP()    | Sample variance                                                                                                          |
| median()      | Finds median value                                                                                                       |

### [SQL Syntax Limitations](\docs\platform\monitor\insights#sql-syntax-limitations)

Some SQL features are not yet supported but are planned for future releases:

- **CTEs (Common Table Expressions)** using `WITH`
- **`IS`** **operator**
- **`NOT`** **operator**

## [Working with Event Data](\docs\platform\monitor\insights#working-with-event-data)

### [Event-Specific Schema](\docs\platform\monitor\insights#event-specific-schema)

Within **`events.data`** , users can send any JSON they want, so the structure and available fields will be specific to their payloads. You can use ClickHouse's JSON functions to extract and query specific fields within your event data.

### [Example Queries](\docs\platform\monitor\insights#example-queries)

### [Basic Event Filtering](\docs\platform\monitor\insights#basic-event-filtering)

Copy Copied

```
SELECT count ( * )
FROM events
WHERE name = 'inngest/function.failed'
AND simpleJSONExtractString( data , 'function_id' ) = 'generate-report'
AND ts > toUnixTimestamp(addHours( now (), - 1 )) * 1000 ;
```

### [Extracting JSON Data and Aggregating](\docs\platform\monitor\insights#extracting-json-data-and-aggregating)

Copy Copied

```
SELECT simpleJSONExtractString( data , 'user_id' ) as user_id, count ( * )
FROM events
WHERE name = 'order.created'
GROUP BY user_id
ORDER BY count ( * ) DESC
LIMIT 10 ;
```

## [Saved Queries](\docs\platform\monitor\insights#saved-queries)

You can save frequently used queries for quick access. Queries are only saved private for you to use; they are not shared across your Inngest organization.

## [Roadmap](\docs\platform\monitor\insights#roadmap)

### [Coming Soon](\docs\platform\monitor\insights#coming-soon)

- Query support for function runs
- `received_at` column for tracking event receipt time
- Pagination for large result sets
- Async data exports for results larger than 1000 rows

### [Future Enhancements](\docs\platform\monitor\insights#future-enhancements)

- Support for CTEs (Common Table Expressions)
- `IS` and `NOT` operators
- Advanced visualization capabilities

## [Need Help?](\docs\platform\monitor\insights#need-help)

If you encounter issues or have questions about Insights:

1. Check this documentation for common solutions
2. Review the [ClickHouse SQL reference](https://clickhouse.com/docs/sql-reference/) for advanced function usage
3. Contact support through the Inngest platform

*Insights is actively under development. Features and column names may change as we continue to improve the product.*