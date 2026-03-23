# Mem0 Service — Architecture

## Overview
Self-hosted Mem0 memory service running on Railway. Phase 1: vector memory only using Qdrant.
No Neo4j graph layer — that's Phase 2 if/when needed.

## Services
| Service | Platform | Purpose |
|---------|----------|---------|
| Qdrant | Railway (template) | Vector database for memory embeddings |
| Mem0 API | Railway (GitHub deploy) | FastAPI server wrapping mem0ai library |

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check — returns {"status": "ok"} |
| POST | /memory/add | Add a memory (body: content, user_id, metadata?) |
| POST | /memory/search | Semantic search (body: query, user_id, limit?) |
| DELETE | /memory/{memory_id} | Delete a specific memory |
| GET | /memory/list/{user_id} | List all memories for a user |

## Authentication
All endpoints (except /health) require `Authorization: Bearer <MEM0_API_KEY>` header.
MEM0_API_KEY is a random string set in Railway environment variables.

## Environment Variables
| Variable | Required | Source |
|----------|----------|--------|
| OPENAI_API_KEY | Yes | OpenAI dashboard |
| QDRANT_URL | Yes | Railway Qdrant internal URL |
| QDRANT_API_KEY | Yes | Railway Qdrant service |
| MEM0_API_KEY | No | Self-generated random string |
| PORT | Auto | Railway sets this |

## How Other Services Connect
1. Set `MEM0_URL` env var to the Mem0 service internal Railway URL
2. Set `MEM0_API_KEY` env var to the same key used by this service
3. Copy `memory_utils.py` into the project or install as dependency
4. Use: `from memory_utils import remember, recall`

## system_id Namespaces
Each project uses a unique system_id to namespace its memories:
- `og_deal_scout` — OG Deal Scout deal analysis
- `seykota_machine` — Seykota Machine trading signals
- `readydocsco_production` — ReadyDocsCo Etsy store
- `cre_distress` — CRE distress pipeline

## Data Flow
```
Other Services → HTTP → Mem0 API → mem0ai → Qdrant (vectors)
                                  → OpenAI (embeddings)
```
