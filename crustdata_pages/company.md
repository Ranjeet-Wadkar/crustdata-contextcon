> ## Documentation Index
> Fetch the complete documentation index at: https://docs.crustdata.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Company APIs

> Find, enrich, and analyze company records with the Crustdata Company APIs.

The Company APIs help you answer practical business questions: Which companies match your target market? What does this company look like before outreach? What are the valid filter values for my search?

There are four core endpoints, each designed for a different step in your workflow.

| API                                        | What it does                                                | Best for                                            |
| ------------------------------------------ | ----------------------------------------------------------- | --------------------------------------------------- |
| [Search](/company-docs/search)             | Find companies matching structured filters                  | Building lists, market scans, segmentation          |
| [Autocomplete](/company-docs/autocomplete) | Discover valid field values for search filters              | Building filter dropdowns, validating filter inputs |
| [Enrich](/company-docs/enrichment)         | Get a detailed company profile from a known identifier      | Research, scoring, personalization                  |
| [Identify](/company-docs/identify)         | Resolve a company from partial info (name, domain, URL, ID) | CRM deduplication, lead routing, entity resolution  |

## At a glance

|                     | Search                                               | Autocomplete                   | Enrich                           | Identify                         |
| ------------------- | ---------------------------------------------------- | ------------------------------ | -------------------------------- | -------------------------------- |
| **Endpoint**        | `/company/search`                                    | `/company/search/autocomplete` | `/company/enrich`                | `/company/identify`              |
| **Data source**     | Crustdata indexed                                    | Crustdata indexed              | Crustdata indexed                | Crustdata indexed                |
| **Purpose**         | Find companies by filters                            | Discover valid filter values   | Get full company profile         | Match partial info to a company  |
| **Filter syntax**   | `{ "field": "dotpath", "type": "op", "value": ... }` | Optional `filters` param       | N/A                              | N/A                              |
| **Pagination**      | Cursor-based                                         | —                              | —                                | —                                |
| **Field selection** | `fields` = dot-paths or sections                     | —                              | `fields` = dot-paths or sections | `fields` = dot-paths or sections |
| **Error codes**     | `400`, `401`, `403`, `500`                           | `400`, `401`, `500`            | `400`, `401`, `403`, `500`       | `400`, `401`, `403`, `500`       |

***

## Before you start

You need:

* A Crustdata API key
* A terminal with `curl` (or any HTTP client)
* The required header: `x-api-version: 2025-11-01`

All requests use **Bearer token authentication** and require the API version header:

```bash theme={"theme":"vitesse-black"}
--header 'authorization: Bearer YOUR_API_KEY'
--header 'x-api-version: 2025-11-01'
```

<Note>Replace `YOUR_API_KEY` in each example with your actual API key.</Note>

<Note>
  **Convention used in these docs:** Information labeled "OpenAPI contract"
  reflects the formal API specification. Information labeled "Current platform
  behavior" (such as rate limits, credit costs, and max page ranges) describes
  observed behavior that may change. See the [API
  reference](/openapi-specs/2025-11-01/introduction) for the formal OpenAPI
  spec.
</Note>

***

## Quickstart: enrich a company from a domain

The fastest way to get started is to enrich a company from its website domain. This single request returns the full company profile.

<CodeGroup>
  ```bash Request theme={"theme":"vitesse-black"}
  curl --request POST \
    --url https://api.crustdata.com/company/enrich \
    --header 'authorization: Bearer YOUR_API_KEY' \
    --header 'content-type: application/json' \
    --header 'x-api-version: 2025-11-01' \
    --data '{
      "domains": ["retool.com"]
    }'
  ```

  ```json Response theme={"theme":"vitesse-black"}
  {
      "results": [
          {
              "matched_on": "retool.com",
              "match_type": "domain",
              "matches": [
                  {
                      "confidence_score": 1.0,
                      "company_data": {
                          "basic_info": {
                              "name": "Retool",
                              "primary_domain": "retool.com",
                              "website": "https://retool.com/",
                              "company_type": "Privately Held",
                              "year_founded": "2017-01-01",
                              "employee_count_range": "201-500",
                              "industries": [
                                  "Software Development",
                                  "Technology, Information and Internet"
                              ]
                          }
                      }
                  }
              ]
          }
      ]
  }
  ```
</CodeGroup>

<Note>
  Response trimmed for clarity. The full response includes headcount, funding,
  hiring, competitors, and more.
</Note>

The response is an object with a `results` array — one entry per identifier you submitted:

* **`matched_on`** — the input you sent (`retool.com`).
* **`match_type`** — which identifier type was used (`domain`, `name`, `crustdata_company_id`, or `professional_network_profile_url`).
* **`confidence_score`** — how confident the match is (`1.0` = exact match).
* **`company_data`** — the full company profile, including `basic_info`, `headcount`, `funding`, `locations`, `taxonomy`, and more.

***

## Which API should you start with?

| If you want to...                                              | Start with                                 |
| -------------------------------------------------------------- | ------------------------------------------ |
| Build a target account list by geography, industry, or funding | [Search](/company-docs/search)             |
| Discover valid filter values before building search queries    | [Autocomplete](/company-docs/autocomplete) |
| Get richer context for scoring, prioritization, or diligence   | [Enrich](/company-docs/enrichment)         |

## Common workflows

1. **Discovery** — Start with [Autocomplete](/company-docs/autocomplete) to find valid filter values, then [Search](/company-docs/search) to build your list, then [Enrich](/company-docs/enrichment) the top matches for full profiles.
2. **Data cleanup** — Use [Enrich](/company-docs/enrichment) with a domain to resolve ambiguous records from CRM imports.
3. **Lead routing** — [Enrich](/company-docs/enrichment) incoming domains to get a stable company ID and industry, then [Search](/company-docs/search) for similar companies.

***

## Error handling

All Company API endpoints return structured errors. The exact status codes vary by endpoint:

| Status | Meaning                                                        | Applies to               |
| ------ | -------------------------------------------------------------- | ------------------------ |
| `400`  | Invalid request (bad field, wrong operator, malformed filters) | All endpoints            |
| `401`  | Invalid or missing API key                                     | All endpoints            |
| `403`  | Permission denied or insufficient credits                      | Search, Enrich, Identify |
| `500`  | Internal server error                                          | All endpoints            |

Error response format:

```json theme={"theme":"vitesse-black"}
{
    "error": {
        "type": "invalid_request",
        "message": "Unsupported columns in conditions: ['nonexistent_field']",
        "metadata": []
    }
}
```

For `401`, the format is simpler: `{"message": "Invalid API key in request"}`.

***

## Terminology reference

These are the most common terms used across the Company APIs:

| You say        | API request field                                                   | Used in          |
| -------------- | ------------------------------------------------------------------- | ---------------- |
| Company domain | `domains`                                                           | Enrich, Identify |
| Company name   | `names`                                                             | Enrich, Identify |
| Company ID     | `crustdata_company_ids`                                             | Enrich, Identify |
| HQ country     | `locations.hq_country` (ISO3: `"USA"`, `"GBR"`)                     | Search           |
| Industry       | `taxonomy.professional_network_industry` or `basic_info.industries` | Search           |
| Employee count | `headcount.total`                                                   | Search           |
| Total funding  | `funding.total_investment_usd`                                      | Search           |

<Note>
  Search uses ISO3 country codes (`"USA"`, `"GBR"`). Use
  [Autocomplete](/company-docs/autocomplete) to discover exact values for
  indexed Search filters.
</Note>

### Company ID fields

The company data model includes two ID fields:

| Field                   | Meaning                                                                                                    | When to use                                                                                     |
| ----------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `crustdata_company_id`  | Stable Crustdata company identifier. Appears at the top level of search results and inside `company_data`. | Use this for Search → Enrich workflows. Pass it in `crustdata_company_ids` when calling Enrich. |
| `basic_info.company_id` | Internal source company identifier. May match `crustdata_company_id` but is not guaranteed to.             | Generally, prefer `crustdata_company_id` for cross-API workflows.                               |

***

## Common footguns

| Mistake                                        | Fix                                                                                                                              |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Using `"United States"` in Search              | Search uses ISO3 codes: `"USA"`, `"GBR"`. Use [Autocomplete](/company-docs/autocomplete) to discover exact values.               |
| Using `>=` or `<=` operators in Search         | Use `=>` and `=<` instead.                                                                                                       |
| Mixing identifier types in Enrich              | Send one type per request: `domains`, `names`, `crustdata_company_ids`, or `professional_network_profile_urls`.                  |
| Confusing Search `fields` with Enrich `fields` | Search `fields` are dot-path response fields (e.g., `basic_info.name`). Enrich `fields` are section groups (e.g., `basic_info`). |
| Omitting `fields` in Search                    | Returns all fields per company — very large payloads. Always specify `fields` in production.                                     |

## Shared guidance

Use the endpoint pages for request/response details and no-match behavior.
For pricing, see [Pricing](/general/pricing). For rate-limit guidance, see
[Rate limits](/general/rate-limits).

***

## Next steps

* [Company Search](/company-docs/search) — find companies by domain, industry, funding, headcount, and more.
* [Company Autocomplete](/company-docs/autocomplete) — discover valid filter values before building queries.
* [Company Enrich](/company-docs/enrichment) — get detailed profiles with headcount, funding, hiring, and competitors.
* [Company Identify](/company-docs/identify) — resolve partial company info to a known entity.
* [Company Examples](/company-docs/examples) — ready-to-copy patterns for common use cases.
