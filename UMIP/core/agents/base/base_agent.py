"""
base_agent.py
=============

Base implementation for every intelligent agent.

All traffic agents inherit from this class.

Responsibilities
----------------
- Capability orchestration
- Lifecycle management
- Execution loop
- Error handling
- Context management
- Memory management
"""

from __future__ import annotations

import logging
from abc import ABC

from .agent_context import AgentContext
from .agent_memory import AgentMemory
from .agent_state import AgentState
from .capability import Capability
from .toolbox import Toolbox


logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all intelligent agents.

    Every JunctionAgent, EmergencyAgent or CoordinatorAgent
    should inherit from this class.
    """

    def __init__(
        self,
        agent_id: str,
        junction_id: str,
    ) -> None:

        self.context = AgentContext(
            agent_id=agent_id,
            junction_id=junction_id,
        )

        self.state = AgentState(
            agent_id=agent_id,
            junction_id=junction_id,
        )

        self.memory = AgentMemory()

        self.toolbox = Toolbox()

        self.context.memory = self.memory
        self.context.toolbox = self.toolbox

        self._capabilities: list[Capability] = []

        logger.info(
            "Created agent '%s' for junction '%s'",
            agent_id,
            junction_id,
        )

    # ======================================================
    # Properties
    # ======================================================

    @property
    def agent_id(self) -> str:
        return self.context.agent_id

    @property
    def junction_id(self) -> str:
        return self.context.junction_id

    @property
    def capabilities(self) -> tuple[Capability, ...]:
        return tuple(self._capabilities)

    # ======================================================
    # Capability Management
    # ======================================================

    def add_capability(
        self,
        capability: Capability,
    ) -> None:
        """
        Register a capability.
        """

        if capability in self._capabilities:
            return

        self._capabilities.append(capability)

        logger.info(
            "[%s] Added capability: %s",
            self.agent_id,
            capability.name,
        )

    def remove_capability(
        self,
        capability_name: str,
    ) -> None:

        self._capabilities = [
            capability
            for capability in self._capabilities
            if capability.name != capability_name
        ]

    def get_capability(
        self,
        capability_name: str,
    ) -> Capability | None:

        for capability in self._capabilities:

            if capability.name == capability_name:
                return capability

        return None

    # ======================================================
    # Initialization
    # ======================================================

    def initialize(self) -> None:
        """
        Initialize the agent.
        """

        logger.info(
            "[%s] Initializing...",
            self.agent_id,
        )

        self.state.initialize()

        for capability in self._capabilities:

            capability.initialize(self.context)

        self.state.start()

        logger.info(
            "[%s] Initialized.",
            self.agent_id,
        )

    # ======================================================
    # Execution
    # ======================================================

    def step(
        self,
        simulation_step: int,
        simulation_time: float,
    ) -> None:
        """
        Execute one reasoning cycle.
        """

        if not self.state.is_running:
            return

        self.context.begin_step(
            simulation_step,
            simulation_time,
        )

        self.state.update_step(
            simulation_step,
            simulation_time,
        )

        try:

            self.before_step()

            for capability in self._capabilities:

                self.state.activate_capability(
                    capability.name
                )

                capability.before_step(
                    self.context
                )

                capability.execute(
                    self.context
                )

                capability.after_step(
                    self.context
                )

            self.after_step()

            self.memory.remember_state(
                self.context.city_state
            )

            if self.context.analytics is not None:

                self.memory.remember_analytics(
                    self.context.analytics
                )

            if self.context.prediction is not None:

                self.memory.remember_prediction(
                    self.context.prediction
                )

            if self.context.current_plan is not None:

                self.memory.remember_plan(
                    self.context.current_plan
                )

            if self.context.selected_action is not None:

                self.memory.remember_action(
                    self.context.selected_action
                )

            self.state.mark_success()

        except Exception as exc:

            logger.exception(
                "[%s] Agent execution failed.",
                self.agent_id,
            )

            self.state.fail(exc)

            raise

    # ======================================================
    # Hooks
    # ======================================================

    def before_step(self) -> None:
        """
        Hook executed before capabilities run.

        Child classes may override this.
        """
        return

    def after_step(self) -> None:
        """
        Hook executed after all capabilities finish.

        Child classes may override this.
        """
        return

    # ======================================================
    # Lifecycle
    # ======================================================

    def shutdown(self) -> None:
        """
        Shutdown agent.
        """

        logger.info(
            "[%s] Shutting down...",
            self.agent_id,
        )

        for capability in self._capabilities:

            try:
                capability.shutdown(
                    self.context
                )

            except Exception:

                logger.exception(
                    "[%s] Failed shutting down capability '%s'",
                    self.agent_id,
                    capability.name,
                )

        self.state.stop()

        logger.info(
            "[%s] Shutdown complete.",
            self.agent_id,
        )

    def pause(self) -> None:
        """
        Pause execution.
        """

        self.state.pause()

    def resume(self) -> None:
        """
        Resume execution.
        """

        self.state.resume()

    # ======================================================
    # Reset
    # ======================================================

    def reset(self) -> None:
        """
        Reset agent.

        Useful for restarting simulations.
        """

        logger.info(
            "[%s] Resetting...",
            self.agent_id,
        )

        self.memory.clear()

        self.context.reset()

        self.context.memory = self.memory
        self.context.toolbox = self.toolbox

        self.state.reset()

        for capability in self._capabilities:

            capability.reset()

        logger.info(
            "[%s] Reset complete.",
            self.agent_id,
        )

    # ======================================================
    # Toolbox
    # ======================================================

    def set_toolbox(
        self,
        toolbox: Toolbox,
    ) -> None:
        """
        Replace toolbox.

        Parameters
        ----------
        toolbox
            Shared dependency container.
        """

        self.toolbox = toolbox

        self.context.toolbox = toolbox

    # ======================================================
    # Memory
    # ======================================================

    def set_memory(
        self,
        memory: AgentMemory,
    ) -> None:
        """
        Replace memory implementation.

        Parameters
        ----------
        memory
            New memory implementation.
        """

        self.memory = memory

        self.context.memory = memory

    # ======================================================
    # Status
    # ======================================================

    @property
    def is_running(self) -> bool:
        return self.state.is_running

    @property
    def is_paused(self) -> bool:
        return self.state.is_paused

    @property
    def has_error(self) -> bool:
        return self.state.has_error

    # ======================================================
    # Information
    # ======================================================

    def summary(self) -> dict:
        """
        Export runtime information.
        """

        return {
            "agent": self.agent_id,
            "junction": self.junction_id,
            "state": self.state.summary(),
            "memory": self.memory.snapshot(),
            "capabilities": [
                capability.name
                for capability in self._capabilities
            ],
        }

    # ======================================================
    # String Representation
    # ======================================================

    def __len__(self) -> int:
        return len(self._capabilities)

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"id='{self.agent_id}', "
            f"junction='{self.junction_id}', "
            f"capabilities={len(self)}, "
            f"status='{self.state.status.value}')"
        )