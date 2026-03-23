"""Shared memory utility for all projects to import.

Usage from any project:
    from memory_utils import remember, recall
    remember("User prefers daily summaries", "og_deal_scout")
    results = recall("user preferences", "og_deal_scout")
"""

import os
import requests


def get_base_url() -> str:
    url = os.getenv("MEM0_URL")
    if not url:
        raise RuntimeError("MEM0_URL environment variable not set")
    return url.rstrip("/")


def get_headers() -> dict:
    api_key = os.getenv("MEM0_API_KEY", "")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def remember(content: str, system_id: str, metadata: dict = None):
    url = f"{get_base_url()}/memory/add"
    payload = {"content": content, "user_id": system_id}
    if metadata:
        payload["metadata"] = metadata
    resp = requests.post(url, json=payload, headers=get_headers())
    resp.raise_for_status()
    return resp.json()


def recall(query: str, system_id: str, limit: int = 5) -> list:
    url = f"{get_base_url()}/memory/search"
    payload = {"query": query, "user_id": system_id, "limit": limit}
    resp = requests.post(url, json=payload, headers=get_headers())
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict) and "results" in data:
        return [r.get("memory", r) for r in data["results"]]
    return data


def list_memories(system_id: str) -> list:
    url = f"{get_base_url()}/memory/list/{system_id}"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()


def forget(memory_id: str):
    url = f"{get_base_url()}/memory/{memory_id}"
    resp = requests.delete(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()
