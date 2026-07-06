"""
toolbox.py
==========

Dependency container used by intelligent agents.

The Toolbox provides access to all external systems used by an agent.

The agent itself should never directly instantiate services.
Everything is injected through this class.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(slots=True)
class Toolbox:
    """
    Shared dependency container.

    Examples
    --------
    toolbox.analytics

    toolbox.prediction

    toolbox.planner

    toolbox.signal_controller
    """

    # ==========================================================
    # Core Engines
    # ==========================================================

    analytics_engine: Optional[Any] = None

    prediction_engine: Optional[Any] = None

    planning_engine: Optional[Any] = None

    communication_engine: Optional[Any] = None

    execution_engine: Optional[Any] = None

    learning_engine: Optional[Any] = None

    # ==========================================================
    # Simulation
    # ==========================================================

    simulator: Optional[Any] = None

    traci: Optional[Any] = None

    # ==========================================================
    # Storage
    # ==========================================================

    database: Optional[Any] = None

    cache: Optional[Any] = None

    # ==========================================================
    # Miscellaneous
    # ==========================================================

    services: Dict[str, Any] = None

    def __post_init__(self) -> None:

        if self.services is None:
            self.services = {}

    # ==========================================================
    # Engine Registration
    # ==========================================================

    def register(self, name: str, service: Any) -> None:
        """
        Register a custom service.
        """

        self.services[name] = service

    def unregister(self, name: str) -> None:
        """
        Remove registered service.
        """

        self.services.pop(name, None)

    # ==========================================================
    # Lookup
    # ==========================================================

    def get(self, name: str, default: Any = None) -> Any:
        """
        Retrieve registered service.
        """

        return self.services.get(name, default)

    def has(self, name: str) -> bool:
        """
        Returns True if service exists.
        """

        return name in self.services

    # ==========================================================
    # Core Engine Checks
    # ==========================================================

    @property
    def has_analytics(self) -> bool:
        return self.analytics_engine is not None

    @property
    def has_prediction(self) -> bool:
        return self.prediction_engine is not None

    @property
    def has_planner(self) -> bool:
        return self.planning_engine is not None

    @property
    def has_communication(self) -> bool:
        return self.communication_engine is not None

    @property
    def has_execution(self) -> bool:
        return self.execution_engine is not None

    @property
    def has_learning(self) -> bool:
        return self.learning_engine is not None

    # ==========================================================
    # Maintenance
    # ==========================================================

    def clear(self) -> None:

        self.analytics_engine = None
        self.prediction_engine = None
        self.planning_engine = None
        self.communication_engine = None
        self.execution_engine = None
        self.learning_engine = None

        self.simulator = None
        self.traci = None

        self.database = None
        self.cache = None

        self.services.clear()

    # ==========================================================
    # Export
    # ==========================================================

    def summary(self) -> dict:

        return {
            "analytics": self.has_analytics,
            "prediction": self.has_prediction,
            "planning": self.has_planner,
            "communication": self.has_communication,
            "execution": self.has_execution,
            "learning": self.has_learning,
            "custom_services": len(self.services),
        }

    def __repr__(self) -> str:

        return (
            "Toolbox("
            f"analytics={self.has_analytics}, "
            f"prediction={self.has_prediction}, "
            f"planning={self.has_planner}, "
            f"communication={self.has_communication}, "
            f"execution={self.has_execution}, "
            f"learning={self.has_learning}, "
            f"services={len(self.services)})"
        )