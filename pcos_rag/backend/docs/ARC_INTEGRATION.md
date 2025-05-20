# ARC Institute Integration

This document provides information about the ARC Institute tools integration in the PCOS Research RAG system.

## Available Endpoints

### 1. Sequence Analysis/Generation

**Endpoint:** `POST /api/v1/arc/sequence`

Analyze or generate DNA/RNA sequences using ARC's Evo 2 model.

**Request Body:**
```json
{
  "sequence": "ATCG...",
  "task": "generate",
  "max_length": 100,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "generated_sequence": "...",
    "metadata": {}
  }
}
```

### 2. Guide RNA Design

**Endpoint:** `GET /api/v1/arc/guides/{transcript_id}`

Get optimized guide RNAs for a specific transcript.

**Parameters:**
- `transcript_id`: Ensembl transcript ID (e.g., "ENST00000...")
- `species`: Species (default: "human")
- `top_n`: Number of top guides to return (default: 5)

**Response:**
```json
{
  "status": "success",
  "data": {
    "transcript_id": "ENST00000...",
    "guides": [
      {
        "sequence": "...",
        "efficiency_score": 0.95,
        "off_target_score": 0.02
      }
    ]
  }
}
```

### 3. Single-Cell Atlas Query

**Endpoint:** `POST /api/v1/arc/single-cell`

Query single-cell transcriptomic data from the ARC atlas.

**Request Body:**
```json
{
  "cell_types": ["theca", "granulosa"],
  "condition": "pcos",
  "include_control": true,
  "min_cells": 10
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "cell_type": "theca",
        "condition": "pcos",
        "differentially_expressed_genes": [
          {
            "gene": "CYP17A1",
            "log2_fold_change": 2.3,
            "p_value": 1e-5,
            "q_value": 0.001
          }
        ]
      }
    ]
  }
}
```

## Setup

1. Get an API key from [ARC Institute](https://arcinstitute.org/developers)
2. Add the API key to your `.env` file:
   ```
   ARC_API_KEY=your-api-key-here
   ```

## Error Handling

All endpoints return appropriate HTTP status codes and error messages in the following format:

```json
{
  "detail": "Error message describing the issue"
}
```

## Rate Limiting

Please be aware that the ARC API may have rate limits. The client includes automatic retry logic for rate-limited requests.

## Support

For issues with the ARC integration, please contact the ARC Institute support team or open an issue in our GitHub repository.
