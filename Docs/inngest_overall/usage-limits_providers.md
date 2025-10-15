#### On this page

- [Providers' Usage Limits](\docs\usage-limits\providers#providers-usage-limits)

Platform [Deployment](\docs\platform\deployment) [Cloud Providers](\docs\deploy\vercel)

# Providers' Usage Limits

As your functions' code runs on the hosting provider of your choice, you will be subject to provider or billing plan

limits separate from

[Inngest's own limits](\docs\usage-limits\inngest) .

Here are the known usage limits for each provider we support based on their documentation.

|                        | Payload size   | Concurrency         | Timeout                   |
|------------------------|----------------|---------------------|---------------------------|
| AWS Lambda             | 6MB - 20MB     | 1000                | 15m                       |
| Google Cloud Functions | 512KB - 32MB   | 3000 (1st gen only) | 10m - 60m                 |
| Cloudflare Workers     | 100MB - 500MB  | 100 - 500           | N/A                       |
| Vercel                 | 4MB - 4.5MB    | 1000                | 10s - 900s, N/A (Edge Fn) |
| Netlify                | 256KB - 6MB    | Undocumented        | 10s - 15m                 |
| DigitalOcean           | 1MB            | 120                 | 15m                       |
| Fly.io                 | Undocumented   | User configured     | Undocumented              |

For more details tailored to your plan, please check each provider's website.