# Mem0 Service — CLAUDE.md
# FIRST: Read C:/Users/micha/Desktop/_master_docs/WORKING_PHILOSOPHY.md

## What This Is
Mem0 self-hosted memory service on Railway. Phase 1: vector memory only (Qdrant).
No Neo4j graph layer — that's Phase 2.

## Architecture
- Qdrant vector database (Railway managed service)
- FastAPI server wrapping mem0ai library
- Both in same Railway project as OG Deal Scout + Seykota Machine

## Endpoints
- GET  /health — returns {"status": "ok"}
- POST /memory/add — add a memory (body: content, user_id)
- POST /memory/search — semantic search (body: query, user_id, limit)
- DELETE /memory/{memory_id} — delete specific memory
- GET  /memory/list/{user_id} — list all memories for user

## Environment Variables (set in Railway dashboard BEFORE deploy)
- OPENAI_API_KEY — for embeddings
- QDRANT_URL — internal Railway URL for Qdrant service
- QDRANT_API_KEY — from Qdrant Railway service
- MEM0_API_KEY — random string for auth (we generate this)
- PORT — Railway sets this automatically

## system_id Namespaces
- og_deal_scout
- seykota_machine
- readydocsco_production
- cre_distress

## Deployment
- GitHub repo: mem0-service (UncleMike1988)
- Railway auto-deploys from main branch
- Shell form CMD in Dockerfile — never JSON array

## Key Files
- main.py — FastAPI app
- config.py — env var loader
- memory_utils.py — shared client utility for other projects
- Dockerfile — uses python:3.11-slim base
- railway.json — Railway build/deploy config
