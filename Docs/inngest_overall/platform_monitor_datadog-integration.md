#### On this page

- [Datadog integration](\docs\platform\monitor\datadog-integration#datadog-integration)
- [Setup](\docs\platform\monitor\datadog-integration#setup)
- [Metrics](\docs\platform\monitor\datadog-integration#metrics)
- [Granularity and delay](\docs\platform\monitor\datadog-integration#granularity-and-delay)

Platform [Monitor](\docs\platform\monitor\insights)

# Datadog integration

Inngest has a native Datadog integration which publishes metrics from your Inngest environment to your Datadog account. This enables you to monitor your Inngest functions and configure alerts based on your Inngest metrics. No Datadog agent configuration is required.

The Datadog integration comes with a default dashboard that you can use to monitor your Inngest functions.

<!-- image -->

## [Setup](\docs\platform\monitor\datadog-integration#setup)

1

Navigate to the Inngest integration's page in the Datadog dashboard:

[Open Datadog integration](https://app.datadoghq.com/integrations/inngest)

If you have multiple Inngest organizations, please use the " [Switch organization](https://app.inngest.com/organization-list) " button located in the user menu in the Inngest dashboard to ensure that you have the correct organization selected.

2

Click the " **Install integration** " button at the top right.

The Datadog integration's install page

<!-- image -->

3

Now click " **Connect Accounts** " to connect your Inngest account to Datadog. This will open an authentication flow. You will be asked to authorize Inngest to access your Datadog account.

The Datadog integration's connect accounts page

<!-- image -->

4

Once you have connected your Inngest account to Datadog, you will be redirected to [the Datadog integration page in the Inngest dashboard](https://app.inngest.com/settings/integrations/datadog) . The connected Inngest environment will begin setup which may take up to 60 seconds to complete.

Here you can connect additional Inngest environments to connect to Datadog as well as add add additional Datadog accounts to send metrics to.

You will see the granularity and delay of the metrics that will be sent to Datadog based on your Inngest [billing plan](\pricing) .

The Datadog integration page

<!-- image -->

The setup process may take up to 60 seconds to complete. You can refresh the page to see the status of the setup.

5

Once the setup is complete, you can navigate to [the Dashboards tab in the Datadog dashboard](https://app.datadoghq.com/dashboard/lists?q=Inngest) and located the newly installed "Inngest" dashboard.

This dashboard (pictured at the top of this page), gives some default visualizations to help you get started. You can also create your own custom dashboards to monitor your Inngest functions using the `inngest.*` metrics.

## [Metrics](\docs\platform\monitor\datadog-integration#metrics)

The integration publishes several metrics including the metrics below. You can also view a full list of metrics available from the integration's "Data Collected" tab:

| Metric Name                                               | Description                                                                                   |
|-----------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **inngest.function\_run.scheduled.total**  (count)        | Function runs scheduled during the time interval  *Unit: run*                                 |
| **inngest.function\_run.started.total**  (count)          | Function runs that started during the time interval  *Unit: run*                              |
| **inngest.function\_run.ended.total**  (count)            | Function runs that ended during the time interval  *Unit: run*                                |
| **inngest.function\_run.rate\_limited.total**  (count)    | Function runs that did not execute due to rate limiting during the time interval  *Unit: run* |
| **inngest.step.output\_bytes.total**  (count)             | Bytes used by step outputs during the time interval  *Unit: byte*                             |
| **inngest.sdk.req\_scheduled.total**  (count)             | Step executions scheduled during the time interval  *Unit: step*                              |
| **inngest.sdk.req\_started.total**  (count)               | Step executions started during the time interval  *Unit: step*                                |
| **inngest.sdk.req\_ended.total**  (count)                 | Step executions that ended during the time interval  *Unit: step*                             |
| **inngest.steps.scheduled**  (gauge)                      | Steps currently scheduled  *Unit: step*                                                       |
| **inngest.steps.running**  (gauge)                        | Steps currently running  *Unit: step*                                                         |
| **inngest.steps.sleeping**  (gauge)                       | Steps currently sleeping  *Unit: step*                                                        |
| **inngest.metric\_export\_integration\_healthy**  (gauge) | Indicates the Inngest integration successfully sent metrics to Datadog  *Unit: success*       |

## [Granularity and delay](\docs\platform\monitor\datadog-integration#granularity-and-delay)

The Datadog integration is available to all paid plans and is subject to the following limits.

| Plan       | Granularity   | Delay      |
|------------|---------------|------------|
| Basic      | 15 minutes    | 15 minutes |
| Pro        | 5 minutes     | 5 minutes  |
| Enterprise | 1 minute      | Immediate  |