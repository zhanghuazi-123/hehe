"""CLI command implementations for Bailongma."""

import json
import time
from typing import Optional

from ..core.client import BailongmaClient


def _client(base_url: str, token: Optional[str]) -> BailongmaClient:
    return BailongmaClient(base_url=base_url, token=token)


def cmd_message(base_url: str, token: Optional[str], content: str, from_id: str, channel: str) -> dict:
    """Send a message to the Bailongma agent."""
    body = {"content": content, "channel": channel}
    if from_id:
        body["from_id"] = from_id
    return _client(base_url, token).post("/message", body)


def cmd_status(base_url: str, token: Optional[str]) -> dict:
    """Get system status."""
    return _client(base_url, token).get("/status")


def cmd_quota(base_url: str, token: Optional[str]) -> dict:
    """Get LLM quota status."""
    return _client(base_url, token).get("/quota")


def cmd_activation_status(base_url: str, token: Optional[str]) -> dict:
    """Get activation status."""
    return _client(base_url, token).get("/activation-status")


def cmd_agent_profile(base_url: str, token: Optional[str]) -> dict:
    """Get agent profile."""
    return _client(base_url, token).get("/agent-profile")


def cmd_memories(base_url: str, token: Optional[str], limit: int = 20, search: Optional[str] = None) -> dict:
    """List or search memories."""
    params = f"?limit={min(limit, 100)}"
    if search:
        params += f"&search={search}"
    return _client(base_url, token).get(f"/memories{params}")


def cmd_memory_update(base_url: str, token: Optional[str], memory_id: int, content: Optional[str] = None, detail: Optional[str] = None) -> dict:
    """Update a memory."""
    body = {}
    if content is not None:
        body["content"] = content
    if detail is not None:
        body["detail"] = detail
    return _client(base_url, token).patch(f"/memories/{memory_id}", body)


def cmd_memory_delete(base_url: str, token: Optional[str], memory_id: int) -> dict:
    """Delete a memory."""
    return _client(base_url, token).delete(f"/memories/{memory_id}")


def cmd_conversations(base_url: str, token: Optional[str], limit: int = 60) -> dict:
    """Get recent conversations."""
    return _client(base_url, token).get(f"/conversations?limit={min(limit, 500)}")


def cmd_admin_stop(base_url: str, token: Optional[str]) -> dict:
    """Pause the consciousness loop."""
    return _client(base_url, token).post("/admin/stop")


def cmd_admin_start(base_url: str, token: Optional[str]) -> dict:
    """Resume the consciousness loop."""
    return _client(base_url, token).post("/admin/start")


def cmd_admin_restart(base_url: str, token: Optional[str]) -> dict:
    """Restart the process."""
    return _client(base_url, token).post("/admin/restart")


def cmd_admin_reset_memories(base_url: str, token: Optional[str]) -> dict:
    """Reset all memories and conversations."""
    return _client(base_url, token).post("/admin/reset-memories")


def cmd_admin_reset_files(base_url: str, token: Optional[str]) -> dict:
    """Clear sandbox files."""
    return _client(base_url, token).post("/admin/reset-files")


def cmd_settings(base_url: str, token: Optional[str]) -> dict:
    """Get LLM settings."""
    return _client(base_url, token).get("/settings")


def cmd_settings_model(base_url: str, token: Optional[str], model: str) -> dict:
    """Switch LLM model."""
    return _client(base_url, token).post("/settings/model", {"model": model})


def cmd_media_history(base_url: str, token: Optional[str], limit: int = 30) -> dict:
    """Get media playback history."""
    return _client(base_url, token).get(f"/media/history?limit={min(limit, 100)}")


def cmd_hotspots(base_url: str, token: Optional[str], refresh: bool = False) -> dict:
    """Get hotspot data."""
    params = f"?refresh={'true' if refresh else 'false'}"
    return _client(base_url, token).get(f"/hotspots{params}")


def cmd_system_prompt(base_url: str, token: Optional[str]) -> str:
    """Get system prompt preview."""
    return _client(base_url, token).get("/system-prompt-preview", raw=True)


def cmd_activate(base_url: str, token: Optional[str], api_key: str, provider: Optional[str] = None, model: Optional[str] = None) -> dict:
    """Activate LLM with new API credentials."""
    body = {"apiKey": api_key}
    if provider:
        body["provider"] = provider
    if model:
        body["model"] = model
    return _client(base_url, token).post("/activate", body)
