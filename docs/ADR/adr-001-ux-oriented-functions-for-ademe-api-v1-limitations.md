# ADR - 0001: Handling ADEME API v1 Limitations for Filtering and Sorting

## Status
Accepted

## Context
The ADEME API (v1) used for retrieving DPE records has a significant limitation: it cannot reliably combine filtering on more than one field with sorting in a single request. When multiple filters are applied alongside sorting, the results are inconsistent and may not reflect the intended query.

## Decision
To address this limitation and provide a better user experience, we will introduce higher-level, UX-oriented functions that encapsulate the low-level API client. These functions will:
- Abstract away the API's technical constraints.
- Allow users to request complex filtering and sorting operations.
- Internally handle the logic required to deliver reliable results, possibly by post-processing data after retrieval.

## Consequences
- The API client remains a thin wrapper around the ADEME API.
- UX-oriented functions will be responsible for ensuring correct results when multiple filters and sorting are needed.
- This approach improves reliability and usability for end users, at the cost of additional processing and abstraction in the codebase.

## Alternatives Considered
- Relying solely on the API client and documenting the limitation. Rejected due to poor UX.
- Requesting API changes from ADEME. Not feasible in the short term.

## Related Issues
- ADEME API v1 documentation and known limitations.
- User feedback regarding filtering and sorting reliability.
****