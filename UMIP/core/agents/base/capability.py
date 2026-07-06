"""
capability.py
==============

Defines the abstract interface for every capability that can be attached
to an AI agent.

A capability represents one cognitive ability of an agent, such as:

- Observation
- Understanding
- Prediction
- Planning
- Communication
- Execution
- Learning

Every capability follows the same lifecycle and is executed by the
BaseAgent during every simulation step.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .agent_context import AgentContext


class Capability(ABC):
    """
    Base class for every Agent Capability.

    Each capability performs one well-defined task.

    Examples
    --------
    ObservationCapability
    PredictionCapability
    PlanningCapability
    CommunicationCapability

    Notes
    -----
    A capability should never directly interact with SUMO.
    It should only use the AgentContext.
    """

    def __init__(self) -> None:
        self._initialized: bool = False

    @property
    def initialized(self) -> bool:
        """
        Returns whether the capability has been initialized.
        """
        return self._initialized

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human readable capability name.
        """
        ...

    def initialize(self, context: "AgentContext") -> None:
        """
        Called once before the simulation starts.

        Parameters
        ----------
        context:
            Shared AgentContext.
        """
        self._initialized = True

    @abstractmethod
    def execute(self, context: "AgentContext") -> None:
        """
        Execute one reasoning step.

        This method is called every simulation step.

        Parameters
        ----------
        context:
            Shared AgentContext.
        """
        ...

    def shutdown(self, context: "AgentContext") -> None:
        """
        Called when the simulation ends.

        Override if cleanup is required.
        """
        pass

    def reset(self) -> None:
        """
        Reset internal state.

        Useful during testing or restarting a simulation.
        """
        self._initialized = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(initialized={self.initialized})"