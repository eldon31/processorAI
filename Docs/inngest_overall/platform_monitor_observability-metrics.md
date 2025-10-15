#### On this page

- [Observability &amp; Metrics](\docs\platform\monitor\observability-metrics#observability-and-metrics)
- [Function runs observability](\docs\platform\monitor\observability-metrics#function-runs-observability)
- [Function metrics](\docs\platform\monitor\observability-metrics#function-metrics)
- [Function Status](\docs\platform\monitor\observability-metrics#function-status)
- [Failed Functions](\docs\platform\monitor\observability-metrics#failed-functions)
- [Total runs throughput](\docs\platform\monitor\observability-metrics#total-runs-throughput)
- [Total steps throughput](\docs\platform\monitor\observability-metrics#total-steps-throughput)
- [Backlog](\docs\platform\monitor\observability-metrics#backlog)
- [Events observability](\docs\platform\monitor\observability-metrics#events-observability)
- [Events metrics and logs](\docs\platform\monitor\observability-metrics#events-metrics-and-logs)
- [Global Search](\docs\platform\monitor\observability-metrics#global-search)

Platform [Monitor](\docs\platform\monitor\insights)

# Observability &amp; Metrics

With hundreds to thousands of events going through your Inngest Apps, triggering multiple Function runs, getting a clear view of what is happening at any time is crucial.

The Inngest Platform provides observability features for both Events and Function runs, coupled with Event logs and [a detailed Function Run details to inspect arguments and steps timings](\docs\platform\monitor\inspecting-function-runs) .

## [Function runs observability](\docs\platform\monitor\observability-metrics#function-runs-observability)

The Functions list page provides the first round of essential information in one place with:

- **Triggers** : Events or Cron schedule
- **Failure rate** : enabling you to quickly identify a surge of errors
- **Volume** : helping in identifying possible drops in processing

The Functions list page lists all available Functions with essential information such as associated Events, Failure rate and Volume.

<!-- image -->

## [Function metrics](\docs\platform\monitor\observability-metrics#function-metrics)

Navigating to a Function displays the Function metrics page, composed of 7 charts:

Clicking on a Function leads us to the Function view, composed of 7 charts.

<!-- image -->

All the above charts can be filtered based on a time range (ex: last 24 hours), a specific Function or [App](\docs\platform\manage\apps) .

Let's go over each chart in detail:

### [Function Status](\docs\platform\monitor\observability-metrics#function-status)

The Function Status chart is a pie chart where each part represents a function status (failed, succeed or cancelled).

<!-- image -->

The Function Status chart provides a snapshot of the number of Function runs grouped by status.

**How to use this chart?**

This chart is the quickest way to identify an unwanted rate of failures at a given moment.

### [Failed Functions](\docs\platform\monitor\observability-metrics#failed-functions)

The *Failed Functions* chart displays the top 6 failing functions with the frequency of failures.

**How to use this chart?**

You can leverage this chart to identify a possible elevated rate of failures and quickly access the Function runs details from the "View all" button.

<!-- image -->

### [Total runs throughput](\docs\platform\monitor\observability-metrics#total-runs-throughput)

The Total runs throughput is a line chart featuring the total number of Function runs per application.

<!-- image -->

The *Total runs throughput* is a line chart featuring the **rate of Function runs started per app** . This shows the performance of the system of how fast new runs are created and are being handled.

**How to use this chart?**

Flow control might intentionally limit throughput, this chart is a great way to visualize it.

### [Total steps throughput](\docs\platform\monitor\observability-metrics#total-steps-throughput)

The Total steps throughput is a line chart featuring the total number of Function steps running at a given time, per application.

<!-- image -->

The *Total steps throughput* chart represents **the rate of which steps are executed, grouped by the selected Apps** .

**How to use these charts?**

The *Total steps throughput* chart is helpful to assess the configuration of your Inngest Functions.

For example, a low *Total steps throughput* might be linked to a high number of concurrent steps combined with a restrictive concurrency configuration.

### [Backlog](\docs\platform\monitor\observability-metrics#backlog)

The\_Backlog highlights the number of Function runs waiting to processed at a given time bucket.

<!-- image -->

The *Backlog* highlights the number of **Function runs waiting to processed at a given time bucket, grouped by the selected Apps** .

**How to use this chart?**

This chart is useful to assess the *Account Concurrency* capacity of your account and to identify potential spikes of activity.

## [Events observability](\docs\platform\monitor\observability-metrics#events-observability)

Events volume and which functions they trigger can become hard to visualize.

Thankfully, the Events page gives you a quick overview of the volume of Events being sent to your Inngest account:

The Events page lists the available Event type. Each list item features the event name along with its associated Functions and a events volume indicator.

<!-- image -->

Get more detailed metrics for a dedicated event by navigating to it from the list:

## [Events metrics and logs](\docs\platform\monitor\observability-metrics#events-metrics-and-logs)

The Event page helps quickly visualize the throughput (the rate of event over time) and functions associated with this event.

The event occurrences feature a "Source" column, which is helpful when an event is triggered from multiple Apps (ex, using different languages):

Clicking on an Events leads us to the Event page that displays, at the top, a chart of events occurrences over the last 24 hours and at the list of associated events.

<!-- image -->

Clicking on a specific event will redirect you to its Logs.

The Event Logs view provides the most precise information, with the linked Function run and raw event data.

Such information, combined with the ability to forward the event to your Local Dev Server instance, makes debugging events much quicker:

Clicking on an event of the below list open the Event Logs view, providing much detailed information such as the Event Payload and triggered Functions.

<!-- image -->

## [Global Search](\docs\platform\monitor\observability-metrics#global-search)

The global search feature helps you quickly find apps, functions, and events in your account using their names or **IDs** . It's more than a search tool - you can also use it to navigate around the environment and take quick actions or access helpful resources.

To open global search, press **Command (⌘) / Ctrl + K** on your keyboard, or click the search icon in the top-left corner.

Global search snippet

<!-- image -->