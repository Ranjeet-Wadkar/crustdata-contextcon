> ## Documentation Index
> Fetch the complete documentation index at: https://docs.crustdata.com/llms.txt
> Use this file to discover all available pages before exploring further.

# Person APIs

> Find, enrich, and analyze people with the Crustdata Person APIs.

The Person APIs help you answer practical questions about people: Who are the decision-makers at a target company? What does this person's professional background look like? Can I find people by name, title, location, or employer? Can I enrich a person from a profile URL or business email?

Start with the indexed endpoints for most workflows, then use the live endpoints when you need fresh results from the web.

| API                                       | What it does                                       | Best for                                            |
| ----------------------------------------- | -------------------------------------------------- | --------------------------------------------------- |
| [Search](/person-docs/search)             | Find people matching structured filters            | Prospecting, talent sourcing, market mapping        |
| [Enrich](/person-docs/enrichment)         | Get a detailed profile from a profile URL or email | Outreach prep, due diligence, profile building      |
| [Autocomplete](/person-docs/autocomplete) | Discover valid field values for search filters     | Building filter dropdowns, validating filter inputs |

### Enterprise live endpoints

| API                                          | What it does                              | Access      |
| -------------------------------------------- | ----------------------------------------- | ----------- |
| [Live Search 🔒](https://crustdata.com/demo) | Search people in real time from the web   | Book a demo |
| [Live Enrich 🔒](https://crustdata.com/demo) | Fetch a fresh person profile from the web | Book a demo |

## At a glance

|                     | Search                                               | Autocomplete                  | Enrich                                 |
| ------------------- | ---------------------------------------------------- | ----------------------------- | -------------------------------------- |
| **Endpoint**        | `/person/search`                                     | `/person/search/autocomplete` | `/person/enrich`                       |
| **Data source**     | Crustdata indexed                                    | Crustdata indexed             | Crustdata indexed                      |
| **Purpose**         | Find people by filters                               | Discover valid filter values  | Get full person profile                |
| **Filter syntax**   | `{ "field": "dotpath", "type": "op", "value": ... }` | Optional `filters` param      | N/A                                    |
| **Pagination**      | Cursor-based                                         | —                             | —                                      |
| **Field selection** | `fields` = dot-paths                                 | —                             | `fields` = dot-paths or section groups |
| **Error codes**     | `400`, `401`, `403`, `500`                           | `400`, `401`, `500`           | `400`, `401`, `403`, `404`, `500`      |

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

## Quickstart: enrich a person from a profile URL

The fastest way to get started is to enrich a person from their profile URL. This single request returns the full person profile from the Crustdata cache.

<CodeGroup>
  ```bash Request theme={"theme":"vitesse-black"}
  curl --request POST \
    --url https://api.crustdata.com/person/enrich \
    --header 'authorization: Bearer YOUR_API_KEY' \
    --header 'content-type: application/json' \
    --header 'x-api-version: 2025-11-01' \
    --data '{
      "professional_network_profile_urls": [
        "https://www.linkedin.com/in/abhilashchowdhary"
      ]
    }'
  ```

  ```json Response theme={"theme":"vitesse-black"}
  [
      {
          "matched_on": "https://www.linkedin.com/in/abhilashchowdhary",
          "match_type": "professional_network_profile_url",
          "matches": [
              {
                  "confidence_score": 1.0,
                  "person_data": {
                      "basic_profile": {
                          "name": "Abhilash Chowdhary",
                          "headline": "Co-founder at Crustdata (YC F24)",
                          "current_title": "Co-Founder & CEO",
                          "location": {
                              "raw": "San Francisco, California, United States"
                          }
                      }
                  }
              }
          ]
      }
  ]
  ```
</CodeGroup>

<Note>
  Response trimmed for clarity. The full response can include employment
  history, education, skills, contact data, and developer platform profiles.
</Note>

The response is an array — one entry per identifier you submitted:

* **`matched_on`** — the input you sent (for example, `https://www.linkedin.com/in/abhilashchowdhary`).
* **`match_type`** — which identifier type was used (`professional_network_profile_url` or `business_email`).
* **`confidence_score`** — how confident the match is (`1.0` = exact match).
* **`person_data`** — the full person profile, including `basic_profile`, `experience`, `education`, `skills`, `contact`, `social_handles`, and more.

***

## Which API should you start with?

| If you want to...                                           | Start with                                   |
| ----------------------------------------------------------- | -------------------------------------------- |
| Find people by name, title, company, or location            | [Search](/person-docs/search)                |
| Get full profile details for a known profile URL            | [Enrich](/person-docs/enrichment)            |
| Reverse-lookup a person from a business email               | [Enrich](/person-docs/enrichment)            |
| Discover valid filter values before building search queries | [Autocomplete](/person-docs/autocomplete)    |
| Build a list of decision-makers at target companies         | [Search](/person-docs/search)                |
| Search people in real time from the web                     | [Live Search 🔒](https://crustdata.com/demo) |
| Fetch fresh profile data from the web                       | [Live Enrich 🔒](https://crustdata.com/demo) |

## Common workflows

1. **Discovery** — Start with [Autocomplete](/person-docs/autocomplete) to find valid filter values (e.g., title variations), then [Search](/person-docs/search) to build your list, then [Enrich](/person-docs/enrichment) the top matches for full profiles.
2. **Data cleanup** — Use [Enrich](/person-docs/enrichment) with `business_emails` to resolve person profiles and fill in missing professional context from CRM imports.
3. **Lead routing** — [Enrich](/person-docs/enrichment) incoming profile URLs to get a stable person profile, then [Search](/person-docs/search) for similar people at the same company or with the same title.

***

## Error handling

All Person API endpoints return structured errors. The exact status codes vary by endpoint:

| Status | Meaning                                                        | Applies to     |
| ------ | -------------------------------------------------------------- | -------------- |
| `400`  | Invalid request (bad field, wrong operator, malformed filters) | All endpoints  |
| `401`  | Invalid or missing API key                                     | All endpoints  |
| `403`  | Permission denied or insufficient credits                      | Search, Enrich |
| `404`  | No data found (per spec)                                       | Enrich         |
| `500`  | Internal server error                                          | All endpoints  |

Error response format:

```json theme={"theme":"vitesse-black"}
{
    "error": {
        "type": "invalid_request",
        "message": "Unsupported filter field: 'current_title'. Supported fields: ['basic_profile.name', 'basic_profile.headline', ...]",
        "metadata": []
    }
}
```

For `401`, the format is simpler: `{"message": "Invalid API key in request"}`.

### No-match behavior

| Endpoint     | No matches found                   | Action                                     |
| ------------ | ---------------------------------- | ------------------------------------------ |
| Search       | `200` with empty `profiles: []`    | Broaden filters or check with Autocomplete |
| Enrich       | `200` with empty `matches: []`     | Try a different identifier type            |
| Autocomplete | `200` with empty `suggestions: []` | Try a broader query                        |

<Note>
  The OpenAPI spec defines `404` for Enrich, but current behavior typically
  returns `200` with empty `matches`. Handle both.
</Note>

### Retry guidance

| Status | Retry? | Action                           |
| ------ | ------ | -------------------------------- |
| `400`  | No     | Fix the request                  |
| `401`  | No     | Check API key                    |
| `403`  | No     | Check permissions/credits        |
| `404`  | No     | Try different identifier         |
| `500`  | Yes    | Exponential backoff (1s, 2s, 4s) |

***

## Terminology reference

These are the most common terms used across the Person APIs:

| You say         | API request field                                                   | Used in              |
| --------------- | ------------------------------------------------------------------- | -------------------- |
| Profile URL     | `professional_network_profile_urls`                                 | Enrich               |
| Business email  | `business_emails`                                                   | Enrich               |
| Person name     | `basic_profile.name` (filter field)                                 | Search, Autocomplete |
| Job title       | `experience.employment_details.current.title` (filter field)        | Search, Autocomplete |
| Current company | `experience.employment_details.current.company_name` (filter field) | Search, Autocomplete |
| Headline        | `basic_profile.headline` (filter field)                             | Search, Autocomplete |
| Location        | `basic_profile.location` (filter field)                             | Search               |

<Note>
  Search uses dot-path field names like
  `experience.employment_details.current.title`. Use Autocomplete to discover
  exact values for indexed Search filters before you build queries.
</Note>

***

## Common footguns

| Mistake                                           | Fix                                                                                         |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Using `column` in Search filters                  | The correct key is `field` (e.g., `"field": "basic_profile.name"`).                         |
| Mixing identifier types in Enrich                 | Send one type per request: either `professional_network_profile_urls` or `business_emails`. |
| Using `current_title` as a filter field in Search | Use the full dot-path: `experience.employment_details.current.title`.                       |
| Omitting `fields` in Search                       | Returns all fields per person — very large payloads. Always specify `fields` in production. |
| Expecting `results` wrapper in Enrich response    | Enrich returns a top-level array, not `{ "results": [...] }`.                               |

***

## Next steps

* [Person Search](/person-docs/search) — find people by name, title, company, location, and more with advanced filters.
* [Person Autocomplete](/person-docs/autocomplete) — discover valid filter values before building queries.
* [Person Enrich](/person-docs/enrichment) — get detailed profiles from profile URLs or business emails, with batch support.
* [Live Search 🔒](https://crustdata.com/demo) — search people in real time from the web.
* [Live Enrich 🔒](https://crustdata.com/demo) — fetch a fresh person profile from the web.
* [Person Examples](/person-docs/examples) — ready-to-copy workflow patterns.
