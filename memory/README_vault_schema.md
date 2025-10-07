# Memory Vault JSONL Schema (append-only)
Each line is one JSON object:
{
  "ts": "2025-09-29T12:34:56Z",
  "type": "identity|skill|project|note|task|link",
  "persona": "river",
  "tags": ["telegram","audiobooks"],
  "text": "Short fact or association to recall later",
  "source": "/opt/sanctuary/memories/…/file.md#L120"
}
