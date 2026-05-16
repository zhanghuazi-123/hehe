#!/usr/bin/env python3
"""Hehe CLI - Control the AI consciousness experiment framework from the command line.

Usage:
  hehe message "Hello"
  hehe status
  hehe memory list --limit 10
  hehe admin stop
  hehe settings show
  hehe                            # enter REPL mode
"""

import json
import sys
import os
from typing import Optional

import click

from .core.commands import (
    cmd_message, cmd_status, cmd_quota, cmd_activation_status,
    cmd_agent_profile, cmd_memories, cmd_memory_update, cmd_memory_delete,
    cmd_conversations, cmd_admin_stop, cmd_admin_start, cmd_admin_restart,
    cmd_admin_reset_memories, cmd_admin_reset_files,
    cmd_settings, cmd_settings_model,
    cmd_media_history, cmd_hotspots, cmd_system_prompt, cmd_activate,
)


def _get_base_url() -> str:
    return os.environ.get("BAILONGMA_URL", "http://127.0.0.1:3721")

def _get_token() -> Optional[str]:
    return os.environ.get("BAILONGMA_TOKEN") or None

def _print_json(data):
    click.echo(json.dumps(data, indent=2, ensure_ascii=False, default=str))

def _handle_result(result):
    if isinstance(result, (dict, list)):
        _print_json(result)
    else:
        click.echo(str(result))


@click.group(invoke_without_command=True)
@click.option("--base-url", envvar="BAILONGMA_URL", default="http://127.0.0.1:3721", help="Hehe API base URL")
@click.option("--token", envvar="BAILONGMA_TOKEN", default=None, help="API auth token")
@click.option("--json", "json_mode", is_flag=True, help="Force JSON output")
@click.pass_context
def cli(ctx, base_url, token, json_mode):
    """Hehe CLI - AI consciousness experiment framework."""
    ctx.ensure_object(dict)
    ctx.obj["base_url"] = base_url
    ctx.obj["token"] = token
    ctx.obj["json_mode"] = json_mode

    if ctx.invoked_subcommand is None:
        _enter_repl(ctx)


def _enter_repl(ctx):
    """Interactive REPL mode."""
    import code
    from .core.client import HeheClient

    client = HeheClient(base_url=ctx.obj["base_url"], token=ctx.obj["token"])
    banner = f"""
╔══════════════════════════════════════════╗
║         Hehe CLI REPL              ║
║  {ctx.obj['base_url']:38} ║
╚══════════════════════════════════════════╝

Quick commands:
  client.get('/status')
  client.post('/message', {{'content':'hello'}})
  client.get('/memories?limit=10')

Type exit() or Ctrl+D to quit.
"""
    local_vars = {
        "client": client,
        "status": lambda: _print_json(client.get("/status")),
        "msg": lambda text: _print_json(client.post("/message", {"content": text})),
        "mem": lambda limit=10: _print_json(client.get(f"/memories?limit={limit}")),
        "conv": lambda limit=10: _print_json(client.get(f"/conversations?limit={limit}")),
    }
    code.interact(banner=banner, local=local_vars)


# ─── message ────────────────────────────────────────────────

@cli.command()
@click.argument("content")
@click.option("--from-id", "-f", default="CLI", help="Sender ID")
@click.option("--channel", "-c", default="API", help="Message channel")
@click.pass_context
def message(ctx, content, from_id, channel):
    """Send a message to the Hehe agent."""
    r = cmd_message(ctx.obj["base_url"], ctx.obj["token"], content, from_id, channel)
    _handle_result(r)


# ─── status ────────────────────────────────────────────────

@cli.command()
@click.pass_context
def status(ctx):
    """Show system status (memory count, running state)."""
    _handle_result(cmd_status(ctx.obj["base_url"], ctx.obj["token"]))


@cli.command()
@click.pass_context
def quota(ctx):
    """Show LLM quota (RPM/TPM usage)."""
    _handle_result(cmd_quota(ctx.obj["base_url"], ctx.obj["token"]))


@cli.command("activation-status")
@click.pass_context
def activation_status(ctx):
    """Show whether LLM is activated."""
    _handle_result(cmd_activation_status(ctx.obj["base_url"], ctx.obj["token"]))


@cli.command("agent-name")
@click.pass_context
def agent_name(ctx):
    """Show agent name."""
    _handle_result(cmd_agent_profile(ctx.obj["base_url"], ctx.obj["token"]))


# ─── memory ────────────────────────────────────────────────

@cli.group()
def memory():
    """Manage memories."""
    pass


@memory.command("list")
@click.option("--limit", "-n", default=20, help="Number of memories (max 100)")
@click.option("--search", "-s", default=None, help="Search keyword")
@click.pass_context
def memory_list(ctx, limit, search):
    """List or search memories."""
    _handle_result(cmd_memories(ctx.obj["base_url"], ctx.obj["token"], limit, search))


@memory.command("update")
@click.argument("memory_id", type=int)
@click.option("--content", "-c", default=None, help="New content")
@click.option("--detail", "-d", default=None, help="New detail")
@click.pass_context
def memory_update(ctx, memory_id, content, detail):
    """Update a memory by ID."""
    _handle_result(cmd_memory_update(ctx.obj["base_url"], ctx.obj["token"], memory_id, content, detail))


@memory.command("delete")
@click.argument("memory_id", type=int)
@click.pass_context
def memory_delete(ctx, memory_id):
    """Delete a memory by ID."""
    _handle_result(cmd_memory_delete(ctx.obj["base_url"], ctx.obj["token"], memory_id))


# ─── conversation ──────────────────────────────────────────

@cli.group()
def conversation():
    """Manage conversations."""
    pass


@conversation.command("list")
@click.option("--limit", "-n", default=60, help="Number of conversations (max 500)")
@click.pass_context
def conversation_list(ctx, limit):
    """List recent conversations."""
    _handle_result(cmd_conversations(ctx.obj["base_url"], ctx.obj["token"], limit))


# ─── admin ─────────────────────────────────────────────────

@cli.group()
def admin():
    """Admin operations (stop/start/restart/reset)."""
    pass


@admin.command("stop")
@click.pass_context
def admin_stop(ctx):
    """Pause the consciousness loop."""
    _handle_result(cmd_admin_stop(ctx.obj["base_url"], ctx.obj["token"]))


@admin.command("start")
@click.pass_context
def admin_start(ctx):
    """Resume the consciousness loop."""
    _handle_result(cmd_admin_start(ctx.obj["base_url"], ctx.obj["token"]))


@admin.command("restart")
@click.pass_context
def admin_restart(ctx):
    """Restart the process."""
    _handle_result(cmd_admin_restart(ctx.obj["base_url"], ctx.obj["token"]))


@admin.command("reset-memories")
@click.pass_context
def admin_reset_memories(ctx):
    """Reset all memories and conversations."""
    _handle_result(cmd_admin_reset_memories(ctx.obj["base_url"], ctx.obj["token"]))


@admin.command("reset-files")
@click.pass_context
def admin_reset_files(ctx):
    """Clear sandbox files."""
    _handle_result(cmd_admin_reset_files(ctx.obj["base_url"], ctx.obj["token"]))


# ─── settings ──────────────────────────────────────────────

@cli.group()
def settings():
    """View and manage settings."""
    pass


@settings.command("show")
@click.pass_context
def settings_show(ctx):
    """Show current LLM configuration."""
    _handle_result(cmd_settings(ctx.obj["base_url"], ctx.obj["token"]))


@settings.command("model")
@click.argument("model_name")
@click.pass_context
def settings_model(ctx, model_name):
    """Switch LLM model."""
    _handle_result(cmd_settings_model(ctx.obj["base_url"], ctx.obj["token"], model_name))


# ─── activate ──────────────────────────────────────────────

@cli.command()
@click.argument("api_key")
@click.option("--provider", "-p", default=None, help="LLM provider (deepseek/minimax/openai)")
@click.option("--model", "-m", default=None, help="Model name")
@click.pass_context
def activate(ctx, api_key, provider, model):
    """Activate LLM with new API credentials."""
    _handle_result(cmd_activate(ctx.obj["base_url"], ctx.obj["token"], api_key, provider, model))


# ─── misc ──────────────────────────────────────────────────

@cli.command("media-history")
@click.option("--limit", "-n", default=30, help="Number of entries")
@click.pass_context
def media_history(ctx, limit):
    """Show media playback history."""
    _handle_result(cmd_media_history(ctx.obj["base_url"], ctx.obj["token"], limit))


@cli.command()
@click.option("--refresh", is_flag=True, help="Force refresh cache")
@click.pass_context
def hotspots(ctx, refresh):
    """Show hotspot data."""
    _handle_result(cmd_hotspots(ctx.obj["base_url"], ctx.obj["token"], refresh))


@cli.command("system-prompt")
@click.pass_context
def system_prompt(ctx):
    """Show the system prompt that the agent sees."""
    _handle_result(cmd_system_prompt(ctx.obj["base_url"], ctx.obj["token"]))


# ─── entry point ───────────────────────────────────────────

def main():
    cli(obj={})


if __name__ == "__main__":
    main()
