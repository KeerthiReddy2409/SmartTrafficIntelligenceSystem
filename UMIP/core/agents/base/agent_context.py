"""
agent_context.py
================

Shared runtime context for an intelligent traffic agent.

The AgentContext is the single source of truth during one
reasoning cycle.

All capabilities communicate only through this object.

Nothing inside this class contains business logic.
It only stores state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class AgentContext:
    """
    Shared runtime context.

    Every capability receives the same context object.

    Observation writes current state.

    Analytics writes analytics.

    Prediction writes predictions.

    Planning writes plans.

    Execution reads selected actions.

    Communication reads/writes messages.

    This prevents capabilities from depending on one another.
    """

    # ==========================================================
    # Agent Information
    # ==========================================================

    agent_id: str

    junction_id: str

    # ==========================================================
    # Simulation
    # ==========================================================

    simulation_step: int = 0

    simulation_time: float = 0.0

    # ==========================================================
    # Current World
    # ==========================================================

    city_state: Optional[Any] = None

    junction_state: Optional[Any] = None

    # ==========================================================
    # Analytics
    # ==========================================================

    analytics: Optional[Any] = None

    # ==========================================================
    # Prediction
    # ==========================================================

    prediction: Optional[Any] = None

    # ==========================================================
    # Planning
    # ==========================================================

    current_plan: Optional[Any] = None

    candidate_plans: List[Any] = field(default_factory=list)

    selected_action: Optional[Any] = None

    # ==========================================================
    # Communication
    # ==========================================================

    incoming_messages: List[Any] = field(default_factory=list)

    outgoing_messages: List[Any] = field(default_factory=list)

    # ==========================================================
    # Agent Components
    # ==========================================================

    memory: Optional[Any] = None

    toolbox: Optional[Any] = None

    # ==========================================================
    # Temporary Workspace
    # ==========================================================

    workspace: Dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Step Management
    # ==========================================================

    def begin_step(
        self,
        simulation_step: int,
        simulation_time: float,
    ) -> None:
        """
        Prepare context for a new simulation step.
        """

        self.simulation_step = simulation_step
        self.simulation_time = simulation_time

        self.analytics = None
        self.prediction = None

        self.current_plan = None
        self.selected_action = None

        self.candidate_plans.clear()

        self.incoming_messages.clear()
        self.outgoing_messages.clear()

        self.workspace.clear()

    # ==========================================================
    # Workspace
    # ==========================================================

    def put(self, key: str, value: Any) -> None:
        """
        Store temporary information.

        Example
        -------
        context.put("queue_growth", 12)
        """

        self.workspace[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Read temporary information.
        """

        return self.workspace.get(key, default)

    def remove(self, key: str) -> None:
        """
        Remove workspace item.
        """

        self.workspace.pop(key, None)

    # ==========================================================
    # Messages
    # ==========================================================

    def add_incoming_message(self, message: Any) -> None:
        """
        Add received message.
        """

        self.incoming_messages.append(message)

    def add_outgoing_message(self, message: Any) -> None:
        """
        Queue message for sending.
        """

        self.outgoing_messages.append(message)

    # ==========================================================
    # Plans
    # ==========================================================

    def add_candidate_plan(self, plan: Any) -> None:
        """
        Store generated plan.
        """

        self.candidate_plans.append(plan)

    def clear_candidate_plans(self) -> None:
        """
        Remove all candidate plans.
        """

        self.candidate_plans.clear()

    # ==========================================================
    # Utility
    # ==========================================================

    @property
    def has_prediction(self) -> bool:
        return self.prediction is not None

    @property
    def has_plan(self) -> bool:
        return self.current_plan is not None

    @property
    def has_action(self) -> bool:
        return self.selected_action is not None

    def reset(self) -> None:
        """
        Reset complete context.
        """

        self.city_state = None
        self.junction_state = None

        self.analytics = None
        self.prediction = None

        self.current_plan = None
        self.selected_action = None

        self.memory = None
        self.toolbox = None

        self.workspace.clear()

        self.candidate_plans.clear()

        self.incoming_messages.clear()
        self.outgoing_messages.clear()

    def __repr__(self) -> str:

        return (
            f"AgentContext("
            f"agent='{self.agent_id}', "
            f"junction='{self.junction_id}', "
            f"step={self.simulation_step}, "
            f"time={self.simulation_time:.2f}"
            f")"
        )