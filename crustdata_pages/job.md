> ## Documentation Index
> Fetch the complete documentation index at: https://docs.crustdata.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Search Jobs

> Query the indexed Crustdata job dataset with structured filters, cursor-based pagination, sorting, field selection, and aggregations.

**Use this when** you need to find, segment, or count job listings across the full Crustdata job dataset — for hiring-trend analysis, building target account lists from recently indexed hiring activity, monitoring specific roles, or powering a dashboard.

<Note>
  **`metadata.date_added` is when Crustdata first indexed the listing, not the
  employer-posted timestamp.** Every query in this page that filters on
  `metadata.date_added` is asking about **indexing time**, not the employer's
  actual publication date. Treat this endpoint as a query interface over
  Crustdata's indexed dataset, not as a direct poll of an employer-managed
  listings feed.
</Note>

```
POST https://api.crustdata.com/job/search
```

<Note>
  Replace `YOUR_API_KEY` in each example with your actual API key. All
  requests require the `x-api-version: 2025-11-01` header.
</Note>

## At a glance

| Detail          | Value                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| **Endpoint**    | `POST https://api.crustdata.com/job/search`                                                                   |
| **Auth**        | `Authorization: Bearer YOUR_API_KEY`                                                                          |
| **API version** | `x-api-version: 2025-11-01` header (required)                                                                 |
| **Body**        | **Required.** Send `{}` to match the whole dataset; every realistic query uses `filters`.                     |
| **Body keys**   | `filters`, `cursor`, `limit` (0–1000, default 20), `sorts`, `fields`, `aggregations` — all optional           |
| **Response**    | `{ "job_listings": [ Job, ... ], "next_cursor": string?, "total_count": integer?, "aggregations"?: [ ... ] }` |
| **Errors**      | `400` invalid request · `401` unauthorized · `500` internal                                                   |

<Note>
  **Jobs ID cheat sheet.** The Jobs APIs use three id concepts — keep them straight:

  * **`crustdata_job_id`** — the stable Crustdata job identifier. Returned on every `Job`. Use it as your dedupe key.
  * **`company.basic_info.crustdata_company_id`** — the stable Crustdata company identifier returned on every `Job`.
  * **`company.basic_info.company_id`** (filter alias) — the dot-path used in `filters` and `aggregations.column` for indexed [Search Jobs](/job-docs/search). It points to the same integer as `company.basic_info.crustdata_company_id`. This alias is **not sortable**; for deterministic pagination, sort on `metadata.date_added` instead.

  When you `group_by` on `company.basic_info.company_id`, each bucket also returns `metadata.company_name`, `metadata.company_website_domain`, and `metadata.linkedin_id` for labeling.
</Note>

### Guaranteed contract vs current behavior

| Topic                               | What it means                                                                                                                                                                                                                                   |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Endpoint, HTTP method, auth headers | `POST /job/search`, bearer auth, `x-api-version: 2025-11-01`.                                                                                                                                                                                   |
| Request body shape                  | Optional `filters`, `cursor`, `limit`, `sorts`, `fields`, `aggregations`. `filters` is a `SearchCondition` or a `SearchConditionGroup`.                                                                                                         |
| Response body shape                 | `{ "job_listings", "next_cursor", "total_count", "aggregations"? }`. Aggregation-only queries return `"job_listings": []`.                                                                                                                      |
| Supported operators                 | `=`, `!=`, `<`, `=<`, `>`, `=>`, `in`, `not_in`, `is_null`, `is_not_null`, `(.)`, `[.]`. See [Filter operators](#filter-operators).                                                                                                             |
| `limit` bounds and default          | Minimum `0`, maximum `1000`, default `20`. Set `limit: 0` when you only want aggregations.                                                                                                                                                      |
| Error status codes                  | `400`, `401`, `500`.                                                                                                                                                                                                                            |
| Indexed-field allowlist             | Only indexed fields can appear in `filters`, `sorts`, or `aggregations.column`. See the inline [Field reference](#field-reference) for the detailed catalog, or [Common indexed fields](#common-indexed-fields) below for the most-used subset. |
| Pricing and rate limits             | See the [Pricing](/general/pricing) and [Rate limits](/general/rate-limits) pages for the current numbers.                                                                                                                                      |

***

## Request body

| Parameter      | Type                          | Required | Default    | Description                                                                                                                                            |
| -------------- | ----------------------------- | -------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `filters`      | object                        | No       | —          | Single `SearchCondition` or nested `SearchConditionGroup`. Omit to match all indexed jobs.                                                             |
| `cursor`       | string                        | No       | —          | Opaque cursor from a prior response's `next_cursor`. Pass it to fetch the next page with the same filter, sort, and field set.                         |
| `limit`        | integer                       | No       | `20`       | Rows per page. Min `0`, max `1000`. Use `0` for aggregation-only queries.                                                                              |
| `sorts`        | array of `SearchSort`         | No       | —          | Ordering rules. Each item has `column` (dot-path) and `order` (`asc` or `desc`). Sorts are applied in array order.                                     |
| `fields`       | string\[]                     | No       | all fields | Dot-paths to include in each returned job. Omit to return everything. Always specify `fields` in production for smaller payloads and faster responses. |
| `aggregations` | array of `AggregationRequest` | No       | —          | Roll-up queries. Supports `count` and `group_by`. Use with `limit: 0` if you only want counts.                                                         |

### Response body

| Field          | Type            | Description                                                                                                                                                                                     |
| -------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `job_listings` | `Job[]`         | Matching job listings for the current page. Empty array `[]` when `limit` is `0` or when an aggregation-only query is made.                                                                     |
| `next_cursor`  | string or null  | Opaque cursor to fetch the next page. `null` when there are no more pages.                                                                                                                      |
| `total_count`  | integer or null | Total number of jobs matching the filter across all pages. Can be `null` for very broad queries where computing an exact total would be prohibitively expensive — never assume it is populated. |
| `aggregations` | array           | Aggregation results, present only when the request included an `aggregations` array.                                                                                                            |

### Rate limits and credits

<Note>Current pricing for indexed Jobs Search:</Note>

<Callout icon="coins" color="#5345e4">
  <strong>Pricing:</strong> <code>0.03 credits per result returned</code>. A
  request with no results does not consume credits.
</Callout>

<Note>
  Default `rate-limit` is 15 requests per minute. Send an email to
  [gtm@crustdata.co](mailto:gtm@crustdata.co) to discuss higher limits if
  needed for your use case.
</Note>

***

## Your first search: filter by company and title

Find the most recent Software Engineer listings at Stripe (filtered via the `company.basic_info.company_id` alias, which maps to `crustdata_company_id = 631394`).

<CodeGroup>
  ```bash curl theme={"theme":"vitesse-black"}
  curl --request POST \
    --url https://api.crustdata.com/job/search \
    --header 'authorization: Bearer YOUR_API_KEY' \
    --header 'content-type: application/json' \
    --header 'x-api-version: 2025-11-01' \
    --data '{
      "filters": {
        "op": "and",
        "conditions": [
          { "field": "company.basic_info.company_id", "type": "=", "value": 631394 },
          { "field": "job_details.title",              "type": "=", "value": "Software Engineer" }
        ]
      },
      "fields": [
        "job_details.title",
        "job_details.url",
        "company.basic_info.name",
        "location.raw",
        "metadata.date_added"
      ],
      "sorts": [
        { "column": "metadata.date_added", "order": "desc" }
      ],
      "limit": 2
    }'
  ```

  ```json Response theme={"theme":"vitesse-black"}
  {
      "job_listings": [
          {
              "job_details": {
                  "title": "Software Engineer",
                  "url": "https://www.linkedin.com/jobs/view/4398377738"
              },
              "company": {
                  "basic_info": { "name": "Stripe" }
              },
              "location": { "raw": "Melbourne, Victoria, Australia" },
              "metadata": { "date_added": "2026-04-07T11:37:29" }
          }
      ],
      "next_cursor": "H4sIAJJG1mkC_xXMPQ7CMAwG0KtEmTvYiR0nXAWhyvlBHRARbTogxN0J01s-vY99nW1_r5sem70YSzEJErG_VwdSnfeMiVpSjhmbUmkanXqXa5rlqsUlTJApUPO1NrsYe_R9zNcVRZgDRhIAWAwhsA_Ct0lGH_pYSz-ffykR8PsDw2G2zooAAAA=",
      "total_count": 1676
  }
  ```
</CodeGroup>

<Tip>
  **Always send `fields`.** The full `Job` schema is large (firmographics +
  location + description + metadata). Fetching only the dot-paths you need
  keeps responses small, fast, and predictable.
</Tip>

***

## Filter grammar

Every filter describes which **individual job rows** to keep. The API checks each job listing against your filter independently — it never groups or combines rows before filtering.

There are two building blocks:

| Building block                    | What it does                                                                 |
| --------------------------------- | ---------------------------------------------------------------------------- |
| **`SearchCondition`** (leaf)      | Tests one field on one job row — e.g. `title = "Software Engineer"`.         |
| **`SearchConditionGroup`** (node) | Combines conditions with `and` or `or`. Groups can nest inside other groups. |

<Warning>
  **Exact-match AND on the same field always returns zero results.** One
  listing has one title, so `(title = "Software Engineer") AND (title =
        "Account Executive")` can never match. This applies to `=` and `in`.
</Warning>

<Info>
  **All-words operators (`(.)`) work fine in AND.** Because `(.)` checks for
  individual words — not a contiguous substring — a query like `(title (.)
        "Software Development") AND (title (.) "Software Engineer")` matches any
  title containing all three words "Software", "Development", and "Engineer"
  (e.g. "Software Development Engineer").
</Info>

<Tip>
  Need *companies* hiring for both role X **and** role Y (two different
  listings)? Run two separate queries and intersect company ids client-side.
  See [Companies indexing both Software Engineers and Account
  Executives](#companies-indexing-both-software-engineers-and-account-executives).
</Tip>

### Single condition

```json theme={"theme":"vitesse-black"}
{
    "filters": {
        "field": "job_details.category",
        "type": "=",
        "value": "Engineering"
    }
}
```

### AND / OR group

```json theme={"theme":"vitesse-black"}
{
    "filters": {
        "op": "and",
        "conditions": [
            {
                "field": "company.basic_info.company_id",
                "type": "=",
                "value": 631394
            },
            {
                "field": "job_details.category",
                "type": "=",
                "value": "Engineering"
            },
            {
                "field": "metadata.date_added",
                "type": "=>",
                "value": "2025-01-01"
            }
        ]
    }
}
```

### Array-field filters and grouping

<AccordionGroup>
  <Accordion title="Filtering on array fields">
    When you filter on a string-array field like
    `company.basic_info.industries`, the condition is satisfied if **any**
    element of the array matches.

    For example:

    ```json theme={"theme":"vitesse-black"}
    { "field": "company.basic_info.industries", "type": "=", "value": "Technology, Information and Internet" }
    ```

    This matches any company whose `industries` array contains that exact
    string. Use `(.)` to match words within any element.
  </Accordion>

  <Accordion title="Grouping by array fields">
    When you `group_by` on an array field, each array element becomes its
    own bucket key. A company in two industries contributes one count to
    **each** of the two industry buckets — so the sum of bucket counts can
    exceed `total_count` for array columns.
  </Accordion>
</AccordionGroup>

### Nested groups (SDR / BDR keyword search across multiple companies)

<Tip>
  The long forms `"Sales Development Representative"` and `"Business
        Development Representative"` use `(.)` (all-words match), but the short
  acronym `"SDR"` uses `[.]` (exact phrase). Short acronyms with `(.)` can
  overmatch — e.g. `"SDR"` would also match `"USDR"`. Use `[.]` for 2–3
  character acronyms.
</Tip>

<CodeGroup>
  ```bash curl theme={"theme":"vitesse-black"}
  curl --request POST \
    --url https://api.crustdata.com/job/search \
    --header 'authorization: Bearer YOUR_API_KEY' \
    --header 'content-type: application/json' \
    --header 'x-api-version: 2025-11-01' \
    --data '{
      "filters": {
        "op": "and",
        "conditions": [
          { "field": "company.basic_info.company_id", "type": "in", "value": [631394, 631811, 673947] },
          { "field": "metadata.date_added",           "type": "=>", "value": "2025-01-01" },
          {
            "op": "or",
            "conditions": [
              { "field": "job_details.title", "type": "(.)", "value": "Sales Development Representative" },
              { "field": "job_details.title", "type": "[.]", "value": "SDR" },
              { "field": "job_details.title", "type": "(.)", "value": "Business Development Representative" }
            ]
          }
        ]
      },
      "fields": [
        "job_details.title",
        "company.basic_info.name",
        "location.raw",
        "metadata.date_added"
      ],
      "sorts": [{ "column": "metadata.date_added", "order": "desc" }],
      "limit": 2
    }'
  ```
</CodeGroup>

***

## Filter operators

Use the table below to pick the right `type` for each condition. Every operator works on indexed fields only.

| Operator | `value` shape                  | Meaning                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| -------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `=`      | scalar (string/number/boolean) | Exact match.                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `!=`     | scalar                         | Not equal.                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `<`      | scalar (numeric or ISO date)   | Less than.                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `=<`     | scalar (numeric or ISO date)   | Less than or equal. **Not** `<=`.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `>`      | scalar (numeric or ISO date)   | Greater than.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `=>`     | scalar (numeric or ISO date)   | Greater than or equal. **Not** `>=`.                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `in`     | array of scalars               | Field value is any entry in the array.                                                                                                                                                                                                                                                                                                                                                                                                                |
| `not_in` | array of scalars               | Field value is none of the entries in the array.                                                                                                                                                                                                                                                                                                                                                                                                      |
| `(.)`    | string                         | **Case-insensitive all-words match.** Every word in the query must appear somewhere in the field, but **not necessarily next to each other or in the same order**. `"Software Engineer"` matches `"Software Engineer"`, `"Software Development Engineer"`, and `"Engineer, Software Systems"`. A single word like `"engineer"` also matches `"Engineering Manager"`. Great for broad keyword hunting in `job_details.title` or `content.description`. |
| `[.]`    | string                         | **Case-insensitive exact-phrase match.** The words must appear **contiguously and in order**. `"Software Engineer"` matches `"Senior Software Engineer"` but **not** `"Software Development Engineer"` (extra word in between) and **not** `"Engineer Software"` (wrong order). Use `[.]` when you need precision over recall.                                                                                                                        |

<Warning>
  **Operator footguns.**

  * Use `=>` for greater-than-or-equal and `=<` for less-than-or-equal — they are **not** `>=` and `<=`.
  * `in` and `not_in` require **JSON arrays**, not comma-separated strings.
</Warning>

***

## Common indexed fields

These are the indexed fields most often used in `filters`, `sorts`, and `aggregations.column`. This table is a **summary of the most common paths**, not an authoritative catalog. For the deeper field catalog — including id semantics, null handling, and bucket metadata — see the inline [Field reference](#field-reference).

<Note>
  **Company id filter alias.** The filterable field path uses the short alias
  `company.basic_info.company_id`, but the response shape returns the same
  integer at `company.basic_info.crustdata_company_id`. They point to the same
  value. See [Jobs IDs: a quick map](#jobs-ids-a-quick-map) for every id
  concept and how they relate.
</Note>

<Tabs>
  <Tab title="Job details">
    | Field                        | Example                                                |
    | ---------------------------- | ------------------------------------------------------ |
    | `job_details.title`          | `"Software Engineer"`                                  |
    | `job_details.category`       | `"Engineering"`, `"Sales"`, `"Operations"`, `"Others"` |
    | `job_details.workplace_type` | `"Remote"`, `"Hybrid"`, `"On-site"`, `""`              |
    | `job_details.reposted_job`   | `true` / `false`                                       |
    | `job_details.url`            | `"https://www.linkedin.com/jobs/view/4398377738"`      |
  </Tab>

  <Tab title="Company basic info">
    | Field                                        | Example                                    |
    | -------------------------------------------- | ------------------------------------------ |
    | `company.basic_info.company_id`              | `631394`                                   |
    | `company.basic_info.name`                    | `"Stripe"`                                 |
    | `company.basic_info.primary_domain`          | `"stripe.com"`                             |
    | `company.basic_info.professional_network_id` | `"2135371"`                                |
    | `company.basic_info.industries`              | `["Technology, Information and Internet"]` |
  </Tab>

  <Tab title="Company firmographics">
    | Field                                       | Example        |
    | ------------------------------------------- | -------------- |
    | `company.headcount.total`                   | `14522`        |
    | `company.headcount.range`                   | `"5001-10000"` |
    | `company.followers.count`                   | `1335688`      |
    | `company.revenue.estimated.lower_bound_usd` | `500000000`    |
  </Tab>

  <Tab title="Location">
    | Field               | Example                            |
    | ------------------- | ---------------------------------- |
    | `location.raw`      | `"Melbourne, Victoria, Australia"` |
    | `location.country`  | `"Australia"`                      |
    | `location.state`    | `"Victoria"`                       |
    | `location.district` | `"Southbank"`                      |
    | `location.city`     | `"Melbourne"`                      |
  </Tab>

  <Tab title="Content, metadata, IDs">
    | Field                   | Example                    |
    | ----------------------- | -------------------------- |
    | `content.description`   | Full job description text. |
    | `crustdata_job_id`      | `41053563`                 |
    | `metadata.date_added`   | `"2026-04-07T11:37:29"`    |
    | `metadata.date_updated` | `"2026-04-08T00:00:00"`    |
  </Tab>
</Tabs>

<Note>
  Sending a filter on a non-indexed field returns `400` with `Unsupported
        columns in conditions: ['...']`. Sending an unsupported `group_by` column
  returns a similar error listing every supported aggregation column.
</Note>

***

## Sorting

`sorts` is an ordered array. Each item has a `column` and `order` (`"asc"` or `"desc"`). Sorts apply in array order — the first sort is the primary key, the second breaks ties, and so on.

```json theme={"theme":"vitesse-black"}
{
    "sorts": [
        { "column": "metadata.date_added", "order": "desc" },
        { "column": "company.headcount.total", "order": "desc" }
    ]
}
```

<Warning>
  **Sort allowlist is narrower than filter allowlist.** Sort only works on
  numeric, date, and a small set of scalar fields. Sorting on text fields like
  `job_details.title`, `job_details.category`, or `company.basic_info.name`
  returns `Unsupported columns in conditions`. See the [Sortable
  fields](#sortable-fields) for the full list of sortable columns.
</Warning>

### Sortable fields

The following indexed fields are verified sortable:

* `metadata.date_added`
* `metadata.date_updated`
* `company.headcount.total`
* `company.followers.count`
* `company.revenue.estimated.lower_bound_usd`
* `company.revenue.estimated.upper_bound_usd`
* `company.funding.total_investment_usd`
* `company.funding.valuation_usd`
* `company.funding.last_fundraise_date`
* `company.funding.num_funding_rounds`

Common sort choices:

* **Newest postings first** — `{ "column": "metadata.date_added", "order": "desc" }`
* **Biggest companies first** — `{ "column": "company.headcount.total", "order": "desc" }`
* **Most followed companies first** — `{ "column": "company.followers.count", "order": "desc" }`
* **Highest-funded companies first** — `{ "column": "company.funding.total_investment_usd", "order": "desc" }`

***

## Pagination

Pagination is **cursor-based**. Each response returns a `next_cursor` (or `null` when you reach the end). To fetch the next page, resend the original request body with `cursor` set to the previous `next_cursor`.

<Steps>
  <Step title="Fetch the first page">
    Omit `cursor` and set `limit` to your page size (max `1000`).
  </Step>

  <Step title="Walk forward">
    Take `next_cursor` from the response and pass it back as `cursor` in the
    next request. Keep `filters`, `sorts`, and `fields` identical — if you
    change them, the cursor becomes meaningless.
  </Step>

  <Step title="Stop when `next_cursor` is null">
    A `null` cursor means you've reached the end of the result set.
  </Step>
</Steps>

### Consistency between pages

<Note>
  **Current platform behavior — best-effort, not strict snapshot.** A cursor
  is consistent with respect to the filter, sort, and field selection you
  sent on the first page, so the same query will keep paging forward over
  a coherent result stream. However, because the underlying indexed
  dataset is continuously updated, new jobs indexed between page requests
  can cause minor drift in `total_count` and in the exact position of
  individual rows. Treat pagination as **best-effort**, not a strict
  snapshot.

  For bulk exports where every row matters:

  * **Constrain your filter to a bounded date window** (for example
    `metadata.date_added >= 2025-01-01` AND `< 2025-07-01`) so newly
    indexed jobs outside the window do not affect the walk, and
  * **Re-run the full walk periodically** and diff against the prior
    snapshot using `crustdata_job_id` as the dedupe key.
</Note>

### Dataset freshness and lifecycle

<Note>
  **What the indexed Jobs dataset represents.** The Search Jobs dataset is
  a rolling index of job listings discovered from the web, refreshed on an
  ongoing basis. Each row has:

  * **`metadata.date_added`** — when Crustdata first saw the listing.
  * **`metadata.date_updated`** — most recent refresh.

  Closed or removed listings are **not** guaranteed to disappear from the
  index immediately. To approximate "currently hiring" queries, filter on a
  recent `metadata.date_added` or `metadata.date_updated` window (for
  example, within the last 30 days) and pair it with the hiring company's
  firmographics. For alerting or repeated exports, keep your date windows
  bounded and dedupe rows with `crustdata_job_id`.
</Note>

### Date filter semantics

<Note>
  **Dates and timezones.** When you pass a date-only value like
  `"2025-01-01"`, the backend interprets it as `2025-01-01T00:00:00` in
  UTC. Ranges using `=>` are inclusive of the boundary and `<` is
  exclusive, so `"metadata.date_added" >= "2025-01-01"` **AND**
  `< "2025-07-01"` covers every listing indexed between Jan 1 (inclusive)
  and Jul 1 (exclusive) in UTC. Pass full timestamps like
  `"2025-01-01T08:00:00"` when you need finer precision.
</Note>

### Fetch page 2

```json theme={"theme":"vitesse-black"}
{
    "filters": {
        "field": "company.basic_info.company_id",
        "type": "=",
        "value": 631394
    },
    "fields": ["job_details.title"],
    "limit": 1,
    "cursor": "H4sIANBG1mkC_xXMOQ4CMQxA0auMUk9hx3YScxWERs6CpkBEzFIgxN0J1W-e_se9zra9l9X21V0mx0kjMgvdq4dYPZGgclOTlLEZl2bJG_lcdVSqFa-okDlwo1qbmye39-0YryvGKBIwsQLAPDGCkAS6DXL0wx5L6efzL2MC_P4A250zQYoAAAA="
}
```

***

## Field selection

Use `fields` to return only the dot-paths you need. The top-level groups are `crustdata_job_id`, `job_details`, `company`, `location`, `content`, `metadata`. You can request:

* **A whole group** — `"company"` returns every `company.*` sub-object.
* **A sub-object** — `"company.basic_info"` returns only the basic info block.
* **A single field** — `"company.basic_info.name"` returns just the name.

```json theme={"theme":"vitesse-black"}
{
    "fields": [
        "job_details.title",
        "job_details.url",
        "company.basic_info.name",
        "company.basic_info.primary_domain",
        "location.raw",
        "metadata.date_added"
    ]
}
```

<Tip>
  **Recommended default field set** for most dashboards:
  `["job_details.title", "job_details.category", "job_details.url",
        "company.basic_info.name", "company.basic_info.primary_domain",
        "location.raw", "metadata.date_added"]`.
</Tip>

***

## Field reference

This section replaces the standalone Jobs field-reference page for the indexed
search endpoint. It covers the return shape, id semantics, aggregation bucket
metadata, and the most important indexed field catalogs in one place.

### Annotated full `Job` example

<Note>
  The code fence below uses `jsonc` because it includes inline `//` comments
  for annotation. Strip the comments before sending it to a strict JSON
  parser.
</Note>

```jsonc theme={"theme":"vitesse-black"}
{
    "crustdata_job_id": 41053563, // stable job id (use as dedupe key)
    "job_details": {
        "job_id": 41053563, // mirrors crustdata_job_id
        "title": "Integration Engineer (AUNZ)",
        "category": "Engineering",
        "workplace_type": "",
        "url": "https://www.linkedin.com/jobs/view/4398377738",
        "reposted_job": false,
        "number_of_openings": 1,
    },
    "company": {
        "basic_info": {
            "crustdata_company_id": 631394, // filter with company.basic_info.company_id
            "name": "Stripe",
            "primary_domain": "stripe.com",
            "website": "https://stripe.com",
            "professional_network_id": "2135371",
            "industries": ["Technology, Information and Internet"],
        },
        "locations": {
            "country": "USA",
            "state": "California",
            "city": "South San Francisco",
            "street_address": "354 Oyster Point Blvd, South San Francisco, California, United States",
        },
        "headcount": {
            "total": 7234,
            "range": "5001-10000",
            "largest_headcount_country": "USA",
        },
        "followers": { "count": 1335688 },
        "revenue": {
            "estimated": {
                "lower_bound_usd": 500000000,
                "upper_bound_usd": 1000000000,
            },
            "public_markets": null,
            "acquisition_status": "",
        },
        "funding": {
            "total_investment_usd": 9440247725.0,
            "valuation_usd": 50000000000.0,
            "last_fundraise_date": "2026-03-09T00:00:00",
            "last_round_type": "secondary_market",
            "num_funding_rounds": 23,
            "investors": [
                "Sequoia Capital",
                "Andreessen Horowitz",
                "Founders Fund",
            ],
        },
        "competitors": {
            "websites": ["https://plaid.com", "https://paystack.com"],
        },
    },
    "location": {
        "raw": "Melbourne, Victoria, Australia",
        "city": "Melbourne",
        "district": null,
        "state": "Victoria",
        "country": "Australia",
        "pincode": null,
    },
    "content": {
        "description": "Stripe is a financial infrastructure platform for businesses...",
    },
    "metadata": {
        "date_added": "2026-04-07T11:37:29",
        "date_updated": "2026-04-08T00:00:00",
    },
}
```

<Tip>
  **Nulls are normal.** Nested objects such as `revenue.public_markets`,
  `location.district`, `location.pincode`, and parts of `company.funding` can
  legitimately be `null` or missing.
</Tip>

### Jobs IDs: a quick map

| ID                                        | Lives on                         | Purpose                                                                                                    |
| ----------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `crustdata_job_id`                        | Top-level on each `Job`          | Stable Crustdata job identifier. Use it as your dedupe key in your own store.                              |
| `job_details.job_id`                      | Inside `Job.job_details`         | Secondary job identifier. It currently mirrors `crustdata_job_id` and is kept for backwards compatibility. |
| `company.basic_info.crustdata_company_id` | Inside `Job.company.basic_info`  | Stable Crustdata company identifier returned on each row.                                                  |
| `company.basic_info.company_id`           | Search filter / aggregation path | Indexed alias for the same company identifier. Use this in `filters.field` and `aggregations.column`.      |

### Aggregation bucket metadata

When you `group_by` on `company.basic_info.company_id`, each bucket carries a
`metadata` object whose keys use bucket-specific names rather than the `Job`
response dot-paths:

| Bucket metadata key      | Equivalent `Job` value                       | Notes                                                               |
| ------------------------ | -------------------------------------------- | ------------------------------------------------------------------- |
| `company_name`           | `company.basic_info.name`                    | Plain company name.                                                 |
| `company_website_domain` | `company.basic_info.primary_domain`          | Primary website domain.                                             |
| `linkedin_id`            | `company.basic_info.professional_network_id` | Public-profile identifier returned only inside aggregation buckets. |

### Job identifiers

| Path                 | Type    | Filter | Sort | Group | Return | Example    |
| -------------------- | ------- | ------ | ---- | ----- | ------ | ---------- |
| `crustdata_job_id`   | integer | ✅      | —    | —     | ✅      | `41053563` |
| `job_details.job_id` | integer | —      | —    | —     | ✅      | `41053563` |

### Job details (`job_details.*`)

| Path                             | Type    | Filter | Sort | Group | Return | Example                                           |
| -------------------------------- | ------- | ------ | ---- | ----- | ------ | ------------------------------------------------- |
| `job_details.title`              | string  | ✅      | —    | ✅     | ✅      | `"Software Engineer"`                             |
| `job_details.category`           | string  | ✅      | —    | ✅     | ✅      | `"Engineering"`                                   |
| `job_details.workplace_type`     | string  | ✅      | —    | ✅     | ✅      | `"Remote"`, `"Hybrid"`, `"On-site"`, `""`         |
| `job_details.reposted_job`       | boolean | ✅      | —    | —     | ✅      | `false`                                           |
| `job_details.url`                | string  | ✅      | —    | —     | ✅      | `"https://www.linkedin.com/jobs/view/4398377738"` |
| `job_details.number_of_openings` | integer | —      | —    | —     | ✅      | `1`                                               |

### Company basic info (`company.basic_info.*`)

| Path                                         | Type      | Filter | Sort | Group | Return | Example                                    |
| -------------------------------------------- | --------- | ------ | ---- | ----- | ------ | ------------------------------------------ |
| `company.basic_info.company_id`              | integer   | ✅      | —    | ✅     | —      | `631394`                                   |
| `company.basic_info.crustdata_company_id`    | integer   | —      | —    | —     | ✅      | `631394`                                   |
| `company.basic_info.name`                    | string    | ✅      | —    | —     | ✅      | `"Stripe"`                                 |
| `company.basic_info.primary_domain`          | string    | ✅      | —    | ✅     | ✅      | `"stripe.com"`                             |
| `company.basic_info.website`                 | string    | —      | —    | —     | ✅      | `"https://stripe.com"`                     |
| `company.basic_info.professional_network_id` | string    | ✅      | —    | —     | ✅      | `"2135371"`                                |
| `company.basic_info.industries`              | string\[] | ✅      | —    | ✅     | ✅      | `["Technology, Information and Internet"]` |

<Note>
  `company.basic_info.company_id` and
  `company.basic_info.crustdata_company_id` refer to the same integer. Use the
  short alias in `filters` and `aggregations.column`. The response shape
  writes the value under `crustdata_company_id`.
</Note>

### Company firmographics

#### Headcount (`company.headcount.*`)

| Path                                          | Type    | Filter | Sort | Group | Return | Example        |
| --------------------------------------------- | ------- | ------ | ---- | ----- | ------ | -------------- |
| `company.headcount.total`                     | integer | ✅      | ✅    | —     | ✅      | `14522`        |
| `company.headcount.range`                     | string  | ✅      | —    | ✅     | ✅      | `"5001-10000"` |
| `company.headcount.largest_headcount_country` | string  | —      | —    | —     | ✅      | `"USA"`        |

#### Followers (`company.followers.*`)

| Path                      | Type    | Filter | Sort | Group | Return | Example   |
| ------------------------- | ------- | ------ | ---- | ----- | ------ | --------- |
| `company.followers.count` | integer | ✅      | ✅    | —     | ✅      | `1335688` |

#### Revenue (`company.revenue.*`)

| Path                                             | Type      | Filter | Sort | Group | Return | Example      |
| ------------------------------------------------ | --------- | ------ | ---- | ----- | ------ | ------------ |
| `company.revenue.estimated.lower_bound_usd`      | integer   | ✅      | ✅    | —     | ✅      | `500000000`  |
| `company.revenue.estimated.upper_bound_usd`      | integer   | ✅      | ✅    | —     | ✅      | `1000000000` |
| `company.revenue.acquisition_status`             | string    | ✅      | —    | —     | ✅      | `""`         |
| `company.revenue.public_markets.stock_symbols`   | string\[] | —      | —    | —     | ✅      | `["STRIPE"]` |
| `company.revenue.public_markets.fiscal_year_end` | string    | —      | —    | —     | ✅      | `""`         |

#### Funding (`company.funding.*`)

| Path                                   | Type              | Filter | Sort | Group | Return | Example                 |
| -------------------------------------- | ----------------- | ------ | ---- | ----- | ------ | ----------------------- |
| `company.funding.total_investment_usd` | number            | ✅      | ✅    | —     | ✅      | `9440247725.0`          |
| `company.funding.valuation_usd`        | number            | ✅      | ✅    | —     | ✅      | `50000000000.0`         |
| `company.funding.last_fundraise_date`  | string (ISO 8601) | ✅      | ✅    | —     | ✅      | `"2026-03-09T00:00:00"` |
| `company.funding.last_round_type`      | string            | ✅      | —    | ✅     | ✅      | `"secondary_market"`    |
| `company.funding.num_funding_rounds`   | integer           | ✅      | ✅    | —     | ✅      | `23`                    |
| `company.funding.investors`            | string\[]         | —      | —    | —     | ✅      | `["Sequoia Capital"]`   |

#### Competitors and company locations

| Path                               | Type      | Filter | Sort | Group | Return | Example                        |
| ---------------------------------- | --------- | ------ | ---- | ----- | ------ | ------------------------------ |
| `company.competitors.websites`     | string\[] | —      | —    | —     | ✅      | `["https://plaid.com"]`        |
| `company.locations.country`        | string    | ✅      | —    | ✅     | ✅      | `"USA"`                        |
| `company.locations.state`          | string    | —      | —    | —     | ✅      | `"California"`                 |
| `company.locations.city`           | string    | —      | —    | —     | ✅      | `"South San Francisco"`        |
| `company.locations.street_address` | string    | —      | —    | —     | ✅      | `"354 Oyster Point Blvd, ..."` |

### Job location (`location.*`)

| Path                | Type   | Filter | Sort | Group | Return | Example                            |
| ------------------- | ------ | ------ | ---- | ----- | ------ | ---------------------------------- |
| `location.raw`      | string | ✅      | —    | —     | ✅      | `"Melbourne, Victoria, Australia"` |
| `location.city`     | string | ✅      | —    | —     | ✅      | `"Melbourne"`                      |
| `location.district` | string | ✅      | —    | —     | ✅      | `"Southbank"`                      |
| `location.state`    | string | ✅      | —    | —     | ✅      | `"Victoria"`                       |
| `location.country`  | string | ✅      | —    | ✅     | ✅      | `"Australia"`                      |
| `location.pincode`  | string | ✅      | —    | —     | ✅      | `"3006"`                           |

<Note>
  **Country value normalization.** `location.country` can appear as full names
  (`"United States"`), ISO-style short forms (`"USA"`), and occasional
  variants (`"United States of America"`). When filtering by country, either
  match multiple variants with `in` or pre-discover the exact indexed values
  by running a `group_by` on `location.country`.
</Note>

### Content (`content.*`)

| Path                  | Type   | Filter | Sort | Group | Return | Example                                     |
| --------------------- | ------ | ------ | ---- | ----- | ------ | ------------------------------------------- |
| `content.description` | string | ✅      | —    | —     | ✅      | `"Stripe is a financial infrastructure..."` |

<Tip>
  Use the `(.)` operator on `content.description` to find listings by
  technology, skill, or keyword.
</Tip>

### Metadata (`metadata.*`)

| Path                    | Type              | Filter | Sort | Group | Return | Example                 |
| ----------------------- | ----------------- | ------ | ---- | ----- | ------ | ----------------------- |
| `metadata.date_added`   | string (ISO 8601) | ✅      | ✅    | —     | ✅      | `"2026-04-07T11:37:29"` |
| `metadata.date_updated` | string (ISO 8601) | ✅      | ✅    | —     | ✅      | `"2026-04-08T00:00:00"` |

### Null, blank, and sparse field behavior

Most `Job` fields are nullable in the spec and can legitimately be absent or
empty.

* **Null or missing** — the field is not present on a given `Job`.
* **Blank string `""`** — the field was present but had no indexable value
  (common for `job_details.workplace_type`). Treat blank as “unspecified”, not
  as the same thing as null.
* **Sparse nested objects** — `company.funding`, `company.revenue`, and
  `company.competitors` are often missing for smaller or private companies.
* **`is_null` / `is_not_null` operators are currently not implemented** —
  request the field via `fields` and filter for null presence client-side.

***

## Aggregations

Aggregations let you roll up results without returning individual job rows. Set `limit: 0` when you only want aggregation output. Two types are supported:

* **`count`** — returns the total number of jobs matching `filters`.
* **`group_by`** — buckets the results by `column` and returns per-bucket counts.

### `AggregationRequest` schema

| Field    | Type          | Required                | Description                                                                           |
| -------- | ------------- | ----------------------- | ------------------------------------------------------------------------------------- |
| `type`   | string (enum) | **Yes**                 | `"count"` for a simple total, `"group_by"` to bucket by `column`.                     |
| `column` | string        | Required for `group_by` | Dot-path to group by. Must be in the [Groupable fields](#groupable-fields) allowlist. |
| `agg`    | string (enum) | Required for `group_by` | Sub-aggregation inside each bucket. Currently only `"count"` is supported.            |
| `size`   | integer       | No (default `100`)      | Maximum number of buckets to return. Min `1`, max `1000`.                             |

Each `AggregationResponseItem` echoes `type` and `column`, then carries:

* **`value`** (integer) — populated for `count` aggregations. The total match count.
* **`buckets`** (array) — populated for `group_by` aggregations. Each bucket has a `key`, `count`, and a `metadata` object whose keys depend on the grouped column. See [Aggregation bucket metadata](#aggregation-bucket-metadata) for the exact keys returned for `group_by` on `company.basic_info.company_id`.

You can include multiple aggregations in a single request; the response returns them in `aggregations[]` in the same order you sent them.

### Count all Engineering jobs

<CodeGroup>
  ```bash curl theme={"theme":"vitesse-black"}
  curl --request POST \
    --url https://api.crustdata.com/job/search \
    --header 'authorization: Bearer YOUR_API_KEY' \
    --header 'content-type: application/json' \
    --header 'x-api-version: 2025-11-01' \
    --data '{
      "filters": { "field": "job_details.category", "type": "=", "value": "Engineering" },
      "limit": 0,
      "aggregations": [ { "type": "count" } ]
    }'
  ```

  ```json Response theme={"theme":"vitesse-black"}
  {
      "job_listings": [],
      "next_cursor": null,
      "total_count": 4354217,
      "aggregations": [{ "type": "count", "column": null, "value": 4354217 }]
  }
  ```
</CodeGroup>

### Top companies indexing "Software Engineer" listings (bounded window)

<CodeGroup>
  ```bash curl theme={"theme":"vitesse-black"}
  curl --request POST \
    --url https://api.crustdata.com/job/search \
    --header 'authorization: Bearer YOUR_API_KEY' \
    --header 'content-type: application/json' \
    --header 'x-api-version: 2025-11-01' \
    --data '{
      "filters": {
        "op": "and",
        "conditions": [
          { "field": "job_details.title",   "type": "=",  "value": "Software Engineer" },
          { "field": "metadata.date_added", "type": "=>", "value": "2025-01-01" },
          { "field": "metadata.date_added", "type": "<",  "value": "2026-01-01" }
        ]
      },
      "limit": 0,
      "aggregations": [
        {
          "type": "group_by",
          "column": "company.basic_info.company_id",
          "agg": "count",
          "size": 5
        }
      ]
    }'
  ```

  ```json Response theme={"theme":"vitesse-black"}
  {
      "job_listings": [],
      "next_cursor": null,
      "total_count": 30495,
      "aggregations": [
          {
              "type": "group_by",
              "column": "company.basic_info.company_id",
              "buckets": [
                  {
                      "key": 821755,
                      "count": 1037,
                      "metadata": {
                          "company_name": "Jobs via Dice",
                          "company_website_domain": "dice.com",
                          "linkedin_id": "104085107"
                      }
                  },
                  {
                      "key": 3674630,
                      "count": 878,
                      "metadata": {
                          "company_name": "Bending Spoons",
                          "company_website_domain": "bndspn.com",
                          "linkedin_id": "3175130"
                      }
                  },
                  {
                      "key": 2110301,
                      "count": 546,
                      "metadata": {
                          "company_name": "Microsoft",
                          "company_website_domain": "microsoft.com",
                          "linkedin_id": "1035"
                      }
                  }
              ]
          }
      ]
  }
  ```
</CodeGroup>

### Groupable fields

`group_by.column` is restricted to the following indexed fields:

* `company.basic_info.company_id`
* `company.basic_info.industries`
* `company.basic_info.primary_domain`
* `company.funding.last_round_type`
* `company.headcount.range`
* `company.locations.country`
* `job_details.category`
* `job_details.title`
* `job_details.workplace_type`
* `location.country`

Sending any other column returns `400` with `Unsupported aggregation column: '...'. Supported: ...`.

***

## Example queries

Use these recipes when you need public, indexed workflows beyond the basic
examples above.

### Companies indexing both Software Engineers and Account Executives

Because filters operate on individual job rows, you cannot ask for “companies
with both roles” in a single query. Instead, run two bounded-window
aggregations and intersect the company ids client-side.

<Tip>
  **Watch out for short-acronym false positives.** `(.)` is an all-words
  match, so a query of `"AE"` in `job_details.title` can also match unrelated
  titles. Prefer `[.]` for 2–3 character acronyms.
</Tip>

<Steps>
  <Step title="Query 1 — companies with Software Engineer listings">
    ```json theme={"theme":"vitesse-black"}
    {
        "filters": {
            "op": "and",
            "conditions": [
                {
                    "field": "metadata.date_added",
                    "type": "=>",
                    "value": "2025-01-01"
                },
                {
                    "field": "metadata.date_added",
                    "type": "<",
                    "value": "2026-01-01"
                },
                {
                    "op": "or",
                    "conditions": [
                        {
                            "field": "job_details.title",
                            "type": "(.)",
                            "value": "Software Engineer"
                        },
                        {
                            "field": "job_details.title",
                            "type": "[.]",
                            "value": "SWE"
                        }
                    ]
                }
            ]
        },
        "limit": 0,
        "aggregations": [
            {
                "type": "group_by",
                "column": "company.basic_info.company_id",
                "agg": "count",
                "size": 500
            }
        ]
    }
    ```
  </Step>

  <Step title="Query 2 — companies with Account Executive listings">
    ```json theme={"theme":"vitesse-black"}
    {
        "filters": {
            "op": "and",
            "conditions": [
                {
                    "field": "metadata.date_added",
                    "type": "=>",
                    "value": "2025-01-01"
                },
                {
                    "field": "metadata.date_added",
                    "type": "<",
                    "value": "2026-01-01"
                },
                {
                    "op": "or",
                    "conditions": [
                        {
                            "field": "job_details.title",
                            "type": "(.)",
                            "value": "Account Executive"
                        },
                        {
                            "field": "job_details.title",
                            "type": "[.]",
                            "value": "AE"
                        }
                    ]
                }
            ]
        },
        "limit": 0,
        "aggregations": [
            {
                "type": "group_by",
                "column": "company.basic_info.company_id",
                "agg": "count",
                "size": 500
            }
        ]
    }
    ```
  </Step>

  <Step title="Intersect the company ids client-side">
    ```python theme={"theme":"vitesse-black"}
    engineering_ids = {b["key"] for b in response_1["aggregations"][0]["buckets"]}
    ae_ids = {b["key"] for b in response_2["aggregations"][0]["buckets"]}

    both = engineering_ids & ae_ids
    ```
  </Step>
</Steps>

### Mid-market companies indexing SDR listings

Combine an inclusive headcount range with keyword search on the title field.

```json theme={"theme":"vitesse-black"}
{
    "filters": {
        "op": "and",
        "conditions": [
            { "field": "company.headcount.total", "type": "=>", "value": 51 },
            { "field": "company.headcount.total", "type": "=<", "value": 500 },
            {
                "field": "metadata.date_added",
                "type": "=>",
                "value": "2025-01-01"
            },
            {
                "op": "or",
                "conditions": [
                    {
                        "field": "job_details.title",
                        "type": "(.)",
                        "value": "Sales Development Representative"
                    },
                    {
                        "field": "job_details.title",
                        "type": "[.]",
                        "value": "SDR"
                    },
                    {
                        "field": "job_details.title",
                        "type": "(.)",
                        "value": "Business Development Representative"
                    }
                ]
            }
        ]
    },
    "fields": [
        "crustdata_job_id",
        "job_details.title",
        "company.basic_info.crustdata_company_id",
        "company.basic_info.name",
        "company.basic_info.primary_domain",
        "company.headcount.total",
        "location.raw",
        "metadata.date_added"
    ],
    "sorts": [{ "column": "metadata.date_added", "order": "desc" }],
    "limit": 50
}
```

### Companies that closed a Series B between two dates and are indexing new listings

```json theme={"theme":"vitesse-black"}
{
    "filters": {
        "op": "and",
        "conditions": [
            {
                "field": "company.funding.last_round_type",
                "type": "=",
                "value": "series_b"
            },
            {
                "field": "company.funding.last_fundraise_date",
                "type": "=>",
                "value": "2025-01-01"
            },
            {
                "field": "company.funding.last_fundraise_date",
                "type": "<",
                "value": "2025-07-01"
            },
            {
                "field": "metadata.date_added",
                "type": "=>",
                "value": "2025-01-01"
            }
        ]
    },
    "fields": [
        "job_details.title",
        "company.basic_info.crustdata_company_id",
        "company.basic_info.name",
        "company.basic_info.primary_domain",
        "company.funding.last_round_type",
        "company.funding.last_fundraise_date",
        "company.funding.total_investment_usd"
    ],
    "sorts": [
        { "column": "company.funding.last_fundraise_date", "order": "desc" }
    ],
    "limit": 100
}
```

### Hiring volume by workplace type in the United States

<Warning>
  **Country values are not normalized.** `location.country` can appear as
  `"USA"`, `"United States"`, or `"United States of America"`. The `in` array
  below covers the three most common forms, but for full coverage you should
  first run a `group_by` on `location.country` and collect the exact bucket
  keys present in your dataset slice.
</Warning>

```json theme={"theme":"vitesse-black"}
{
    "filters": {
        "op": "and",
        "conditions": [
            {
                "field": "location.country",
                "type": "in",
                "value": ["USA", "United States", "United States of America"]
            },
            {
                "field": "metadata.date_added",
                "type": "=>",
                "value": "2025-01-01"
            },
            {
                "field": "metadata.date_added",
                "type": "<",
                "value": "2026-01-01"
            }
        ]
    },
    "limit": 0,
    "aggregations": [
        {
            "type": "group_by",
            "column": "job_details.workplace_type",
            "agg": "count",
            "size": 10
        }
    ]
}
```

### Full-text keyword hunt in job descriptions

```json theme={"theme":"vitesse-black"}
{
    "filters": {
        "op": "and",
        "conditions": [
            {
                "field": "content.description",
                "type": "(.)",
                "value": "kubernetes"
            },
            {
                "field": "metadata.date_added",
                "type": "=>",
                "value": "2025-01-01"
            }
        ]
    },
    "fields": [
        "job_details.title",
        "company.basic_info.name",
        "location.raw",
        "metadata.date_added"
    ],
    "sorts": [{ "column": "metadata.date_added", "order": "desc" }],
    "limit": 20
}
```

***

## Errors

| Status | Envelope shape                                               | Meaning                                                                                                                                                                                                                             |
| ------ | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `400`  | `{ "error": { "type", "message", "metadata" } }`             | Invalid request — unsupported filter column, unsupported aggregation column, `limit` out of range, or malformed body. `error.type` is `invalid_request` for validation failures and `internal_error` for unsupported-column checks. |
| `401`  | `{ "message": "..." }` (flat — **not** the `error` envelope) | Unauthorized — the `Authorization` header is missing, malformed, or contains an invalid API key.                                                                                                                                    |
| `500`  | `{ "error": { "type", "message", "metadata" } }`             | Internal server error — retry after a short delay.                                                                                                                                                                                  |

<Warning>
  `401` uses a **different** response shape than `400`/`500`. Parse the
  response based on HTTP status: `401` is a flat `{ "message": ... }`,
  every other 4xx/5xx is the nested `{ "error": { "type", "message", "metadata" } }` envelope.
</Warning>

<CodeGroup>
  ```json 400 — Unsupported filter column theme={"theme":"vitesse-black"}
  {
      "error": {
          "type": "internal_error",
          "message": "Unsupported columns in conditions: ['invalid_field']",
          "metadata": []
      }
  }
  ```

  ```json 400 — Unsupported group_by column theme={"theme":"vitesse-black"}
  {
      "error": {
          "type": "internal_error",
          "message": "Unsupported aggregation column: 'company.basic_info.name'. Supported: company.basic_info.company_id, company.basic_info.industries, company.basic_info.primary_domain, company.funding.last_round_type, company.headcount.range, company.locations.country, job_details.category, job_details.title, job_details.workplace_type, location.country",
          "metadata": []
      }
  }
  ```

  ```json 400 — limit out of range theme={"theme":"vitesse-black"}
  {
      "error": {
          "type": "invalid_request",
          "message": "1 validation error for JobSearchRequest\nlimit\n  Input should be less than or equal to 1000 [type=less_than_equal, input_value=5000, input_type=int]",
          "metadata": []
      }
  }
  ```

  ```json 401 — Invalid API key theme={"theme":"vitesse-black"}
  {
      "message": "Invalid API key in request"
  }
  ```
</CodeGroup>

***

## What's next

* **Review the public Jobs quickstart** — see [Jobs Search API](/job-docs/quickstart).
* **Reuse the inline recipes on this page** — jump to [Example queries](#example-queries).
* **Inspect the full schema** — read the [OpenAPI reference](/openapi-specs/2025-11-01/introduction).
