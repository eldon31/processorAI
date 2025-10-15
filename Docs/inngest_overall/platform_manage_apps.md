#### On this page

- [Apps](\docs\platform\manage\apps#apps)
- [Apps Overview](\docs\platform\manage\apps#apps-overview)
- [Unattached Syncs](\docs\platform\manage\apps#unattached-syncs)
- [App management](\docs\platform\manage\apps#app-management)
- [Overview](\docs\platform\manage\apps#overview)
- [Syncs](\docs\platform\manage\apps#syncs)
- [Archive an app](\docs\platform\manage\apps#archive-an-app)

Platform [Manage](\docs\platform\environments)

# Apps

Inngest enables you to manage your Inngest Functions deployments via [Inngest Environments and Apps](\docs\apps) . Inngest Environments (ex, production, testing) can contain multiple Apps that can be managed using:

- [The Apps Overview](\docs\platform\manage\apps#apps-overview) - A quick access to all apps, including the unattached syncs
- [Syncs management](\docs\platform\manage\apps#syncs) - Run App diagnostics and access all syncs history
- [Archiving](\docs\platform\manage\apps#archive-an-app) - Archive inactive Apps

## [Apps Overview](\docs\platform\manage\apps#apps-overview)

The Apps Overview is the main entry page of the Inngest Platform, listing the Apps of the active Environment, visible in the top left Environment selector:

The home page of the Inngest Platform is an Apps listing. Each App item display the App status along with some essential information such as active Functions count and the SDK version used.

<!-- image -->

The Apps Overview provides all the essential information to assess the healthy sync status of your active Apps: Functions identified, Inngest SDK version. You can switch to "Archived Apps" using the top left selector.

### [Unattached Syncs](\docs\platform\manage\apps#unattached-syncs)

Automatic syncs or an App misconfiguration can result in syncs failing to attach to an existing app.

These unsuccessful syncs are listed in the "Unattached Syncs" section where detailed information are available, helping in resolving the issue:

The Unattached Syncs list provides detailed information regarding failed syncs.

<!-- image -->

Please read our [Syncs Troubleshooting section](\docs\apps\cloud#troubleshooting) for more information on how to deal with failed sync.

## [App management](\docs\platform\manage\apps#app-management)

### [Overview](\docs\platform\manage\apps#overview)

Navigating to an App provides more detailed information (SDK version and language, deployment URL) that can be helpful when interacting with our Support.

You will also find quick access to all active functions and their associated triggers:

Clicking on an App from the home page will give you more detailed information about the current App deployment such as: the Functions list, the target URL. Those information can be useful when exchanging with Support.

<!-- image -->

### [Syncs](\docs\platform\manage\apps#syncs)

Triggering a Manual Sync from the Inngest Platform sends requests to your app to fetch the up-to-date configuration of your applications's functions. At any time, access the history of all syncs from the App page:

The list of an App Syncs provide helpful information to navigate through recent deployments and their associated Functions changes.

<!-- image -->

If a sync fails, try running an App Diagnostic before reaching out to Support:

A App Diagnostic tool is available to help mitigating any sync issues. You can access it by opening the top left menu from the App Syncs listing page.

<!-- image -->

### [Archive an app](\docs\platform\manage\apps#archive-an-app)

Apps can be archived and unarchived at any time. Once an app is archived, all of its functions are archived.

When the app is archived:

- New function runs will not be triggered.
- Existing function runs will continue until completion.
- Functions will be marked as archived, but will still be visible, including their run history.

If you need to cancel all runs prior to completion, read our [cancellation guide](\docs\guides\cancel-running-functions) .

**How to archive an app**

1. Navigate to the app you want to archive. You will find an "Archive" button at the top-right corner of the page.

Archiving an app is accessible from an App page by using the top left menu.

<!-- image -->

2. Confirm that you want to archive the app by clicking "Yes".

A confirmation modal will open to confirm the action. Please note that archiving is not an irreversible action.

<!-- image -->

3. Your app is now archived. 🎉

An archived App features a top informative banner.

<!-- image -->

In the image below, you can see how archived apps look like in Inngest Cloud:

An archived App is still accessible from the Home page, by switching the top left filter to "Archived Apps".

<!-- image -->