"""
agent_state.py
==============

Defines the runtime state of an intelligent agent.

This object stores the current lifecycle state of the agent,
not the traffic state.

Traffic information belongs to AgentContext.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional


class AgentStatus(str, Enum):
    """
    Lifecycle status of an agent.
    """

    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass(slots=True)
class AgentState:
    """
    Runtime information of an intelligent agent.

    Notes
    -----
    This class does NOT store traffic information.
    It only stores information about the agent itself.
    """

    # ==========================================================
    # Identity
    # ==========================================================

    agent_id: str

    junction_id: str

    # ==========================================================
    # Lifecycle
    # ==========================================================

    status: AgentStatus = AgentStatus.CREATED

    # ==========================================================
    # Simulation
    # ==========================================================

    current_step: int = 0

    current_time: float = 0.0

    # ==========================================================
    # Execution
    # ==========================================================

    total_steps: int = 0

    successful_steps: int = 0

    failed_steps: int = 0

    last_error: Optional[str] = None

    # ==========================================================
    # Capabilities
    # ==========================================================

    active_capability: Optional[str] = None

    capability_statistics: Dict[str, int] = field(default_factory=dict)

    # ==========================================================
    # Timing
    # ==========================================================

    created_at: datetime = field(default_factory=datetime.utcnow)

    started_at: Optional[datetime] = None

    stopped_at: Optional[datetime] = None

    last_execution: Optional[datetime] = None

    # ==========================================================
    # Lifecycle Management
    # ==========================================================

    def initialize(self) -> None:
        """
        Initialize agent.
        """
        self.status = AgentStatus.INITIALIZED

    def start(self) -> None:
        """
        Start agent execution.
        """
        self.status = AgentStatus.RUNNING
        self.started_at = datetime.utcnow()

    def stop(self) -> None:
        """
        Stop agent.
        """
        self.status = AgentStatus.STOPPED
        self.stopped_at = datetime.utcnow()

    def pause(self) -> None:
        """
        Pause execution.
        """
        self.status = AgentStatus.PAUSED

    def resume(self) -> None:
        """
        Resume execution.
        """
        self.status = AgentStatus.RUNNING

    def fail(self, error: Exception | str) -> None:
        """
        Mark current execution as failed.
        """

        self.status = AgentStatus.ERROR

        self.failed_steps += 1

        self.last_error = str(error)

    # ==========================================================
    # Simulation Updates
    # ==========================================================

    def update_step(
        self,
        step: int,
        simulation_time: float,
    ) -> None:
        """
        Update simulation information.
        """

        self.current_step = step

        self.current_time = simulation_time

        self.total_steps += 1

        self.last_execution = datetime.utcnow()

    def mark_success(self) -> None:
        """
        Record successful execution.
        """

        self.successful_steps += 1

        if self.status == AgentStatus.ERROR:
            self.status = AgentStatus.RUNNING

    # ==========================================================
    # Capability Tracking
    # ==========================================================

    def activate_capability(self, capability_name: str) -> None:
        """
        Mark currently executing capability.
        """

        self.active_capability = capability_name

        self.capability_statistics.setdefault(
            capability_name,
            0,
        )

        self.capability_statistics[capability_name] += 1

    # ==========================================================
    # Statistics
    # ==========================================================

    @property
    def success_rate(self) -> float:

        if self.total_steps == 0:
            return 0.0

        return self.successful_steps / self.total_steps

    @property
    def failure_rate(self) -> float:

        if self.total_steps == 0:
            return 0.0

        return self.failed_steps / self.total_steps

    @property
    def is_running(self) -> bool:
        return self.status == AgentStatus.RUNNING

    @property
    def is_paused(self) -> bool:
        return self.status == AgentStatus.PAUSED

    @property
    def has_error(self) -> bool:
        return self.status == AgentStatus.ERROR

    # ==========================================================
    # Reset
    # ==========================================================

    def reset(self) -> None:
        """
        Reset runtime state.
        """

        self.status = AgentStatus.CREATED

        self.current_step = 0
        self.current_time = 0.0

        self.total_steps = 0
        self.successful_steps = 0
        self.failed_steps = 0

        self.last_error = None

        self.active_capability = None

        self.capability_statistics.clear()

        self.started_at = None
        self.stopped_at = None
        self.last_execution = None

    # ==========================================================
    # Export
    # ==========================================================

    def summary(self) -> dict:
        """
        Export runtime statistics.
        """

        return {
            "agent_id": self.agent_id,
            "junction_id": self.junction_id,
            "status": self.status.value,
            "step": self.current_step,
            "simulation_time": self.current_time,
            "total_steps": self.total_steps,
            "successful_steps": self.successful_steps,
            "failed_steps": self.failed_steps,
            "success_rate": self.success_rate,
            "active_capability": self.active_capability,
        }

    def __repr__(self) -> str:

        return (
            f"AgentState("
            f"id='{self.agent_id}', "
            f"junction='{self.junction_id}', "
            f"status='{self.status.value}', "
            f"step={self.current_step})"
        )