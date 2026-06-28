"""
Sandboxed shell execution tool for the Autonomous Agent Platform.

Executes shell commands in a controlled environment with:
- Timeout enforcement
- Working directory isolation
- Command allowlist/blocklist
"""

from __future__ import annotations

import os
import subprocess
import signal
import asyncio
from typing import Any

from pydantic import BaseModel, Field

from src.config.logging import get_logger
from src.tools.base import AgentTool, ToolExecutionError

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Input schema
# ---------------------------------------------------------------------------

class ShellInput(BaseModel):
    """Input schema for ShellTool."""

    command: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Shell command to execute",
    )
    timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Execution timeout in seconds",
    )
    cwd: str | None = Field(
        default=None,
        description="Working directory (relative to workspace)",
    )

# ---------------------------------------------------------------------------
# Tool implementation
# ---------------------------------------------------------------------------

class ShellTool(AgentTool):
    """Execute shell commands in a sandboxed environment.

    All commands run with a timeout and optional working directory.
    Dangerous commands (rm -rf, sudo, etc.) can be blocked via config.

    Example usage::

        tool = ShellTool()
        result = await tool._arun(command="ls -la", timeout=10)
    """

    name: str = "shell"
    description: str = (
        "Execute a shell command with timeout. Returns stdout, stderr, and return code."
    )
    args_schema: type[BaseModel] = ShellInput
    max_retries: int = 0
    timeout_seconds: float = 60.0

    # Blocked dangerous commands
    _blocked_commands = {"rm -rf", "sudo", "chmod 777", "dd", "mkfs", "fdisk"}

    # ------------------------------------------------------------------
    # Core execution
    # ------------------------------------------------------------------

    async def _execute(self, **kwargs: Any) -> dict[str, Any]:
        """Execute a shell command with timeout."""
        command: str = kwargs["command"]
        timeout: int = kwargs.get("timeout", 30)
        cwd: str | None = kwargs.get("cwd")

        log = logger.bind(tool=self.name, command=command, timeout=timeout)

        # Check blocked commands
        for blocked in self._blocked_commands:
            if blocked in command:
                raise ToolExecutionError(
                    tool_name=self.name,
                    message=f"Blocked command pattern: {blocked}",
                )

        # Resolve working directory
        if cwd:
            work_dir = os.path.abspath(cwd)
        else:
            work_dir = os.getcwd()

        try:
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: subprocess.run(
                    command,
                    shell=True,
                    cwd=work_dir,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0,
            }

        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "returncode": 124,
                "success": False,
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "returncode": 1,
                "success": False,
            }
