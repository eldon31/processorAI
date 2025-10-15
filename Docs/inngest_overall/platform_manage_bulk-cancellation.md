#### On this page

- [Function runs Bulk Cancellation](\docs\platform\manage\bulk-cancellation#function-runs-bulk-cancellation)
- [Cancelling Function runs](\docs\platform\manage\bulk-cancellation#cancelling-function-runs)

Platform [Manage](\docs\platform\environments)

# Function runs Bulk Cancellation

In addition to providing [SDK Cancellation features](\docs\features\inngest-functions\cancellation\cancel-on-events) and a [dedicated REST API endpoint](\docs\guides\cancel-running-functions) , the Inngest Platform also features a Bulk Cancellation UI.

This feature comes in handy to quickly stop unwanted runs directly from your browser.

## [Cancelling Function runs](\docs\platform\manage\bulk-cancellation#cancelling-function-runs)

To cancel multiple Function runs, navigate to the Function's page on the Inngest Platform and open the "All actions" top right menu:

The bulk cancellation button can be found from a Function page, in the top right menu.

<!-- image -->

Clicking the "Bulk cancel" menu will open the following modal, asking you to select the date range that will be used to select and cancel Function runs:

The Bulk cancel modal is composed, from top to bottom, of an input to name the cancellation process and a date range selector. Once those information filled, a estimation of the impacted Function Runs. The cancellation cannot be started if no Function runs match the criteria.

<!-- image -->

The Bulk Cancellation will start cancelling the matching Function runs immediately; the Function runs list will update progressively, showing runs as cancelled:

Once the Bulk Cancellation completed, the impacted Function Runs will appear as "cancelled" in the Function Runs list.

<!-- image -->

You can access the history of running or completed Bulk Cancellation processes via the "Cancellation history" tab:

The "Cancellation history" tab lists all the Bulk Cancellations.

<!-- image -->

**Considerations**

Cancellation is useful to stop running Functions or cancel scheduled ones; however, keep in mind that:

- Steps currently running on your Cloud Provider won't be forced to stop; the Function will cancel upon the current step's completion.
- Cancelling a Function run does not prevent new runs from being enqueued. If you are looking to mitigate an unwanted loop or to cope with an abnormal number of executions, consider using [Function Pausing](\docs\guides\pause-functions) .