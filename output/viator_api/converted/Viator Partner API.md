## Viator Partner API (2.0)

Download OpenAPI specification:

Download

License:

CC BY 4.0

## Updates

## Latest updates:

| Date        | Description                                                                                                                                                                                                                                                                                             |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 11 Sep 2025 | Updated /bookings/modified-since response with new eventTypes and enabled endpoint access to all partner types.                                                                                                                                                                                         |
| 01 Jul 2025 | Added /amendment/check/{booking-reference} , /amendment/quote and /amendment/amend/{quote-reference} endpoints to Bookings section                                                                                                                                                                      |
| 27 Mar 2025 | Update /search/freetext request section add filtering by tags for "searchType": "PRODUCTS"                                                                                                                                                                                                              |
| 20 Mar 2025 | Added /products/recommendations to Products section. This endpoint will provide product-to-product recommendations to users.                                                                                                                                                                            |
| 19 Mar 2025 | Updated endpoints /availability/schedules/{product-code} , /availability/schedules/bulk , /availability/schedules/modified-since , /availability/check , /search/freetext , /products/search , /bookings/cart/hold and /bookings/hold as well as Inclusions & exclusions with Extra Charges information |
| 11 Feb 2025 | Removed TRANSACTION_NOT_ALLOWED , CARD_INACTIVE and CARD_RESTRICTED rejection reasons from /bookings/cart/book .                                                                                                                                                                                        |
| 4 Dec 2024  | Updated /bookings/cart/book response with the following new rejection reason: PROCESSOR_ISSUE_WITH_PAYMENT .                                                                                                                                                                                            |

| Date        | Description                                                                                                                                                                                                                                                              |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 19 Nov 2024 | Updated /bookings/cart/book response with the following new rejection reasons: SUSPECTED_FRAUD , SOFT_DECLINE , HARD_DECLINE , THREE_D_SECURE_REQUIRED , INTERNAL_ERROR , PROCESSOR_UNAVAILABLE .                                                                        |
| 24 Oct 2024 | Deprecated /v1/product/photos endpoint                                                                                                                                                                                                                                   |
| 23 Oct 2024 | Added /attractions/search and /attractions/{attraction-id} to Attractions section Added /destinations to Auxiliary section Updated Access to endpoints section to include new endpoints and removed the ones marked for deprecation Updated Resolving references section |
| 21 Oct 2024 | Removed VIATOR_EXCLUSIVE flag from product search endpoints                                                                                                                                                                                                              |
| 1 Oct 2024  | Removed COVID-19 safety attributes from AdditionalInfo schema (part of product content response; e.g., from /products/{product-code} endpoint)                                                                                                                           |
| 6 Aug 2024  | Changes to behaviour with DEFAULT tour grade for product, availability, book hold and confirm endpoints. See note at end of section Product Option Code . Note: these changes are backwards compatible.                                                                  |
| 29 Jul 2024 | Updated /bookings/modified-since response with new eventType: CUSTOMER_CANCELLATION, for Customer initiated cancellations.                                                                                                                                               |
| 14 Mar 2024 | Updated /bookings/cart/book response with the following new rejection reasons: INSUFFICIENT_FUNDS , INVALID_PAYMENT_DETAILS , TRANSACTION_NOT_ALLOWED , CARD_INACTIVE and CARD_RESTRICTED . Updated /bookings/status response with ON_HOLD status                        |
| 13 Feb 2024 | Updated /suppliers/search/product-codes with the following new attributes: supplierAgreedToLegalCompliance , registrationCountry , tradeRegisterName and registeredBusinessNumber . Also updated the ContactDetails schema with a new attribute countryCode .            |
| 11 Sep 2023 | Added support for PDF vouchers. Made bookerInfo firstName required to match definition.                                                                                                                                                                                  |
| 5 Jul 2023  | Added /bookings/cart/hold and /bookings/cart/book to Bookings section Added /v1/checkoutsessions/{sessionToken}/paymentaccounts to Payments section                                                                                                                      |
| 15 May      | Modified Accept-Language-header-parameter section to accurately reflect currently allowed values                                                                                                                                                                         |

| Date        | Description                                                                                                                                                                                                                                                                                                                                                        |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2023        |                                                                                                                                                                                                                                                                                                                                                                    |
| 16 Mar 2023 | Added /search/freetext and /suppliers/search/product-codes to Access to endpoints section                                                                                                                                                                                                                                                                          |
| 6 Mar 2023  | Added Canadian dollars (CAD) as currency option in request and response to /bookings/hold , /bookings/book and /bookings/status endpoints                                                                                                                                                                                                                          |
| 6 Jan 2023  | Added two new COVID-19 safety attributes to AdditionalInfo schema (part of product content response; e.g., from /products/{product-code} endpoint)                                                                                                                                                                                                                 |
| 4 Jan 2023  | Updated or created ProductSearchFiltering , ProductSummary , ProductSearchSorting , ProductSearchFlag , TranslationDetails , SearchDurationInfo and SearchRatingInfo schemata for the /products/search endpoint request/response, updated example request and merchant and affiliate response examples, and updated Postman collections in line with these changes |
| 3 Jan 2023  | Updated example request and response for /search/freetext endpoint                                                                                                                                                                                                                                                                                                 |
| 12 Dec 2022 | Added /search/freetext endpoint                                                                                                                                                                                                                                                                                                                                    |
| 10 Nov 2022 | Updated /bookings/hold and /bookings/modified-since/acknowledge descriptions                                                                                                                                                                                                                                                                                       |

## Update history:

- All significant modifications made to this document since its creation can be found in the Update history section.

## Support

Onboarding / integration

If you require help or technical advice while you are carrying out your integration, please contact the onboarding team via email at: affiliateapi@tripadvisor.com

## Integration guides

Our onboarding specialists have put together in-depth guides covering various topics to help you during your integration.

## Site certification for merchant partners

If you are a merchant partner, once your API integration has been completed, it must pass certification prior to going live in order to ensure data integrity and the appropriate use of API services. Please peruse and bear in mind our certification requirements prior to and during development.

## Operational support

If are a merchant partner, have completed your integration and your site is operational, please see the Partner Help Center - Merchant partner support page for information about what to do if you encounter a problem and require support.

## About

## Viator Partner-API v2

## What is it?

The Viator Partner API v2 comprises a set of endpoints that can support the operation of a fully-featured tours and experiences booking website or application; or, it can be integrated with your existing travelbooking software.

The API exposes a variety of services that allow the retrieval of all product details, such as descriptive text and structured metadata, pricing, terms and conditions, photos and reviews. This data can either be ingested and managed on your local system, or calls can be made in real time to retrieve content in response to your users' activity on your systems.

The API allows product content, pricing and availability data to be retrieved in bulk or queried in real-time, it can perform pricing calculations according to the number and type of traveler and product option combinations available, and it supports availability and pricing holds as part of its booking and bookingcancellation functionality.

## Who is it for?

The Viator Partner-API is a designed for use by organizations partnered with Viator as Affiliate partners or Merchant partners .

## Affiliate partners

Affiliate partners have full access to the areas of the API relating to content, but sales of Viator products must be carried out on the Viator site itself.

When a customer wishes to book a product from an affiliate's site, they are instead redirected to the relevant product page on viator.com via a unique URL in order to complete the purchase. Once on the Viator site, a cookie is set such that all transactions will accrue a commission for that partner until the cookie expires.

Purchases of products originating from the affiliate's site are recorded and a commission on these sales is paid periodically.

For more information on this partner type, see: Viator's Affiliate API Solution

## Merchant partners

The merchant partner relationship is one in which the partner is the merchant of record ; i.e., the partner takes full responsibility for all financial records and transactions carried out by their users, as well as providing customer support with regard to providing general assistance, processing cancellations and refunds, and liaising between suppliers and customers when the need to communicate arises.

For more information on this partner type, see: Viator's Merchant API Solution

## New features in this version

The Viator Partner-API v2.0 is a fully-redesigned system with regard to our previous API products. It includes all key fuctionality available in previous versions, but now provides nearly fully-structured data elements, and a more modern, concise and easily-understandable interface.

In addition, we have made significant improvements to performance across all functions of the API, and particularly in the area of product content and availability data ingestion.

## Simplified and optimized data ingestion

Data ingestion has been greatly improved over previous versions of this API. Now, partners need only perform a single initial ingestion of data; then, only new and updated product content, availability and pricing information is retrieved as a 'delta update' as it becomes available.

## In addition:

- A single end-point allows both bulk ingestion and delta updates, which can be controlled using a pagination cursor or with a time-stamp parameter to allow for point-in-time ingestion of any new updates and easy recovery from ingestion failure
- The structure of a product's pricing and availability schedules has been simplified to reduce response size

## Product content

- All pricing is standardized to the supplier's currency, avoiding the need to update on account of exchange rate fluctuations
- Structured location, tag, booking question, review and photo data is available from separate endpoints to allow for parallel ingestion, and resusable data can be ingested once and applied globally

## Availability schedule information

Improvements to availability schedule ingestion performance and usability have been achieved:

- Availability is now communicated by providing an overall schedule season and specifying unavailable dates instead of available dates, a significantly more compact format that improves transfer speeds and minimizes storage needs
- Availability and pricing information is given on a days-of-the-week basis, which can help with filtering and improving visibility of product availability for customers.
- Information about special pricing periods that may be running throughout a product's seasons is included and is easy to interpret, allowing partners to surface promotions to customers.
- Accurate pricing and applicability information for products that have 'per unit' (group) pricing is now included in the availability &amp; pricing response; whereas support for this pricing model was limited in previous versions of this API. This allows partners to improve pricing exposure for these products.

## Structure-rich content

Providing structured content is a major focus of this API. Product information that was previously stored as natural-language descriptions in a single, lengthy field is now represented in intuitively-structured, machine-interpretable schemata that empowers partners to apply finely-grained merchandising control, including:

- Tour itineraries with comprehensive location data to allow for graphical display and advanced search
- Tour details, inclusions and dynamic health &amp; safety information to support changing requirements due to global pandemic response initiatives
- Machine-parseable booking questions and answers

## Improved real-time availability and pricing checking

## The real-time availability check endpoint :

- Allows you to check availability and pricing in real-time for a specific product / product-option / date / starting time / pax mix combination
- Returns the ticket availability status along with a pricing breakdown (by age band) and total price (all age bands) in a simplified format to reduce response size
- Pricing components are stated explicitly, including the Recommended Retail Price (RRP), partner net price, special-offer pricing and booking fee component details

## Improved booking workflow

The booking workflow now includes an optional booking-hold step, which allows you greater predictability of a successful booking, thereby increasing conversion rates by decreasing friction in the booking flow.

The booking hold endpoint supports two kinds of hold:

- Inventory/availability hold (increased likelihood of receiving a booking confirmation)
- Pricing hold (mitigates against pricing changes at the time of booking)

The real-time availability and pricing endpoint also delivers ~5% faster performance than previous versions of this API.

## Access to endpoints

The API endpoints accessible to you depend on which kind of partner you are; affiliate or merchant.

Basic-access Affiliate partners have access to a limited subset of the non-transactional endpoints of the Viator Partner API. The basic-access tier allows affiliates to quickly get started building their site with fewer complexities. The following step-by-step guide explains how to do it: Golden Path - Basic Access Affiliate Partners

Full-access Affiliate partners have access to all non-transactional endpoints; i.e., everything except booking, booking hold and booking cancellation endpoints.

Full-access + Booking Affiliate partners have access to all the same endpoints as Full-access Affiliate partners as well as transactional endpoints. i.e., including cart booking, cart booking hold and booking cancellation endpoints.

Merchant partners have access to all endpoints.

The following table describes which partner types have access to which endpoints:

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

✅

| Endpoint                                   | Basic- access Affiliate   | Full- access Affiliate   | Full- access + Booking Affiliate   | Merc   |
|--------------------------------------------|---------------------------|--------------------------|------------------------------------|--------|
| /products/modified-since                   | ❌                        | ✅                       | ✅                                 |        |
| /products/bulk                             | ❌                        | ✅                       | ✅                                 |        |
| /products/{product-code}                   | ✅                        | ✅                       | ✅                                 |        |
| /products/tags                             | ✅                        | ✅                       | ✅                                 |        |
| /products/booking-questions                | ❌                        | ❌                       | ✅                                 |        |
| /products/search                           | ✅                        | ✅                       | ✅                                 |        |
| /products/recommendations                  | ❌                        | ✅                       | ✅                                 |        |
| /attractions/search                        | ✅                        | ✅                       | ✅                                 |        |
| /attractions/{attraction-id}               | ✅                        | ✅                       | ✅                                 |        |
| /availability/check                        | ❌                        | ✅                       | ✅                                 |        |
| /availability/schedules/{product-code}     | ✅                        | ✅                       | ✅                                 |        |
| /availability/schedules/bulk               | ❌                        | ✅                       | ✅                                 |        |
| /availability/schedules/modified-since     | ❌                        | ✅                       | ✅                                 |        |
| /bookings/cart/hold                        | ❌                        | ❌                       | ✅                                 |        |
| /bookings/cart/book                        | ❌                        | ❌                       | ✅                                 |        |
| /bookings/hold                             | ❌                        | ❌                       | ❌                                 |        |
| /bookings/book                             | ❌                        | ❌                       | ❌                                 |        |
| /bookings/status                           | ❌                        | ❌                       | ✅                                 |        |
| /bookings/cancel-reasons                   | ❌                        | ❌                       | ✅                                 |        |
| /bookings/{booking-reference}/cancel-quote | ❌                        | ❌                       | ✅                                 |        |
| /bookings/{booking-reference}/cancel       | ❌                        | ❌                       | ✅                                 |        |
| /bookings/modified-since                   | ✅                        | ✅                       | ✅                                 |        |
| /bookings/modified-since/acknowledge       | ❌                        | ❌                       | ✅                                 |        |
| /amendment/check/{booking-reference}       | ❌                        | ❌                       | ✅                                 |        |
| /amendment/quote                           | ❌                        | ❌                       | ✅                                 |        |

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

✅

<!-- image -->

<!-- image -->

❌

✅

<!-- image -->

✅

<!-- image -->

✅

<!-- image -->

✅

<!-- image -->

✅

<!-- image -->

✅

<!-- image -->

| Endpoint                                            | Basic- access Affiliate   | Full- access Affiliate   | Full- access + Booking Affiliate   | Merc   |
|-----------------------------------------------------|---------------------------|--------------------------|------------------------------------|--------|
| /amendment/amend/{quote-reference}                  | ❌                        | ❌                       | ✅                                 |        |
| /v1/checkoutsessions/{sessionToken}/paymentaccounts | ❌                        | ❌                       | ✅                                 |        |
| /search/freetext                                    | ✅                        | ✅                       | ✅                                 |        |
| /destinations                                       | ✅                        | ✅                       | ✅                                 |        |
| /locations/bulk                                     | ✅                        | ✅                       | ✅                                 |        |
| /exchange-rates                                     | ✅                        | ✅                       | ✅                                 |        |
| /reviews/product                                    | ❌                        | ✅                       | ✅                                 |        |
| /suppliers/search/product-codes                     | ❌                        | ❌                       | ✅                                 |        |

## Authentication

## API-key

Access to the API is managed using an API key that is included as a header parameter to every call made to all API endpoints described in this document.

| Header parameter name   | Example value                        |
|-------------------------|--------------------------------------|
| exp-api-key             | bcac8986-4c33-4fa0-ad3f-75409487026c |

If you do not know the API key for your organization, please contact your business development account manager for these details.

Please note that language localization is now controlled on a per-call basis. Previously, localization settings were configured per API-key; whereas, under the present scheme, organizations have a single API

key .

Language localization is accomplished by specifying the desired language as a header parameter ( Accept-Language ). See Accept-Language header for available language codes.

## Localization

## Accept-Language header parameter

The Accept-Language header parameter specifies into which language the natural language fields in the response from each endpoint will be translated.

Note: All partners using the V2 endpoints have access to all supported languages for their partner type.

## Languages available to all partners

<!-- image -->

| Language   | Accept-Language parameter value                                                                  |
|------------|--------------------------------------------------------------------------------------------------|
| English    | en , en-US en-AU , en-CA , en-GB , en-HK , en-IE , en-IN , en-MY , en-NZ , en-PH , en-SG , en-ZA |
| Danish     | da                                                                                               |
| Dutch      | nl , nl-BE                                                                                       |
| Norwegian  | no                                                                                               |
| Spanish    | es , es-AR , es-CL , es-CO , es-MX , es-PE , es-VE                                               |
| Swedish    | sv                                                                                               |
| French     | fr , fr-BE , fr-CA , fr-CH                                                                       |
| Italian    | it , it-CH                                                                                       |
| German     | de , de-DE                                                                                       |
| Portuguese | pt , pt-BR                                                                                       |
| Japanese   | ja                                                                                               |

## Additional languages available to merchant partners only

| Language              | Accept-Language parameter value   |
|-----------------------|-----------------------------------|
| Chinese (traditional) | zh-TW                             |
| Chinese (simplified)  | zh-CN                             |
| Korean                | ko , ko-KR                        |

## API versioning strategy

In order to ensure the predictability of the behavior of this software, we have implemented a versioning strategy to handle updates to the API contract, as well as a mechanism to specify which version of the API you wish to access.

When we release a new version of this API, partners have the option of continuing to use the existing version or migrating to the updated version when they are ready.

- Note : The version of this API that this document pertains to is that indicated in the title of this document.

The approach to versioning for this API is as follows:

## Global versioning

- Version numbers are global across all endpoints. When a new version of this API is released, all endpoints will increment to the latest version. Viator does not support a heterogenous implementation with calls being made to different endpoints with different version numbers.

## Version release and deprecation

- New versions of this software are released on an ad-hoc basis. Breaking changes will always result in a version increment.
- Viator will inform partners about all version releases, including details about the new features available and any breaking changes that have been introduced.
- Once a version of the API is deprecated, you will have a minimum of 12 months from the date of receiving notice of the change in which to modify your systems. Requests made to deprecated endpoint versions may result in a 400 Bad Request response after 12 months.

## Release candidates

- Release candidate (RC) versions of this API may be made available to allow partners to preview changes in a non-production (sandbox) environment. When available, RC versions will be announced

in this documentation, however these will not be subject to version control and breaking changes may be introduced prior to official release.

## Release criteria

## Backward-compatible changes

The following types of change are considered backward-compatible, and will not result in a version release when introduced. Therefore, partners must ensure their implementation can handle such changes gracefully.

## These changes comprise:

- Introduction of new API endpoints
- Addition of any properties to an endpoint's response schema
- Addition of non-required properties to an endpoint's request schema
- Unexpected receipt of an HTTP redirect response code ( 301 Moved Permanently or 302 Found )
- Addition of new HTTP methods (POST, GET, PUT, PATCH, DELETE, etc.)
- Addition of new key values to existing fields that represent a set, insofar as no operating logic is likely to be affected

## Breaking changes

The following types of change are considered breaking changes and will result in the release of an incremented version of this software:

- Addition of required properties to an endpoint's request schema
- Removal of required properties from an endpoint's request or response schemata
- Changing the data-type or format (e.g., date format) of an existing field in an endpoint's request or response schemata
- Adding, removing or changing the meaning of the HTTP status codes in an endpoint's response
- Removing or modifying the Content-Type on existing endpoints
- Modifying or removing field key values in a set
- Modifying the operationId of an endpoint

## Version specification mechanism

It is mandatory to specify which version of the API you wish to use via the ' Accept' header parameter in the request to each API endpoint; e.g., Accept: application/json;version=2.0 . Omitting the version parameter will result in a 400 Bad Request response.

## Example valid request :

<!-- image -->

## Example error response :

```
{ "code":"INVALID_HEADER_VALUE", "message":"Accept header  is missing or has invalid version information", "timestamp":"2020-09-02T03:43:23.303946Z", "trackingId":"3D45567E:2D25_0A5D03AB:01BB_5F4F14A5_394639:3DB7" }
```

## Accept-Encoding

This API supports gzip compression. Therefore, if you include gzip in the Accept-Encoding header parameter in the request, the API will respond with a gzip-compressed response.

## Endpoint timeout settings

If you wish to implement internal timeout settings for calls to this API, we recommend a setting of 120s .

This is due to the fact that some of the products in our inventory rely on the operation of external supplier systems, which we do not control. Because of that, it may take up to 120s to receive a response when making a booking. In rare cases, booking response times in excess of 120s can sometimes occur.

This means that a booking may have actually succeeded even if the /bookings/book or /bookings/cart/book endpoints time-out or respond with a HTTP 500 error.

Therefore, it is strongly recommended that you check the status of the booking using the /bookings/status endpoint to make sure the booking was not created before you attempt to make the booking again.

Furthermore, you can avoid creating duplicate bookings by making sure that you supply the same value for partnerBookingRef in the request to /bookings/book or /bookings/cart/book as you did for the booking you believe may have failed. The partnerBookingRef value must be unique; therefore, a duplicate booking will not be created.

## Key concepts

## Product content and availability endpoints

## Product content endpoints

You can retrieve the core product-content details from the following endpoints:

- /products/{product-code} : Retrieve content for a single product in real time when the product is selected by the customer
- Used by : API partners who do not ingest the product database, but instead get each product's details only when required
- /products/modified-since : Retrieve content for all products with filtering according to modification date
- Used by : API partners who ingest the entire product catalog into a local database and perform regular delta updates via this endpoint to keep their local data in-sync with Viator's
- /products/bulk : Retrieve content for multiple products, as specified in the request.
- Please note : This endpoint must not be used for ingestion; rather, it should only be used to retrieve product details for the selected products when needed.

## Availability schedules endpoints

You can retrieve the availability schedules for products using the following endpoints:

- /availability/schedules/{product-code} : Retrieve availability schedules for a single product in real time when the product is selected by the customer.
- Used by : API partners who do not ingest the availability database, but instead get the availability schedules associated with a product at the time that it is required
- /availability/schedules/modified-since : Retrieve future availability schedules for all products with filtering according to modification date
- Used by : API partners who ingest all availability schedules into a local database and perform regular delta updates via this endpoint to keep their local data in-sync with Viator's
- /availability/schedules/bulk : Retrieve availability schedules for all products specified in the request.
- Please note : This endpoint must not be used for ingestion; rather, it should only be used to retrieve the availability schedules for the selected products when needed.

## Product options

Any particular product may consist of a number of variants, each of which is referred to as a 'product option'. In previous versions of this API, and in the tours and activities sector in general, product options are also referred to as 'tour grades'.

For example, product options might represent different departure times, tour routes, or packaged extras like additional meals, transport and so forth.

The product options available for a product can be found in the productOptions array in the responses from any of the product content endpoints .

An example productOptions array for the product 5010SYDNEY is as follows:

```
"productOptions": [ { "productOptionCode": "48HOUR", "description": "Duration: 2 days: FREE BONUS ENTRY to Sydney Tower with eve "title": "48 Hour Premium Ticket ", "languageGuides": [...] }, { "productOptionCode": "TG1", "description": "Hop-on Hop-Off and Attractions: 48hr Big Bus Tours, 1-day H "title": "48Hour Deluxe PLUS Attractions", "languageGuides": [...] }, { "productOptionCode": "24HOUR", "description": "Unlimited use on Big Bus Sydney & Bondi Hop-on Hop-off Tour "title": "24 Hour Classic Ticket ", "languageGuides": [...] }, { "productOptionCode": "DELUXE", "description": "Big Bus and Habour Cruise: Combine two great Sydney experie "title": "48 Hour Deluxe Bus and Cruise", "languageGuides": [...] } ]
```

This product has four product options, each with an identifying code given in the productOptionCode field:

- "48HOUR"
- "TG1"
- "24HOUR"
- "DELUXE"

Product options are essentially a subcategory of the tour or activity. You will need to specify the product option you wish to book when making a booking.

## Note on DEFAULT productOptionCodes:

Previously, DEFAULT productOptionCodes were treated differently from other tour grades and were omitted from requests/responses when only one 'DEFAULT' tour grade was present. This special treatment has been removed. All tour grades can be handled consistently. For backward compatibility, DEFAULT codes can still be omitted from some requests, but it is recommended to avoid this practice.

## Availability schedules

The availability schedules endpoints provide information about the availability of a product (along with its various product options and starting times, if they exist) and its pricing in the supplier's currency.

This section explains how to interpret the response from the availability schedules endpoints .

Example response snippet from /availability/schedules/10212P2 (some starting times were removed for brevity):

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

- Each item in the bookableItems[] array contains the availability and pricing data for one of the product's product-options ( productOptionCode ).
- Each item in the seasons[] array describes the availability and pricing for the product-option during the 'season' (period of time) delimited by startDate and endDate . If endDate is not present, this means the season extends 384 days (approximately 12.5 months) into the future from the current date.
- Each item in the pricingRecords[] array describes which days of the week ( daysOfWeek[] ) the availability and pricing data pertains to during the season, as well as which starting times are in operation ( timedEntries[] ) and on which dates ( unavailableDates[] ) each starting time is unavailable (e.g., due to being sold out).
- Each item in the pricingDetails[] array describes the pricing that applies to each age-band during the season.

## Interpreting the availability schedule

We can thereby interpret the availability schedule snippet above as follows:

- For the product-option code "TG45" of product "10212P2" , during the period from "2019-05-01" to "2021-12-31" , on all days of the week , there are starting times at 10:00 and 11:00 .
- The 11:00 starting time is unavailable due to being 'sold out' on the following dates:
- 2020-09-16
- 2020-09-22
- 2020-09-23
- 2020-09-27

- 2020-09-29
- 2020-09-30
- The 10:00 starting time is unavailable due to being 'sold out' on the following dates:
- 2020-09-25
- 2020-09-26
- 2020-09-27
- 2020-09-28
- 2020-09-29
- 2020-09-30
- Infant tickets are free (USD 0)
- Adults are charged per-person; the normal recommended retail price ( original ) is USD 100.02
- A pricing special ( special ) is in effect for adults between 2020-08-28 and 2020-09-30; the special recommended retail price is USD 90.02

Using this information, a complete schedule - including which product-codes and starting times are available on which dates and the pricing (including special discounts) that applies on each date - can be constructed in your database.

## Itineraries

The itinerary for a product is used to communicate to customers what to expect with regard to where they will go when participating in the tour or activity. On the Viator.com website , this information is displayed in the What to expect section on each product's product display page.

Itinerary information is available from this API in a machine-interpretable, structured format that facilitates graphical display and advanced search, should you choose to implement it.

The itinerary information for each product is contained in the itinerary object in the response from any of the product content endpoints .

There are five types of itinerary, and the type is specified in the itinerary.itineraryType field. They are as follows:

| Itinerary type   | itineraryType   | Meaning                                                                                                                                                              |
|------------------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Standard         | "STANDARD"      | A tour-based product (focused on visiting and viewing) that occurs at a single location or proceeds through a set of locations on a single day.                      |
| Activity         | "ACTIVITY"      | An activity-based product (focused on the activity rather than the location) that occurs at a single location or proceeds through a set of locations on a single day |

| Itinerary type   | itineraryType    | Meaning                                                                                                                                                                                                                                    |
|------------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Multi-day tour   | "MULTI_DAY_TOUR" | A tour or activity that occurs over multiple days, and therefore includes food and accommodation                                                                                                                                           |
| Hop-on / hop-off | "HOP_ON_HOP_OFF" | A tour that operates continuously, such as a bus tour, wherein passengers can use their ticket to board and alight as they please at any of the stops along the route                                                                      |
| Unstructured     | "UNSTRUCTURED"   | Not all suppliers have upgraded the itinerary information for their products from a text-based description to structured data; therefore, the itinerary information for a small number of products remains unparseable for the time being. |

## Common elements

The itinerary object is polymorphic depending on the itineraryType , but all variants contain standard information, as follows:

| Field name               | Meaning                                                                                                                                      |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| skipTheLine              | true if a ticket for this product allows participants to attend a location without having to obtain a separate ticket on the occasion itself |
| privateTour              | true if only the travelers who have booked this product will be present; false if it is a shared tour                                        |
| maxTravelersInSharedTour | If privateTour is false , this value represents the maximum number of people that will be able to participate in the tour or activity.       |
| unstructuredDescription  | In the event that structured information is not available, this field will contain a plain-text description of the itinerary.                |

All other elements in the itinerary object differ slightly according to the value of itineraryType

## Standard itinerary

Products with a "STANDARD" itinerary type are tour-based products (focused on visiting and viewing) that occur at a single location or proceed through a set of locations on a single day.

An example of a "STANDARD" itinerary product is Barossa Valley Highlights from Barossa Valley Including Wine and Cheese Tasting (21381P1) .

The itinerary object in the product-content response for this tour is as follows (truncated to the first three items for brevity):

.

```
"itinerary": { "itineraryType": "STANDARD", "skipTheLine": false, "duration": { "fixedDurationInMinutes": 360 }, "itineraryItems": [ { "pointOfInterestLocation": { "location": { "ref": "LOC-5620ab70-c813-4904-ad13-bcf527540d3e" }, "attractionId": 17873 }, "duration": { "fixedDurationInMinutes": 45 }, "passByWithoutStopping": false, "admissionIncluded": "YES", "description": "Guests will experience the majesty of (...) " }, { "pointOfInterestLocation": { "location": { "ref": "LOC-7ae41705-fd91-4500-8cde-bbe9b3a00df4" } }, "duration": { "fixedDurationInMinutes": 40 }, "passByWithoutStopping": false, "admissionIncluded": "YES", "description": "Guests will enjoy a truly unique offering (...)" }, { "pointOfInterestLocation": { "location": { "ref": "LOC-9494c4cf-f4e4-4e7f-8213-0cf1b9980097" } }, "duration": { "fixedDurationInMinutes": 30 }, "passByWithoutStopping": false, "admissionIncluded": "YES", "description": "No trip to the Barossa would be complete without (...)"
```

<!-- image -->

The itineraryItems[] array describes the itinerary of locations for this tour and can be used in conjunction with the /locations/bulk endpoint to contruct a What to expect section, similar to what is seen for this product on viator.com , as in the following screen-shot:

<!-- image -->

The elements highlighted in red boxes are sourced as follows:

## "Stop At: Seppeltsfield"

The name of each location (in the highlighted case, 'Seppeltsfield') is not included in the response and must be determined by submitting the location reference code in the pointOfInterestLocation.location.ref field to the /locations/bulk endpoint.

The location reference is "LOC-5620ab70-c813-4904-ad13-bcf527540d3e" :

<!-- image -->

## "ref": "LOC-5620ab70-c813-4904-ad13-bcf527540d3e"

}

Submitting this code to the /locations/bulk endpoint yields the following response:

```
{ "locations": [ { "provider": "TRIPADVISOR", "reference": "LOC-5620ab70-c813-4904-ad13-bcf527540d3e", "name": "Seppeltsfield", "address": { "street": "730 Seppeltsfield Rd", "administrativeArea": "Seppeltsfield", "state": "South Australia", "country": "Australia", "countryCode": "AU", "postcode": "5355" }, "center": { "latitude": -34.489162, "longitude": 138.91866 } } ] }
```

The name of the location is in the

## Description

The description for each itinerary stop is given in the description field; in this case:

<!-- image -->

## "Duration: 45 minutes"

The duration spent at an itinerary location is given in the duration element. This can be a fixed duration, as in this example and indicated by the fixedDurationInMinutes field being filled; i.e.:

```
"duration": { "fixedDurationInMinutes": 45 },
```

name element; i.e.,

"Seppeltsfield"

.

Or, the time spent at the location might be variable, in which case only the

```
variableDurationFromMinutes and variableDurationToMinutes fields will appear; e.g.:
```

```
"duration": { "variableDurationFromMinutes": 10, "variableDurationToMinutes": 30 },
```

## "Admission Ticket Included"

This item of information indicates to the traveler whether or not they will be required to pay for admission to a location or whether admission is included in the price of the tour. It is indicated by the admissionIncluded field; which in this case is:

"admissionIncluded": "YES"

The possible values this field can take are:

- "YES"
- "NO"
- "NOT\_APPLICABLE"

## Pass by without stopping

In this example, the passByWithoutStopping element is false for all locations. On some tours, however, the vehicle will merely pass by a certain location, without stopping, for viewing purposes. If that is the case, this field will be true .

## Activity itinerary

The "activity" itinerary is designed for products where the focus of the experience is the activity itself (e.g., cooking classes), rather than the location(s) at which it occurs.

The itinerary object for this type of product includes the activityInfo and foodMenus objects, which contain details about the activity and any meals being served (or created), respectively.

Example activity experience : Traditional Cooking Class - 114869P3

```
"itinerary": { "itineraryType": "ACTIVITY", "skipTheLine": false, "privateTour": true, "duration": { "fixedDurationInMinutes": 240 }, "pointsOfInterest": [
```

```
{ "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5C7cXoFi13Pb8aiiiEWiVprM1MtQdt/DIeeb7ErQo1SK } ], "activityInfo": { "location": { "ref": "LOC-dwbUKYXwDvt911EeSQVjwo4itqM47D/JrJBMhEHXctp6Yj8SzOvLCGbeQQ0arbNw }, "description": "Embark on a culinary adventure unlocking the secrets of authent }, "foodMenus": [ { "course": "MAIN", "dishName": "Gado-gado", "dishDescription": "Mixed vegetables with peanut sauce" }, { "course": "MAIN", "dishName": "Opor Ayam", "dishDescription": "Braised Chicken in Coconut Milk" } ] }
```

All information for the 'What to Expect' section on the product display page on Viator.com is can be sourced from this object.

## Multi-day tour itinerary

Products with a "MULTI\_DAY\_TOUR" itinerary type are tours or activities that occur over multiple days, and therefore include a breakdown of the itinerary for each day of the tour, as well as extra information about food and accommodation.

Example multi-day tour : Active Winter Adventure in Yukon | 5 days (7110P7)

Screenshot of 'What to expect' section from the viator.com site:

## Itinerary

<!-- image -->

Arrival Whitehorse

Stop

- Erik Nielsen Whitehorse International Airport

From the airport we drive you to your hotel located in the centre of Whitehorse

Admission Ticket Free

Accommodation: Overnight in downtown Whitehorse Hotel

Meals:

Not Included

## Day 2

Wildlife and Hot Springs; a Bird's-Eye-View and Northern Lights

3 Stops

## Yukon Wildlife Preserve

Later we drive to the Yukon Wildlife Preserve where we can see up close inhabitant game like the Mountain Goats and Porcupines in their natural surrounding. Elk;

Duration: 1 hour 30 minutes

Admission Ticket Included

## Takhini Hot Springs

Not far from here we will visit the Takhini Hotsprings and endulge ourself in the natural hot waters and relax in a breathtaking winter mountain setting:

Duration: 1 hour 30 minutes

Admission Ticket Included

## Arctic Range Adventure

After a relaxed dinner in Whitehorse, be back on the road again; this time to seek views of the stunning Northern Lights. Relax in sheltered comfort; or under the starry sky beside a warm fire at one of our tailor-made aurora viewing locations. you'll

Admission Ticket Included

Accommodation: Overnight in downtown Whitehorse Hotel

Meals:

Not Included

## Day 3

The Huskies are waiting for us and Northern Lights

Multi-day tour itinerary example from viator.com

Snippet of the itinerary object in the product content response for 7110P7 (truncated to first two items of days[] array):

```
"itinerary": { "itineraryType": "MULTI_DAY_TOUR", "skipTheLine": false, "duration": {
```

```
"fixedDurationInMinutes": 7200 }, "days": [ { "title": "Arrival Whitehorse", "dayNumber": 1, "items": [ { "pointOfInterestLocation": { "location": { "ref": "LOC-99b0f435-fa6a-469f-8f96-f983b82f74c5" } }, "duration": {}, "admissionIncluded": "NOT_APPLICABLE", "description": "From the airport we drive you to your hotel located in th } ], "accommodations": [ { "description": "Overnight in downtown Whitehorse Hotel" } ] }, { "title": "Wildlife and Hot Springs, a Bird's-Eye-View and Northern Lights", "dayNumber": 2, "items": [ { "pointOfInterestLocation": { "location": { "ref": "LOC-799e6c90-d0bb-4ec4-9cf6-c40459ff0463" }, "attractionId": 25942 }, "duration": { "fixedDurationInMinutes": 90 }, "admissionIncluded": "YES", "description": "Later we drive to the Yukon Wildlife Preserve where we ca }, { "pointOfInterestLocation": { "location": { "ref": "LOC-cf8d0f7a-54d6-4cc1-9911-480b4934c752" },
```

```
"attractionId": 25951 }, "duration": { "fixedDurationInMinutes": 90 }, "admissionIncluded": "YES", "description": "Not far from here we will visit the Takhini Hotsprings an }, { "pointOfInterestLocation": { "location": { "ref": "LOC-3251a39d-aa69-4229-9ba4-57d5b417e6db" } }, "duration": { "fixedDurationInMinutes": 240 }, "admissionIncluded": "YES", "description": "After a relaxed dinner in Whitehorse, you'll be back on t } ], "accommodations": [ { "description": "Overnight in downtown Whitehorse Hotel" } ] }, (...) ] }
```

Within the days[] array, each day of the multi-day tour is described. The items[] array within each item of the days[] array largely follows the structure of the items in the itineraryItems[] array of the "STANDARD" itinerary and can be interpreted for display.

The fixedDurationInMinutes in the itinerary[] array represents the total duration of the tour.

Note : The example above does not include the foodAndDrinks[] element, as it is not relevant to this product.

## Hop-on / hop off itinerary

A hop-on/hop-off product is one that typically operates continuously during its hours of operation, such as a bus tour, and passengers can use their ticket to board and alight as they please at any of the stops along the route.

Such products may also operate multiple routes simultaneously.

## Example hop-on / hop-off tour : Big Bus Sydney and Bondi Hop-on Hop-off Tour (5010SYDNEY)

<!-- image -->

Snippet of itinerary object in the product content response for 5010SYDNEY ( operatingSchedule , stops and pointsOfInterest truncated in first route):

```
"itinerary": { "itineraryType": "HOP_ON_HOP_OFF", "skipTheLine": false, "privateTour": false, "duration": { "fixedDurationInMinutes": 120 }, "routes": [ { "operatingSchedule": "1st bus departs from Stop 1 Circular Quay at 9.00am.. ( "duration": { "fixedDurationInMinutes": 120 }, "name": "Red Route - Sydney Icons", "stops": [...], "pointsOfInterest": [...] ] }, { "operatingSchedule": "1st bus departs from Stop 12/24 Central Station at 10.0 "duration": { "fixedDurationInMinutes": 120 }, "name": "Blue Route - Bondi Lifestyle", "stops": [ { "stopLocation": { "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5Psa0O7zv6as2RgNgIaUx0EFjKH/7fL3wV6nAS8 }, "description": "Central Station, Pitt Street, Bus Bay 18" }, { "stopLocation": { "ref": "LOC-RaYlfRSLaIsd0SlazqDQk19G5f6qNrg0gjGUG4TKX09ebeQFQmF/tcZGYdP }, "description": "Australian Museum " }, { "stopLocation": { "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5Nh4BzPY4JhOxIuD4/Do8pUJ7t+9MCl62rbq6KV }, "description": "" }, { "stopLocation": { "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5HyrAalNU3M4hS1T1NGhMtCdFsSEh+RkFpJBmFZ
```

```
}, "description": "" }, { "stopLocation": { "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5ADNeEAMR25x+3AtosA/mPk102O66T1JygFmomn }, "description": "" }, { "stopLocation": { "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5DlsAklW6JtKr4LQsnhsvv7JxEYbLQWAsKDqTrC }, "description": "" }, { "stopLocation": { "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5BLsCa3M6INxXNpkE2r1BTHxvB0gY1MP6WB9Yxs }, "description": "" }, { "stopLocation": { "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5PrdhQ/J96Gq+dweFD3sOSrkBFH5QSJjP1VJ0a/ }, "description": "" } ], "pointsOfInterest": [ { "location": { "ref": "LOC-6eKJ+or5y8o99Qw0C8xWyIiKlXuqcCaUR/8Ng7CZSLI=" }, "attractionId": 14159 }, { "location": { "ref": "LOC-6eKJ+or5y8o99Qw0C8xWyOEUrjaNrfQuPK4sfYmEGio=" } }, { "location": { "ref": "LOC-6eKJ+or5y8o99Qw0C8xWyPTry/4ZvItH2jj+ziZ16zY=" } }, {
```

<!-- image -->

By comparing the response snippet with the screenshot above, you can see that:

- There are two routes - "Red Route - Sydney Icons" and "Blue Route - Bondi Lifestyle"
- The Blue Route has 8 stops and 5 points of interest
- Only the first two stops on the Blue Route have descriptive text entered by the supplier, as seen in the screenshot and in the snippet ( description field)

All location details (including the name) must be retrieved by sending the location reference to the /locations/bulk endpoint.

The total duration of the tour can be found in the itinerary[] array. If all tour routes have the same duration, the fixedDurationInMinutes field will be returned. When tour routes have different duration, only the variableDurationFromMinutes and variableDurationToMinutes fields will appear.

## Unstructured itinerary

Although our systems have been upgraded to support structured itinerary information, this feature is only availabe once the supplier manually updates their product details. A small number of suppliers have not yet made these updates. As such, some products retain their legacy itinerary information, and this case is handled with the "UNSTRUCTURED" itinerary type.

Snippet of itinerary object in the product content response for 5524GOLD - Private Tour: 4-Day Golden Triangle Trip to Agra and Jaipur from Delhi :

```
"itinerary": { "itineraryType": "UNSTRUCTURED", "skipTheLine": false, "privateTour": false, "unstructuredDescription": "Please read the Itinerary section for details on your "unstructuredItinerary": " Day 1: Delhi - AgraMorning departure from your hotel i "duration": { "fixedDurationInMinutes": 5760
```

<!-- image -->

Use the unstructuredDescription and unstructuredItinerary fields to create the section on your site that corresponds to the What to expect section on the Viator product display page. Note that the unstructuredItinerary field is not always populated - in that case, just use the unstructuredDescription field.

All products with an "UNSTRUCTURED" itinerary type are in the process of being updated to the appropriate structured type. Eventually, all products will support structured itinerary information.

<!-- image -->

## Protecting unique content

In order to prevent our unique content from being utilized by unauthorized third parties, we require that you design your site in such a way that this content will not be indexed by search engines.

The content that must be protected comprises:

- Product reviews - This includes all review text (from any provider) as obtained via the /reviews/product endpoint; and, that in the reviews element in the product content response.
- Viator unique content - This includes all data in all elements within the viatorUniqueContent element in the product content response.

## Guidelines to prevent indexing of unique content

In order to properly protect reviews and other unique content, you must ensure that the protected content never appears directly in the source code of the loaded page. This includes both HTML and Javascript.

In order to do this correctly, the unique content must be loaded via a call to an external Javascript, and that Javascript must be blocked in robots.txt so that search engines can not see or index it.

## How to check

A simple way to check that the unique content does not appear in the source code of the loaded page and, therefore, cannot be indexed - is to copy a snippet of the unique content text that is displayed when you load the page normally in your browser. Approximately 10 words will suffice.

Then, access the source code of that page using the View Source feature in your browser. Use your browser's in-page search feature to search for the text snippet copied in the previous step. If the text is found anywhere in the source code of the page, then your implementation is not correctly protecting the content, as it will be able to be indexed by search enginges.

## Example implementations

<!-- image -->

## ❌ Unacceptable implementation : pure HTML

Here the protected content appears directly in the HTML and can be indexed by search engines:

```
html head head body div 'I had a great time at this hotel' div body html < > < > </ > < > < > </ > </ > </ >
```

- ❌ Unacceptable implementation : Javascript in the page source

Here, the protected content still appears in the page source, even though it is in the 'script' section, and will therefore be indexed by search engines:

```
html head script var review_content = 'I had a great time at this hotel'; $('review').html(review_content); script head body div id 'review' div body html < > < > < > </ > </ > < > < = ></ > </ > </ >
```

<!-- image -->

- ✅ Acceptable implementation: protected content is loaded using an external Javascript and access to that endpoint is blocked using robots.txt:

```
html head script var review_content = $.ajax('https://api.hello.xyz/getReviewContentForHotel/1 $('review').html(review_content); script < > < > < > </ >
```

```
head body div id 'review' div body html </ > < > < = ></ > </ > </ >
```

Robots.txt in the document root for https://api.hello.xyz :

```
User-Agent: *
```

```
Disallow: /getReviewContentForHotel
```

Note : The robots.txt file must be in the root directory for whichever domain or subdomain the call is being made to. Please review the robots.txt guidelines to determine the correct syntax for your site.

## Review authenticity

## Viator performs checks on reviews

You can only submit a review or rating of an experience to Viator if you were the person who made the booking through Viator. Before publication, each review goes through an automated tracking system, which collects information for each of the following criteria: who, what, how, and when.

If the system detects something that contradicts our publication criteria, the review is not published. When the system detects a problem with a review, it may be automatically rejected, sent to the reviewer for validation, or manually reviewed by our team of content specialists who work 24/7 to maintain the quality of the reviews on our site. In some cases, we will also send Viator customers an email asking them to validate their review before it is published.

All Viator customers need to do is to click on the link provided in the email.

After publication, our team checks each review reported to it as not meeting our publication criteria. Tripadvisor reviews that appear on the Viator site are subject to the same checks and moderation processes as set out above. It is not necessary to have booked an experience through Viator (or Tripadvisor) to submit a review of an experience to the Tripadvisor site.

## Booking concepts

## Working with age bands

## Why have age bands?

Tour and experience product suppliers can set different prices for (and impose different rules on) customers according to how old they are.

For example, suppliers might choose to charge people 18 years and older ('adults') the full ticket price, while 'children' can book at a lower price.

Or, the tour operator may only allow children to make a group booking for the tour so long as the group contains 'at least one adult'.

Viator provides six age-band categories that product suppliers can use to segregate travelers into age groups (the limits of which they also define) in order to set pricing and traveler-count participation rules for their product according to the age band categories.

The age-bands available for a particular product, such as adult , child , infant , etc., are returned by the /products/{product-code} service. Your customer should be able to select a different number of people from each available age-band during the price check and checkout process.

To learn more about how to implement age bands, see the following guide: Implementing age bands &amp; pax mix

## Age-band categories

The age bands supported by the Viator API are as follows:

| bandId      | Description                                 |
|-------------|---------------------------------------------|
| "ADULT"     | Adult                                       |
| "CHILD"     | Child                                       |
| "INFANT"    | Infant                                      |
| "YOUTH"     | Youth                                       |
| "SENIOR"    | Senior                                      |
| "TRAVELER " | Catch-all age-band for unit-priced products |

Note that the "TRAVELER" is only used for bookings with unit pricing , in which case it will be the only age-band available.

The exact age range to which each category pertains is defined by the supplier, and the maximum and minimum ages that each age band describes for each product can be found in the product content response; e.g.:

<!-- image -->

For this product, the age bands have been defined as follows:

| ageBand   |   ageFrom |   ageTo |
|-----------|-----------|---------|
| ADULT     |        13 |      64 |
| SENIOR    |        65 |      99 |
| CHILD     |         4 |      12 |

Product suppliers must define at least one age band for their tour, and there are no 'default' age ranges. Therefore, if the supplier has only specified a single 'adult' age band covering ages 18-99, it must be assumed that only people aged 18-99 are eligible to book the tour, essentially excluding children and centenarians in this case.

## When you will use age-bands

The age-band of a customer needs to be communicated via the API in the following situations:

1. When placing a booking-hold
2. you will need to supply the age-band of each of the travelers being booked for in the paxMix element in the request to /bookings/hold or /bookings/cart/hold .
2. When making a booking
4. As with the booking hold, age-bands must be supplied in the paxMix element
5. If the supplier has specified "AGEBAND" as a booking question, you must additionally provide these details in the bookingQuestionAnswers array in the request to /bookings/book or /bookings/cart/book . Note that these details are verified by the booking server and the booking will be rejected if the details do not match. For more information about answering the "AGEBAND" booking question, see Booking concepts - Booking questions .

## Cancellation policy

Note : This section applies to affiliate partners with API access level "Full Access + Booking" and merchant partners only.

As well as making bookings, affiliate and merchant partners are also able to cancel bookings through the Viator API using the /bookings/cancel-reasons , /bookings/{booking-ref}/cancel-quote and /bookings/{booking-ref}/cancel endpoints. Items cancelled via the /bookings/{booking-ref}/cancel endpoint will be cancelled in full, and only one booking can be cancelled at a time.

For more information about how to perform cancellations using this API, see the Cancellation API workflow section and our in-depth guide about cancellation policies and how to handle cancellations: All you need to know about cancellation policies .

## Cancellation policies

All products can be cancelled by the affiliate or merchant partner; however, the refund granted by the supplier depends on the cancellation policy for the product in question.

There are three cancellation policy categories, standard , custom and all sales final , indicated by the type element of the cancellationPolicy object in the responses from the product content endpoints .

Note: These policies are those provided by Viator to you, the merchant partner. As the merchant of record, you can choose whether to extend these terms to your customers unchanged; or, set your own cancellation terms. For example, you might choose to make all products non-refundable; or, you might extend the full-refund cancellation window to 72 hours instead of 24 hours, and so forth. However, you will still be invoiced according to Viator's cancellation policies communicated via the API

Standard cancellation policy ( "STANDARD" )

Products in this category can be cancelled up to 24 hours before the travel time (local supplier time) and a full refund will be granted. However, a 100% cancellation penalty applies for cancellations submitted less than 24 hours before the start time. Most products (about 85%) fall into this category.

## Example response snippet

- Source endpoint : /products/{product-code}
- Product : 5010SYDNEY

<!-- image -->

This product has the standard cancellation policy; i.e., when a booking is cancelled:

| Policy                                        |   dayRangeMin | dayRangeMax   | Logic                                                                                                   |   percentageRefundable |
|-----------------------------------------------|---------------|---------------|---------------------------------------------------------------------------------------------------------|------------------------|
| less than one day (24 hours) before the start |             0 | 1             | (product_start_time - cancellation_time) >= 0 days && (product_start_time - cancellation_time) < 1 days |                      0 |
| more than                                     |             1 | (absent)      | (product_start_time - cancellation_time)                                                                |                    100 |

| Policy                                   | dayRangeMin   | dayRangeMax   | Logic    | percentageRefundable   |
|------------------------------------------|---------------|---------------|----------|------------------------|
| one day (24 hours) before the start time |               |               | >= 1 day |                        |

## Custom cancellation policy ( "CUSTOM" )

The refund amount for products in this category varies depending on how long before its start time the product is cancelled. Many products on a custom policy are multi-day tours, which require more sophisticated planning on the supplier's end. Only a small number of products (around 5%) fall into this category.

- Note : the description field contains a natural-language (and therefore language-localized) description of the policy described in the refundEligibility array. You can use this description for customer-messaging directly, or implement your own natural-language generation techique. With the cancellation policy encoded in a structured way, it would also be possible to display this information graphically.

## Example response snippet

- Source endpoint : /products/{product-code}
- Product : 2264RJ410

<!-- image -->

<!-- image -->

This product has a complex cancellation policy; where cancellations processed:

| Policy                                                                 |   dayRangeMin | dayRangeMax   | Logic                                                                                                     |   percentageRefundable |
|------------------------------------------------------------------------|---------------|---------------|-----------------------------------------------------------------------------------------------------------|------------------------|
| 30 days or more before the start time                                  |            30 | (absent)      | (product_start_time - cancellation_time) >= 30 days                                                       |                    100 |
| 10 days and less than 30 days (10 to 30 days) before the start time or |            10 | 30            | (product_start_time - cancellation_time) >= 10 days && (product_start_time - cancellation_time) < 30 days |                     50 |
| less than 10 days before the start time                                |             0 | 10            | (product_start_time - cancellation_time) < 10 days                                                        |                      0 |

Note: When the dateRangeMax field is absent, this means infinity. Therefore, the second element in the refundEligibility array above indicates that the time period begins infinitely far in the past until 30 days prior to the tour or activity commencing.

## 3 - All sales final (100% cancellation penalty / no refund offered)

<!-- image -->

Products in this category cannot be cancelled or amended without incurring a 100% penalty; i.e., the refund amount will be zero. Around 10% of products fall into this category.

## Example response snippet

- Source endpoint : /products/{product-code}
- Product : 5985P7

<!-- image -->

Products in this category can be cancelled, but no refund will be granted.

## startTimeStamp and endTimeStamp

Within the cancellationPolicy object in the response from /bookings/book or /bookings/cart/book , the refundEligibility.startTimestamp and refundEligibility.endTimestamp fields contain time-stamps (UTC) that indicate the exact times between which the different cancellation refund rates apply.

## Note :

- refundEligibility.startTimestamp will always be further in the past than refundEligibility.endTimestamp .
- Please use startTimestamp and endTimestamp , rather than dayRangeMin and dayRangeMax , to determine which cancellation policy is in effect.

Example response snippet from /bookings/book and /bookings/cart/book :

<!-- image -->

## Post-travel cancellations

Occasionally, customers seek a refund for a product after completing their travels.

The reason for this might be because they were unable to attend the tour due to the supplier having cancelled the tour due to bad weather or other reasons beyond the customer's control; or, the customer might have been extremely dissatisfied with the tour itself, felt that it was misrepresented in its advertising, or some other serious complaint.

When this occurs, you will need to send a refund request by email to dpsupport and include both "CANCEL" and the booking reference number in the subject line.

For all post-travel cancellation requests, you will need to include a detailed description of the issue.

Except in cases of known service interruptions (e.g., due to extreme weather events), we will first verify the issue and seek authorization from the product supplier.

Once a decision regarding the refund has been made, we will notify your Customer Services Department with this information. You will then need to advise your customer directly and process the refund if granted.

## Partial refunds

While we recommend that merchant partners support the processing of partial refunds for their customers, it is ultimately up to the partner whether to implement this functionality.

If you would prefer to only grant the full (100%) refund that is offered on most products so long as the cancellation is processed more than 24 hours prior to the product's start time, we recommend that you implement logic that checks whether a 100% refund is available for the product at the time the customer wishes to cancel their booking.

Type 1: Standard policy ( cancellationPolicy.type is "STANDARD" )

The 100% refund is available so long as the cancellation is performed more than 24 hours prior to the product start time

Type 2: Custom policy ( cancellationPolicy.type is "CUSTOM" )

You will need to check whether any of the canellation policy objects in the refundEligibility array have:

- a percentageRefundable value that is non-zero, and
- dayRangeMin and dayRangeMax describe an epoch that includes the present time

Type 3: All sales final ( cancellationPolicy.type is "ALL\_SALES\_FINAL" )

No refunds are available (except in the case of manual confirmation products that are still in a 'pending' state and special exceptions for post-trip cancellations); therefore, under normal conditions, if you grant a refund to your customer for this kind of product, it will be solely at your expense (i.e., you will still be invoiced for the cost of the product by Viator). Therefore, we recommend that you do not allow refunds for products with this policy.

## Per-person and unit pricing

Note : This section applies to affiliate partners with API access level "Full Access + Booking" and merchant partners only.

The products in our catalogue fall into two pricing categories: per-person and unit pricing.

A product's pricing category is given in the pricingInfo.type field of the product content response. Depending on whether the product has per-person or unit pricing, this value will be "PER\_PERSON" or "UNIT" , respectively.

For more information, see this article: Per-person and unit pricing .

## Per-person pricing

If the pricing is per-person , then the total price of the booking will be directly proportional to the number of participants (passengers) of each age-band type that are being booked for the product; i.e., a direct

multiple of the per-person price.

For example:

<!-- image -->

## Per-unit pricing

If the product has unit pricing, then the total price of the booking will depend on the number of units (groups) and types of unit that ideally accommodate the participant mix. Additionally, the pricingInfo object in the response will specify the type of unit in the unitType field; e.g., in this case, "VEHICLE" :

<!-- image -->

<!-- image -->

The

<!-- image -->

will be one of:

<!-- image -->

| unitType   | Example product   | Meaning                                                                                                                                                                                                                                                                                                                                                                 |
|------------|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| "GROUP"    | 10847P42          | Per-group pricing - the unit price is calculated according to the number of groups the specified passenger mix will fit into rather than the exact number of participants. minTravelersPerBooking and maxTravelersPerBooking must be considered as these fields relate to the available group sizes.                                                                    |
| "ROOM"     | 16621P2           | Per-room pricing relates the room price, which depends on the number of participants making the booking.                                                                                                                                                                                                                                                                |
| "PACKAGE"  | 186385P1          | Per-package pricing refers to products that are sold as part of a package; for example a family package stipulating a passenger mix of two adults and two children.                                                                                                                                                                                                     |
| "VEHICLE"  | 10175P10          | Per-vehicle pricing is calculated according to the number of vehicles required for the specified passenger mix rather than the exact number of participants. minTravelersPerBooking and maxTravelersPerBooking must be considered as these fields relate to the occupancy limitations for each vehicle. The minimum price will depend on the rate for a single vehicle. |
| "BIKE"     | 153074P3          | Per-bike pricing - identical to "per vehicle", but refers specifically to vehicles that are bikes.                                                                                                                                                                                                                                                                      |
| "BOAT"     | 35157P2           | Per-boat pricing - identical to "per vehicle", but refers specifically to vehicles that are boats.                                                                                                                                                                                                                                                                      |
| "AIRCRAFT" | 14876P5           | Per-aircraft pricing - identical to "per vehicle", but refers specifically to vehicles that are aircraft.                                                                                                                                                                                                                                                               |

## Low-margin products

Note : This section applies to affiliate partners with API access level "Full Access + Booking" and merchant partners only.

When setting the price at which you sell products on your site, it's important to remember that the recommendedRetailPrice is just the price at which the product is currently advertised on the Viator site and is only a recommendation.

However, the recommendedRetailPrice may be less than the partnerTotalPrice (i.e., the amount you will be invoiced for the sale).

If you sell the product for less than the partnerTotalPrice , you will make a loss on that sale.

Therefore, to ensure that you sell the product at a price which guarantees that you receive at least as much as you will be invoiced for, as well as any extra profit margin that you desire to generate, we recommend you include logic to check that these requirements are satisfied by comparing recommendedRetailPrice and partnerTotalPrice and adjusting the price at which you advertise and sell the product accordingly.

For example: If the partnerTotalPrice for a product is $100, the recommendedRetailPrice is $101, and you require a minimum margin of 5%, you should adjust the price at which you advertise the product to $105.

While we do recommend that you set your prices according to the value of recommendedRetailPrice , it is ultimately up to you what price you set for the product, bearing in mind that the amount Viator will invoice you for the sale will be the value of partnerTotalPrice .

For more information, see this article about how to deal with Low-margin products .

## Supplier communications

Note : This section applies to affiliate partners with API access level "Full Access + Booking" and merchant partners only.

## How can suppliers communicate with end customers?

Suppliers occasionally need to reach out to customers for a variety of reasons, such as:

- Requesting pickup locations, flight details or passenger weight information
- Providing weather alerts, sold-out notifications or general messaging

To allow suppliers to contact customers directly, Viator provides Closed-Loop Communication (CLC) .

## How to set up CLC for a booking

The recipient(s) of suppliers' CLC messages is set for each booking at the time of booking by supplying the customer's email address ( email ) as well as their phone number ( phone ) in the communication object in the request sent to the /booking/book or /bookings/cart/book endpoints when making a booking.

This will direct CLC messages sent by suppliers directly to that customer's email; no action from your support team will be necessary for suppliers to communicate with customers.

Partners choosing this option should mention to their customers that they are purchasing a product from a third-party supplier, and that they may, therefore, receive communications regarding the purchase directly from that supplier.

## Note:

- To have a CC of each message a supplier sends to their customer sent to your (the partner's) customer support email address (in case further assistance is required) you must include your customer support email address in the email field, after the customer's email and separated from that address with a comma.

## Example request body snippet to enable direct CLC

```
{ ... "communication": { "email": "john.smith@tripadvisor.com", "phone": "+61 4121121121" }
```

Example request body snippet to enable direct CLC with a CC of each message sent to your customer support

```
{ ... "communication": { "email": "john.smith@tripadvisor.com,customersupport@bookatrip4me.com", "phone": "+61 4121121121" }
```

## Supplier communications without CLC

To have CLCs from the supplier sent only to your (the merchant's) customer support team, supply the email address of your customer support function in the email field of the communication object in the request to the /bookings/book or /bookings/cart/book endpoints when making a booking.

Note: Utilizing this option requires you, the merchant, to manage the final loop of communication with the end customer to ensure that their tour/activity can be fulfilled successfully.

## Example request body snippet to disable CLC

<!-- image -->

## Default behavior

If an email address is not supplied in the communications object, the default behavior will be to use the partner's customer support email address for correspondence regarding this booking. Please contact your account manager to set or change the customer support email address for your organization.

Example request body snippet that would trigger the default behavior

```
{ ... "communication": { "phone": "+61 4121121121" }
```

## More information

For additional information about all communications sent by Viator, including CLC, see: All you need to know about cancellation policies - Managing Communications .

## Booking questions

Note : This section applies to affiliate partners with API access level "Full Access + Booking" and merchant partners only.

The booking-questions functionality of this API allows vital information specified by the supplier about the individual travelers or the group as a whole to be sent to the supplier as part of the request when making a booking using the /bookings/book or /bookings/cart/book endpoints.

The booking questions available for a product are specified in the bookingQuestions array in the response from any of the product content endpoints for that product. For example, for the product 10212P2 (Taste of Miami Helicopter Tour) , the bookingQuestions array is as follows:

```
"bookingQuestions": [ "FULL_NAMES_LAST", "SPECIAL_REQUIREMENTS", "FULL_NAMES_FIRST", "WEIGHT", "AGEBAND" ],
```

Each key string ( "FULL\_NAMES\_LAST" , etc.) identifies a booking question, details about which can be found in the response from the /products/booking-questions endpoint.

Relevant booking question details in example response snippet from /products/booking-questions :

<!-- image -->

<!-- image -->

The required field indicates whether an answer to the booking question must be provided in the booking request. It is necessary to provide an answer to all specified booking questions for which required is MANDATORY .

Additionally, the group field indicates whether an answer to the booking question must be answered for each traveler ( "PER\_TRAVELER" ) or for the booked group as a whole ( "PER\_BOOKING" ).

In this case:

<!-- image -->

| Booking question id    | required    | group          |
|------------------------|-------------|----------------|
| "WEIGHT"               | "MANDATORY" | "PER_TRAVELER" |
| "FULL_NAMES_FIRST"     | "MANDATORY" | "PER_TRAVELER" |
| "FULL_NAMES_LAST"      | "MANDATORY" | "PER_TRAVELER" |
| "AGEBAND"              | "MANDATORY" | "PER_TRAVELER" |
| "SPECIAL_REQUIREMENTS" | "OPTIONAL"  | "PER_BOOKING"  |

Therefore, to book this product, you must provide an answer to the "WEIGHT" ,

"FULL\_NAMES\_FIRST" , "FULL\_NAMES\_LAST" and "AGEBAND" questions for each traveler, and, optionally (if specified by the user at the time of booking) "SPECIAL\_REQUIREMENTS" for the booked group.

Answers to the booking questions are sent in the bookingQuestionAnswers[] array in the request to /bookings/book or /bookings/cart/book . The following example shows a valid and complete set of booking-question answers for this product.

|   Traveler number | First name   | Last name   | age band   |
|-------------------|--------------|-------------|------------|
|                 1 | John         | Smith       | ADULT      |
|                 2 | Mary         | Jones       | ADULT      |

<!-- image -->

When to use travelerNum

Please note that travelerNum indicates which traveler the answer pertains to. All PER\_TRAVELER questions must be answered for all travelers in the booking. travelerNum must be omitted for PER\_BOOKING booking questions.

## Booking questions with units

Some booking questions require you to specify the unit type when providing an answer to the questions.

## Example: 'HEIGHT' booking question

Definition of question from /products/booking-questions :

<!-- image -->

A valid answer to this booking question for a traveler who is 193 centimetres tall is as follows:

<!-- image -->

## Example: 'WEIGHT' booking question

Definition of question from /products/booking-questions :

```
{ "legacyBookingQuestionId": 23, "id": "WEIGHT", "type": "NUMBER_AND_UNIT",
```

```
"group": "PER_TRAVELER", "label": "Traveler weight in pounds or kilograms (required for safety reasons)", "units": [ "kg", "lbs" ], "required": "MANDATORY", "maxLength": 50 },
```

A valid answer to this booking question for a traveler who weighs 69 kilograms would be as follows:

```
"bookingQuestionAnswers": [ { "question": "WEIGHT", "answer": "69", "unit": "kg", "travelerNum": 1 } ]
```

## Booking questions with allowed answers

Some booking questions must be answered in a specific way. These questions include an allowedAnswers array containing the set of valid answers to the question.

Example booking question with allowed answers:

<!-- image -->

A valid answer to this booking question would be:

```
{ "question": "TRANSFER_ARRIVAL_MODE", "answer": "AIR" },
```

## Note:

- Not all allowed answers are applicable to all products, so you should not always display all 4 arrival/departure modes for all products. You should validate the arrival/departure modes based on the presence of questions applicable to a specific arrival/departure mode for each product.
- These questions will help you identify arrival modes available for a product:
- "AIR" : "TRANSFER\_AIR\_ARRIVAL\_AIRLINE" , "TRANSFER\_AIR\_ARRIVAL\_FLIGHT\_NO"
- "SEA" : "TRANSFER\_PORT\_ARRIVAL\_TIME" ( "TRANSFER\_PORT\_CRUISE\_SHIP" applies also to departure mode)
- "RAIL" : "TRANSFER\_RAIL\_ARRIVAL\_LINE" , "TRANSFER\_RAIL\_ARRIVAL\_STATION"
- If any of these questions is returned (even just one), the relevant option for arrival mode applies. Once an arrival mode is selected, travellers are required to answer all questions related to the selected arrival mode that are returned for the product in the bookingQuestions array (see the table below).
- The same applies in case of departure modes, you need to look for these questions specific to each departure mode:
- "AIR" : "TRANSFER\_AIR\_DEPARTURE\_AIRLINE" , "TRANSFER\_AIR\_DEPARTURE\_FLIGHT\_NO" "SEA" : "TRANSFER\_PORT\_DEPARTURE\_TIME" ( "TRANSFER\_PORT\_CRUISE\_SHIP" applies also to arrival mode) "RAIL" : "TRANSFER\_RAIL\_DEPARTURE\_LINE" , "TRANSFER\_RAIL\_DEPARTURE\_STATION"
- If these questions are not returned, the departure mode doesn't apply. Once a departure mode is selected, travellers are required to answer all questions related to the selected departure mode that are returned for the product in the bookingQuestions array (see the table below).

We recommend partners to translate these answers to natural language on their platforms, see recommendation below:

- "AIR" - airport
- "RAIL" - train station
- "SEA" - port
- "OTHER" - hotel / specific address

## Conditional booking questions

There are some booking questions that may or may not have to be answered, depending on the presence of - or answer to - another booking question. These questions are 'conditional', as indicated by the required field containing "CONDITIONAL" ; e.g.:

```
{ "legacyBookingQuestionId": 7, "id": "TRANSFER_AIR_ARRIVAL_AIRLINE", "type": "STRING",
```

<!-- image -->

So, when is an answer to a "CONDITIONAL" booking question required?

At present, the logic cannot be inferred from the response from the /products/booking-questions endpoint, but it can be explained here. You will need to hard-code this logic into your implementation in order to correctly present the required booking questions to the user.

The logic runs as follows:

| For this booking question   | if the user's answer is   | these questions must also be answered                                                                                                                                  |
|-----------------------------|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| "TRANSFER_ARRIVAL_MODE"     | "AIR"                     | "TRANSFER_AIR_ARRIVAL_AIRLINE" "TRANSFER_AIR_ARRIVAL_FLIGHT_NO" "TRANSFER_ARRIVAL_TIME" "TRANSFER_ARRIVAL_DROP_OFF" (see condition 1) "PICKUP_POINT" (see condition 1) |
| "TRANSFER_ARRIVAL_MODE"     | "RAIL"                    | "TRANSFER_RAIL_ARRIVAL_LINE" "TRANSFER_RAIL_ARRIVAL_STATION" "TRANSFER_ARRIVAL_TIME" "TRANSFER_ARRIVAL_DROP_OFF"                                                       |
| "TRANSFER_ARRIVAL_MODE"     | "SEA"                     | "TRANSFER_PORT_ARRIVAL_TIME" "TRANSFER_PORT_CRUISE_SHIP" "TRANSFER_ARRIVAL_DROP_OFF" (see condition 2) "PICKUP_POINT" (see condition 2)                                |
| "TRANSFER_ARRIVAL_MODE"     | "OTHER"                   | "PICKUP_POINT" (see condition 3)                                                                                                                                       |
| "TRANSFER_DEPARTURE_MODE"   | "AIR"                     | "TRANSFER_AIR_DEPARTURE_AIRLINE" "TRANSFER_AIR_DEPARTURE_FLIGHT_NO" "TRANSFER_DEPARTURE_DATE" "TRANSFER_DEPARTURE_TIME" "TRANSFER_DEPARTURE_PICKUP"                    |
| "TRANSFER_DEPARTURE_MODE"   | "RAIL"                    | "TRANSFER_RAIL_DEPARTURE_LINE" "TRANSFER_RAIL_DEPARTURE_STATION" "TRANSFER_DEPARTURE_DATE"                                                                             |

| For this booking question   | if the user's answer is   | these questions must also be answered                                                                       |
|-----------------------------|---------------------------|-------------------------------------------------------------------------------------------------------------|
| "TRANSFER_DEPARTURE_MODE"   | "SEA"                     | "TRANSFER_DEPARTURE_TIME" "TRANSFER_DEPARTURE_PICKUP" "TRANSFER_PORT_CRUISE_SHIP" "TRANSFER_DEPARTURE_DATE" |
| "TRANSFER_DEPARTURE_MODE"   | "OTHER"                   | n/a (see condition 4)                                                                                       |

## Conditions :

1. Rule applies only if logistics.travelerPickup.locations[] includes an item with pickupType : "AIRPORT" ; or , if logistics.travelerPickup.allowCustomTravelerPickup is true . "PICKUP\_POINT" answer must be a location for which pickupType is "AIRPORT" if answer to "TRANSFER\_ARRIVAL\_MODE" is "AIR" .
2. Rule applies only if logistics.travelerPickup.locations[] includes an item with pickupType : "PORT" ; or , if logistics.travelerPickup.allowCustomTravelerPickup is true . "PICKUP\_POINT" answer must be a location for which pickupType is "PORT" if answer to "TRANSFER\_ARRIVAL\_MODE" is "SEA" .
3. Rule applies only if logistics.travelerPickup.locations[] includes an item with pickupType : "HOTEL" or pickupType : "LOCATION" or pickupType : "OTHER" ; or , if logistics.travelerPickup.allowCustomTravelerPickup is true .
4. This question may only be answered "OTHER" if "OTHER" is also an available option for the "TRANSFER\_ARRIVAL\_MODE" booking question.

## Extra notes :

- Not all allowed answers are applicable to all products, so you don't have to always display all 4 arrival/departure modes. For each prodyct, you must validate if arrival/departure modes apply by checking if questions applicable to a specific arrival/departure are present. Read more about this validation here: Booking questions with allowed answers .
- All "CONDITIONAL" booking questions that depend on the answer given to either "TRANSFER\_ARRIVAL\_MODE" or "TRANSFER\_DEPARTURE\_MODE" (i.e., those questions in the righthand column in the table above) should be considered "MANDATORY" if they are stipulated in the "bookingQuestions" array of the product content response, and the respective transfer mode question is not stipulated. That is to say, for example, if "TRANSFER\_AIR\_ARRIVAL\_AIRLINE" is present, but "TRANSFER\_ARRIVAL\_MODE" is absent from "bookingQuestions" , then "TRANSFER\_AIR\_ARRIVAL\_AIRLINE" should be considered "MANDATORY" .
- The "TRANSFER\_PORT\_CRUISE\_SHIP" question is required to be answered when the customer's response to either "TRANSFER\_ARRIVAL\_MODE" or "TRANSFER\_DEPARTURE\_MODE" is "SEA" ; however, this question must only be answered once per booking. I.e., the answer for "TRANSFER\_PORT\_CRUISE\_SHIP" pertains to both questions. There is no provision for the customer to specify different cruise ships for arrival and departure.

- Please note that the inclusion of the "TRANSFER\_ARRIVAL\_MODE" , "TRANSFER\_DEPARTURE\_MODE" or their corollary conditional booking questions does not necessarily imply that pickup is offered for the product or product option being booked. It may be that these relate to another aspect of the service being offered; for example, an airport greeting product. When returned for a product, these questions must be answered.
- The "TRANSFER\_ARRIVAL\_DROP\_OFF" and "TRANSFER\_DEPARTURE\_PICKUP" questions are related to locations (arrival drop off and departure pickup) however there are no specific location references or conditions that apply to these questions (see the table). Therefore, customers should be provided with a freetext input field for these questions and the answers must include the FREETEXT designation if the customer answered freely, via text.
- Whether or not pickup is available should be determined at the product level by the value of logistics.travelerPickup.pickupOptionType being either "PICKUP\_EVERYONE" or "PICKUP\_AND\_MEET\_AT\_START\_POINT" and not "MEET\_EVERYONE\_AT\_START\_POINT" ; or, the presence of the phrase "pickup included" in the productOptions[].description field for the product option.
- Pickup must be validated on the product option level. It's possible that the product has multiple product options with a different setup for each one - i.e. one product option offers pickup, another product option requires to meet at the meeting point. The correct validation must be applied as described here: How to determine if a product option supports pickup.
- logistics.travelerPickup.pickupOptionType in the product content response could return "PICKUP\_AND\_MEET\_AT\_START\_POINT" for products that don't have product options. In such cases travelers should be allowed to either select a pickup location, or decide to meet at the meeting point.
- Pickup locations shouldn't be displayed at checkout for product options without pickup (this includes the option to contact the supplier later). Please refer to the 'Pickup point question' section below for further details on how to handle pickups.

## Pickup point question

The booking question that requests the location for pickup is as follows:

```
{ "legacyBookingQuestionId": 6, "id": "PICKUP_POINT", "type": "LOCATION_REF_OR_FREE_TEXT", "group": "PER_BOOKING", "label": "Hotel pickup", "hint": "E.g. 1234 Cedar Way, Brooklyn NY 00123", "units": [ "LOCATION_REFERENCE", "FREETEXT" ], "required": "CONDITIONAL", "maxLength": 1000 }
```

As you can see, this question can be answered using a location reference or 'freetext' (i.e., a written address in this context). Whether freetext is allowed for this answer depends on the value of logistics.travelerPickup.allowCustomTravelerPickup in the response from any of the product content endpoints . If true , freetext is allowed. Otherwise, a location reference - in particular, one of the location references included in the logistics.travelerPickup.locations[] array - must be supplied.

Example "FREETEXT" answer:

```
"bookingQuestionAnswers": [ { "question": "PICKUP_POINT", "answer": "1234 Cedar Way, Brooklyn NY 00123", "unit": "FREETEXT" } ]
```

Example

"LOCATION\_REFERENCE"

answer:

```
"bookingQuestionAnswers": [ { "question": "PICKUP_POINT", "answer": "LOC-6cb31b00-1fb4-4218-9b50-63f66531d735", "unit": "LOCATION_REFERENCE" } ]
```

## Special pickup-point location references

The logistics.travelerPickup.locations[] array in the response from the product content endpoints contains the location references for all available pickup locations for a product.

As well as standard location reference codes; e.g., "LOC-6cb31b00-1fb4-4218-9b50-63f66531d735", there are two special codes that specify instructions rather than locations.

## These are:

- "MEET\_AT\_DEPARTURE\_POINT"
- "CONTACT\_SUPPLIER\_LATER"

When selecting available pickup points, our suppliers also have the option of specifying one or both of these pseudo-locations. These instruct the customer to either meet at one of the locations specified in logistics.start[] , or to contact the supplier later to arrange a pickup point, respectively.

When building a list of available pickup locations for the customer to select at the time of booking, the descriptive text for these locations can be used. This is available from the /locations/bulk endpoint in the

<!-- image -->

field, as follows:

```
{ "locations": [ { "provider": "TRIPADVISOR", "reference": "CONTACT_SUPPLIER_LATER", "name": "I will contact the supplier later" }, { "provider": "TRIPADVISOR", "reference": "MEET_AT_DEPARTURE_POINT", "name": "I will meet at the departure point" } ] }
```

Or, you can provide a selection button in your UI, as we have done on the viator.com site:

<!-- image -->

```
This button appears when the "CONTACT_SUPPLIER_LATER" location reference is included in the logistics.travelerPickup.locations[] array.
```

How to determine if a product option supports pickup

When the value of logistics.travelerPickup.pickupOptionType in the product content response is "PICKUP\_AND\_MEET\_AT\_START\_POINT" , it means that the product includes both 'hotel pickup' and

'meet at the departure point' variants in its product options; e.g., one product option may be for hotel pickup while another is for meeting at the start/departure point.

To determine which product options offer what, it is necessary to inspect each product option's details in the productOptions[] array in the product content response.

If pickup is included for a product option, the phrase Pickup included will be present in the productOptions[].description field, as well as any other comments provided by the supplier. For example, the following two product options from product 8374P24 both offer pickup:

<!-- image -->

When booking a product option with pickup included , such as this, you must collect a pickup point from the user that corresponds to one of the entries in the logistics.travelerPickup.locations[] array in the product content response.

All booking questions related to arrival/departure must be displayed as normal to allow customers to select the desired arrival/departure mode and provide all relevant information to the supplier before travel.

All answers provided by the customer must be captured and submitted in the booking request following the logic for conditional booking questions from the table in the API documentation .

If the productOptions[].description field does not contain the phrase Pickup included , this indicates that this product option does not include pickup and should be considered to follow a "MEET\_AT\_DEPARTURE\_POINT" arrangement.

For example, the following product option (also from product 8374P24 ) requires meeting at the departure point and does not include pickup:

<!-- image -->

In case of product options without pickup, you shouldn't ask arrival or departure-related questions at checkout (but you will still need to answer the questions returned in the API using values hardcoded into your implementation). If you wish, you can display at checkout the meeting point location(s) for informational purposes (not collecting answers) but not the pickup locations and no questions related to arrival/departure should be displayed in that case.

The option to contact the supplier later ( "CONTACT\_SUPPLIER\_LATER" ) doesn't apply to this scenario either and should not be present as it applies only to product options with pickup.

In the answer to the "PICKUP\_POINT" question, you will need to send the location reference "MEET\_AT\_DEPARTURE\_POINT" (returned under travelerPickup.locations ). In case the product returns the "TRANSFER\_ARRIVAL\_MODE" or "TRANSFER\_DEPARTURE\_MODE" questions, these must be answered with "OTHER" . Product examples for testing: 9025P51 , 62450P1 .

## When other product options support transfer pickup :

While you might be booking a product option that does not support pickup, if the overall product itself supports, for example, pickup from an airport, in one of its other product options, it will contain the "TRANSFER\_ARRIVAL\_MODE" booking question in the bookingQuestions[] array in the product content response.

This means that this booking question, because it is "MANDATORY" , must be answered in order to make a valid booking, even though such information would be irrelevant in this context.

Transfer arrival mode question details from /products/booking-questions :

<!-- image -->

As you can see, one of the allowed answers to this question is

<!-- image -->

Therefore, in the case that you must answer this booking question because it is stipulated at the product level, but it does not pertain to the product option being booked, please do not prompt the user to provide an answer to this question , rather, have your internal logic send the value "OTHER" as the answer; i.e.:

```
"bookingQuestionAnswers": [ { "question": "TRANSFER_ARRIVAL_MODE", "answer": "OTHER" }, ... ]
```

The same applies for the "TRANSFER\_DEPARTURE\_MODE" booking question, as it is also mandatory and can be validly answered as "OTHER" .

```
The only "CONDITIONAL" booking question that must be answered for a product option without pickup (in addition to "MANDATORY" questions) is "PICKUP_POINT" (answer: "MEET_AT_DEPARTURE_POINT" )
```

## Examples of booking requests

Product: 9025P51

Product option details returned in the product content response:

<!-- image -->

<!-- image -->

Example booking request for product option with pickup (TG2):

```
{ "productCode": "9025P51", "productOptionCode": "TG2", "startTime": "08:00", "currency": "USD",
```

```
"travelDate": "2024-11-27", "paxMix": [ { "ageBand": "ADULT", "numberOfTravelers": 2 } ], "partnerBookingRef": "test123456", "languageGuide": { "type": "GUIDE", "language": "en" }, "bookerInfo": { "firstName": "XXXX", "lastName": "XXXX" }, "bookingQuestionAnswers": [ { "question": "FULL_NAMES_FIRST", "answer": "XXXX", "travelerNum": 1 }, { "question": "FULL_NAMES_LAST", "answer": "XXXX", "travelerNum": 1 }, { "question": "AGEBAND", "answer": "ADULT", "travelerNum": 1 }, { "question": "AGEBAND", "answer": "ADULT", "travelerNum": 2 }, { "question": "FULL_NAMES_FIRST", "answer": "XXXX", "travelerNum": 2 }, { "question": "FULL_NAMES_LAST", "answer": "XXXX", "travelerNum": 2
```

```
}, { "question": "TRANSFER_ARRIVAL_MODE", "answer": "OTHER" }, { "question": "TRANSFER_DEPARTURE_MODE", "answer": "OTHER" }, { "question": "PICKUP_POINT", "answer": "LOC-6eKJ+or5y8o99Qw0C8xWyGStvfcGJMWF/jrN0iaZD8s=", "unit": "LOCATION_REFERENCE" } ], "communication": { "phone": "+44 987667889", "email": "noreply@test.com" }, "additionalBookingDetails": { "voucherDetails": { "companyName": "Test", "email": "customerservice@test.com", "phone": "+44 876778998", "voucherText": "Thank you for booking with us!" } } }
```

Example booking request for product option without pickup (TG1):

<!-- image -->

<!-- image -->

```
{ "question": "PICKUP_POINT", "answer": "MEET_AT_DEPARTURE_POINT", "unit": "LOCATION_REFERENCE" } ], "communication": { "phone": "+44 987667889", "email": "noreply@test.com" }, "additionalBookingDetails": { "voucherDetails": { "companyName": "Test", "email": "customerservice@test.com", "phone": "+44 876778998", "voucherText": "Thank you for booking with us!" } } }
```

To learn more about booking questions and get a step-by-step guide on how to implement conditional booking questions, see this guide: Implementing Booking Questions .

## Age-bands

If "AGEBAND" is specified as a booking question in the bookingQuestions array in the product content response, you must supply the age-band for each traveler in bookingQuestionAnswers when making the booking using /bookings/book or /bookings/cart/book .

Furthermore, the answer(s) to the "AGEBAND" booking question that you submit in the request to /bookings/book or /bookings/cart/book must match the age-bands given in the paxMix element in the request to /bookings/hold or /bookings/cart/hold . Otherwise, the booking server will reject the booking on account of the booking and booking-hold not matching.

The valid age-bands for the product are given in the pricingInfo array in the product content response; e.g.:

<!-- image -->

<!-- image -->

Note that if bookingRequirements.requiresAdultForBooking is true in the product content response, at least one traveler must have an "ADULT" or "SENIOR" age-band.

<!-- image -->

To learn more about how age-bands are used during the booking process, see the following guide: Implementing age bands &amp; pax mix .

## Age-bands with unit pricing

In the case that the product uses unit pricing; i.e., pricing based on the number of groups of travelers, then the product will have a single available age-band: "TRAVELER" , as given in the pricingInfo array in the product content response; e.g.:

<!-- image -->

For such products, even if "AGEBAND" is specified as a booking question, the only applicable age-band is "TRAVELER" . However, you must still supply this value for the age-band booking question for each traveler when making the booking using /bookings/book or /bookings/cart/book . Even if bookingRequirements.requiresAdultForBooking is true for such products, you must still supply the "TRAVELER" value.

## Booking cutoff times

Note : This section applies to affiliate partners with API access level "Full Access + Booking" and merchant partners only.

This section describes how the booking cutoff time information given by the product supplier, which may affect a product's availability (and therefore its ability to be booked) is communicated via this API. While you are welcome to develop logic to support the display and utilisation of this information, it is not necessary to do so . Indeed, as most implementations are unlikely to benefit, we recommend simply using the real-time /availability/check endpoint as the primary means to determine and communicate a product's availability in your product booking workflow.

Many products in our inventory are subject to a booking cutoff time. Tickets for such products may only be purchased up until a certain time. This information is given in the bookingConfirmationSettings object in the product content response .

Example bookingConfirmationSettings object:

```
"bookingConfirmationSettings": { "bookingCutoffType": "START_TIME", "bookingCutoffInMinutes": 0, "confirmationType": "INSTANT" },
```

There are four booking cutoff types, indicated by the value of the bookingCutoffType element; they are:

- "START\_TIME" - booking cutoff is relative to the product's start time
- "OPENING\_TIME" - booking cutoff is relative to the product's opening time
- "CLOSING\_TIME" - booking cutoff is relative to the product's closing time
- "FIXED\_TIME" - booking cutoff is relative to the time given in the bookingCutoffFixedTime element

In addition, the booking cutoff time may be offset by the number of minutes given in bookingCutoffInMinutes ; for example, product 57377P9's booking cutoff is 120 minutes prior to its start time:

```
"bookingConfirmationSettings": { "bookingCutoffType": "START_TIME", "bookingCutoffInMinutes": 120, "confirmationType": "INSTANT" }
```

The availability of products that have a bookingCutoffType of "START\_TIME" can be determined by inspecting the pricingRecords[].timedEntries[].startTime field in the response from /availability/schedules/{product-code} . This type of product can be booked up until bookingCutoffInMinutes prior to its starting time in the time-zone in which the product operates, which is given in the timeZone field in the product content response .

The booking cutoff time for products with a "FIXED\_TIME" type is that given in the bookingCutoffFixedTime element, offset by the number of minutes given in bookingCutoffInMinutes . In the fixed time scenario, bookingCutoffInMinutes can only be 0, 1440 (24 hours) or 2880 (48 hours). This means that the booking cutoff time is at a certain time on the day on which the product operates; or, at that same time but one or two days before the tour date, respectively.

In the following example, the booking cutoff is 10:00am on the day before the tour or activity operates:

```
"bookingConfirmationSettings": { "bookingCutoffType": "FIXED_TIME", "bookingCutoffInMinutes": 1440, "confirmationType": "INSTANT", "bookingCutoffFixedTime": "10:00:00" }
```

You may not be able to book a product (using /bookings/book or /bookings/cart/book ) or place a booking hold on a product using /bookings/hold or /bookings/cart/hold after it is past the booking cutoff time. However, this is not always the case. Always check real-time availability using the /availability/check endpoint.

Nonetheless, in displaying the availability of a product on your site, you may wish to mark products as 'unavailable' for a particular day or starting time if it is presently past the booking cutoff time if you feel that doing so will improve your site's UX.

However, because the availability schedule data in general can rapidly fall out of date, we again encourage you to always utilise the real-time /availability/check endpoint as the primary means to determine and communicate a product's availability in your product booking workflow.

## Booking confirmation types

Note : This section applies to affiliate partners with API access level "Full Access + Booking" and merchant partners only.

A product's booking confirmation type indicates whether the booking will be confirmed or rejected immediately and automatically; or, whether it will remain in a 'pending' state until actioned manually by the supplier.

The product's booking confirmation type can be identified by the value of

```
bookingConfirmationSettings.confirmationType in the product content response. There are three confirmation types: instant , manual and instant-then-manual , represented by the confirmationType values "INSTANT" , "MANUAL" and "INSTANT_THEN_MANUAL" , respectively.
```

<!-- image -->

## Booking confirmation type in the API

## Instant confirmation:

Instant confirmation products are confirmed automatically at the time of booking, and the customer should be charged immediately.

E.g. (product-code: 5010SYDNEY):

```
"bookingConfirmationSettings": { "bookingCutoffType": "CLOSING_TIME", "bookingCutoffInMinutes": 0, "confirmationType": "INSTANT" }
```

## Manual confirmation

Manual confirmation products are those that only operate at the discretion of the supplier, who must confirm or reject each booking request manually. Once the booking is requested, it will remain in a 'pending' state until actioned by the supplier; or, if no action is taken by the supplier, the time-out period (72 hours) is exceeded. The customer should only be charged once confirmation is received.

E.g. (product-code: 161500P1):

```
"bookingConfirmationSettings": { "bookingCutoffType": "START_TIME", "bookingCutoffInMinutes": 1440, "confirmationType": "MANUAL" }
```

## Instant-then-manual confirmation

Instant-then-manual confirmation products behave like instant confirmation products up until a certain time prior to the product's starting time. From that point on, the product will require manual confirmation

by the supplier.

E.g. (product-code: 100035P1):

```
"bookingConfirmationSettings": { "bookingCutoffType": "START_TIME", "bookingCutoffInMinutes": 720, "confirmationType": "INSTANT_THEN_MANUAL", "manualConfirmationPeriod": 2880 }
```

The manualConfirmationPeriod indicates when the product changes from instant to manual confirmation. In the example above, this period is 2880 minutes (48 hours or 2 days). Therefore, this product will be confirmed instantly if the booking is made more than 2 days in advance of the start time (in the time zone in which the product operates); if the booking is made less than 2 days in advance, it will require manual confirmation from the supplier.

## How to support manual confirmation products

In order to support manual confirmation products on your site, you will need to introduce support for an asynchronous flow that monitors the booking's status, determines when its status changes and notifies the customer when their booking has been confirmed or rejected by the supplier.

You will need to:

- Create back-end logic that periodically checks the status of pending bookings using the /bookings/status endpoint (we recommend polling no more than once every 3 minutes)
- Establish and support an extra, email-based communications channel with your customers
- Create email templates for the various scenarios that may arise
- Ensure that your platform's front end accommodates the extra steps required in the booking process
- Ensure that customers clearly understand that they are booking a product that will not be confirmed or charged immediately

## Product detail page

Managing customer expectations is a key factor in supporting manual confirmation products on your booking platform.

Make clear mention on the product detail page that confirmation will not be received immediately, but rather within 72 hours of making the booking.

You are free to include this note in the Additional Info section, or elsewhere on your product display page; for example:

## Additional Info

- Confirmation will be received within 48 hours of booking; subject to availability
- Children must be accompanied by an adult
- Minimum drinking age is 18 years
- The duration of transfers are approximate; the exact duration will depend on the time of and traffic conditions day
- Passport name; number; expiry and country is required at time of booking for all participants

Manual confirmation info displayed on a product page on the Viator site

## Check-out

As you will only charge the customer's credit card once the booking is confirmed by the product's supplier, it's best to display a message to this effect at a prominent point of the check-out flow for all manual confirmation products.

- If confirmation isn't received instantly; an authorization for the total amount will be held until your bcoking is confirmed.
- You can cancel for free up to 24 hours before the of the experience; local time day

## Book Now

Example checkout-flow instruction on the Viator site

In this way, customers can be reassured that they are not being charged for a booking that may never be confirmed, thereby helping to reduce the number of calls to your customer service team.

## Combination purchases

If your customer has both instant and manual booking confirmation products in their shopping cart, only the amount for the confirmed booking(s) should be charged immediately; the portion corresponding to the pending bookings should be held as a pre-authorization against the customer's credit card, and the transaction completed only once confirmation is received.

It is important that you clearly differentiate between bookings that have been confirmed and those that are pending confirmation and communicate the status of each item. Also, be sure to make clear that the preauthorization will only finalize once the manual confirmation bookings are confirmed.

## Confirmation page

Changes will need to be made to your confirmation page because it will not be possible for your customer to download their voucher immediately after completing a manual confirmation booking. Rather, the

<!-- image -->

voucher will be made available after the booking is confirmed.

Vouchers for instant confirmation products, however, must be made available immediately following the completion of the booking process.

## Customer communications

Confirmation message (e.g., email) templates for manual confirmation bookings should indicate that the item is pending confirmation from the supplier; and, that confirmation for this activity will take up to 72 hours, depending on availability.

You will also need to create templates for the following scenarios:

- When the manual confirmation booking is confirmed by the supplier (this time including the voucher details)
- If the manual confirmation booking is rejected
- If multiple manual confirmation products have been booked:
- When all items have been accepted/confirmed
- When there are mixed statuses; i.e., 'pending' + 'rejected' + 'canceled'
- If all items were rejected
- If a mixture of instant and manual confirmation products are booked at the same time; i.e., in the same cart

Note : When a booking is declined, it is useful to mention that the customer's card was not charged.

Example email for a manual confirmation booking pending confirmation:

<!-- image -->

## Booking Information

Dear Homer Simpson Test;

Thank you for your booking.

reservation for Test On Request OR is awaiting confirmation.You will receive notification of your reservation by email. Alternatively; you can monitor the status of your booking by clicking on the link(s) provided below for each pending activity. Whether you're traveling across town or across the globe, we are proud to be part of your Your travel plans. We hope you have an incredible trip; and we appreciate your business.

Happy travels , Viator

PS: Its easy to stay in touch with Viator on the road. Download our mobile apps or follow us on Facebook; Twitter or Google+

## TourlActivity Details

Itinerary Number: IT-300155592

1. Test On Request OR

Booking Reference: BR-200187197

Lead Traveler: Mr Homer Simpson Test

Number of Travelers: 2 (2 Adults)

Travel Date: Monday October 10, 2016

Location: San Francisco; California

Voucher Information: e-Voucher

USD $0.30 PENDING

## Your voucher is not available. You can or bookmark the Voucher after your reservation is confirmed. print yet

Total Price: USD $0.30

## Payment Details

Pending tansactions have been authorized and will be charged to your credit card once they have been

Credit Card: Visa XXXX-XXXX-XXXX-0106

Order Total: USD 50.30

## Important Information

voucher your tourlactivity requires. Voucher requirerents vary; so if you've booked more than one tour; be sure lo check each one Here are the 3 voucher types we offer:

- Paper Voucher Requlred

On lhe to present a printed copy of your voucher; you will be refused service andlor admission to the activity you have purchased . Viator will not refund, credit or otherwise compensate you for failure to present a printed copy of your voucher on the day day

- e-Voucher

On Ihe supplier will accept both printed and e-vouchers . Simply present your photo ID with your voucher on an electranic device (smartphone or tablet) or a printed voucher on the of bavel. day day

On Ihe of travel you can present a paper or e-voucher for your tourlactivity; or you can simply present the Lead Traveler's Photo ID. Our supplier has your reservation on file and only requires of identity (valid photo ID for the Lead Traveler) on the day of travel. day proof

- Voucher Not Requlred

## Terms &amp; Conditions

Read our complete Terms &amp; Conditions for information on cancelations; date changes, and other modifications to this confirmed reservation.

## Alternate Ways to Receive Your Confirmation

If are departing home and have not received final notification of your booking, please check your spam folder to make sure you havent already received your confirmation voucher. Otherwise; simply access the Bookings" section in your account and select have not yet received confination of my traveling with cellrobile phone with an alternative phone number. from yet you "My your

## Have A Question or Need Help?

Visit our Frequently Asked Questions (FAQs) to learn more

If you need to contact our Customer Care team about this tour or activity; for fastest service simply access the Bcokings" section in your account. "My

## Confirmation time-outs resulting in rejection

As mentioned above, when a booking request for a manual confirmation product is made, it will have a status of 'pending' until it is confirmed by the supplier. The supplier has the option of confirming or rejecting the booking.

If the supplier does not confirm the booking within 72 hours - or, if they have not confirmed the booking by the time it reaches bookingCutoffInMinutes from the product's start time or whichever is specified in the bookingCutoffType - our systems will automatically reject the booking, and this will be reflected in the response from the /bookings/status endpoint.

## Building in the sandbox environment

Upgrading your booking platform to support manual confirmation products will require you to build and test this functionality in the sandbox environment.

However, when using the sandbox environment, no actual booking request is sent to the supplier's system; rather, manual-confirmation products behave like instant-confirmation products, and you will receive a bookingStatus of "CONFIRMED" immediately on making the booking unless you set the exp-demo header parameter to false in the request to /bookings/book . In this case, you will receive a bookingStatus of "PENDING" in the response, which is the expected behavior when making a booking request for a manual-confirmation product. Note: This is not supported using the /bookings/cart/book endpoint.

In order to test the complete booking flow, you will need to contact our API tech support team at apitechsupport@viator.com and request that we change the status of the booking (specified by the bookingRef ) to "CONFIRMED" or "REJECTED" as you require.

Please note that because this is a manual process, we'd genuinely appreciate your effort in keeping the number of these requests to a minimum.

## Making a booking

Note : This section applies to affiliate partners with API access level "Full Access + Booking" and merchant partners only.

Broadly speaking, to book a product via this API, you must do the following:

1. Check availability and pricing : Determine that a ticket for the desired tour or activity is available for a specific date, time and passenger mix combination using the /availability/check endpoint. Accurate pricing details in the currency that you wish to be invoiced in (one of GBP , EUR, USD, CAD or AUD) are also returned in the response from this endpoint. This includes recommendedRetailPrice and partnerNetPrice .
2. Request a booking hold : If a ticket is availabile, request a pricing/availability hold for the booking using the /bookings/hold or /bookings/cart/hold endpoints.
3. Collect payment : With a booking hold requested and suitable to proceed, collect payment using the iframe solution or via your own payment details form and submit using the API solution . Note: These payment options are only available to affiliate partners with API access level "Full Access + Booking".
4. Confirm the booking : Confirm/finalize the held booking using the /bookings/book or /bookings/cart/book endpoints.

See Getting availability and pricing for products and Creating a seamless booking experience for more information.

## Cancellation API workflow

Note : This section applies to affiliate partners with API access level "Full Access + Booking" and merchant partners only.

All booking cancellations (except for those requested after the date of travel) must now be performed via the API. Viator no longer offers ordinary cancellation services via our customer support function. To cancel a booking after the tour or activity has occurred, please contact Viator Partner Support

See our in-depth guide about cancellation policies and how to handle cancellations: All you need to know about cancellation policies .

## Getting cancellation reasons

When canceling a booking, you are required to submit a valid 'reason for the cancellation' to assist with Viator's internal processes. This is accomplished via the inclusion of a valid reason code in the body of the request. The reason codes can be retrieved from the /bookings/cancel-reasons endpoint.

As the acceptable reasons for cancellation may be altered at any point, we recommend retrieving an up-todate list from this endpoint at least weekly.

The output from the /bookings/cancel-reasons endpoint at the time of writing is as follows:

<!-- image -->

]

}

## Canceling a booking

## Getting a cancellation quote

Before canceling the booking, call the /bookings/{booking-reference}/cancel-quote endpoint to get information about whether the booking can be canceled using this endpoint and what the refund will be, for example:

```
GET https //api viator com/partner/bookings/BR-580254558/cancel-quote : . .
```

- Note : For bookings made with v1 of this API, this code corresponds to data.itemSummaries[].itemId (in the response from v1's /booking/book endpoint) but prepended with BR. For example, if the itemId is 580254558 , this field should be BR-580254558 .

You will receive a cancellation quote object, e.g.:

<!-- image -->

Note : Bookings that have not been confirmed by the supplier and have a status of "PENDING" will report an itemPrice , refundAmount and refundPercentage of 0 , as no fees are charged until the booking's status is "CONFIRMED" .

The data elements in this object have meanings as follows:

| Element   | Meaning                                                                     | Example      |
|-----------|-----------------------------------------------------------------------------|--------------|
| bookingId | the booking reference number prepended with BR-                             | BR-580254556 |
| status    | One of the following: CANCELLABLE : the booking is eligible to be cancelled | CANCELLABLE  |

| Element          | Meaning                                                                                                                                                                                                                                                                                                                                                   | Example   |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| refundDetails    | NOT_CANCELLABLE : the booking is for a product that operated in the past, and therefore cannot be cancelled using this endpoint (you will need to send an email to dpsupport including both "CANCEL" and the booking reference number in the subject line in order to request a refund for such a booking) object containing information about the refund |           |
| itemPrice        | the merchant net price + transaction fee for this product at the time of booking in the currency specified by currencyCode                                                                                                                                                                                                                                | 109.77    |
| refundAmount     | the amount that will be deducted from your invoice if the booking is cancelled now                                                                                                                                                                                                                                                                        | 109.77    |
| currencyCode     | the currency code for the currency in which pricing information is displayed                                                                                                                                                                                                                                                                              | USD       |
| refundPercentage | the refund amount expressed as a percentage of the itemPrice                                                                                                                                                                                                                                                                                              | 100.00    |

Will there ever be a discrepancy between the amount charged for a tour and the amount refunded due to currency exchange-rate fluctuations?

- In short: no. I.e., if the cost of the booking was USD 100 and the refund percentage is 100% (full refund, as per the response from /bookings/{booking-reference}/cancel-quote ), Viator will simply not invoice you for that USD 100 that we would have if the booking had not been canceled. Furthermore, we do not invoice you for the cost of a booking prior to its departure date.

## Requesting the cancellation

If the status field has a value of CANCELLABLE and you are happy with the refundAmount , call the /bookings/{booking-reference}/cancel endpoint to cancel the booking, e.g.:

POST https //api viator com/partner/bookings/BR-580254558/cancel : . .

A reason code corresponding to the reason for cancellation must be included in the request body; e.g.:

<!-- image -->

}

You should receive a response indicating that the cancellation was successful, e.g.:

<!-- image -->

A status of ACCEPTED indicates that the booking was successfully canceled.

<!-- image -->

## Checking booking status

Note : This section applies to affiliate partners with API access level "Full Access + Booking" and merchant partners only.

Once a booking has been made, you can check on its status using the /bookings/status endpoint.

You can use either the bookingRef or partnerBookingRef in the request to this service.

- If the booking was made using v1 of the Viator Partner API, you will receive a HTTP 400 Bad Request response. Only bookings made using v2 or later of this API are compatible with this endpoint.
- If the booking is the subject of a booking hold (via /bookings/hold or /bookings/cart/hold ) but the booking has not yet been confirmed using /bookings/book , you will receive a HTTP 404 Not Found response.
- If the booking was confirmed but later canceled, you will receive a HTTP 200 Success response that indicates the canceled status.
- If the booking has been confirmed and has not been canceled, you will receive a response with the same structure as the response from /bookings/book

## Confirmed booking

Example request : Get the status of the booking with the booking reference

<!-- image -->

<!-- image -->

Example response

: The status of this booking is "CONFIRMED"

<!-- image -->

```
"voucherInfo": { "url": "https://www.viator.com/ticket?code=1187186744:8ac3e6308555ab632fe89e8a6 "format": "HTML", "type": "STANDARD" } }
```

## Canceled booking

Example request : Get the status of the booking with the partner booking reference

```
"test-partner-ref-aejsmont-num-1604985575"
```

```
{ "partnerBookingRef": "test-partner-ref-aejsmont-num-1604985575" }
```

Example response : The status of this booking is

<!-- image -->

```
{ "bookingRef": "BR-582323272", "status": "CANCELED", "partnerBookingRef": "test-partner-ref-aejsmont-num-1604985575" }
```

## Testing

## Postman collections for testing

To facilitate your testing of the API's functionality in the sandbox environment, please use one of the following Postman collections, depending on which type of partner you are:

- Viator Basic-access Affiliate API Postman collection
- Viator Full-access Affiliate API Postman collection
- Viator Full-access + Booking Affiliate API Postman collection

## Viator Merchant API Postman collection

To access the sandbox environment, please replace api.viator.com with sandbox.viator.com in the endpoint URLs provided in the Postman collections for testing

## Set up the your-api-key environment variable

As all services in this API require that your API-key be passed as a header parameter in every request made to this API, this value has been set to reference a Postman environment variable called your-api-key .

Once you import the collection into Postman, set this variable to your organization's API-key and save the collection.

## Workflows

## Ingesting and updating the product catalogue

The recommended way to initialize and keep your local copy of our products database up-to-date is by using the /products/modified-since endpoint in the following way:

## Initialize your local copy of our products database by ingesting all product records

Make a request to /products/modified-since , but only include the count parameter. Do not supply values for modified-since or cursor . This instructs the system to return any products modified since the beginning of time; i.e., all of them.

Note : This is the only occasion on which you will need to call /products/modified-since without the modified-since or cursor parameter.

count specifies how many product records will be returned per page. For practical purposes, setting count to its maximum value (500) is advised. However, for the purposes of brevity, I am using a count of 5 in this example; i.e.:

GET https //api sandbox viator com/partner/products/modified-since?count=5 : . . .

You will receive a response similar to the following:

<!-- image -->

```
"location": { "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5Cdd0Y9TkTxkcosDq0rJgjR }, "description": "The meeting point is on the way to Lumbisí } ], "end": [ { "location": { "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5Cdd0Y9TkTxkcosDq0rJgjR }, "description": "The meeting point is on the way to Lumbisí } ], "redemption": { "redemptionType": "NONE", "specialInstructions": "" }, "travelerPickup": { "pickupOptionType": "MEET_EVERYONE_AT_START_POINT", "allowCustomTravelerPickup": true } }, "timeZone": "America/Guayaquil", "description": "the only legal paragliding operator in ecuador. See an "inclusions": [ { "category": "OTHER", "categoryDescription": "Other", "type": "OTHER", "typeDescription": "Other", "otherDescription": "Paragliding Kit" }, { "category": "OTHER", "categoryDescription": "Other", "type": "OTHER", "typeDescription": "Other", "otherDescription": "Air-conditioned vehicle" } ], "additionalInfo": [ { "type": "STROLLER_ACCESSIBLE", "description": "Infants and small children can ride in a pram o },
```

```
{ "type": "NO_PREGNANT", "description": "Not recommended for pregnant travelers" }, { "type": "NO_HEART_PROBLEMS", "description": "Not recommended for travelers with poor cardiov }, { "type": "PHYSICAL_EASY", "description": "Suitable for all physical fitness levels" } ], "cancellationPolicy": { "type": "STANDARD", "description": "For a full refund, cancel at least 24 hours before "cancelIfBadWeather": true, "cancelIfInsufficientTravelers": false, "refundEligibility": [ { "dayRangeMin": 1, "percentageRefundable": 100 }, { "dayRangeMin": 0, "dayRangeMax": 1, "percentageRefundable": 0 } ] }, "bookingConfirmationSettings": { "bookingCutoffType": "FIXED_TIME", "bookingCutoffInMinutes": 1440, "confirmationType": "INSTANT", "bookingCutoffFixedTime": "16:00:00" }, "bookingRequirements": { "minTravelersPerBooking": 1, "maxTravelersPerBooking": 4, "requiresAdultForBooking": false }, "bookingQuestions": [ "FULL_NAMES_LAST", "PASSPORT_EXPIRY", "PASSPORT_PASSPORT_NO", "SPECIAL_REQUIREMENTS",
```

<!-- image -->

<!-- image -->

The example above gives the first five product records in the catalogue, with modification dates in chronological order. Note that products with a "status" of "INACTIVE" are products that have been temporarily disabled by the supplier and are therefore unavailable - when this is the case, all other requests for this product should be avoided.

Included in the response is the nextCursor element, which contains an identification code that points to the next page of product records; i.e.:

"nextCursor": "MTYwNTI3NzMyOHwxNjQ0MTNQMXxJTkFDVElWRQ=="

In your next call to /products/modified-since , provide the value of nextCursor in the cursor parameter to get the next page of results:

GET https //api sandbox viator com/partner/products/modified-since?count=500&amp;curso : . . .

The response will be similar to the initial response shown above, except it will contain the next 500 product records and a new nextCursor that points to the following page, and so on.

Continue calling /products/modified-since using the nextCursor value in the cursor parameter to retrieve all pages of results. You will eventually receive a response that contains an empty products array and does not contain a nextCursor element. The absence of the nextCursor element indicates that you have, for the time being, reached the end of the list and have received all product records from our catalogue.

## Example final page response

{

"products": []

}

## Periodically update your product records

Now that you have all product records from our catalogue, you can keep it up-to-date by periodically polling the service using the most-recent nextCursor code you received. Regardless of how frequently you call /products/modified-since , you will always receive all product update information so long as you keep track of the last cursor you received and use that in your subsequent call.

You should never need to re-ingest the entire product catalogue unless you need to re-initialize your database. This may happen frequently during development, but never (or rarely) in production. Due to the large volume of data, we strongly recommend keeping it to a minimum.

Products are considered updated when the supplier makes any changes to the product's details, excluding pricing and availability changes, which are retrieved from the availability schedules endpoints.

When the supplier publishes their product detail updates, the modified product /products/modified-since service will respond to this same call with newly-modified products in the products array and a new nextCursor element with which to poll the service for future updates in the same way.

It would be reasonable to poll this service on an hourly basis, updating those records in your local copy of the product catalogue as they become available.

Note that the nextCursor code is valid indefinitely; it will not expire.

## Filtering out products

You are free to choose which products to store on your system and sell. As the product content endpoints return all available products, you will need to perform the filtering step yourself at the time of ingestion. If a product contains attributes that you do not desire; e.g., the type of product, where it operates, etc., simply discard the update and do not add it to your database.

## Filtering out manual-confirmation products

Unless you have established the required functionality on your site to sell manual confirmation products you will need to exclude all non-instant confirmation products from your catalogue.

Instant confirmation products can be identified by the value of bookingConfirmationSettings.confirmationType

content response ; e.g.:

<!-- image -->

Products wih a confirmationType of "MANUAL" or "INSTANT\_THEN\_MANUAL" should be excluded if you do not wish to sell manual confirmation products.

## Please note :

- The product catalog must be ingested and updated using the /products/modified-since endpoint, unless you are only selling a relatively small subset of the products available in the Viator catalog. If that is the case, you may prefer to use the /products/bulk endpoint to ingest your selected products.
- Important : the /products/{product-code} endpoint should not be used for bulk ingestion purposes. Your product ingestion/update strategy is one of our certification requirements and must be verified by us prior to your accessing the production server. To find out what our certification requirements are, see: Viator Merchant API Certification .

## Resolving references

Some information in the product content response is not communicated explicity; but rather, by reference, and therefore requires an extra de-referencing step to acquire the full details of the element.

These data types comprise:

- locations
- destinations
- tags

The following sections describe how to de-reference these elements using the API.

## Location references

being

<!-- image -->

in the response product

All locations within the product content response are given as a location reference; e.g.:

```
"activityInfo": { "location": { "ref": "LOC-o0AXGEKPN4wJ9sIG0RAn5Cdd0Y9TkTxkcosDq0rJgjR12IzpogNi5POX+yGLXEo },
```

These location references can be resolved using the /locations/bulk endpoint; for example:

## Request :

```
{ "locations": [ "LOC-o0AXGEKPN4wJ9sIG0RAn5Cdd0Y9TkTxkcosDq0rJgjR12IzpogNi5POX+yGLXEoq", "LOC-6eKJ+or5y8o99Qw0C8xWyK8Z2imHSU8Ozi+NYupJVyI=" ] }
```

## Response :

```
{ "locations": [ { "provider": "GOOGLE", "reference": "LOC-o0AXGEKPN4wJ9sIG0RAn5Cdd0Y9TkTxkcosDq0rJgjR12IzpogNi5POX+yG "providerReference": "ChIJS1UFbTyX1ZER0vTgCLKWCEQ" }, { "provider": "TRIPADVISOR", "reference": "LOC-6eKJ+or5y8o99Qw0C8xWyK8Z2imHSU8Ozi+NYupJVyI=", "name": "Valley of the Roses", "address": { "street": "Dades Valley, near Bouteghrar", "administrativeArea": "El Kelaa M'gouna", "country": "Morocco", "countryCode": "MA", "postcode": "43000" }, "center": { "latitude": 34.00061, "longitude": -6.84494 } }
```

]

}

Note that there are two different location information providers, "TRIPADVISOR" and "GOOGLE" , referring to locations in the Tripadvisor location database or locations provided by the Google Maps platform via the Google Places API , respectively.

<!-- image -->

Tripadvisor locations include full details of the location in the response from /locations/bulk , including address and geolocation information. However, you will need to use the Google Places API to retrieve details for Google Maps locations.

The purpose of referring to locations by reference is to avoid the unnecessary transmission of duplicate data, as multiple products may include the same location reference. Therefore, we recommend caching the data received from this endpoint, checking this first to see if a particular location's details have been retrieved by your system in the past before making a request to /locations/bulk .

Requests can be made to /locations/bulk asynchronously; e.g., during the content ingestion process.

## Destination references

Every product in the Viator catalogue is categorized according to the destination/locale in which it operates.

There are multiple kinds of destination, which includes cities, regions, countries and others

## Example destinations *:

| type          | destinationId   | destinationName            |
|---------------|-----------------|----------------------------|
| AREA          | 51912           | Machame                    |
| CITY          | 343             | Bangkok                    |
| COUNTRY       | 749             | Panama                     |
| COUNTY        | 51632           | Xiahe County               |
| DISTRICT      | 51921           | Hunza                      |
| HAMLET        |                 |                            |
| ISLAND        | 51220           | Syros                      |
| NATIONAL PARK | 51196           | Death Valley National Park |
| NEIGHBORHOOD  | 60465           | Kensington                 |
| PENINSULA     | 51769           | Michamwi                   |
| PROVINCE      | 51255           | Mendoza Province           |

| type            | destinationId   | destinationName   |
|-----------------|-----------------|-------------------|
| REGION          | 4431            | Northern China    |
| STATE           |                 |                   |
| TOWN            | 50971           | Swansea           |
| UNION TERRITORY | 51542           | Daman and Diu     |
| VILLAGE         | 51011           | Pyrgos            |
| WARD            | 52140           | Shibuya           |

- Notes: The examples above are subject to change. These are all currently supported destination types, though for some there are no live examples at the moment

Every product has one or more destinations associated with it by way of its destination reference. This is given in the destinations object in the response from any of the product content endpoints; e.g.:

```
"destinations": [ { "ref": "34198", "primary": true } ],
```

To de-reference destination identifiers, you must use our destination taxonomy, which can be retrieved from the /destinations endpoint.

You may wish to filter products according to destination.

A call to /destinations will return data for all available destinations. You must store a local copy of this mapping information, as destination data does not change frequently - i.e., new destinations are rarely added. On-demand updates can be done in the event you encounter a product associated to a destination reference for which you do not have the details.

Example snippet of destination taxonomy :

<!-- image -->

```
"latitude": -8.68877, "longitude": 115.161267 } }, { "destinationId": 901, "name": "Buenos Aires", "type": "CITY", "parentDestinationId": 22280, "lookupId": "9.78.22280.901", "destinationUrl": "https://shop.live.rc.viator.com/x/d901-ttd?mcid=42383&pid=P001 "defaultCurrencyCode": "ARS", "timeZone": "America/Argentina/Buenos_Aires", "iataCode": "BUE", "center": { "latitude": -34.6084175, "longitude": -58.3731613 } }, ...
```

Note that destinations are organized into a hierarchy. The destination's position in the hierarchy can be determined according to the parentDestinationId and lookupId fields.

In the second example above, Buenos-Aires is a "CITY" , and it has a parentDestinationId of 22280 , which is the destinationId of "The Pampas" - the "REGION" in South America where Buenos-Aires is located.

The destination's full lineage with respect to the hierarchy is given in lookupId , which is a series of destination ids separated by periods - in this case:

```
"lookupId": "9.78.22280.901"
```

|   Component | Destination name   | Destination type                |
|-------------|--------------------|---------------------------------|
|           9 | (unnamed)          | (broad continental designation) |
|          78 | Argentina          | "COUNTRY"                       |
|       22280 | The Pampas         | "REGION"                        |
|         901 | Buenos-Aires       | "CITY"                          |

Using this information, you are able to categorize each product into its geographical location for display and search purposes.

## Tag references

Each product is also categorized according to its content, features or theme. Each attribute has a corresponding identifier called a 'tag'. The tag references for each product are contained in the tags array, in the response from any of the product content endpoints.

Example tags array (product 250380P1 - Surf lessons Bali, Canggu ):

```
"tags": [ 20246, 21946, 20244 ],
```

These numeric tag identifiers can be de-referenced using information available from the /products/tags endpoint. This service takes no parameters and retrieves information for all available tags.

To learn more about tags, see this article: Viator tags, explained

We recommend you store a local copy of this information, as tags do not change frequently. It is only necessary to re-ingest from this endpoint in the event you encounter a product that references a tag for which you do not have the details.

As with destinations, tags are organized into a hierarchy. A tag's relative position within that hierarchy can be determined by tracing back through its parent tag ids, which (if the tag has any) are listed in its parentTagIds element. Each tag can have multiple parent tags, and each tag can eventually be traced back to its parent. Parent tags are tags that have no parents; i.e., they are at the top of the hierachy.

For example, tag: 20244 (Sports Lessons) in /products/tags response:

<!-- image -->

<!-- image -->

The parentTagIds for 20244 - Sports lessons are:

- 21478 - "Active &amp; Outdoor Classes"
- 21909 - "Outdoor Activities"
- 21915 - "Classes &amp; Workshops"

These three tags have no parent tags, and are therefore at the top of the hierarchy. Applying this same process to the other tags in the tags array, we can determine the full set of tags for this product, in this case:

- 21909 - "Outdoor Activities"
- 21478 - "Active &amp; Outdoor Classes"
- 20244 - "Sports lessons"
- 21915 - "Classes &amp; Workshops"
- 21946 - "Good for avoiding crowds"
- 21442 - "On the water"
- 20246 - "Surfing lessons"

By traversing the hierarchy in this way, we have surfaced seven tags that pertain to this product with different levels of generality; i.e. it is an 'active and outdoor class', and it is a 'sports lesson'. More generally, it is an 'outdoor activity', a class or workshop, and is 'good for avoiding crowds':

In this way, you can categorize products for search and recommendation purposes, or to create category display and search buttons as seen on viator.com 'things to do' pages ; e.g.:

## Brisbane Tours

## Add dates

<!-- image -->

Outdoor

Activities

<!-- image -->

<!-- image -->

<!-- image -->

## Ingesting and updating availability schedules

Availability schedule information for all products is available to be ingested and updated via the /availablity/schedules/modified-since endpoint. This endpoint functions in a similar manner to the /products/modified-since endpoint; i.e., an initial call is made that returns all availability data in bulk, and then calls are made periodically to that same endpoint, which will return a delta update.

Therefore, to initialize your local copy of our availability schedule information, make a call to /availability/schedules/modified-since , including only the count query parameter, which we recommend setting to 500 .

For the sake of brevity, in the following example,

## Example request

<!-- image -->

You will receive a response similar to the following:

<!-- image -->

<!-- image -->

is set to

<!-- image -->

<!-- image -->

<!-- image -->

The endpoint returns an array ( availabilitySchedules ) where each item contains all availabilty schedule information for a single product, and a cursor ( nextCursor ) that is to be used in subsequent calls to this endpoint to retrieve the next page of results.

For details on how to interpret the availability schedule object, see Availability schedules .

Note : An empty bookableItems array means that the product indicated by productCode is not active, has no availability, and therefore cannot be booked. This fact will be reflected if the product details are requested from the /products/{product-code} endpoint; e.g., for product 3033ENTRY\_TR :

<!-- image -->

## Pagination

As with the /products/modified-since endpoint, you will receive as many records as requested via the count request parameter. Included in the response is the nextCursor element, which contains a code that points to the next page of availability records.

After receiving this first response, your next request to the /availablity/schedules/modified-since service should include the value of nextCursor in the cursor request parameter; i.e.:

## GET https //api sandbox viator com/partner/availability/schedules/modified-since?c : . . .

The response will be similar to the initial response shown above, except it will contain the next count number of availability schedule records and a new nextCursor that points to the following page.

Loop through this process until you receive a response that contains an empty availabilitySchedules array and does not contain a nextCursor element. The absence of the nextCursor element indicates that you have, for the time being, reached the end of the list and your availability information is fully up-to-date.

## Example final page response

{

"availabilitySchedules": []

}

## Periodically update your availability information

Once your availability schedule information ingestion is complete, you can keep it up-to-date by periodically polling the service using the latest nextCursor code you received; i.e., from the page prior to the final, empty page.

If new availability schedule information is available, the service will respond with new availability information in the availabilitySchedules array and a new nextCursor element with which to poll the service for future updates in the same way. Note that the nextCursor code is valid indefinitely; it will not expire.

As with the /products/modified-since endpoint, we recommend polling this service on an hourly basis. The longer the interval between updates, the more likely your availability information will be out of date, raising the likelihood of availability differences when you make a real-time availability check using the /availability/check service.

Again, you should only need to call /availablity/schedules/modified-since without a cursor parameter once , for the first call of the initial ingestion. All future calls should include the cursor parameter and the results used to update your database.

## Filtering out availability schedules

As you may not be offering Viator's full product catalogue for sale on your site, you are only required to store availability information for the products you support. Therefore, if you are filtering out products from our catalogue, you should also perform a check with regard to the availability schedule information received from the /availablity/schedules/modified-since to ensure that it pertains to a product in your catalogue.

This can be done by checking the productCode field in the ProductAvailabilitySchedule object response.

## Please note :

- The availability and pricing schedules must be ingested and updated using the /availability/schedules/modified-since endpoint, unless you are only selling a relatively small subset of the products available in the Viator catalog. If that is the case, you may prefer to use the /availability/schedules/bulk endpoint to ingest your selected product availability schedules.
- Important : the /availability/schedules/{product-code} endpoint should not be used for bulk ingestion purposes. Your availability schedule ingestion/update strategy is one of our certification requirements and must be verified by us prior to your accessing the production server. To find out what our certification requirements are, see: Viator Merchant API Certification .

## Update frequency

We expect that your update frequency will not be more frequent than the following guidelines. More frequent updates will place an excessive burden on our systems and may result in your integration being shut off.

See section on Rate Limiting for more information.

## Fixed-cadence delta updates

In order to keep your local databases up-to-date without placing an excessive burden on our servers, we expect you use the following fixed cadences at which you should poll the content-ingestion endpoints:

| Endpoint                                | Update cadence                                                                                                                                                                                                 |
|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /products/modified-since                | Every 15-30 minutes following initial ingestion                                                                                                                                                                |
| /availability/schedules/modified- since | Every 15-30 minutes following initial ingestion                                                                                                                                                                |
| /bookings/modified-since                | Every 5-10 minutes following initial ingestion to stop notification emails sent by Viator for supplier cancellations of bookings made through the API (merchant partners only). Hourly for all other scenarios |
| /bookings/modified- since/acknowledge   | Right after ingesting the booking modifications                                                                                                                                                                |

## Fixed-cadence full updates

To ensure your systems reflect any removals of or changes to existing destinations, locations or booking questions, we expect that you retrieve full updates from these endpoints as follows:

| Endpoint                        | Update cadence   |
|---------------------------------|------------------|
| /destinations                   | Weekly           |
| /attractions/search             | Weekly           |
| /products/booking-questions     | Monthly          |
| /products/tags                  | Weekly           |
| /products/recommendations       | Weekly           |
| /locations/bulk                 | Monthly          |
| /reviews/product                | Weekly           |
| /bookings/cancel-reasons        | Monthly          |
| /suppliers/search/product-codes | Weekly           |
| /bookings/status                | Hourly           |
| /exchange-rates                 | Daily            |

## On-demand updates

When ingesting product content, in the event that you encounter an unknown reference - i.e., a new location reference, booking question, tag or destination id - or, if you need to perform a currency conversion for which the last exchange rate you retrieved has expired, we expect you to call the relevant endpoint to resolve the new reference immediately or just after completing the product content update.

| Endpoint                     | When to update                                                                                                                                                                                                                                                             |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /exchange-rates              | Whenever you encounter a currency that you need to convert, but the last-retrieved exchange-rate for that currency-pair is no longer valid due to having expired (according to the expiry value in the response from this endpoint)                                        |
| /locations/bulk              | Whenever you encounter a location reference code that you do not yet have the details for (we recommend retrieving location details in batches using this endpoint; therefore, the retrieval of new location data can commence after all new product content is retrieved) |
| /products/tags               | Whenever you encounter a tag reference code that you do not yet have the details for                                                                                                                                                                                       |
| /destinations                | Whenever you encounter a destination id that you do not yet have the details for                                                                                                                                                                                           |
| /products/booking- questions | Whenever you encounter a booking question identifier that you do not yet have the details for                                                                                                                                                                              |

| Endpoint                      | When to update                                                                                                                                                                                                                                                                                                                                                             |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /attractions/{attraction- id} | Whenever you encounter an attraction identifier that you do not yet have the details for                                                                                                                                                                                                                                                                                   |
| /reviews/product              | If the number of reviews available for a product, which is reported in the reviews.totalReviews element in the product content response , has changed compared with its previous value, the reviews for that product should also be refreshed by calling the /reviews/product endpoint. We request that you rate-limit your use of this service to 30 requests per minute. |
| /bookings/status              | Whenever you encounter a booking waiting for manual confirmation. Must not be called more than once every 3 minutes.                                                                                                                                                                                                                                                       |

## Rate limiting

We impose rate limits on the usage of this API to prevent excessive demands being made of our system that might otherwise affect its availability for all users.

Our methodology involves applying a rate-limit on a per-endpoint / per-PUID (Partner Unique ID) basis; therefore, reaching the rate-limit with respect to your usage of one endpoint will only affect the availablility of that endpoint, not the others.

We do not have a universal rate limit that applies to all users. The rate limit you are required to operate within is based on a standard commensurate with the scale of your operation.

This is to say that if the volume of traffic to your site is such that under normal conditions your operations are causing you to frequently receive HTTP 429 (Too Many Requests) responses, you can ask for your ratelimit to be increased. If that is the case, please speak to your account manager to discuss whether increasing your rate limit would be the appropriate solution.

## Interpreting the HTTP 429 response

If a request to an endpoint yields an HTTP 429 (Too Many Requests) response, information regarding your present usage status can be located in the following four header fields:

- RateLimit-Limit
- Total limit of requests for this endpoint per rolling 10s time window
- RateLimit-Remaining :
- The number of requests that remain available to you in the present 10s period
- RateLimit-Reset :
- How long (in seconds) from the present moment it would take for the number of available requests to reach its maximum value

- Retry-After :
- A recommendation regarding how long (in seconds) it would be optimal to wait before making a subsequent call to that endpoint

## Example HTTP 429 response:

```
HTTP/1.1 429 ... .. RateLimit-Limit: 16 RateLimit-Remaining: 0 RateLimit-Reset: 10 Retry-After: 10 ... .. { "code":"TOO_MANY_REQUESTS", "message":"Too many requests, please try again", "timestamp":"2022-09-13T13:25:26.179433Z", "trackingId":"4badb933-ad65-4464-ae9c-c20e4a70c0d2" }
```

This can interpreted as:

```
RateLimit-Limit: 16
```

- You can make 16 requests to this endpoint per 10s rolling time window
- You have no remaining requests available in the current 10s epoch (as you would expect, since it is for this reason that you are receiving this response in the first place)
- If you were to wait 10s, your RateLimit-Remaining value would reach its maximum; which, in this case, is 16 requests
- It is recommended you pause for 10s before re-attempting to call this endpoint

```
RateLimit-Remaining: 0
```

```
RateLimit-Reset: 10
```

```
Retry-After: 10
```

Note that these rate-limit-related values will also be returned in the HTTP 200 (success) response. Inspect these values if you wish to estimate whether your method of implementing this API will remain sustainable at scale.

## Concurrency-based rate limiting

While rate-limiting is imposed per API key, if our system reaches its capacity on account of high demand overall, you may be rate limited even though you have not personally exceeded your individual rate limit.

In this case, you will receive a HTTP 503 (Service Unavailable) response. The header of this response will include the Retry-After field. In the example below, the recommendation is to pause for 60s before retrying the request: e.g.:

<!-- image -->

## Appendices

## Inclusions &amp; exclusions

The inclusions and exclusions arrays are returned for active products in the response from the product content endpoints . The array items for both inclusions and exclusions are objects defined by the same schema, InclusionExclusionItem .

The following table describes the mapping of the possible combinations of category , categoryDescription , type , and typeDescription elements of the object in the response that you may encounter.

New Categories and types can be added over time, allowing flexibility for different use cases.

Note: Changes on the table below become effective by the end of April 2025, see Notes column for details.

<!-- image -->

<!-- image -->

|                  |                | "ALL_FEES_AND_TAXES"                       |
|------------------|----------------|--------------------------------------------|
|                  |                | "FUEL_SURCHARGE"                           |
|                  |                | "GRATUITIES"                               |
|                  |                | "GST"                                      |
|                  |                | "LANDING_AND_FACILITY_FEES"                |
|                  |                | "PARKING_FEES"                             |
|                  |                | "ADMISSION_FEES"                           |
|                  |                | "ENTRANCE_FEES"                            |
|                  |                | "GOVERNMENT_FEES"                          |
|                  |                | "ALCOHOLIC_BEVRAGES" "ALCOHOLIC_BEVERAGES" |
|                  |                | "BOTTLED_WATER"                            |
|                  |                | "BREAKFAST"                                |
|                  |                | "BRUNCH"                                   |
|                  |                | "COFFEE_AND_TEA"                           |
| "FOOD_AND_DRINK" | Food and drink | "DINNER"                                   |
|                  |                | "LUNCH"                                    |
|                  |                | "REFRESHMENTS"                             |
|                  |                | "SNACKS"                                   |
|                  |                | "SODA_POP"                                 |
|                  |                | "MEALS"                                    |
| "SOUVENIRS"      | Souvenirs      | "CERTIFICATE"                              |

<!-- image -->

|                       |                          | "RECIPE_BOOKLET"              |
|-----------------------|--------------------------|-------------------------------|
| "TRANSPORT_AMENITIES" | Transportation amenities | "AIR_CONDITIONED_VEHICLE"     |
| "TRANSPORT_AMENITIES" | Transportation amenities | "PRIVATE_TRANSPORTATION"      |
| "TRANSPORT_AMENITIES" | Transportation amenities | "RESTROOM_ON_BOARD"           |
| "TRANSPORT_AMENITIES" | Transportation amenities | "WIFI_ONBOARD"                |
| "TRANSPORT_AMENITIES" | Transportation amenities | "PUBLIC_TRANSPORTATION"       |
| "EQUIPMENT"           |                          | "ALL_INGREDIENTS"             |
| "EQUIPMENT"           |                          | "USE_OF_OTHER_EQUIPMENT"      |
| "EQUIPMENT"           |                          | "USE_OF_BICYCLE"              |
| "EQUIPMENT"           |                          | "USE_OF_COOKING_UTENSILS"     |
|                       | Use of Equipment         | "USE_OF_SCUBA_EQUIPMENT"      |
|                       | Use of Equipment         | "USE_OF_SEGWAY"               |
|                       | Use of Equipment         | "USE_OF_SNORKELING_EQUIPMENT" |
|                       | Use of Equipment         | "USE_OF_TRIKKE"               |
|                       | Use of Equipment         | "BOOSTER_SEAT"                |
|                       | Use of Equipment         | "LOCKER"                      |
| "EXCESS_CHARGES"      | Excess charges           | "EXCESS_BAGGAGE"              |
| "EXCESS_CHARGES"      | Excess charges           | "OVER_WEIGHT_LIMIT"           |
| "OTHER"               | Other                    | "OTHER"                       |

## Update history

| Date         | Description                                                                                                                                                                               |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 31 Oct 2022  | Removed v1-v2 migration reference section                                                                                                                                                 |
| 14 Sep 2022  | Revised Workflows - Rate limiting and HTTP 429 response description with respect to new rate-limiting policy                                                                              |
| 23 Aug 2022  | Clarified new standard rate-limiting policy that applies to all endpoints in new section: Workflows - Rate limiting                                                                       |
| 15 Aug 2022  | Altered advice regarding the recommended frequency for fixed cadence full updates for various endpoints in Workflows - Update frequency section                                           |
| 3 Aug 2022   | Updated descriptions of /products/modified-since , /products/bulk and /products/{product- code} to highlight the polymorphism in the response / discriminator drop-down on status element |
| 1 Aug 2022   | Renamed Key Concepts - Content ingestion endpoints to Key Concepts - Product Content and availability endpoints and updated this section with usage recommendations                       |
| 27 July 2022 | Updated conditonal booking questions logic table to include advice about TRANSFER_DEPARTURE_MODE booking question                                                                         |
| 18 July 2022 | Modifed /bookings/cancel-reasons endpoint to accept a query parameter to specify customer or supplier-initiated cancellation reasons                                                      |
| 18 July 2022 | Added two new endpoints to allow merchant partners to manage supplier-initiated booking cancellations: /bookings/modified-since and /bookings/modified-since/acknowledge                  |
| 6 July 2022  | Improved descriptions of lineItems and totalPrice elements of bookableItems[] object array in /availability/check endpoint response                                                       |

| Date         | Description                                                                                                                                                                                                                                                                 |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 30 June 2022 | Clarified conditions in conditional booking questions section of Booking concepts - Booking questions section                                                                                                                                                               |
| 29 June 2022 | Added target-lander query parameter to /products/{product-code} , /products/modified-since , /products/bulk and /products/search endpoints                                                                                                                                  |
| 23 June 2022 | Added attractionId to filtering options in /products/search endpoint                                                                                                                                                                                                        |
| 22 June 2022 | Updated string length specifications in VoucherInfo schema and partnerBookingRef in /bookings/book request object                                                                                                                                                           |
| 20 June 2022 | Updated maximum string length specifications for /bookings/book request object (BookerInfo and CommunicationInfo schemata)                                                                                                                                                  |
| 3 June 2022  | Added new supplier search endpoint: /suppliers/search/product-codes                                                                                                                                                                                                         |
| 1 June 2022  | Added links to various articles on the Viator Partner Resource Center throughout document                                                                                                                                                                                   |
| 26 May 2022  | Added advice about review authenticity: Key concepts - Review authenticity                                                                                                                                                                                                  |
| 23 May 2022  | Added partnerNetFromPrice property to ProductSearchPricing schema spec in response from /products/search endpoint                                                                                                                                                           |
| 20 May 2022  | Added advice regarding whether or not an endpoint should be used to ingest details about the entire product catalog to /products/{product-code} , /products/bulk , /availability/schedules/{product-code} and /availability/schedules/modified-since endpoint descriptions. |
| 17 May 2022  | Added note about extra validation requirements for communication.phone field in request to /bookings/book endpoint                                                                                                                                                          |
| 11 May 2022  | Modified update frequency recommendation for /locations/bulk endpoint from 'weekly' to 'monthly' due to the relatively changeless nature of locations data.                                                                                                                 |

| Date        | Description                                                                                                                                                                            |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 10 May 2022 | Modified description of /exchange-rates endpoint to include additional currencies (ARS, CLP, COP, ILS, PEN, PHP) available for conversion                                              |
| 1 Apr 2022  | Modified note to Booking questions - Conditional booking questions (third bullet in 'Extra notes')                                                                                     |
| 22 Mar 2022 | Added note to Booking questions - Conditional booking questions (third bullet in 'Extra notes')                                                                                        |
| 8 Mar 2022  | Corrected "OTHER_HEALTH" to "HEALTH_OTHER" in AdditionalInfo schema used in the product response                                                                                       |
| 11 Feb 2022 | Removed note about no-index policy from /v1/attraction/products endpoint                                                                                                               |
| 9 Feb 2022  | Added Booking concepts - Low-margin products section                                                                                                                                   |
| 1 Feb 2022  | Added Conventions - Endpoint timeout settings section                                                                                                                                  |
| 5 Jan 2022  | Corrected response schema details in /bookings/{booking-reference}/cancel and /bookings/{booking-reference}/cancel-quote to indicate that status and bookingId are required properties |
| 15 Nov 2021 | Added Basic-access Affiliate postman collection to Testing section                                                                                                                     |
| 5 Nov 2021  | Clarified description of exp-demo header parameter                                                                                                                                     |
| 2 Nov 2021  | Added "LOCATION" as option for logistics.travelerPickup.locations[].pickupType in product content response                                                                             |
| 5 Jan 2022  | Corrected response schema details in /bookings/{booking-reference}/cancel and /bookings/{booking-reference}/cancel-quote to indicate that status and bookingId are required properties |
| 15 Nov 2021 | Added Basic-access Affiliate postman collection to Testing section                                                                                                                     |
| 5 Nov 2021  | Clarified description of exp-demo header parameter                                                                                                                                     |

| Date        | Description                                                                                                                                                              |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2 Nov 2021  | Added "LOCATION" as option for logistics.travelerPickup.locations[].pickupType in product content response                                                               |
| 28 Oct 2021 | Updated Booking Concepts - Booking questions - Conditional booking questions table                                                                                       |
| 15 Oct 2021 | Modified PriceObject schema in response from /availabililty/* endpoints to include provision for commission-payment-model merchants. See /availability/check for example |
| 13 Oct      | Added section: How to determine if a product option supports pickup                                                                                                      |
| 7 Oct 2021  | Added "TRANSFER_ARRIVAL_DROP_OFF" booking question details in Booking details - conditional booking concepts section                                                     |
| 1 Oct 2021  | Changed 'standard access' to 'full access' in Access to endpoints section                                                                                                |
| 1 Oct 2021  | Added note about "TRANSFER_PORT_CRUISE_SHIP" booking question to Booking concepts - Booking questions section                                                            |
| 27 Sep 2021 | Added note about time-out recommendation to /bookings/book                                                                                                               |
| 16 Sep 2021 | Removed topX and modified options for sortOrder request parameters in /attraction/reviews/ endpoint                                                                      |
| 13 Sep 2021 | Added reference element to Supplier schema of ActiveProduct                                                                                                              |
| 6 Sep 2021  | Modified available options for sortOrder request parameter in /v1/taxonomy/attractions and /v1/search/attractions endpoints                                              |
| 27 Aug 2021 | Added basic and full-access affiliate types to Access to endpoints section                                                                                               |
| 26 Aug 2021 | Added Key concepts - Protecting unique content section                                                                                                                   |
| 23 Aug      | Added Key concepts - v1 to v2 migration reference - Mapping categories to tags section                                                                                   |

| Date        | Description                                                                                     |
|-------------|-------------------------------------------------------------------------------------------------|
| 2021        |                                                                                                 |
| 19 Aug 2021 | Added Tripadvisor as an additional reviews provider in /reviews/product endpoint                |
| 12 Aug 2021 | Updated Access to endpoints section to include /products/booking-questions and /bookings/status |
| 10 Aug      | Bugfix - provider element in request to /reviews/product now listed as 'required'               |
| 5 Aug 2021  | Added new sorting options to /reviews/product endpoint                                          |
| 1 Jul 2021  | Added Workflows - Update frequency section                                                      |
| 22 Jun 2021 | Deprecated /v1/product/reviews endpoint                                                         |
| 21 Jun 2021 | Added /reviews/product endpoint                                                                 |
| 18 Jun 2021 | Added /products/search endpoint                                                                 |
| 9 Jun 2021  | Added Booking concepts - supplier communications                                                |
| 9 Jun 2021  | Added Booking concepts - working with age bands section                                         |
| 4 Jun 2021  | Added premium viatorUniqueContent element to ActiveProduct                                      |
| 27 May 2021 | Added Booking-concepts - Per-person and unit pricing section                                    |
| 21 May 2021 | Added reviews element to responses of product content endpoints                                 |

| Date        | Description                                                                                                                                                                                                          |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 14 May 2021 | Added Age-bands section to Booking concepts - Booking questions section                                                                                                                                              |
| 5 May 2021  | Updated Conditional booking questions table in Booking concepts - Booking questions section                                                                                                                          |
| 25 Mar 2021 | Added v1 endpoints for affiliate partners                                                                                                                                                                            |
| 23 Mar      | Added Resolving references section                                                                                                                                                                                   |
| 11 Mar 2021 | Added campaign-value parameter to /products/modified-since , /products/bulk and /products/{product-code} endpoints; added AvailabilityScheduleSummary summary schema to /availability/schedules/* endpoint responses |
| 16 Feb 2021 | Added Determining ratings section; added Conventions - Accept-Encoding section                                                                                                                                       |
| 21 Jan 2021 | Extended BookingBookRequest schema (used in /bookings/book ) to include new AdditionalBookingDetails schema to allow custom voucher text                                                                             |
| 18 Jan 2021 | Modified rejectionReasonCode in responses from /bookings/book and /bookings/status endpoints                                                                                                                         |
| 12 Jan 2021 | Added Key concepts - Booking confirmation types section as sale of manual confirmation products has now been enabled.                                                                                                |
| 7 Dec 2020  | Added DayOperatingHours schema array to BookableItemSeason schema in availability- schedules endpoints                                                                                                               |
| 24 Nov 2020 | Added Key concepts - Booking cutoff times section                                                                                                                                                                    |
| 12 Nov 2020 | Added Workflows - Checking booking status section                                                                                                                                                                    |
| 6 Nov 2020  | Added /bookings/status endpoint specification                                                                                                                                                                        |

| Date        | Description                                                                                                                                                                                                             |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 5 Nov 2020  | Added Workflows - Ingesting and updating availability schedules section                                                                                                                                                 |
| 4 Nov 2020  | Updated id values in /products/booking-questions endpoint                                                                                                                                                               |
| 3 Nov 2020  | Added Key concepts - V1 to V2 migration reference section                                                                                                                                                               |
| 28 Oct 2020 | Added sections for Activity , Hop-on hop-off and Unstructured itinerary types                                                                                                                                           |
| 13 Oct 2020 | - Added maxLength field to BookingQuestion schema in response from /products/booking-questions - Updated AdditionalInfo schema                                                                                          |
| 6 Oct 2020  | - Added Appendices - Inclusions and exclusions - Modified ActiveProduct schema to include new required Supplier element                                                                                                 |
| 1 Oct 2020  | Added About section                                                                                                                                                                                                     |
| 29 Sep 2020 | Added Key concepts - Availability Schedules section Added legacy helper endpoints /v1/taxonomy/destinations , /v1/taxonomy/attractions , v1/product/reviews , /v1/product/photos                                        |
| 28 Sep 2020 | Updated response schema for /products/tags                                                                                                                                                                              |
| 23 Sep 2020 | Added Key concepts - Booking questions section                                                                                                                                                                          |
| 22 Sep 2020 | Added Versioning section                                                                                                                                                                                                |
| 22 Sep 2020 | Fixed typo in StandardItineraryItem schema ( pointsOfInterestLocation -> pointOfIterestLocation ); added explanation of policy window time-stamps & updated response samples in Workflows - Cancellation policy section |
| 21 Sep 2020 | Added Making a booking section under Workflows                                                                                                                                                                          |
| 20 Sep      | Added currency element to /bookings/hold response schema                                                                                                                                                                |

| Date        | Description                                                                                                                                                                                                                                                                      |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2020        |                                                                                                                                                                                                                                                                                  |
| 17 Sep 2020 | Breaking change: /exchange-rates endpoint refactored                                                                                                                                                                                                                             |
| 16 Sep 2020 | Note : ONLY freesale products (those with a confirmation type of "INSTANT") are presently able to be booked. See Ingesting and updating the product catalogue (Filtering-out on- request products) for instructions on how to filter-out on-request products from your catalogue |
| 16 Sep 2020 | Breaking change: languageGuideDetails element in ActiveProduct schema changed to languageGuides (array of LanguageGuide schema)                                                                                                                                                  |
| 15 Sep 2020 | Breaking change: removed travelerPickup element from /booking/book request                                                                                                                                                                                                       |
| 10 Sep 2020 | Added /bookings/book endpoint specification                                                                                                                                                                                                                                      |
| 1 Sep 2020  | Added description element to MultiDayTourFoodAndDrinks and InclusionExclusionItem schemata; added version=2.0 to Accept request header parameter across all endpoints                                                                                                            |
| 26 Aug 2020 | CancellationConditionType schema key strings updated (now "STANDARD", "MODERATE", "STRICT" & "ALL_SALES_FINAL"; PricingLineItem updated (affects /availability/check and /bookings/hold-confirm responses); /availability/* endpoints moved to separate 'Availability' section   |
| 25 Aug 2020 | Breaking changes : see below                                                                                                                                                                                                                                                     |
| 25 Aug 2020 | Regenerated response samples                                                                                                                                                                                                                                                     |
| 11 Aug 2020 | Updated paxMix schema in /availability/check                                                                                                                                                                                                                                     |
| 6 Aug 2020  | Added COVID-safety-measure keys to additionalInfo schema                                                                                                                                                                                                                         |
| 4 Aug 2020  | Added /bookings/hold endpoint                                                                                                                                                                                                                                                    |

| Date          | Description                                                                                                                                                                |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 28 July 2020  | Added Ingesting and updating the product catalogue section                                                                                                                 |
| 23 July 2020  | Added Product options , Cancellation policy sections                                                                                                                       |
| 16 Jul 2020   | Added /bookings/hold endpoint                                                                                                                                              |
| 3 Jul 2020    | Modified availability endpoint schema and regenerated examples                                                                                                             |
| 1 Jul 2020    | Removed internal-only markup for release                                                                                                                                   |
| 16 Jun 2020   | Added Workflows->Cancellation API workflow section                                                                                                                         |
| 15 Jun 2020   | Removed enum data type specification from UnavailableDate , ageBand , CancellationQuoteBookingStatus , CancellationResultItemReason and CancellationBookingStatus schemata |
| 18 May 2020   | Refactored LHS nav to use 'summary' name instead of operationId name                                                                                                       |
| 28 April 2020 | Added legacyGuide field to LanguageGuide object specification                                                                                                              |

## 25 August breaking changes

The following breaking changes have been made. Please update your OpenAPI specification by downloading from the link at the top of the page.

## Endpoint URL changes

- /availability-schedule/{product-code} -&gt; /availability/schedules/{product-code}
- /availability-schedule/bulk -&gt; /availability/schedules/bulk
- /availability-schedule/modified-since -&gt; /availability/schedules/modified-since

## Element name changes

A number of name changes have been made to the Product schema. This affects the following endpoints:

- /products/modified-since
- /products/bulk
- /products/{product-code}

<!-- image -->

## Products

## /products/modified-since

<!-- image -->

Get full product details for all products modified since a specified time. Initiate a full ingestion only to establish your local copy; this should be a rare occurrence compared to regular updates. Fetch incremental updates through this endpoint on an hourly basis. You are welcome to poll for updates as frequently as every 15 minutes if desired. Be mindful that excessive frequency beyond these recommendations may trigger rate limits.

## Note :

- See Ingesting and updating the product catalogue for instructions on how to use this service to ingest the full product catalogue and ensure that it remains up-to-date.
- The response object utilizes polymorphism and differs markedly depending on whether the product is active or inactive. Click the drop-down selector in the status description to toggle between an "ACTIVE" and "INACTIVE" product response.

## Examples:

Get all products in the Viator inventory with 500 products per response page:

GET https://api.sandbox.viator.com/partner/products/modified-since?count=500

Get the next page of results:

GET https://api.sandbox.viator.com/partner/products/modified-since?count=500&amp;cursor

Alternative pagination method (not recommended); e.g., if you have misplaced the cursor value or if for any other reason you wish to get all products modified since 2019-09-17T03:20:45.737043Z:

GET https://api.sandbox.viator.com/partner/products/modified-since?count=500&amp;modifi

(Response sample generated on: 2020-10-06)

AUTHORIZATIONS:

API-key

QUERY PARAMETERS

string

Pagination cursor received from a previous call to this endpoint that points to the desired starting point for the results.

Note : Pagination will come into play when the number of results exceeds the figure given in the count parameter. In this case, pass the content of the nextCursor element for the value of cursor to receive the next page of results. The final page of results will not include the nextCursor element. For more information, see: Ingesting and updating the product catalogue .

- Example: 'MTU3NDA0MzU1NQ=='

integer [ 1 .. 500 ]

cursor

count

required

campaign-value target-lander

modified-since

HEADER PARAMETERS

Specifies the maximum number of product detail items to be returned in each response from this endpoint string &lt;= 200 characters

Affiliate partners only : Specifies the campaign tracking identifier that will be appended to the URL returned in productUrl as a query parameter. Campaigns allow you to track how specific links perform, with metrics such as sessions, bookings, and commission. Reports are available via the Viator Partner Platform.

Note : If you wish to use a campaign value that includes non-alphanumeric characters (e.g., '+', '-', etc.), you must URL-encode these characters.

string

Affiliate partners only : Specifies the type of landing page customers will be shown when opening the link provided in the productUrl field.

Ordinarily, when customers follow the link in productUrl , they are redirected to a sales-conversion-optimized affiliate landing page. This default behavior can be disabled by setting this parameter to "NONE" , which will modify the productUrl query string such that when opened, the customer will instead land on the standard viator.com product display page, which is not optimized for affiliate-link sales.

## Available values:

- "NONE" : Causes target\_lander=NONE to be included in the productUrl query string, which will disable redirection to an affiliate landing page when the link is followed.

Our recommendation is for you to allow the default behavior by not including this parameter, unless you have a specific technical or business requirement to do so.

string &lt;date-time&gt; ^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])... Show pattern Only return products that have been modified since the date and time (UTC) specified by this timestamp

## Note :

- As this is a query parameter, colons (i.e., : ) in the timestamp should be URL-encoded as %3A ; e.g.: " 2020-09-30T00%3A00%3A01.737043Z "
- Using this parameter is not recommended as the standard pagination method; rather, use the cursor parameter to ensure all product updates are captured during ingestion.

Accept-Language required

Accept required

## Responses

## 200 Success

## RESPONSE HEADERS

|                                               | X-Unique-ID required                          | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|-----------------------------------------------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                               | RateLimit-Limit required                      | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
|                                               | RateLimit-Remaining required                  | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
|                                               | RateLimit-Reset required                      | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0                                                                                                                                  |
|                                               | products required                             | Array of objects (Product) Products that fall within the search/filter criteria                                                                                                |

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

string

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

## Pagination cursor pointing to the next page of results

- Example: "MTU3NDA0NDczOQ=="

<!-- image -->

Get full product details for all requested products (limited to 500 products per request)

## Note :

- This endpoint should not be used to ingest or update the product catalog. Instead, please use the /products/modified-since endpoint for that purpose.
- The response object utilizes polymorphism and differs markedly depending on whether the product is active or inactive. Click the drop-down selector in the status description to toggle between an "ACTIVE" and "INACTIVE" product response.

(Response sample generated on: 2020-10-06)

AUTHORIZATIONS:

QUERY PARAMETERS

campaign-value target-lander

API-key string &lt;= 200 characters

Affiliate partners only : Specifies the campaign tracking identifier that will be appended to the URL returned in productUrl as a query parameter. Campaigns allow you to track how specific links perform, with metrics such as sessions, bookings, and commission. Reports are available via the Viator Partner Platform.

Note : If you wish to use a campaign value that includes non-alphanumeric characters (e.g., '+', '-', etc.), you must URL-encode these characters.

string

Affiliate partners only : Specifies the type of landing page customers will be shown when opening the link provided in the productUrl field.

Ordinarily, when customers follow the link in productUrl , they are redirected to a sales-conversion-optimized affiliate landing page. This default behavior can be disabled by setting this parameter to "NONE" , which will modify the productUrl query string such that when opened, the customer will instead land on the standard viator.com product display page, which is not optimized for affiliate-link sales.

## Available values:

- "NONE" : Causes target\_lander=NONE to be included in the productUrl query string, which will disable redirection to an affiliate landing page when the link is followed.

Our recommendation is for you to allow the default behavior by not including this parameter, unless you have a specific technical or business requirement to

## HEADER PARAMETERS

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

REQUEST BODY SCHEMA:

application/json;version=2.0

Array of strings

&lt;= 500 items

List of product codes for which to retrieve full product details

Accept-Language required

Accept

required

- productCodes required

## Responses

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required     | string                                                                                                                                                                         |

do so.

The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.

RESPONSE SCHEMA: application/json;version=2.0

<!-- image -->

ticketInfo required

pricingInfo required

images logistics

required timeZone

required description

required inclusions

exclusions additionalInfo

required cancellationPolicy

object (TicketInfo)

Ticket/voucher details for this product

| object (PricingInfo)                                  |
|-------------------------------------------------------|
| Ticket/voucher details for this product               |
| Array of objects (Image) Images for this product      |
| object (Logistics) Logistics details for this product |

string(?s).*[\S].*

Code for the time zone in which this product operates (IANA TZ data format)

- Example : 'Australia/Sydney'

## string(?s).*[\S].*

Description of this product

- Example : "Climb the Sydney Harbour Bridge with an expert guid ultimate Sydney experience..."
- Note : This field contains natural language suitable for display to content will be translated (if necessary) into the language speci Accept-Language header parameter

## Array of objects

Features that are included with this product package

- Note : The same inclusion item may appear multiple times in this example, 'Lunch' . For a 7-day multi-day tour, 'Lunch' appearin times indicates that lunch is included on each of the seven days tour. This can be displayed as "Lunch (7)"

## Array of objects

Features that are not included with this product package

Array of objects (AdditionalInfo)

Facts necessary to communicate to travelers regarding this product

Note : Items included only if they apply, if they do not apply they will n included in the response.

object (CancellationPolicy)

| required                             | Cancellation policy details for this product.                                                                                                                                                             |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| bookingConfirmationSettings required | object (BookingConfirmationSettings) How this product's bookings are confirmed                                                                                                                            |
| bookingRequirements required         | object (BookingRequirements) Passenger type and number requirements for booking                                                                                                                           |
| languageGuides                       | Array of objects (LanguageGuide) Language guides available for this product across all product option                                                                                                     |
| bookingQuestions required            | Array of strings Array of machine-interpretable values specifying the facts that the tr must provide when booking this product; further details can be retrie /products/booking-questions endpoint        |
| tags required                        | Array of integers Array of numeric tag identifiers indicating the product categories into this product falls To retrieve details about which tags these identifie please use the /products/tags endpoint. |
| destinations required                | Array of objects (Destination) Destinations - i.e., cities, states, countries and regions - in which th can be considered to operate                                                                      |
| itinerary                            | object (Itinerary) Details about the places this product visits See: Key concepts - Itineraries for more information                                                                                      |
| productOptions                       | Array of objects (ProductOption) Product options (tour grades) available for this product                                                                                                                 |
| translationInfo                      | object (TranslationDetails) Information about whether the text in this response was machine-tra                                                                                                           |
| supplier required                    | object (Supplier) Supplier details                                                                                                                                                                        |
| productUrl                           | string URL for this product on the viator.com site, where the customer will their booking.                                                                                                                |

]

reviews required viatorUniqueContent

## 400 Bad Request

## 401 Unauthorized

This URL includes all the necessary information for viator to correctl and pay commission for the sale to the referring partner.

If campaign-value is included in the request, this URL will also inc campaign tracking value that you set.

For more information, see our guide to Affiliate Attribution on the Vi Partner Resource Center.

## Note :

- This element is only returned for affiliate partners.
- You must use the full URL and not modify it in any way - any ch could result in failure to attribute the sale to you, which means not be paid a commission for this sale.

Example format : https://www.viator.com/tours/Sydney/Sydney-and Hop-on-Hop-off-Tour/d357-5010SYDNEY? mcid=42383&amp;pid=P00045135&amp;medium=api&amp;version=2.0&amp;campaig object (ProductReviews)

Summary of reviews and ratings for this product

## Note :

- Review data is updated daily; i.e., all reviews received on a day w added and averages re-calculated in a single event.
- Viator performs checks on reviews - for more information, see K concepts - Review authenticity

object (ViatorUniqueContent)

Product details unique to Viator.com

## Note :

- Access to this information is only available if it is enabled for yo Please speak to your account manager if you would like to take of our unique content.
- You must ensure that your site is configured such that no Viator Content is indexed by any search engine . This is a requirement certification. For more information, see Key concepts - Protect content

- 403 Forbidden
- 404 Not Found
- 405 HTTP Method Not Allowed
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

-

{

}

+

"status": "ACTIVE",

"productCode": "2050\_PA",

"language": "en-US",

"createdAt": "2004-01-01T08:00:00Z",

"title": "Louvre Museum Skip the Line Access Guided Tour",

"ticketInfo":

…

{

},

- "pricingInfo": … + { },
- "images": … + [ ],

+

"logistics":

…

{

},

"timeZone": "Europe/Paris",

"description": "Paris's Louvre Museum is no less than the world's biggest museu

- "inclusions": … + [ ],
- "exclusions": … + [ ],
- "additionalInfo": … + [ ],
- "cancellationPolicy": … + { },
- "bookingConfirmationSettings": … + { },
- "bookingRequirements": … + { },
- "languageGuides": … + [ ],
- "bookingQuestions": … + [ ],
- "tags": … + [ ],
- "destinations": … + [ ],
- "itinerary": … + { },
- "productOptions": … + [ ],
- "translationInfo": … + { },
- "supplier": … + { },
- "reviews": … + { },
- "viatorUniqueContent": … + { }

,

```
-{ "status": "ACTIVE", "productCode": "5010SYDNEY", "language": "en-US", "createdAt": "2008-01-22T08:00:00Z", "title": "Big Bus Sydney and Bondi Hop-on Hop-off Tour", "ticketInfo": … + { }, "pricingInfo": … + { }, "images": … + [ ], "logistics": … + { }, "timeZone": "Australia/Sydney", "description": "Explore Sydney and Bondi Beach on this hop-on hop-off sightseei "inclusions": … + [ ], "exclusions": … + [ ], "additionalInfo": … + [ ], "cancellationPolicy": … + { }, "bookingConfirmationSettings": … + { }, "bookingRequirements": … + { }, "languageGuides": … + [ ], "bookingQuestions": … + [ ], "tags": … + [ ], "destinations": … + [ ], "itinerary": … + { }, "productOptions": … + [ ], "translationInfo": … + { }, "supplier": … + { }, "reviews": … + { }, "viatorUniqueContent": … + { } } ]
```

## /products/{product-code}

<!-- image -->

/products/{product-code}

Get full product details for a single product.

Note :

- This endpoint should not be used to ingest or update the product catalog. Instead, please use the /products/modified-since endpoint for that purpose.
- The response object utilizes polymorphism and differs markedly depending on whether the product is active or inactive. Click the drop-down selector in the status description to toggle between an "ACTIVE" and "INACTIVE" product response.

Example: Get details for "Big Bus Sydney and Bondi Hop-on Hop-off Tour" (product code: 5010SYDNEY):

## GET https://api.sandbox.viator.com/partner/products/5010SYDNEY

(Response samples generated on: 2021-03-29)

AUTHORIZATIONS:

API-key

PATH PARAMETERS

- string product-code
- required

## QUERY PARAMETERS

campaign-value target-lander

Retrieve details of the product identified by this product code string &lt;= 200 characters

Affiliate partners only : Specifies the campaign tracking identifier that will be appended to the URL returned in productUrl as a query parameter. Campaigns allow you to track how specific links perform, with metrics such as sessions, bookings, and commission. Reports are available via the Viator Partner Platform.

Note : If you wish to use a campaign value that includes non-alphanumeric characters (e.g., '+', '-', etc.), you must URL-encode these characters.

string

Affiliate partners only : Specifies the type of landing page customers will be shown when opening the link provided in the productUrl field.

Ordinarily, when customers follow the link in productUrl , they are redirected to a sales-conversion-optimized affiliate landing page. This default behavior can be disabled by setting this parameter to "NONE" , which will modify the productUrl query string such that when opened, the customer will instead land on the standard viator.com product display page, which is not optimized for affiliate-link sales.

## Available values:

- "NONE" : Causes target\_lander=NONE to be included in the productUrl query string, which will disable redirection to an affiliate

## HEADER PARAMETERS

<!-- image -->

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

Accept-Language required

Accept required

## Responses

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |

landing page when the link is followed.

Our recommendation is for you to allow the default behavior by not including this parameter, unless you have a specific technical or business requirement to do so.

<!-- image -->

<!-- image -->

images

- logistics required
- timeZone required
- description required

inclusions exclusions

- additionalInfo required
- cancellationPolicy required
- bookingConfirmationSettings required

Array of objects (Image)

Images for this product object (Logistics)

Logistics details for this product string(?s).*[\S].*

Code for the time zone in which this product operates (IANA TZ datab format)

- Example : 'Australia/Sydney'

string(?s).*[\S].*

Description of this product

- Example : "Climb the Sydney Harbour Bridge with an expert guide ultimate Sydney experience..."
- Note : This field contains natural language suitable for display to t content will be translated (if necessary) into the language specifie Accept-Language header parameter

Array of objects

Features that are included with this product package

- Note : The same inclusion item may appear multiple times in this example, 'Lunch' . For a 7-day multi-day tour, 'Lunch' appearing times indicates that lunch is included on each of the seven days o tour. This can be displayed as "Lunch (7)"

Array of objects

Features that are not included with this product package

Array of objects (AdditionalInfo)

Facts necessary to communicate to travelers regarding this product.

Note : Items included only if they apply, if they do not apply they will no included in the response.

object (CancellationPolicy)

Cancellation policy details for this product.

object (BookingConfirmationSettings)

How this product's bookings are confirmed

For more information, see Booking concepts - Booking cutoff times

| bookingRequirements required   | object (BookingRequirements) Passenger type and number requirements for booking                                                                                                                             |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| languageGuides                 | Array of objects (LanguageGuide) Language guides available for this product across all product option c                                                                                                     |
| bookingQuestions required      | Array of strings Array of machine-interpretable values specifying the facts that the trav must provide when booking this product; further details can be retriev /products/booking-questions endpoint       |
| tags required                  | Array of integers Array of numeric tag identifiers indicating the product categories into this product falls To retrieve details about which tags these identifiers please use the /products/tags endpoint. |
| destinations required          | Array of objects (Destination) Destinations - i.e., cities, states, countries and regions - in which this can be considered to operate                                                                      |
| itinerary                      | object (Itinerary) Details about the places this product visits                                                                                                                                             |
| productOptions                 | Array of objects (ProductOption) Product options (tour grades) available for this product                                                                                                                   |
| translationInfo                | object (TranslationDetails) Information about whether the text in this response was machine-tran                                                                                                            |
| supplier required              | object (Supplier) Supplier details                                                                                                                                                                          |
| productUrl                     | string URL for this product on the viator.com site, where the customer will co their booking. This URL includes all the necessary information for viator to correctly                                       |

reviews required viatorUniqueContent

- 400 Bad Request

- 401 Unauthorized

- 403 Forbidden

- 404 Not Found

- 405 HTTP Method Not Allowed

For more information, see our guide to Affiliate Attribution on the Viat Partner Resource Center.

## Note :

- This element is only returned for affiliate partners.
- You must use the full URL and not modify it in any way - any cha could result in failure to attribute the sale to you, which means yo not be paid a commission for this sale.

Example format : https://www.viator.com/tours/Sydney/Sydney-and-B Hop-on-Hop-off-Tour/d357-5010SYDNEY? mcid=42383&amp;pid=P00045135&amp;medium=api&amp;version=2.0&amp;campaign object (ProductReviews)

Summary of reviews and ratings for this product

## Note :

- Review data is updated daily; i.e., all reviews received on a day wi added and averages re-calculated in a single event.
- Viator performs checks on reviews - for more information, see Ke concepts - Review authenticity

object (ViatorUniqueContent)

Product details unique to Viator.com

## Note :

- Access to this information is only available if it is enabled for you Please speak to your account manager if you would like to take a of our unique content.
- You must ensure that your site is configured such that no Viator U Content is indexed by any search engine . This is a requirement fo certification. For more information, see Key concepts - Protectin content

- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

-

-

-

"cancellationPolicy":

{

"type": "STANDARD",

"description": "For a full refund, cancel at least 24 hours before the schedule

"cancelIfBadWeather": false,

"cancelIfInsufficientTravelers": false,

"refundEligibility":

[

…

]

+

},

"bookingConfirmationSettings":

{

"bookingCutoffType": "CLOSING\_TIME",

"bookingCutoffInMinutes": 0,

"confirmationType": "INSTANT"

{

},

"bookingRequirements":

- "minTravelersPerBooking": 1,
- "maxTravelersPerBooking": 9,
- "requiresAdultForBooking": false

},

- "languageGuides": -[
- … , + { }
- … , + { }
- … , + { }
- … , + { }
- … , + { }
- … , + { }
- … , + { }
- … + { }

],

- "bookingQuestions": -

[

- "PICKUP\_POINT",
- "SPECIAL\_REQUIREMENTS"

],

<!-- image -->

```
"viatorUniqueContent": -{ "shortDescription": "Join a hop-on hop-off sightseeing tour by double-decker bu "longDescription": "The warm and mild year-round climate in Sydney and Bondi ma "insiderTips": "This tour takes you to Sydney's top destinations so you don't h "highlights": … + [ ] } }
```

## /products/tags

<!-- image -->

/products/tags

Get details for all tags (includes all languages/localizations) Tags should be cached and refreshed weekly.

To learn more about tags, see this article: Viator tags, explained

Note : If no response is received for a given tag reference, this means that the tag was removed from our database and the associated product has not yet been updated with a replacement tag. If this occurs, please disregard the removed tag.

Note : The example response has been truncated to five entries for brevity.

(Response sample generated on: 2020-08-25)

AUTHORIZATIONS:

HEADER PARAMETERS

- Accept

required

## Responses

## 200 Success

API-key string

Example:

application/json;version=2.0

Specifies the version of this API to access

## RESPONSE HEADERS

|                           | X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|---------------------------|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                           | RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
|                           | RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
|                           | RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE SCHEMA:          | application/json;version=2.0 | application/json;version=2.0                                                                                                                                                   |
|                           | tags required                | Array of objects (TagWithAllLocalizations)                                                                                                                                     |
| 400 Bad Request           | 400 Bad Request              | 400 Bad Request                                                                                                                                                                |
| 401 Unauthorized          | 401 Unauthorized             | 401 Unauthorized                                                                                                                                                               |
| 403 Forbidden             | 403 Forbidden                | 403 Forbidden                                                                                                                                                                  |
| 404 Not Found             | 404 Not Found                | 404 Not Found                                                                                                                                                                  |
| 429 Too Many Requests     | 429 Too Many Requests        | 429 Too Many Requests                                                                                                                                                          |
| 500 Internal Server Error | 500 Internal Server Error    | 500 Internal Server Error                                                                                                                                                      |
| 503 Service Unavailable   | 503 Service Unavailable      | 503 Service Unavailable                                                                                                                                                        |

<!-- image -->

## /products/booking-questions

<!-- image -->

/products/booking-questions

<!-- image -->

Get full details of all available preset booking questions. Booking questions should be cached and refreshed monthly.

Note : This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

(Response sample generated on: 2020-08-25)

AUTHORIZATIONS:

HEADER PARAMETERS

API-key

<!-- image -->

## Responses

## 200 Success

## RESPONSE HEADERS

|                                               | X-Unique-ID required                          | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|-----------------------------------------------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                               | RateLimit-Limit required                      | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
|                                               | RateLimit-Remaining required                  | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
|                                               | RateLimit-Reset required                      | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0                                                                                                                                  |
|                                               | bookingQuestions required                     | Array of objects (BookingQuestion) Booking questions for this product                                                                                                          |

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

## /products/search

<!-- image -->

<!-- image -->

Returns a list of filtered, ordered and sorted product summaries for products that match the given search criteria. This endpoint must not be used to ingest the catalog of products, the /products/modified-since endpoint must be used for that purpose.

If you're a Basic Access Affiliate Partner, this endpoint provides all the essential functionality that you need to implement in order to use the Viator API. The following article describes how to do this in the most efficient way: Golden Path - Basic Access Affiliate Partners .

Note : At present, only active products are returned

AUTHORIZATIONS:

## QUERY PARAMETERS

campaign-value target-lander

HEADER PARAMETERS

API-key string &lt;= 200 characters

Affiliate partners only : Specifies the campaign tracking identifier that will be appended to the URL returned in productUrl as a query parameter. Campaigns allow you to track how specific links perform, with metrics such as sessions, bookings, and commission. Reports are available via the Viator Partner Platform.

Note : If you wish to use a campaign value that includes non-alphanumeric characters (e.g., '+', '-', etc.), you must URL-encode these characters.

string

Affiliate partners only : Specifies the type of landing page customers will be shown when opening the link provided in the productUrl field.

Ordinarily, when customers follow the link in productUrl , they are redirected to a sales-conversion-optimized affiliate landing page. This default behavior can be disabled by setting this parameter to "NONE" , which will modify the productUrl query string such that when opened, the customer will instead land on the standard viator.com product display page, which is not optimized for affiliate-link sales.

## Available values:

- "NONE" : Causes target\_lander=NONE to be included in the productUrl query string, which will disable redirection to an affiliate landing page when the link is followed.

Our recommendation is for you to allow the default behavior by not including this parameter, unless you have a specific technical or business requirement to do so.

<!-- image -->

Example:

<!-- image -->

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

REQUEST BODY SCHEMA:

application/json;version=2.0

<!-- image -->

| filtering required   | object (ProductSearchFiltering) Only return products that match all the criteria provided here.                                      |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| sorting              | object (ProductSearchSorting) How the search results will be sorted                                                                  |
| pagination           | object (ProductSearchPagination) Pagination details specifying which search results to return based on start position and item count |
| currency required    | string <currency>                                                                                                                    |

Currency code for all prices provided in the request; and, the currency in which all pricing will be denominated in the response.

## One of:

- "AUD"
- "BRL"
- "CAD"
- "CHF"
- "DKK"
- "EUR"
- "GBP"
- "HKD"
- "INR"
- "JPY"
- "NOK"
- "NZD"
- "SEK"
- "SGD"
- "TWD"
- "USD"
- "ZAR"

## Responses

## 200 Success

## RESPONSE HEADERS

|                                               | X-Unique-ID required                          | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|-----------------------------------------------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                               | RateLimit-Limit required                      | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
|                                               | RateLimit-Remaining required                  | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
|                                               | RateLimit-Reset required                      | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0                                                                                                                                  |
|                                               | products required                             | Array of objects (ProductSummary) List of products matching the filtering criteria, sorted and paginated as specified in the request                                           |
|                                               | totalCount                                    | integer Total number of products matching the filtering criteria - these may be accessed via multiple calls to this service using the pagination feature.                      |
| 400 Bad Request                               | 400 Bad Request                               | 400 Bad Request                                                                                                                                                                |

Note : The currency you display to your users may not be the currency they see when they click through to the viator.com site. Instead, they will see the default currency for the locale from which they are accessing the site.

- 401 Unauthorized
- 403 Forbidden
- 405 HTTP Method Not Allowed
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

## /products/recommendations

<!-- image -->

<!-- image -->

Retrieve a list of sorted product-to-product recommendations that match the given search criteria.

Recommendations are algorithm-generated based on various factors such as shared attributes, category, customer purchase patterns, browsing behavior, and other relevant metrics.

This endpoint can be used to enhance product discovery, suggest alternatives, improve cross-selling by displaying related products to customers, etc...

## Notes:

- The recommendations object may contain multiple recommendation types based on different algorithms or business logic.
- New recommendation types can be added over time, allowing flexibility for different use cases.
- Clients should handle cases where a recommendation category may be empty if no suitable products are found.
- This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

AUTHORIZATIONS:

API-key

## HEADER PARAMETERS

string

Example:

application/json;version=2.0

Specifies the version of this API to access

REQUEST BODY SCHEMA:

application/json;version=2.0

Array of strings

&lt;= 50 items

The unique identifier of the product(s) for which recommendations are being retrieved.

Array of strings

Types of recommendation. One of:

- IS\_SIMILAR\_TO : returns products that are deemed similar to the requested product based on machine learning algorithms, considering attributes such as location, category, itinerary, price range and others.

Note: New recommendation types can be added over time, allowing flexibility for different use cases.

- Accept

required

productCodes required

recommendationTypes required

## Responses

## 200 Success

## RESPONSE HEADERS

X-Unique-ID required string

Tracking identifier for this response. Please include the value of this field when making help requests.

## Example :

"0A871A13:DE2A\_0A8712F9:01BB\_5DCCC98C\_260DAA:0D5B"

| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                             |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                   |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only. |

RESPONSE SCHEMA:

application/json;version=2.0

Array [

]

| productCode required     | string(?s).*[\S].* The unique identifier of the product for which recommendations are being retrieved.                                                                                       |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| recommendations required | object A map of recommended product lists, categorized by different recommendation types. The keys being the recommendation type and the values being the list of recommended product codes. |

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 405 HTTP Method Not Allowed
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

## Attractions

## /attractions/search

<!-- image -->

/attractions/search

Get a list of attractions associated with a given destinationId , along with all relevant information about them, including products mapped.

Attractions should be cached and refreshed weekly.

## Note :

- Pages generated using data from this endpoint are subject to a strict no-index policy. You must ensure that your site is configured such that no Viator Unique Content is indexed by any search engine . This is a requirement for site certification. For more information, see Key concepts - Protecting unique content . If you are unsure about whether you are correctly following this rule or if you would like to take advantage of our unique content, please reach out to our support team .

AUTHORIZATIONS:

## QUERY PARAMETERS

- campaign-value

## HEADER PARAMETERS

<!-- image -->

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

Accept-Language

required

Accept

required

API-key string &lt;= 200 characters

Affiliate partners only : Specifies the campaign tracking identifier that will be appended to the URL returned in attractionUrl as a query parameter. Campaigns allow you to track how specific links perform, with metrics such as sessions, bookings, and commission. Reports are available via the Viator Partner Platform.

Note : If you wish to use a campaign value that includes non-alphanumeric characters (e.g., '+', '-', etc.), you must URL-encode these characters.

<!-- image -->

<!-- image -->

REQUEST BODY SCHEMA:

application/json;version=2.0

| destinationId required   | integer Unique numeric identifier of the destination to retrieve attractions for                           |
|--------------------------|------------------------------------------------------------------------------------------------------------|
| sorting                  | object How the search results will be sorted                                                               |
| pagination               | object Pagination details specifying which search results to return based on start position and item count |

## Responses

## 200 Success

## RESPONSE HEADERS

|                  | X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                  | RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
|                  | RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
|                  | RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE SCHEMA: | RESPONSE SCHEMA:             | application/json;version=2.0                                                                                                                                                   |
|                  | attractions                  | Array of objects (AttractionDetails)                                                                                                                                           |

totalCount

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 405 HTTP Method Not Allowed
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

integer &lt;int32&gt;

Total number of products matching the filtering criteria - these may be accessed via multiple calls to this service using the pagination feature

<!-- image -->

## /attractions/{attraction-id}

<!-- image -->

/attractions/{attraction-id}

Get all relevant information about a specific attractionId , including products mapped.

## Note :

- Pages generated using data from this endpoint are subject to a strict no-index policy. You must ensure that your site is configured such that no Viator Unique Content is indexed by any search engine . This is a requirement for site certification. For more information, see Key concepts - Protecting unique content . If you are unsure about whether you are correctly following this rule or if you would like to take advantage of our unique content, please reach out to our support team .

AUTHORIZATIONS:

QUERY PARAMETERS

- campaign-value

API-key string &lt;= 200 characters

Affiliate partners only : Specifies the campaign tracking identifier that will be appended to the URL returned in attractionUrl as a query parameter. Campaigns allow you to track how specific links perform, with metrics such as

## HEADER PARAMETERS

<!-- image -->

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

- Accept-Language required

Accept required

## Responses

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |

sessions, bookings, and commission. Reports are available via the Viator Partner Platform.

Note : If you wish to use a campaign value that includes non-alphanumeric characters (e.g., '+', '-', etc.), you must URL-encode these characters.

<!-- image -->

| attractionId required   | integer Unique numeric identifier for this attraction                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| name required           | string Natural-language title of this attraction Note : This field contains natural language suitable for display to the user; conten will be translated (if necessary) into the language specified in the Accept-Langu header parameter                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| destinations required   | Array of objects Destinations associated with this attraction                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| attractionUrl required  | string URL to forward users to in order to complete their purchase on the Viator site This URL includes all the necessary information for Viator to correctly attribute pay commission for the sale to the referring partner. If campaign-value is included in the request, this URL will also include the campaign tracking value that you set. For more information, see our guide to Affiliate Attribution on the Viator Partner Resource Center. Note : This element is only returned for affiliate partners. You must use the full URL and not modify it in any way - any changes coul result in failure to attribute the sale to you, which means you will not be pa commission for this sale. Example: https://www.viator.com/Inverness-attractions/Loch-Ness/d5051-a31? mcid=42383&pid=P00045135&medium=api&version=2.0&campaign=exam |
| productCount required   | integer Number of products associated with the attraction                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| productCodes required   | Array of strings List of productCodes associated with the attraction                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| images required         | Array of objects (ImageVariant) Images for this attraction                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

reviews

- translationInfo

center address

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

object (ProductReviewsSummary)

Summary of reviews and ratings for this attraction

## Note :

- Review data is updated daily; i.e., all reviews received on a day will be added and averages re-calculated in a single event.
- Viator performs checks on reviews - for more information, see Review authenticity

boolean

Identifies if a admission fee is required to access this attraction

string

This attraction Opening Hours

object

Attraction details unique to Viator.com

freeAttraction

openingHours

- viatorUniqueContent

## Note :

- Access to this information is only available if it is enabled for your account. Please reach out to our support team if you would like to take advantage of unique content..
- You must ensure that your site is configured such that no Viator Unique Content is indexed by any search engine . This is a requirement for site certification. For more information, see Key concepts - Protecting unique content

object (TranslationDetails)

Information about whether the text in this response was machine-translated object (LocationCenter)

Geographic coordinates (latitude/longitude) for this location object

Address details for this attraction

- 404 Not Found
- 405 HTTP Method Not Allowed
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

## Availability

/availability/check

<!-- image -->

Check real-time availability and pricing for a product depending on the date, pax-mix, start time and/or product option.

We recommend using the pricing information returned by this endpoint as the source of truth for the amount you will be invoiced by Viator for the sale of the product in question.

The third response example - 265910P1 (commission payment model) - shows the alternative PriceObject for merchants using the commission payment model.

Note : This service should only be used to determine the availability of a product immediately prior to booking. Bulk operations pertaining to product availability; e.g., generating a calendar of availability for a product, should use the availability schedule endpoints .

(Response sample generated on: 2021-04-06)

AUTHORIZATIONS:

HEADER PARAMETERS

string

Example:

application/json;version=2.0

Specifies the version of this API to access

REQUEST BODY SCHEMA:

application/json;version=2.0

string(?s).*[\S].*

Retrieve availability details for the product identified by this product code

string

Retrieve availability details for the product option (tour grade) identified by this product option code

For more information see:

Key concepts: Product options

string &lt;time&gt;

Retrieve availability details only for items that start at this time. If this parameter is omitted, information about all available starting times for the specified date will be included in the response.

- Example

- : "17:15"

string &lt;date&gt;

Retrieve availability details for items that operate on this date

- Accept

required

productCode required

productOptionCode

startTime

travelDate required

API-key

<!-- image -->

## Responses

## 200 Success

## RESPONSE HEADERS

|                  | X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                  | RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
|                  | RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
|                  | RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE SCHEMA: | RESPONSE SCHEMA:             | application/json;version=2.0                                                                                                                                                   |
|                  | currency required            | string(?s).*[\S].* Currency in which pricing is expressed in this response (as specified in the request)                                                                       |

## string(?s).*[\S].*

Display pricing in the currency identified by this 3-letter code

- Example : "USD"

Array of objects (PaxMixItem)

Passenger-mix information

{

- productCode required
- travelDate required
- bookableItems required
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

## Request samples

application/json;version=2.0 Content type

5010SYDNEY Example

```
"productCode": "5010SYDNEY", "travelDate": "2020-12-12", "currency": "AUD",
```

string(?s).*[\S].*

Product code of the product that this availability response pertains to string &lt;date&gt;

Date of travel for all bookable items returned in this response (relative to the time zone in which the product operates)

Array of objects (CheckAvailabilityBookableItem) Bookable items for this product

Expand all

Collapse all

Copy

<!-- image -->

## /availability/schedules/{product-code}

GET

/availability/schedules/{product-code}

<!-- image -->

Get availability and pricing details for all product options of the requested product. The pricing is returned in the supplier's currency. We recommend using the /exchange-rates endpoint to get the Viator exchange rates and apply them for pricing conversion.

Note : This endpoint should not be used for ingesting or updating the availability and pricing details for the entire catalog of Viator products. Instead, please use the /availability/schedules/modified-since endpoint for that purpose.

(Response sample generated on: 2021-03-12)

AUTHORIZATIONS:

API-key

PATH PARAMETERS

string

Retrieve availability details for the product identified by this product code

## HEADER PARAMETERS

string

Example:

application/json;version=2.0

Specifies the version of this API to access

- product-code required

- Accept required

## Responses

## 200 Success

## RESPONSE HEADERS

|          | X-Unique-ID required                 | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|----------|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|          | RateLimit-Limit required             | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
|          | RateLimit-Remaining required         | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
|          | RateLimit-Reset required             | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE | SCHEMA: application/json;version=2.0 | SCHEMA: application/json;version=2.0                                                                                                                                           |

| productCode required   | string(?s).*[\S].* Unique identifier for this product                                                                                                                                                                                                                                                                                                                                          |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| bookableItems required | Array of objects (ProductBookableItemSchedule) Bookable items for this product                                                                                                                                                                                                                                                                                                                 |
| currency required      | string(?s).*[\S].* Three letter currency code for all pricing information in this response; based on the supplier's currency.                                                                                                                                                                                                                                                                  |
| summary required       | object (AvailabilityScheduleSummary) Information about the lowest price available for this product                                                                                                                                                                                                                                                                                             |
|                        | Note : The pricing information given here is based on the recommended retail price (RRP). While affiliate partners must sell at this price, merchant partners set their own prices according to their own margins and booking fees; therefore, merchant partners must calculate their own from-price for display, rather than using these values, unless they have elected to sell at the RRP. |
| extraChargesSummary    | object (AvailabilityScheduleExtraChargesSummary) Information about the lowest price with extra charges available for this product                                                                                                                                                                                                                                                              |

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 405 HTTP Method Not Allowed
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

## /availability/schedules/bulk

<!-- image -->

<!-- image -->

Get availability and pricing details for all product options of all requested products. The pricing is returned in the supplier's currency. We recommend using the /exchange-rates endpoint to get the Viator exchange rates and apply them for pricing conversion.

Note : This endpoint should not be used for ingesting or updating the availability and pricing details for the entire catalog of Viator products. Instead, please use the /availability/schedules/modified-since endpoint for that purpose.

(Response sample generated on: 2021-03-12)

<!-- image -->

## HEADER PARAMETERS

string

Example:

application/json;version=2.0

Specifies the version of this API to access

REQUEST BODY SCHEMA:

application/json;version=2.0

Array of strings

&lt;= 500 items

List of product codes for which to retrieve availability schedules

- Accept

required

- productCodes required

## Responses

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required                          | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required                      | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required                  | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required                      | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0                                                                                                                                  |

## API-key

- availabilitySchedules required
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 405 HTTP Method Not Allowed
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

Example

Array of objects (ProductAvailabilitySchedule) Array of availability schedule objects

Example

<!-- image -->

## /availability/schedules/modified-since

<!-- image -->

/availability/schedules/modified-since

Get full future availability details for all products modified since the specified time. The pricing is returned in the supplier's currency. We recommend using the /exchange-rates endpoint to get the Viator exchange rates and apply them for pricing conversion. Initiate a full ingestion only to establish your local copy; this should be a rare occurrence compared to regular updates. Fetch incremental updates through this endpoint on an hourly basis. You are welcome to poll for updates as frequently as every 15 minutes if desired. Be mindful that excessive frequency beyond these recommendations may trigger rate limits.

(Response sample generated on: 2021-03-12)

AUTHORIZATIONS:

QUERY PARAMETERS

cursor

API-key string

Pagination cursor received from a previous call to this endpoint that points to the desired starting point for the results.

Note : Pagination will come into play when the number of results exceeds the figure given in the count parameter. In this case, pass the content of the nextCursor element for the value of cursor to receive the next page of results. The final page of results will not include the nextCursor element. For more information, see: Ingesting and updating availability schedules .

- Example: 'MTYwNTA2ODAwOXw1NjcyUDk='

count modified-since

## HEADER PARAMETERS

- Accept required

## Responses

## 200 Success

## RESPONSE HEADERS

X-Unique-ID required integer [ 1 .. 500 ]

<!-- image -->

The maximum number of products to be returned in response.

- Maximum allowed and default value: 500

string &lt;date-time&gt; ^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])... Show pattern Only retrieve availabilty schedules that have been modified since the date and time (UTC) specified by this timestamp

## Note :

- As this is a query parameter, colons (i.e., : ) in the timestamp should be URL-encoded as %3A ; e.g.: " 2020-09-30T00%3A00%3A01.737043Z "
- Using this parameter is not recommended as the standard pagination method; rather, use the cursor parameter to ensure all availability schedule updates are captured during ingestion.

string

Example:

application/json;version=2.0

Specifies the version of this API to access

string

Tracking identifier for this response. Please include the value of this field when making help requests.

- Example : "0A871A13:DE2A\_0A8712F9:01BB\_5DCCC98C\_260DAA:0D5B"
- RateLimit-Limit required

string

Total limit of requests for this endpoint for a given window. For informational purposes only.

- string RateLimit-Remaining

required

RateLimit-Reset required

Remaining requests for this endpoint for a given window. For informational purposes only string

The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.

## RESPONSE SCHEMA:

application/json;version=2.0

availabilitySchedules required nextCursor

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

Array of objects (ProductAvailabilitySchedule)

Array of availability schedule objects string

A cursor to use when fetching the next set of products.

- Example : "MTU3NDA0NDczOQ=="

<!-- image -->

## Bookings

## /bookings/cart/hold

<!-- image -->

/bookings/cart/hold

Requests the creation of a hold for each item in the cart.

A hold is a guarantee that either the price or availability (or both) of the product will be retained until a booking request is made using the /bookings/cart/book endpoint.

A hold consists of two components availability and pricing . The response to this service indicates whether one, both or neither has been granted, and until when for each item.

- The length of time for which the availability hold will be granted is determined by the supplier, and therefore varies between products.
- The length of time for the pricing hold is determined by Viator, and is therefore standard across all products.

This endpoint must not be used to check availability of a product. Instead, always use the /availability/check endpoint to perform the final availability check.

Note : This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

<!-- image -->

## HEADER PARAMETERS

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

Accept-Language required

Accept

required

REQUEST BODY SCHEMA:

application/json;version=2.0

partnerCartRef required currency required

items required paymentDataSubmissionMode

hostingUrl string (PartnerCartReference) &lt;= 100 characters (?s).*[\S].* Partner-generated unique cart reference for this group of bookable items.

string (Currency)

```
Merchant Partners: One of USD , EUR , GBP , AUD , CAD
```

```
Affiliate Partners with API access level "Full Access + Booking": One
```

```
of USD , EUR , GBP , AUD , CAD , CHF , DKK , FJD , HKD , JPY , NOK , NZD , SEK , SGD , THB , ZAR , INR , BRL , TWD , MXN , CLP , IDR , ILS , KRW , PHP , PLN , TRY
```

Array of objects (BookingsCartHoldRequestItem)

List of bookable items (Limited to 16)

string

Defines the payment solution used to submit payment details, two modes are supported:

- PARTNER\_FORM for partners hosting their own payment form.
- VIATOR\_FORM for partners using the Viator iframe payment form.

Note : This element is only applicable for affiliate partners with API access level "Full Access + Booking".

string

The URL of the page where the payment form is hosted. This is required if paymentDataSubmissionMode is set to VIATOR\_FORM .

## API-key

## Responses

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |

RESPONSE SCHEMA:

application/json;version=2.0

| cartRef required        | string (CartReference) Viator-generated unique reference for this cart of bookable items, e.g. CR-44e4a3f8b65d11edafa10242ac120002     |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| partnerCartRef required | string (PartnerCartReference) <= 100 characters (?s).*[\S].* Partner-generated unique cart reference for this group of bookable items. |
| currency required       | string (Currency) Merchant Partners: One of USD , EUR , GBP , AUD , CAD                                                                |

This should include the protocol, domain and any non-standard port excluding the trailing '/'. E.g.: https://www.yourdomain.com

|                          | Affiliate Partners with API access level "Full Access + Booking": One of USD , EUR , GBP , AUD , CAD , CHF , DKK , FJD , HKD , JPY , NOK , NZD , SEK , SGD , THB , ZAR , INR , BRL , TWD ,                         |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| items required           | Array of any List of bookable items.                                                                                                                                                                               |
| totalHeldPrice required  | object The total price of all bookable items.                                                                                                                                                                      |
| paymentDataSubmissionUrl | string The API URL to provide payment details to the Viator payment gateway. Only returned if paymentDataSubmissionMode is set to PARTNER_FORM .                                                                   |
| paymentSessionToken      | string The payment session token, if paymentDataSubmissionMode is set, used to facilitate fraud prevention when Implementing the API Solution or providing payment details when Implementing the iFrame Solution . |
| extraChargesSummary      | object Total amount of Extra Charges considering all cart bookable items.                                                                                                                                          |
| translationInfo          | object (TranslationDetails) Information about whether the text in this response was machine- translated                                                                                                            |

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

## /bookings/cart/book

<!-- image -->

/bookings/cart/book

<!-- image -->

Requests a booking for each item in the cart.

- As some products are booked on external supplier systems, it may take &gt; 90s to receive a response from this endpoint. For this reason, we recommend setting your internal time-out for this service to 120s . In the event that this service does time-out, or you receive a HTTP 500 error, you should check the status of the booking using the /bookings/status endpoint to ensure the booking was not created before you attempt to make the booking again.
- The status of each item will indicate if the item booking:
- is still awaiting confirmation ( PENDING ); or,
- was CONFIRMED if it was eventually successful, or
- was REJECTED if there are valid reasons why it could not be booked; such as, if it was bookedout or other changes to availability occurred; or,
- failed for an unknown reason if it did eventually fail. In this scenario, a new booking can be attempted using a new partnerBookingRef

Note : This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

<!-- image -->

AUTHORIZATIONS:

API-key

HEADER PARAMETERS

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Accept-Language

required

Accept

required

## Specifies the version of this API to access

## REQUEST BODY SCHEMA:

application/json;version=2.0

| cartRef required         | string (CartReference) Viator-generated unique reference for this cart of bookable items, e.g. CR-44e4a3f8b65d11edafa10242ac120002   |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| bookerInfo required      | object (BookerInfo) Name details for the person making this booking.                                                                 |
| communication required   | object (CartBookCommunicationInfo) Details for correspondence regarding this booking.                                                |
| additionalBookingDetails | object Optional extra details to include with the booking.                                                                           |
| items required           | Array of objects (BookingsCartBookRequestItem) List of bookable items.                                                               |
| paymentToken             | string The payment token obtained from the payments endpoint or from the iframe Javascript library.                                  |

## Responses

## 200 Success

## RESPONSE HEADERS

- X-Unique-ID required

RateLimit-Limit required string

Tracking identifier for this response. Please include the value of this field when making help requests.

- Example :

"0A871A13:DE2A\_0A8712F9:01BB\_5DCCC98C\_260DAA:0D5B"

string

|                              | Total limit of requests for this endpoint for a given window. For informational purposes only.                                    |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                   |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only. |

## RESPONSE SCHEMA:

application/json;version=2.0

| cartRef required             | string (CartReference) Viator-generated unique reference for this cart of bookable items, e.g. CR-44e4a3f8b65d11edafa10242ac120002                                                                                                                                                                               |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| partnerCartRef required      | string (PartnerCartReference) <= 100 characters (?s).*[\S].* Partner-generated unique cart reference for this group of bookable items.                                                                                                                                                                           |
| currency required            | string (Currency) Merchant Partners: One of USD , EUR , GBP , AUD , CAD Affiliate Partners with API access level "Full Access + Booking": One of USD , EUR , GBP , AUD , CAD , CHF , DKK , FJD , HKD , JPY , NOK , NZD , SEK , SGD , THB , ZAR , INR , BRL , TWD , MXN , CLP , IDR , ILS , KRW , PHP , PLN , TRY |
| items required               | Array of any List of bookable items.                                                                                                                                                                                                                                                                             |
| voucherInfo                  | object Voucher information for this booking.                                                                                                                                                                                                                                                                     |
| totalConfirmedPrice required | object The total price of all confirmed bookable items.                                                                                                                                                                                                                                                          |
| totalPendingPrice required   | object The total price of all pending bookable items.                                                                                                                                                                                                                                                            |

## 400 Bad Request

## 401 Unauthorized

- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

## /bookings/hold

<!-- image -->

Note : This endpoint is only available to merchant partners.

Requests the creation of a booking-hold - a guarantee that either the price or availability (or both) of the product will be retained until a booking request is made using the /bookings/book endpoint.

<!-- image -->

The booking-hold consists of two components availability and pricing . The response to this service indicates whether one, both or neither has been granted, and until when.

- The length of time for which the availability hold will be granted is determined by the supplier, and therefore varies between products.
- The length of time for the pricing-hold is determined by Viator, and is therefore standard across all products.

This endpoint must not be used to check availability of a product. Instead, always use the /availability/check endpoint to perform the final availability check.

(Response sample generated on: 2020-08-25)

<!-- image -->

exp-demo

boolean

Default:

false

Example:

true

Specifies whether this request is a demo/test booking. Demo bookings do not send any notifications and are automatically confirmed. Also, manualconfirmation products behave as if they were instant-confirmation products.

## Set this value to true when:

- Making a test booking in the production environment
- Making a test booking of a manual-confirmation product in the sandbox environment and you wish to receive a booking status of "CONFIRMED" in the response

## Set this value to false when:

- Making a real booking in the production environment
- Making a test booking of a manual-confirmation product in the sandbox environment and you wish to receive a booking status of "PENDING" in the response

REQUEST BODY SCHEMA:

application/json;version=2.0

| productCode required   | string(?s).*[\S].* Unique identifier for the product                                                                                                                                  |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| productOptionCode      | string Product option identifier.                                                                                                                                                     |
| startTime              | string Starting time for the item in the case that the product/product option has multiple start times. Note : This element must be included for products that have multiple starting |

currency required travelDate required

paxMix required

## Responses

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |

string.*[\S].*

Three-letter currency code for the currency in which to return pricing information; one of:

- "USD"
- "CAD"
- "GBP"
- "AUD"
- "EUR"

string &lt;date&gt;

Date of travel (according to the time zone in which the product operates)

Array of objects (PaxMixItem)

Passenger details

## bookingRef required

- bookingHoldInfo required

currency lineItems

totalPrice

- extraChargesSummary

translationInfo string(?s).*[\S].*

Viator-generated booking reference for this booked item in format BR-123456789

This value can be used in the request to:

- /bookings/book ( bookingRef )
- /bookings/status ( bookingRef )
- /bookings/{booking-reference}/cancel-quote (in-query parameter)
- /bookings/{booking-reference}/cancel (in-query parameter)

object (BookingHoldInfo)

Availability and pricing hold information.

string

Three-letter currency code for the currency in which pricing information is displayed; one of:

- "USD"
- "CAD"
- "GBP"
- "AUD"
- "EUR"

Array of objects (PricingLineItem)

Array of pricing details for each traveler in this booking object

Details about the total price of this booking object (ExtraChargesSummary)

Information about the Extra Charges applicable to this bookableItem

## Note :

- Prices payable to third parties are provided to us by the operator, and may be subject to change.

object (TranslationDetails)

Information about whether the text in this response was machinetranslated

.

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

## /bookings/book

<!-- image -->

/bookings/book

Requests a booking for a product.

## Note :

- This endpoint is only available to merchant partners.
- The amount that you will be invoiced for the sale of this tour (in the specified currency) is given in the totalPrice element in the response from this endpoint.
- As some products are booked on external supplier systems, it may take &gt; 90s to receive a response from this endpoint. For this reason, we recommend setting your internal time-out for this service to 120s . In the event that this service does time-out, or you receive a HTTP 500 error, you should check the status of the booking using the /bookings/status endpoint to ensure the booking was not created before you attempt to make the booking again.
- The booking status will indicate if the booking:
- is still awaiting confirmation ( "PENDING" ); or,

- was "CONFIRMED" if it was eventually successful, or
- was "REJECTED" if there are valid reasons why it could not be booked; such as, if it was booked-out or other changes to availability occurred; or,
- failed for an unknown reason if it did eventually fail. In this scenario, a new booking can be attempted using a new "partnerBookingRef"

(Response sample generated on: 2020-08-25)

AUTHORIZATIONS:

## HEADER PARAMETERS

Accept-Language required

Accept required exp-demo

API-key string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access boolean

Default:

false

Example:

true

Specifies whether this request is a demo/test booking. Demo bookings do not send any notifications and are automatically confirmed. Also, manualconfirmation products behave as if they were instant-confirmation products.

## Set this value to true when:

- Making a test booking in the production environment
- Making a test booking of a manual-confirmation product in the sandbox environment and you wish to receive a booking status of "CONFIRMED" in the response

## Set this value to false when:

- Making a real booking in the production environment
- Making a test booking of a manual-confirmation product in the sandbox environment and you wish to receive a booking status of "PENDING" in the response

REQUEST BODY SCHEMA:

application/json;version=2.0

productCode required

productOptionCode startTime

currency required

- travelDate required

paxMix required

bookingRef

- partnerBookingRef required

languageGuide string(?s).*[\S].*

Unique identifier for the product string

Product option identifier.

For more information see: Key concepts: Product options string

Starting time for the item in the case that the product/product option has multiple start times.

Note : This element must be included for products that have multiple starting times.

string.*[\S].*

Three-letter currency code for the currency in which to return pricing information; one of:

- "USD"
- "CAD"
- "GBP"
- "AUD"
- "EUR"

string &lt;date&gt;

Date of travel (according to the time zone in which the product operates)

Array of objects (PaxMixItem)

Passenger details string

The booking reference code that is generated by Viator and returned in the bookingRef element in the response from /bookings/hold .

```
string <= 100 characters (?s).*[\S].*
```

Partner-generated unique booking reference for this bookable item object

Specifies which language and what type of language guide to include if language guides are available for this product.

Note: This element must be included in order to book products that offer language guides.

object (BookerInfo)

Name details for the person making this booking.

Array of objects (BookingQuestionAnswers)

Answers to booking questions required for this booking

- See: Booking concepts - Booking questions for more information.

object (CommunicationInfo)

Details for correspondence regarding this booking.

See : Booking concepts - Supplier communications for information about closed-loop communication.

object (AdditionalBookingDetails-2)

Optional extra details to include with booking

bookerInfo required

- bookingQuestionAnswers

- communication required

additionalBookingDetails

## Responses

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required     | string                                                                                                                                                                         |

The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.

## RESPONSE SCHEMA: application/json;version=2.0

status rejectionReasonCode

bookingRef partnerBookingRef

currency string

Indicates the outcome of the booking request; one of:

- "CONFIRMED" - the booking has been confirmed
- "REJECTED" - the booking request was declined
- "CANCELED" - the booking has been canceled
- "PENDING" - the booking request has been submitted to the supplier and is awaiting their response.
- "IN\_PROGRESS" - the booking is still being processed by the booking server.
- "ON\_HOLD" - booking hold made but no booking request made yet
- "FAILED" - the booking request failed

Note: For "PENDING" and "IN\_PROGRESS" poll /booking/status for further booking status updates string

In the case that status is "REJECTED" , this field provides a code as to the reason for the rejection; one of:

- "BOOKABLE\_ITEM\_IS\_NO\_LONGER\_AVAILABLE" - this bookable item is no longer available
- "DUPLICATE\_BOOKING" - this is a duplicate booking
- "OTHER" - other/unlisted reason

string

Viator-generated booking reference number string

Partner-generated booking reference number (if sent in the request)

string

One of the available billing currencies:

- "USD"
- "CAD"
- "GBP"
- "AUD"
- "EUR"

| lineItems          | Array of objects (PricingLineItem) Array of pricing details for each traveler in this booking   |
|--------------------|-------------------------------------------------------------------------------------------------|
| totalPrice         | object Total price of this booking                                                              |
| cancellationPolicy | object (CancellationPolicy) Cancellation policy details for this product.                       |
| voucherInfo        | object (VoucherInfo) Voucher information for this booking.                                      |

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

```
"lineItems": -[ … + { } ], "totalPrice": -{ "price": … + { } }, "cancellationPolicy": -{ "type": "STANDARD", "description": "For a full refund, cancel at least 24 hours before the schedule "cancelIfBadWeather": false, "cancelIfInsufficientTravelers": false, "refundEligibility": … + [ ] }, "voucherInfo": -{ "url": " https://shop.live.rc.viator.com/ticket?code=1006658118:1176d4aed0e88ffe "format": "HTML", "type": "STANDARD" } }
```

## /bookings/status

<!-- image -->

/bookings/status

Note : This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

Requests the status of an existing booking using either the Viator-generated booking reference ( bookingRef ) or the reference generated by the partner ( partnerBookingRef ). For bookings made through v1 endpoints, only Viator-generated booking reference is supported.

Checking the status of a booking is only necessary to retrieve updates on:

- manual confirmation products status
- bookings that were left in "PENDING" / "IN\_PROGRESS" status at time of /booking call for other reasons
- bookings that timed out at time of /booking call
- amendments that were left in
- "IN\_PROGRESS" status at time of /amend call

<!-- image -->

The endpoint should only be called intermittently and based on the cadence recommended at nextPollAt. To avoid unnecessary calls, do not poll the endpoint before the next recommended polling time, as no updates will be returned.

(Response sample generated on: 2020-11-10)

AUTHORIZATIONS:

API-key

HEADER PARAMETERS

string

Example:

application/json;version=2.0

Specifies the version of this API to access

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

REQUEST BODY SCHEMA:

application/json;version=2.0

string

The booking reference code (in format BR-123456789 , which is generated by Viator and returned in the bookingRef element in the response from /bookings/hold ) for the booking for which to retrieve status information

string

&lt;= 100 characters (?s).*[\S].*

The booking reference code generated by you (the partner) that was provided in in the request to /bookings/book ) for the booking for which to retrieve status information

string

File format of the voucher; one of:

- PDF

- HTML

Default is HTML if not specified.

Accept required

Accept-Language

bookingRef

partnerBookingRef

voucherFormat

## Responses

200 Success

<!-- image -->

## RESPONSE HEADERS

| X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |

## RESPONSE SCHEMA:

application/json;version=2.0

| bookingRef        | string Viator-generated booking reference number                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| partnerBookingRef | string Partner-generated booking reference number (if sent in the request)                                                                                                                                                                                                                                                                                                                                                                                                          |
| status            | string Indicates the outcome of the booking request; one of: "CONFIRMED" - the booking has been confirmed "REJECTED" - the booking request was declined "CANCELED" - the booking has been canceled "PENDING" - the booking request has been submitted to the supplier and is awaiting their response "IN_PROGRESS" - the booking is still being processed by the booking server "ON_HOLD" - booking hold made but no booking request made yet "FAILED" - the booking request failed |

amendmentStatus amendmentRejectionReasonCode

## CONFIRMED

string (AmendmentStatus)

Machine-interpretable string indicating the outcome of the booking amendment request. One of:

- AMENDED : The amendment was successful
- REJECTED : The amendment was rejected
- PENDING : The amendment is pending

Note : If booking has been amended multiple times, this field will only reflect the latest amendment request status (ie, if the booking was amended once and a second amendment request is rejected, the amendment status response will be REJECTED )

string (AmendmentRejectionReasonCode)

Machine-interpretable reason code indicating why the amendment was REJECTED . One of:

- "BOOKABLE\_ITEM\_IS\_NO\_LONGER\_AMENDABLE' - this bookable item is no longer eligible to be amended due to updated restrictions or conditions.
- "BOOKABLE\_ITEM\_IS\_NO\_LONGER\_AVAILABLE" - this bookable item is no longer available. The selected bookable item is no longer available for the specified travel date /start time / pax mix combination. Retrieve current availability and generate a new quote before attempting the amendment again.
- "PRICE\_MISMATCH" - the quotePriceDifference is no longer valid. The product's price has changed since the quotePriceDifference was generated, re-submit the amendment request to receive an updated quote.
- "ISSUE\_WITH\_PAYMENT" - the customer's payment was declined due to an issue trying to process the payment. This could be caused by generic errors, suspected fraud, or incomplete billing information.
- "INSUFFICIENT\_FUNDS" - the customer's payment was declined due to insufficient funds
- "INVALID\_PAYMENT\_DETAILS" - the customer's payment was declined due to invalid payment details
- "SUSPECTED\_FRAUD" - the customer payment was declined due to security measures flagging it as potentially fraudulent
- "SOFT\_DECLINE" - the customer's payment was declined due to fixable issues (eg insufficient funds)

currency lineItems

totalPrice

- cancellationPolicy
- voucherInfo

nextPollAt

- "HARD\_DECLINE" - the customer's payment was declined due to an error or issue which can't be resolved immediately. Action such a new payment method or the customer contacting their bank will need to be taken to resolve the issue before the transaction can be retried.
- "THREE\_D\_SECURE\_REQUIRED" - the customer's payment was declined due to unsuccessful authentication through 3DS
- "INTERNAL\_ERROR" - the customer's payment was declined due to an internal error in our system
- "PROCESSOR\_UNAVAILABLE" - the customer's payment was declined due to temporary unavailability on the processor's end
- "PROCESSOR\_ISSUE\_WITH\_PAYMENT" - the customer's payment was declined due to an issue on the processor's end
- "OTHER" - other/unlisted reason

Note : New values may be added over time, allowing flexibility for different use cases.

string

One of the available billing currencies:

- "USD"
- "CAD"
- "GBP"
- "AUD"
- "EUR"

Array of objects (PricingLineItem)

Array of pricing details for each traveler in this booking object

Total price of this booking object (CancellationPolicy)

Cancellation policy details for this product.

object (VoucherInfo)

Voucher information for this booking.

string &lt;date-time&gt; (NextPollAt)

Timestamp (UTC) indicating the recommended time the endpoint should be hit again.

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

## Example: "2025-04-03T02:54:29.082753Z"

```
{ "status": "CONFIRMED", "bookingRef": "BR-791143912", "partnerBookingRef": "BR-791143912", "currency": "USD", "lineItems": -[ … + { } ], "totalPrice": -{ "price": … + { } }, "cancellationPolicy": -{ "type": "STANDARD", "description": "For a full refund, cancel at least 24 hours before the schedule "cancelIfBadWeather": false, "cancelIfInsufficientTravelers": false, "refundEligibility": … + [ ] }, "voucherInfo": -{ "url": " https://www.viator.com/ticket?code=1187186744:8ac3e6308555ab632fe89e8a6 "format": "HTML", "type": "STANDARD" } }
```

## /bookings/cancel-reasons

<!-- image -->

/bookings/cancel-reasons

<!-- image -->

Retrieves a dictionary of unique identification codes ( cancellationReasonCode ) and their associated natural-language descriptions ( cancellationReasonText ). Cancellation reasons should be cached and refreshed monthly. Note :

- This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.
- As the data returned by this endpoint may change from time to time, it is recommended that you retrieve the latest cancellation reasons at a fixed cadence - we recommend monthly. For more information, see: Update frequency .

(Response sample generated on: 2022-07-22)

AUTHORIZATIONS:

QUERY PARAMETERS

type

## HEADER PARAMETERS

<!-- image -->

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

Accept-Language required

Accept

required

## Responses

## 200 Success

## RESPONSE HEADERS

X-Unique-ID required

API-key string

Default:

"CUSTOMER"

Specifies which set of cancellation reasons to retrieve; one of:

- "CUSTOMER" - (default) gets the set of customer -initiated cancellation reasons (for use with the /bookings/{booking-reference}/cancel endpoint)
- "SUPPLIER" - gets the set of supplier -initiated cancellation reasons (for use with the /bookings/modified-since endpoint)

string

Tracking identifier for this response. Please include the value of this field when making help requests.

- Example :

"0A871A13:DE2A\_0A8712F9:01BB\_5DCCC98C\_260DAA:0D5B"

| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                             |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                   |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only. |

## RESPONSE SCHEMA:

application/json;version=2.0

- reasons
- 401 Unauthorized
- 403 Forbidden
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

Array of objects (CancellationReason)

Array of cancellation reason codes and their asssociated texts for display to the user

<!-- image -->

## /bookings/{booking-reference}/cancel-quote

<!-- image -->

/bookings/{booking-reference}/cancel-quote

Gets the cancellation quote for an existing booking.

Note : This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

For more information about how to perform cancellations using this API, see the Cancellation API workflow section and our in-depth guide about cancellation policies and how to handle cancellations: All you need to know about cancellation policies .

(Response sample generated on: 2020-08-25)

AUTHORIZATIONS:

PATH PARAMETERS

- booking-reference required

HEADER PARAMETERS

API-key

- string

The booking reference code (in format BR-123456789 , which is generated by Viator and returned in the bookingRef element in the response from /bookings/book ) of the booking for which to retrieve a cancellation quote

<!-- image -->

- Accept

required

## Responses

## 200 Success

## RESPONSE HEADERS

|                                               | X-Unique-ID required                          | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"                                                                                                                                  |
|-----------------------------------------------|-----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                               | RateLimit-Limit required                      | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                                                                                                                                                         |
|                                               | RateLimit-Remaining required                  | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                                                                                                                                               |
|                                               | RateLimit-Reset required                      | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                                                                                                                                                             |
| RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0                                                                                                                                                                                                                                                                 |
|                                               | bookingId required                            | string Booking reference number for this booking Note : For bookings made with v1 of this API, this code corresponds to data.itemSummaries[].itemId (in the response from v1's /booking/book endpoint) but prepended with BR- . For example, if the itemId is 580669678 , this field should be BR-580669678 . |
|                                               | refundDetails                                 | object (RefundDetails) Details of the refund.                                                                                                                                                                                                                                                                 |

string

Example:

application/json;version=2.0

Specifies the version of this API to access

<!-- image -->

- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

Note : Bookings that have not been confirmed by the supplier and have a status of "PENDING" will report an itemPrice , refundAmount and refundPercentage of 0 , as no fees are charged until the booking has been accepted by the supplier and its status is "CONFIRMED" .

string (CancellationQuoteBookingStatus)

Machine-interpretable string indicating the cancellation status of this itinerary item:

- "CANCELLABLE" - this booking is available to be cancelled
- "CANCELLED" - this booking has already been cancelled
- "NOT\_CANCELLABLE" - this booking cannot be cancelled (because the product's start time was in the past)

```
"refundDetails": -{ "itemPrice": 60.2, "refundAmount": 60.2, "refundPercentage": 100, "currencyCode": "AUD" }, "status": "CANCELLABLE" }
```

## /bookings/{booking-reference}/cancel

<!-- image -->

/bookings/{booking-reference}/cancel

Cancels existing booking with given Viator-generated booking-reference

Note : This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

For more information about how to perform cancellations using this API, see the Cancellation API workflow section and our in-depth guide about cancellation policies and how to handle cancellations: All you need to know about cancellation policies .

(Response sample generated on: 2020-08-25)

AUTHORIZATIONS:

PATH PARAMETERS

- booking-reference required

HEADER PARAMETERS

Accept-Language required

API-key string

The booking reference code (in format BR-123456789 , which is generated by Viator and returned in the bookingRef element in the response from /bookings/book ) of the booking for which to request cancellation string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

REQUEST BODY SCHEMA:

application/json;version=2.0

string

Machine-interpretable identification code for this cancellation reason, retrieved from /bookings/cancel-reasons

Accept

required

- reasonCode required

## Responses

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required                          | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required                      | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required                  | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required                      | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0                                                                                                                                  |

string

Booking reference code for this booking

bookingId

required

reason

- 400 Bad Request

- 401 Unauthorized

- 403 Forbidden

- 404 Not Found

- 406 Not Acceptable

- 429 Too Many Requests

- 500 Internal Server Error

- 503 Service Unavailable

## Request samples

- Note : For bookings made with v1 of this API, this code corresponds to data.itemSummaries[].itemId (in the response from v1's /booking/book endpoint) but prepended with BR. For example, if the itemId is 580669678 , this field should be BR-580669678 .

string (CancellationResultItemReason)

Machine-interpretable reason code indicating why the cancellation was not successful

- "ALREADY\_CANCELLED" : The booking has already been cancelled
- "NOT\_CANCELLABLE" : The booking cannot be canceled because the product start time was in the past

Note : This field will not be present in the response if the cancellation was successful status required

string (CancellationBookingStatus)

Machine-interpretable string indicating the outcome of the booking cancellation request. One of:

- "ACCEPTED" : The cancellation was successful
- "DECLINED" : The cancellation failed

<!-- image -->

## /bookings/modified-since

<!-- image -->

/bookings/modified-since

<!-- image -->

Gets all booking-event notifications relevant to the partner since a point in time indicated by a timestamp or pagination cursor. This endpoint should be polled hourly, except in supplier cancellation scenarios, in which case polling should occur every 5 minutes.

Merchant partners only: In order to stop notification emails sent by Viator for supplier cancellations of bookings made through the API you must poll this endpoint every 5 minutes and send an acknowledge using /bookings/modified-since/acknowledge endpoint. See the guide on how to automate the flow for supplier cancellations in this article: Automating supplier cancellations in V.2 Partner API . Viator will not send notification emails to partners for customer-initiated cancellations.

Affiliate partners only: affiliate partners with API access level Basic or Full will only have access to events of bookings made past September 2025.

<!-- image -->

modified-since cursor

count

## HEADER PARAMETERS

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

Accept-Language required

Accept required

## Responses

string &lt;date-time&gt; ^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])... Show pattern Only retrieve booking events that have occurred since the point in time indicated by this timestamp.

## Note :

- As this is a query parameter, colons (i.e., : ) in the timestamp should be URL-encoded as %3A ; e.g.: " 2020-09-30T00%3A00%3A01.737043Z "
- Using this parameter is not recommended as the standard pagination method; instead, we recommend using the cursor parameter to ensure all booking event notifications are captured.

string

Pagination cursor received from a previous call to this endpoint that points to the starting point for the next page of results.

Note : Pagination will come into play when the number of results exceeds the figure given in the count parameter. In this case, pass the content of the nextCursor element for the value of cursor to receive the next page of results. The final page of results will not include the nextCursor element.

integer

Default:

<!-- image -->

50

Specifies the maximum number of booking events to be included in each page of results returned from this endpoint.

## 200 Success

## RESPONSE HEADERS

## X-Unique-ID required

string

Tracking identifier for this response. Please include the value of this field when making help requests.

- Example :

"0A871A13:DE2A\_0A8712F9:01BB\_5DCCC98C\_260DAA:0D5B"

string

Total limit of requests for this endpoint for a given window. For informational purposes only.

string

Remaining requests for this endpoint for a given window. For informational purposes only

string

The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.

- RateLimit-Limit required

- RateLimit-Remaining required

- RateLimit-Reset required

## RESPONSE SCHEMA:

application/json;version=2.0

## bookings required

nextCursor

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable

Array of objects (BookingEvent)

List of booking event notifications string

The cursor to use to fetch the next page of booking notification events.

## Example :

MTU3NDA0NDczOQ==

- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

## /bookings/modified-since/acknowledge

<!-- image -->

/bookings/modified-since/acknowledge

Acknowledges receipt of one or more booking event notifications returned by the /bookings/modifiedsince endpoint. Merchants who wish to assume control of the customer service workflow surrounding booking change events must carry out this step before the time indicated in the bookings[].acknowledgeBy field, otherwise Viator will automatically send a cancellation notification to the email address provided by the partner for cancellation notifications. This endpoint should be called in order to stop notification emails from being sent by Viator. See the guide on how to automate the flow for supplier cancellations in this article: Automating supplier cancellations in V.2 Partner API

Note : This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

AUTHORIZATIONS:

API-key

HEADER PARAMETERS

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

REQUEST BODY SCHEMA:

application/json;version=2.0

Array of strings

List of booking event notification reference codes for which to acknowledge receipt

- Accept-Language required

Accept

required

- transactionRefs required

## Responses

## 200 Success

## RESPONSE HEADERS

- X-Unique-ID required

string

Tracking identifier for this response. Please include the value of this field when making help requests.

- Example :

"0A871A13:DE2A\_0A8712F9:01BB\_5DCCC98C\_260DAA:0D5B"

- RateLimit-Limit required

string

Total limit of requests for this endpoint for a given window. For informational purposes only.

- string RateLimit-Remaining required

RateLimit-Reset required

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

## Request samples

```
application/json;version=2.0 Expand all Copy "PBE-e60bb92c-f1fc-11ec-b939-0242ac120002", Content type
```

```
{ "transactionRefs": -[ "PBE-e60bb92c-f1fc-11ec-b939-0242ac120003" ] }
```

## Response samples

Remaining requests for this endpoint for a given window. For informational purposes only string

The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.

Collapse all

<!-- image -->

## /amendment/check/{booking-reference}

<!-- image -->

/amendment/check/{booking-reference}

<!-- image -->

Returns the amendability status of a given bookingRef , along with a list of booking components (e.g., booking details, traveller info, pickup location) that can be amended.

## Notes :

- Only bookings made after July 2025 are eligible to be amended.
- This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

The booking reference code (in format BR-123456789 ), generated by Viator and returned in the bookingRef element in the response from

/bookings/book and /bookings/cart/book for which to retrieve amendability

- AUTHORIZATIONS: API-key PATH PARAMETERS string Example: BR-123456789 status and details booking-reference

## 200 Success

## RESPONSE HEADERS

|                                               | X-Unique-ID required                          | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"                                                                                                                     |
|-----------------------------------------------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                               | RateLimit-Limit required                      | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                                                                                                                                            |
|                                               | RateLimit-Remaining required                  | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                                                                                                                                  |
|                                               | RateLimit-Reset required                      | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                                                                                                                                                |
| RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0                                                                                                                                                                                                                                                    |
|                                               | bookingRef required                           | string (BookingRef) The booking reference code (in format BR-123456789 ), generated by Viator and returned in the bookingRef element in the response from /bookings/book and /bookings/cart/book                                                                                                 |
|                                               | isAmendable required                          | boolean Indicates whether the booking can be amended. If false , the booking cannot be amended.                                                                                                                                                                                                  |
|                                               | reason                                        | string Machine-interpretable reason code indicating why the amendment can not proceed. One of: "UNSUPPORTED_PRODUCT" : This booking cannot be amended due to product configurations "UNSUPPORTED_CANCELLATION_POLICY" : The booking cannot be amended because of its cancellation policy "OTHER" |

amendmentTypes paxMixSummary

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- This field will not be present in the response if isAmendable is
- true
- New values may be added over time, allowing flexibility for different use cases.

Array of strings (AmendmentTypes) unique

List of booking components that can be amended in this booking:

- "BOOKING\_DETAILS"
- "UPDATE\_PAX\_MIX"
- "PER\_TRAVELER\_QUESTIONS"
- "PER\_BOOKING\_QUESTIONS"

## Notes :

- Only one amendmentType can be updated per request
- This field will not be present in the response if isAmendable is false
- New values may be added over time, allowing flexibility for different use cases.

Array of objects (PaxMixSummary)

Summary of the current PAX MIX of the booking. It ensures each traveler listed in the PaxMix is assigned a travelerNum and informs which Booking Questions have been answered for each at the time of the booking.

Note : This field will not be present in the response if isAmendable is false

## 503 Service Unavailable

<!-- image -->

## /amendment/quote

<!-- image -->

Gets the amendment quote for an existing booking.

## Notes :

<!-- image -->

- Only one amendmentType can be updated per request.
- This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

<!-- image -->

## Responses

<!-- image -->

| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                             |
|------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                   |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only. |

## RESPONSE SCHEMA:

application/json;version=2.0

| bookingRef required           | string (BookingRef) The booking reference code (in format BR-123456789 ), generated by Viator and returned in the bookingRef element in the response from /bookings/book and /bookings/cart/book                                               |
|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| status required               | string (QuoteStatus) Machine-interpretable string indicating the outcome of the quote request. One of: CONFIRMED : The quote was successful REJECTED : The quote was rejected                                                                  |
| quoteRef required             | string (QuoteReference) Unique Viator-generated quote reference for a booking.                                                                                                                                                                 |
| quoteExpiresAt required       | string <date-time> (QuoteValidUntil) Timestamp (UTC) indicating when the quote expires.                                                                                                                                                        |
| initialBookingPrice required  | number (QuoteInitialPrice) Total price of the booking at the time of purchase.                                                                                                                                                                 |
| quotePriceDifference required | object (QuotePriceDifference) The price difference that must be paid (or refunded, if negative) to apply the requested amendment to the booking. This value reflects the cost impact of the proposed changes compared to the original booking. |

- amendedBookingPrice required

currency required

paymentMethod

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

object (QuoteAmendedPrice)

A detailed breakdown of the total booking price after the requested amendment has been applied.

string

Currency in which the amendment will be processed. Merchant

```
Partners: One of USD , EUR , GBP , AUD , CAD
```

Affiliate Partners with API access level "Full Access + Booking": One

```
of USD , EUR , GBP , AUD , CAD , CHF , DKK , FJD , HKD , JPY , NOK , NZD , SEK , SGD , THB , ZAR , INR , BRL , TWD , MXN , CLP , IDR , ILS , KRW , PHP , PLN , TRY
```

Note: The currency for all price values will always match the currency used in the original booking.

object (PaymentMethod)

Information about the payment method to be used for this transaction.

## Notes:

- The transaction will be processed using the payment method already associated with the booking being amended.
- Payment method is only relevant for transactional affiliates.

## Request samples

<!-- image -->

## Response samples

<!-- image -->

```
"identifierType": "CARD_LAST_FOUR",
```

```
"amendedBookingPrice": -{ "lineItems": … + [ ], "totalPrice": … + { } }, "currency": "EUR", "paymentMethod": -{ "type": "CARD", "identifier": 7 } }
```

## /amendment/amend/{quote-reference}

POST

/amendment/amend/{quote-reference}

Amends existing booking with given Viator-generated quoteRef

Note : This endpoint is only available to affiliate partners with API access level "Full Access + Booking" and merchant partners.

AUTHORIZATIONS:

PATH PARAMETERS

- quote-reference

## Responses

200 Success

API-key string Example: QR-4891fddc-7e2e-4203-9517-ec75703daa8a The booking reference code (in format ), generated by Viator and

QR-4891fddc-7e2e-4203-9517-ec75703daa8a returned in the quoteRef element in the response from /amendments/check endpoint.

<!-- image -->

## RESPONSE HEADERS

| X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |

## RESPONSE SCHEMA:

application/json;version=2.0

status required initialBookingPrice required

string

Machine-interpretable string indicating the outcome of the booking amendment request. One of:

- AMENDED : The amendment was successful
- REJECTED : The amendment was rejected
- PENDING : The amendment is pending

Note : If booking has been amended multiple times, this field will only reflect the latest amendment request status (ie, if the booking was amended once and a second amendment request is rejected, the amendment status response will be REJECTED )

AMENDED

number (QuoteInitialPrice)

Total price of the booking at the time of purchase.

| quotePriceDifference required   | object (QuotePriceDifference) The price difference that must be paid (or refunded, if negative) to apply the requested amendment to the booking. This value reflects the cost impact of the proposed changes compared to the original booking.                                                                                                                                                                                  |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| amendedBookingPrice required    | object (QuoteAmendedPrice) A detailed breakdown of the total booking price after the requested amendment has been applied.                                                                                                                                                                                                                                                                                                      |
| currency required               | string Currency in which the amendment will be processed. Merchant Partners: One of USD , EUR , GBP , AUD , CAD Affiliate Partners with API access level "Full Access + Booking": One of USD , EUR , GBP , AUD , CAD , CHF , DKK , FJD , HKD , JPY , NOK , NZD , SEK , SGD , THB , ZAR , INR , BRL , TWD , MXN , CLP , IDR , ILS , KRW , PHP , PLN , TRY Note: The currency for all price values will always match the currency |
| paymentMethod                   | object (PaymentMethod) Information about the payment method to be used for this transaction. Notes: The transaction will be processed using the payment method already associated with the booking being amended.                                                                                                                                                                                                               |
| voucherInfo required            | object (VoucherInfo) Voucher information for this booking.                                                                                                                                                                                                                                                                                                                                                                      |

## 400 Bad Request

- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable

- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

## Payments

## /v1/checkoutsessions/{sessionToken}/paymentaccounts

<!-- image -->

/v1/checkoutsessions/{sessionToken}/paymentaccounts

Creates a payment token from raw credit card details for use with the /bookings/cart/book endpoint.

The URL should not be constructed manually, instead use the paymentDataSubmissionUrl value returned from the /bookings/cart/hold endpoint.

When using the API payment solution, it is a requirement that you implement our fraud prevention solution. See Implementing the API Solution for more details.

## Note :

- This endpoint utilises a different domain to other endpoints referenced in the API.
- This endpoint is only available to affiliate partners with API access level "Full Access + Booking".

## PATH PARAMETERS

string

Example:

CSI-P-kwftrgmrbfbglkaw4espjdr52e

The sessionToken is obtained from calling the /bookings/cart/hold endpoint and embedded in the paymentDataSubmissionUrl .

Note: The paymentDataSubmissionUrl value should be used instead of contructing the URL manually.

- sessionToken required

any

Example:

application/json

Identifies the payload as application/json.

any

Example:

P0123456789

This is your unique partner identifier, which you can find in the Viator Partner

Program:

https://partners.viator.com/login

any

Example:

9dbb490a-d953-4a9b-875a-728b5f335b29

Any client-side generated request identifier, unique per request.

any

Example:

curl/8.8.0

value should be appropriate to the client you are using, e.g. "curl/8.8.0"

REQUEST BODY SCHEMA:

application/json

object (PaymentAccountsRequest)

Wrapper element around payment data.

Content-Type

- required

- x-trip-clientid required

- x-trip-requestid required

User-Agent

required

- paymentAccounts

required

## Responses

## 200 Card successfully stored.

## RESPONSE SCHEMA:

application/json

object (PaymentAccounts)

## -404 Checkout session expired or not found.

- paymentAccounts

required

## Request samples

<!-- image -->

## Auxiliary

## /search/freetext

<!-- image -->

/search/freetext

Perform a search for products, attractions and/or destinations that contain a free-text search term. Product results can be filtered and sorted according to various criteria. This endpoint must not be used to ingest the catalog of products, the /products/modified-since endpoint must be used for that purpose.

Note : Only active products are returned in the response from this endpoint.

AUTHORIZATIONS:

QUERY PARAMETERS

campaign-value target-lander

## HEADER PARAMETERS

string

Example:

en, en-AU

Specifies the language into which the natural-language fields in the response from this service will be translated.

REQUEST BODY SCHEMA:

application/json

- Accept-Language required

API-key string

&lt;= 200 characters

Affiliate partners only : Specifies the campaign tracking identifier that will be appended to the URL returned in productUrl as a query parameter. Campaigns allow you to track how specific links perform, with metrics such as sessions, bookings, and commission. Reports are available via the Viator Partner Platform.

Note : If you wish to use a campaign value that includes non-alphanumeric characters (e.g., '+', '-', etc.), you must URL-encode these characters.

string

Target lander page for affiliate productUrl

- string Return results that contain this free-text search term object (FreetextSearchProductFiltering) Criteria by which to filter product search results (i.e., when searchTypes includes "PRODUCTS" ) object (FreetextSearchProductSorting) Specify the sorting method for product results (i.e., when searchTypes includes "PRODUCTS" ) Array of objects (SearchType) [ 1 .. 3 ] items Specifies the domain(s) in which to search for the searchTerm and the respective pagination details for each type of search results string &lt;currency&gt; Currency code of price range in request filter and the prices in response. searchTerm required productFiltering productSorting searchTypes required currency required
- string

```
One of: "AUD" , "BRL" , "CAD" , "CHF" , "DKK" , "EUR" , "GBP" , "HKD" , "INR" , "JPY" , "NOK" , "NZD" , "SEK" , "SGD" , "TWD" , "USD" , "ZAR" .'
```

Tracking identifier for this response. Please include the value of this field when making help requests.

- Example :

"0A871A13:DE2A\_0A8712F9:01BB\_5DCCC98C\_260DAA:0D5B"

RESPONSE SCHEMA: application/json;version=2.0

destinations object

Destinations that include the searchTerm

are requested via searchTypes

## Responses

## 200 Success

## RESPONSE HEADERS

- X-Unique-ID required

when

"DESTINATIONS"

results

attractions products

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

object

Attractions that include the searchTerm

are requested via searchTypes

object

Products that include the searchTerm

requested via searchTypes

when

"ATTRACTIONS"

when

"PRODUCTS"

results results are

<!-- image -->

<!-- image -->

## /locations/bulk

<!-- image -->

/locations/bulk

<!-- image -->

Get full location details for the requested location references. Locations should be cached and refreshed monthly. Additionally, the /locations/bulk endpoint should be used on demand for any new location references returned in the product content response.

Note : If no response is received for a given location reference, this means that the location was either removed from our database or replaced by a different one. If this occurs, please disregard the removed location reference and make sure you update the associated product information.

(Response sample generated on: 2020-08-25)

AUTHORIZATIONS:

HEADER PARAMETERS

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

REQUEST BODY SCHEMA:

application/json;version=2.0

Array of strings

&lt;= 500 items

List of location reference identifiers for which to retrieve full location details.

Accept-Language required

Accept

required

- locations

required

API-key

## Responses

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required                          | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required                      | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required                  | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required                      | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0                                                                                                                                  |
| locations required                            | Array of objects (Location) Locations                                                                                                                                          |
| 400 Bad Request                               | 400 Bad Request                                                                                                                                                                |
| 401 Unauthorized                              | 401 Unauthorized                                                                                                                                                               |
| 403 Forbidden                                 | 403 Forbidden                                                                                                                                                                  |
| 404 Not Found                                 | 404 Not Found                                                                                                                                                                  |
| 429 Too Many Requests                         | 429 Too Many Requests                                                                                                                                                          |
| 500 Internal Server Error                     | 500 Internal Server Error                                                                                                                                                      |

## 503 Service Unavailable

<!-- image -->

## /exchange-rates

<!-- image -->

This endpoint gets the exchange rates for conversions between specified currencies. Exchange rates should be cached and refreshed based on the expiry timestamp (at the moment daily).

In this API, all pricing is denominated in the currency of the supplier. For example, if a tour operates in Thailand, its prices will be given in Thai Baht (THB).

Not all supplier currencies are supported, but many are. They comprise:

- AED, ARS, AUD, BRL, CAD, CHF, CLP , CNY, COP , DKK, EUR, FJD, GBP
- HKD, IDR, ILS, INR, ISK, JPY, KRW, MXN, MYR, NOK, NZD, PEN, PHP , PLN,
- RUB, SEK, SGD, THB, TRY, TWD, USD, VND, ZAR

While pricing can be in any of the currencies listed above, payments for bookings can only be made using the following four currencies:

- GBP (British Pound)
- EUR (Euros)
- USD (US Dollars)
- AUD (Australian dollars)

In order that you display the correct price to the user and charge accordingly, it is important that you perform the currency conversion based on the exchange rates given in the response from this endpoint and that these conversion rates are valid at the time of conversion (as given in the expiry field).

In doing so, you ensure the amount that you, the merchant, will be invoiced by Viator for this product matches your records. Discrepancies are bound to occur if you perform the calculations using expired exchange rates or those from an alternative source.

An additional measure to ensure that you charge your customer accurately is to confirm that the pricing details returned by the /availability/check endpoint (in the billing currency specified in the request) conform to your expectations. The information provided by this service is the definitive source of truth with regard to product pricing.

Note: If you attempt to use an unsupported currency when making a booking request, you will receive the following error:

## Incorrect currency code provided

Note : In order to reduce the number of calls made to this service, we recommend retrieving the exchange rate for the currency pair in question just once for the time period during which it is valid, and then applying

that rate to all products with pricing denominated in that currency rather than calling this endpoint for each product requiring currency conversion.

Learn more about calculating product pricing in this article: Calculating Product Pricing

(Response sample generated on: 2020-09-17)

AUTHORIZATIONS:

API-key

REQUEST BODY SCHEMA:

application/json;version=2.0

Array of strings

List of three-letter currency codes for the source currencies for which to retrieve exchange rate data

Array of strings

List of three-letter currency codes for the target currencies for which to retrieve exchange rate data

sourceCurrencies

targetCurrencies

## Responses

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required     | string                                                                                                                                                                         |

The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.

| RESPONSE SCHEMA:          | application/json;version=2.0                                |
|---------------------------|-------------------------------------------------------------|
| rates                     | Array of objects (ExchangeRateItem) Currency exchange rates |
| 400 Bad Request           |                                                             |
| 401 Unauthorized          |                                                             |
| 403 Forbidden             |                                                             |
| 429 Too Many Requests     |                                                             |
| 500 Internal Server Error |                                                             |
| 503 Service Unavailable   |                                                             |

<!-- image -->

<!-- image -->

## /reviews/product

<!-- image -->

<!-- image -->

Retrieves and filters reviews for a single product Reviews should be cached and refreshed weekly, as well as on-demand when you see that the product content endpoint returns a different review count than saved in your database for the product.

## Non-indexing of reviews

- Review content is protected proprietary information; therefore, you may not allow review content to be indexed by search engines. In order for your site to be certified, you will need to demonstrate that you have implemented systems to ensure that review content is non-indexed. For more information, see Key concepts - Protecting unique content .

## Availability of reviews

- Occasionally, reviews are deleted due to inauthenticity, offensive language, etc. Furthermore, we cannot guarantee that non-Viator reviews (i.e., those for which the provider is not "VIATOR" ) will remain available in future (however, you will receive a notification email to inform you should this occurr). As such, we require that you implement a mechanism by which locally-cached reviews are automatically deleted from your records (and are not displayed on your site) if they do not appear in the most recent response from this endpoint.

## Viator performs checks on reviews

- For more information, see Key concepts - Review authenticity

<!-- image -->

<!-- image -->

AUTHORIZATIONS:

API-key

HEADER PARAMETERS

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

REQUEST BODY SCHEMA:

application/json;version=2.0

string

Retrieve reviews for the product identified by this product code

integer &lt;int32&gt;

Number of reviews to be returned in the response; used for pagination

integer &lt;int32&gt;

Position of first review to be returned in the response; used for pagination

Accept-Language

required

Accept

required

productCode

required

count

required

start

required

provider required sortBy

reviewsForNonPrimaryLocale showMachineTranslated

ratings

## Responses

string

Limit the reviews returned in the response to those associated with this provider; one of:

- "VIATOR" - only include reviews submitted on viator.com
- "TRIPADVISOR" - only include reviews submitted on tripdavisor.com
- "ALL" - include reviews from all providers

string

## One of:

- "HIGHEST\_RATING\_PER\_LOCALE" - sort by rating (descending) for each locale
- "MOST\_RECENT\_PER\_LOCALE" - sort by publication date (descending) for each locale
- "MOST\_HELPFUL\_PER\_LOCALE" - sort by the number of 'helpful' votes (descending) for each locale
- "HIGHEST\_RATING" - sort by rating (descending) across all locales
- "MOST\_RECENT" - sort by publication date (descending) across all locales
- "MOST\_HELPFUL" - sort by the number of 'helpful' votes (descending) across all locales

If this element is omitted, the default sort option is

"MOST\_RECENT"

<!-- image -->

boolean

Set to true to include reviews submitted by users from locales that are not the primary locale as given in the Accept-Language header parameter.

boolean

Set to true to include machine-translated reviews.

Array of integers &lt;int32&gt; [ items &lt;int32 &gt; ]

Only include reviews with these ratings

Example : [3,4,5] to receive reviews with a rating of 3 or above

## 200 Success

## RESPONSE HEADERS

| X-Unique-ID required         | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RateLimit-Limit required     | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
| RateLimit-Remaining required | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
| RateLimit-Reset required     | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |

RESPONSE SCHEMA:

application/json;version=2.0

<!-- image -->

| reviews required             | Array of objects (ProductReview) Reviews and review metadata for this product, from start to ( start + count )                                                       |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| totalReviewsSummary required | object Summary of the set of all reviews available for this product                                                                                                  |
| filteredReviewsSummary       | object Summary of the set of reviews available for this product filtered by provider , ratings , reviewsForNonPrimaryLocale and showMachineTranslated in the request |

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden

<!-- image -->

- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

<!-- image -->

## /suppliers/search/product-codes

<!-- image -->

/suppliers/search/product-codes

Gets a collection of supplier information objects for the provided products. Limited to 500 products per request. Supplier details should be cached and refreshed weekly.

AUTHORIZATIONS:

HEADER PARAMETERS

API-key

<!-- image -->

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

REQUEST BODY SCHEMA:

application/json;version=2.0

Array of strings

Accept-Language

required

Accept

required

- productCodes

required

## Responses

## 200 Success

## RESPONSE HEADERS

|          | X-Unique-ID required                 | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|----------|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|          | RateLimit-Limit required             | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
|          | RateLimit-Remaining required         | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
|          | RateLimit-Reset required             | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE | SCHEMA: application/json;version=2.0 | SCHEMA: application/json;version=2.0                                                                                                                                           |

- suppliers required
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

Array of objects (SupplierProductInfo)

```
{ "suppliers": -[ … + { } ] }
```

## /destinations

GET

/destinations

Get details of all destinations supported by the API. Destinations should be refreshed weekly (in addition to on-demand updates when a new destination is returned in the product content response).

## Note :

- Returns a complete list of Viator destinations, including destination names and parent identifiers
- Used to provide navigation through drill down lists or combo boxes
- Use the data received from this endpoint to resolve the destination identifier(s) in the destinations[].ref element in the product content response

AUTHORIZATIONS:

QUERY PARAMETERS

- campaign-value

HEADER PARAMETERS

API-key string &lt;= 200 characters

Affiliate partners only : Specifies the campaign tracking identifier that will be appended to the URL returned in destinationUrl as a query parameter. Campaigns allow you to track how specific links perform, with metrics such as sessions, bookings, and commission. Reports are available via the Viator Partner Platform.

Note : If you wish to use a campaign value that includes non-alphanumeric characters (e.g., '+', '-', etc.), you must URL-encode these characters.

<!-- image -->

## Responses

## 200 Success

## RESPONSE HEADERS

|                                               | X-Unique-ID required                          | string Tracking identifier for this response. Please include the value of this field when making help requests. Example : "0A871A13:DE2A_0A8712F9:01BB_5DCCC98C_260DAA:0D5B"   |
|-----------------------------------------------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                               | RateLimit-Limit required                      | string Total limit of requests for this endpoint for a given window. For informational purposes only.                                                                          |
|                                               | RateLimit-Remaining required                  | string Remaining requests for this endpoint for a given window. For informational purposes only                                                                                |
|                                               | RateLimit-Reset required                      | string The fixed window in time, in seconds, which represents when a limit is fully replenished. For informational purposes only.                                              |
| RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0 | RESPONSE SCHEMA: application/json;version=2.0                                                                                                                                  |
|                                               | destinations                                  | Array of objects (DestinationDetails)                                                                                                                                          |

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

string

Example:

application/json;version=2.0

Specifies the version of this API to access

totalCount

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 406 Not Acceptable
- 429 Too Many Requests
- 500 Internal Server Error
- 503 Service Unavailable

<!-- image -->

integer &lt;int32&gt;

## Total count of Destinations returned

## Deprecated

## /v1/taxonomy/destinations

<!-- image -->

/v1/taxonomy/destinations

This endpoint is marked for deprecation , but it will remain available to partners that started their integration prior to October 2024 to ensure backwards compatibility of existing integrations. Partners who got API access after October 2024 will not have access to this endpoint. To retrieve destinations information moving forward, please use the new /destinations endpoint.

Get details of all destinations supported by this API. Destinations should be refreshed weekly (in addition to on-demand updates when a new tag/booking question/location/destination is returned in the product content response).

- Note : This endpoint uses conventions from V1 of this API. See Key-concepts - V1 endpoint conventions for further information
- Retrieves all the country taxonomy/city nodes as a flat list
- Returns a complete list of Viator destinations, including destination names and parent identifiers
- Used to provide navigation through drill down lists or combo boxes
- Use the data received from this endpoint to resolve the destination identifier(s) in the destinations[].ref element in the product content response

AUTHORIZATIONS:

API-key

## HEADER PARAMETERS

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

- Accept-Language required

## Responses

<!-- image -->

## 200 Success

| RESPONSE SCHEMA:         | application/json                                                                                                                              |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| errorReference dateStamp | string or null reference number of this error                                                                                                 |
| errorType                | string or null timestamp of this response                                                                                                     |
|                          | string or null code specifying the type of error                                                                                              |
| errorCodes               | Array of strings or null array of error codes pertaining to this error                                                                        |
| errorMessage             | Array of arrays or null or null array of error message strings                                                                                |
| errorName                | string or null name of this type of error                                                                                                     |
| extraInfo                | object or null ignore (Viator only)                                                                                                           |
| extraObject              | object or null ignore (Viator only)                                                                                                           |
| success                  | boolean or null boolean indicator of this request's outcome true : the request was successful with no errors false : an error was encountered |
| totalCount               | integer or null number of results available for this service                                                                                  |
| errorMessageText         | string or null array of error message strings in plain text                                                                                   |
| vmid                     | string or null unique numeric id of the server that processed this request                                                                    |

Array of objects

## array of destination objects

<!-- image -->

## /v1/taxonomy/attractions

<!-- image -->

/v1/taxonomy/attractions

<!-- image -->

This endpoint is marked for deprecation , but it will remain available to partners that started their integration prior to October 2024 to ensure backwards compatibility of existing integrations. Partners who got API access after October 2024 will not have access to this endpoint. To retrieve attractions information moving forward, please use the new /attractions/search endpoints

Get attractions. Attractions should be cached and refreshed weekly.

- Note : This endpoint uses conventions from V1 of this API. See Key-concepts - V1 endpoint conventions for further information
- Retrieves a list of attractions (things like the Eiffel Tower or Empire State Building) and their associated unique numeric identifiers
- Use this endpoint to resolve the numeric attraction references ( seoId in this response) to the ( itinerary.routes[].pointsOfInterest[].attractionId ) in the response from any of the product content endpoints.

AUTHORIZATIONS:

HEADER PARAMETERS

- Accept-Language required

API-key string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

REQUEST BODY SCHEMA:

application/json

destId topX

integer unique numeric identifier of the destination in which to search for attractions

string (topX)

start and end rows to return in the format {start}-{end}

- e.g. '1-10' , '11-20'

## Note :

- the maximum number of rows per request is 100; therefore, '100-400' will return the same as '100-200'
- if topX is not specified, the default is '1-100'

string

sortOrder

Sort order for the results; one of:

- 'RECOMMENDED' - sorted in order of recommendation ( Note : What Viator gets paid impacts this sort order)
- 'SEO\_ALPHABETICAL' - Alphabetical (A-&gt;Z)

## Responses

## 200 Success

## RESPONSE SCHEMA: application/json

| errorReference   | string or null reference number of this error                          |
|------------------|------------------------------------------------------------------------|
| dateStamp        | string or null timestamp of this response                              |
| errorType        | string or null code specifying the type of error                       |
| errorCodes       | Array of strings or null array of error codes pertaining to this error |
| errorMessage     | Array of arrays or null or null array of error message strings         |
| errorName        | string or null name of this type of error                              |
| extraInfo        | object or null ignore (Viator only)                                    |
| extraObject      | object or null ignore (Viator only)                                    |

boolean or null boolean indicator of this request's outcome true : the request was successful with no errors false : an error was encountered integer or null number of results available for this service string or null array of error message strings in plain text string or null unique numeric id of the server that processed this request Array of objects array of attraction objects success totalCount errorMessageText vmid data

<!-- image -->

<!-- image -->

## /v1/product/reviews

<!-- image -->

<!-- image -->

/v1/product/reviews

This endpoint is now deprecated, but it will remain available to ensure backwards compatibility of existing integrations. To retrieve product reviews, please use the new /reviews/product endpoint.

Get user-submitted reviews of a product

- Note : This endpoint uses conventions from V1 of this API. See Key-concepts - V1 endpoint conventions for further information
- Only reviews in the language specified in the Accept-Language request header parameter will be returned. The value given in totalCount represents the total number of reviews for this product across all languages. Therefore, the number of reviews you can access may be fewer than this value for the language you specify.

Example: "Get the first three reviews for product 5010SYDNEY sorted by rating in ascending order":

## https://viatorapi sandbox viator com/service/product/reviews?sortOrder=REVIEW\_RATIN . . .

For information about how to find the review count and average rating, see: Determining ratings

AUTHORIZATIONS:

QUERY PARAMETERS

sortOrder topX

code showUnavailable

HEADER PARAMETERS

API-key string

```
Enum: "REVIEW_RATING_A" "REVIEW_RATING_D" "REVIEW_RATING_SUBMISSION_DATE_D"
```

specifier of the order in which to return reviews

## Sort order options:

- "REVIEW\_RATING\_A" : Traveler Rating (low → high) Average
- "REVIEW\_RATING\_D" : Traveler Rating (high → low) Average
- "REVIEW\_RATING\_SUBMISSION\_DATE\_D" : Most recent review

string

Example:

topX=1-3

start and end rows to return in the format {start}-{end}

- e.g. '1-10' , '200-299'

## Note :

- the maximum number of rows per request is 100; therefore, '100-400' will return the same as '100-200'
- if topX is not specified, the default is '1-100'

string

Example:

code=5010SYDNEY

unique alphanumeric identifier productCode product content

## boolean

specifier as to whether or not to show 'unavailable' products:

- true : return both available and unavailable products
- false : return only available products (default)

of the product, corresponding to in the response from the endpoints

- Accept-Language required

## Responses

## 200 Success

RESPONSE SCHEMA:

application/json

| errorReference   | string or null reference number of this error                          |
|------------------|------------------------------------------------------------------------|
| dateStamp        | string or null timestamp of this response                              |
| errorType        | string or null code specifying the type of error                       |
| errorCodes       | Array of strings or null array of error codes pertaining to this error |
| errorMessage     | Array of arrays or null or null array of error message strings         |
| errorName        | string or null name of this type of error                              |
| extraInfo        | object or null ignore (Viator only)                                    |
| extraObject      | object or null ignore (Viator only)                                    |
| success          | boolean or null boolean indicator of this request's outcome            |

- true : the request was successful with no errors

- false : an error was encountered

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

| totalCount       | integer or null number of results available for this service               |
|------------------|----------------------------------------------------------------------------|
| errorMessageText | string or null array of error message strings in plain text                |
| vmid             | string or null unique numeric id of the server that processed this request |
| data             | Array of objects (reviewObject) array of review objects                    |

<!-- image -->

<!-- image -->

## /v1/product/photos

<!-- image -->

<!-- image -->

/v1/product/photos

This endpoint is marked for deprecation, but it will remain available to ensure backwards compatibility of existing integrations. To retrieve photos of a product submitted by users moving forward, please use the /reviews/product endpoint.

Get photos of a product submitted by users. If you are using the /reviews/product endpoint for reviews, you should pull traveler photos from that endpoint. If you need to use the /v1/product/photos endpoint to retrieve traveler photos, the responses should be cached and refreshed weekly, as well as when you see that the product content endpoint returns a different review count than saved in your database.

You can learn more about how to implement traveler photos in this article: Implementing traveler photos via the Viator API .

- Note : This endpoint uses conventions from V1 of this API. See Key-concepts - V1 endpoint conventions for further information

<!-- image -->

API-key

topX

code showUnavailable

## HEADER PARAMETERS

- Accept-Language required

## Responses

## 200 Success

RESPONSE SCHEMA:

application/json

errorReference string or null

reference number of this error string

Example:

topX=1-3

start and end rows to return in the format {start}-{end}

- e.g. '1-10' , '200-299'

## Note :

- the maximum number of rows per request is 100; therefore, '100-400' will return the same as '100-200'
- if topX is not specified, the default is '1-100'

string

Example:

code=5010SYDNEY

unique alphanumeric identifier of the product, corresponding to productCode in the response from the product content endpoints

## boolean

specifier as to whether or not to show 'unavailable' products:

- true : return both available and unavailable products
- false : return only available products (default)

string

Example:

<!-- image -->

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

| dateStamp        | string or null timestamp of this response                                                                                                     |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| errorType        | string or null code specifying the type of error                                                                                              |
| errorCodes       | Array of strings or null array of error codes pertaining to this error                                                                        |
| errorMessage     | Array of arrays or null or null array of error message strings                                                                                |
| errorName        | string or null name of this type of error                                                                                                     |
| extraInfo        | object or null ignore (Viator only)                                                                                                           |
| extraObject      | object or null ignore (Viator only)                                                                                                           |
| success          | boolean or null boolean indicator of this request's outcome true : the request was successful with no errors false : an error was encountered |
| totalCount       | integer or null number of results available for this service                                                                                  |
| errorMessageText | string or null array of error message strings in plain text                                                                                   |
| vmid             | string or null unique numeric id of the server that processed this request                                                                    |
| data             | Array of objects (photoObject) array of photo objects                                                                                         |

## Response samples

<!-- image -->

## /v1/search/attractions

<!-- image -->

<!-- image -->

/v1/search/attractions

<!-- image -->

This endpoint is marked for deprecation , but it will remain available to partners that started their integration prior to October 2024 to ensure backwards compatibility of existing integrations. Partners who got API access after October 2024 will not have access to this endpoint. To retrieve attractions information moving forward, please use the new /attractions/search and /attractions/{attraction-id} endpoints

This service retrieves a list of attractions associated with the given destination. Attractions should be cached and refreshed weekly.

## Note :

- This endpoint uses conventions from V1 of this API. See Key-concepts - V1 endpoint conventions for further information
- This endpoint is only available to affiliate partners
- Pages generated using data from this endpoint are subject to a strict no-index policy . If you are unsure about whether you are correctly following this rule, please reach out to your account manager for advice.

AUTHORIZATIONS:

## HEADER PARAMETERS

- Accept-Language required

REQUEST BODY SCHEMA:

destId required

topX

seoType sortOrder

API-key string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

application/json integer

unique numeric identifier of the destination in which to search for attractions string (topX)

start and end rows to return in the format {start}-{end}

- e.g. '1-10' , '11-20'

## Note :

- the maximum number of rows per request is 100; therefore, '100-400' will return the same as '100-200'
- if topX is not specified, the default is '1-100'

<!-- image -->

string

Sort order for the results; one of:

- 'RECOMMENDED' - sorted in order of recommendation ( Note : What Viator gets paid impacts this sort order)
- 'SEO\_ALPHABETICAL' - Alphabetical (A-&gt;Z)

## Responses

## 200 Success

## RESPONSE SCHEMA: application/json

| errorReference   | string or null reference number of this error                                                                                                 |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| dateStamp        | string or null timestamp of this response                                                                                                     |
| errorType        | string or null code specifying the type of error                                                                                              |
| errorCodes       | Array of strings or null array of error codes pertaining to this error                                                                        |
| errorMessage     | Array of arrays or null or null array of error message strings                                                                                |
| errorName        | string or null name of this type of error                                                                                                     |
| extraInfo        | object or null ignore (Viator only)                                                                                                           |
| extraObject      | object or null ignore (Viator only)                                                                                                           |
| success          | boolean or null boolean indicator of this request's outcome true : the request was successful with no errors false : an error was encountered |
| totalCount       | integer or null number of results available for this service                                                                                  |
| errorMessageText | string or null array of error message strings in plain text                                                                                   |

<!-- image -->

## Request samples

<!-- image -->

## Response samples

200

Content type application/json

```
{ "errorReference": null, "data": -[ … , + { } … , + { } … + { } ], "dateStamp": "2020-04-20T22:11:05+0000", "errorType": null, "errorCodes": [ ], "errorMessage": null, "errorName": null,
```

string or null

## unique numeric id of the server that processed this request

Array of objects

Copy

Expand all

Collapse all

<!-- image -->

<!-- image -->

<!-- image -->

This endpoint is marked for deprecation , but it will remain available to partners that started their integration prior to October 2024 to ensure backwards compatibility of existing integrations. Partners who got API access after October 2024 will not have access to this endpoint. To retrieve attractions information moving forward, please use the new /attractions/search and /attractions/{attraction-id} endpoints

This service returns the details of an attraction. Attractions should be cached and refreshed weekly.

## Note :

- This endpoint uses conventions from V1 of this API. See Key-concepts - V1 endpoint conventions for further information
- This endpoint is only available to affiliate partners
- Pages generated using data from this endpoint are subject to a strict no-index policy . If you are unsure about whether you are correctly following this rule, please reach out to your account manager for advice.

<!-- image -->

## HEADER PARAMETERS

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

- Accept-Language required

## Responses

## 200 Success

## RESPONSE SCHEMA: application/json

| errorReference   | string or null reference number of this error                          |
|------------------|------------------------------------------------------------------------|
| dateStamp        | string or null timestamp of this response                              |
| errorType        | string or null code specifying the type of error                       |
| errorCodes       | Array of strings or null array of error codes pertaining to this error |
| errorMessage     | Array of arrays or null or null array of error message strings         |
| errorName        | string or null name of this type of error                              |

## Note:

- You must have multiple currencies enabled in order to set the currency using this parameter. Please speak to your account manager if you wish to have this enabled.
- If you omit this parameter; or, if you do not have multiple currencies enabled, pricing will be returned in the default currency for your account.

| extraInfo        | object or null ignore (Viator only)                                                                                                           |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| extraObject      | object or null ignore (Viator only)                                                                                                           |
| success          | boolean or null boolean indicator of this request's outcome true : the request was successful with no errors false : an error was encountered |
| totalCount       | integer or null number of results available for this service                                                                                  |
| errorMessageText | string or null array of error message strings in plain text                                                                                   |
| vmid             | string or null unique numeric id of the server that processed this request                                                                    |
| data             | object                                                                                                                                        |

<!-- image -->

```
"data": -{ "webURL": " http://shop.live.rc.viator.com/Las-Vegas-attractions/Shark-Reef-Aqua "pageUrlName": "Shark-Reef-Aquarium-at-Mandalay-Bay", "primaryDestinationUrlName": "Las-Vegas", "publishedDate": "2020-02-27", "panoramaCount": 0, "userName": "", "userPhotos": … + [ ], "reviews": … + [ ], "products": … + [ ], "ratingCounts": … + { }, "infoPageOverviewTitle1": "", "infoPageOverviewTitle2": "", "infoPageOverview1": "<div style=\"\">Get up close and personal with some of th "infoPageOverview2": "", "attractionAdmission": "Varies", "attractionTransit": "", "attractionOpenHours": "", "keywordCount": 1, "showReviews": true, "tabTitle": "Shark Reef", "descriptionIntro": "Shark Reef", "keywords": … + [ ], "reviewCount": 97, "seoType": "ATTRACTION", "pageTitle": "Shark Reef Aquarium at Mandalay Bay", "editorsPick": false, "showPhotos": true, "descriptionText": "<p>Inside the Mandalay Bay Hotel and Casino is the Shark Re "overviewSummary": "<div style=\"\">Get up close and personal with some of the "pagePrimaryLanguage": "en", "attractionLatitude": 36.09215, "attractionLongitude": -115.17665, "attractionStreetAddress": "3950 Las Vegas Blvd South", "attractionCity": "Las Vegas", "attractionState": "Nevada", "destinationId": 684, "thumbnailHiResURL": " http://cache-graphicslib.viator.com/graphicslib/page-imag "photoCount": 14, "primaryDestinationId": 684, "seoId": 14235, "productCount": 1,
```

"primaryDestinationName":

"Las Vegas",

p

a y est at

o

a e

:

as egas

,

```
"thumbnailURL": " http://cache-graphicslib.viator.com/graphicslib/page-images/56 "rating": 4.5, "title": "Shark Reef Aquarium at Mandalay Bay" }, "dateStamp": "2020-04-20T22:23:44+0000", "errorType": null, "errorCodes": [ ], "errorMessage": null, "errorName": null, "extraInfo": { }, "extraObject": null, "success": true, "totalCount": 1, "errorMessageText": null, "vmid": "331003" }
```

## /v1/attraction/products

<!-- image -->

/v1/attraction/products

<!-- image -->

This endpoint is marked for deprecation , but it will remain available to partners that started their integration prior to October 2024 to ensure backwards compatibility of existing integrations. Partners who got API access after October 2024 will not have access to this endpoint. To retrieve attractions information moving forward, please use the new /attractions/search and /attractions/{attraction-id} endpoints

This service gets attraction-related products (for cross-selling purposes). Attractions should be cached and refreshed weekly.

## Note :

- This endpoint uses conventions from V1 of this API. See Key-concepts - V1 endpoint conventions for further information
- This endpoint is only available to affiliate partners

AUTHORIZATIONS:

<!-- image -->

QUERY PARAMETERS

API-key

<!-- image -->

seoId required topX

sortOrder currencyCode

## HEADER PARAMETERS

- Accept-Language required

integer

Example:

seoId=14235

unique numeric identifier for the attraction to retrieve recommmendation details for string

Example:

topX=1-3

start and end rows to return in the format {start}-{end}

- e.g. '1-10' , '200-299'

## Note :

- the maximum number of rows per request is 100; therefore, '100-400' will return the same as '100-200'
- if topX is not specified, the default is '1-100'

string

Example:

sortOrder=SEO\_PRODUCT\_TOP\_SELLERS

sort order in which to return results; one of:

- SEO\_PRODUCT\_TOP\_SELLERS - Top Sellers ( Note : What Viator gets paid impacts this sort order)
- SEO\_PRODUCT\_REVIEW\_AVG\_RATING\_A - Traveller Rating (low-&gt;high)
- SEO\_PRODUCT\_REVIEW\_AVG\_RATING\_D - Traveller Rating (high-&gt;low)
- SEO\_PRODUCT\_PRICE\_FROM\_A - Price (low-&gt;high)
- SEO\_PRODUCT\_PRICE\_FROM\_D - Price (high-&gt;low)

string

Example:

currencyCode=EUR

currency-code for the currency in which to display pricing details for the products associated with the attraction specified.

## Note:

- You must have multiple currencies enabled in order to set the currency using this parameter. Please speak to your account manager if you wish to have this enabled.
- If you omit this parameter; or, if you do not have multiple currencies enabled, pricing will be returned in the default currency for your account.

string

Example:

en-US

## Responses

## 200 Success

RESPONSE SCHEMA:

application/json

|              | string or null reference number of this error errorReference                                                                                  |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| dateStamp    | string or null timestamp of this response                                                                                                     |
| errorType    | string or null code specifying the type of error                                                                                              |
| errorCodes   | Array of strings or null array of error codes pertaining to this error                                                                        |
| errorMessage | Array of arrays or null or null array of error message strings                                                                                |
| errorName    | string or null name of this type of error                                                                                                     |
| extraInfo    | object or null ignore (Viator only)                                                                                                           |
| extraObject  | object or null ignore (Viator only)                                                                                                           |
| success      | boolean or null boolean indicator of this request's outcome true : the request was successful with no errors false : an error was encountered |

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

| totalCount       | integer or null number of results available for this service               |
|------------------|----------------------------------------------------------------------------|
| errorMessageText | string or null array of error message strings in plain text                |
| vmid             | string or null unique numeric id of the server that processed this request |
| data             | Array of objects                                                           |

<!-- image -->

## /v1/support/customercare

<!-- image -->

<!-- image -->

/v1/support/customercare

This endpoint returns the URL to the Viator help page.

- Note : This endpoint uses conventions from V1 of this API. See Key-concepts - V1 endpoint conventions for further information
- Note : This endpoint is only available to affiliate partners

AUTHORIZATIONS:

API-key

## HEADER PARAMETERS

string

Example:

en-US

Specifies the language into which the natural-language fields in the response from this service will be translated (see Accept-Language header for available language codes)

- Accept-Language required

## Responses

## 200 Success

| RESPONSE SCHEMA:   | application/json                                                       |
|--------------------|------------------------------------------------------------------------|
| errorReference     | string or null reference number of this error                          |
| dateStamp          | string or null timestamp of this response                              |
| errorType          | string or null code specifying the type of error                       |
| errorCodes         | Array of strings or null array of error codes pertaining to this error |
| errorMessage       | Array of arrays or null or null                                        |

|                  | array of error message strings                                                                                                                |
|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| errorName        | string or null name of this type of error                                                                                                     |
| extraInfo        | object or null ignore (Viator only)                                                                                                           |
| extraObject      | object or null ignore (Viator only)                                                                                                           |
| success          | boolean or null boolean indicator of this request's outcome true : the request was successful with no errors false : an error was encountered |
| totalCount       | integer or null number of results available for this service                                                                                  |
| errorMessageText | string or null array of error message strings in plain text                                                                                   |
| vmid             | string or null unique numeric id of the server that processed this request                                                                    |
| data             | object                                                                                                                                        |

<!-- image -->

<!-- image -->