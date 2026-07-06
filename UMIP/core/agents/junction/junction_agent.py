"""
junction_agent.py
=================

Concrete implementation of an intelligent traffic junction agent.

A JunctionAgent represents exactly one signalized intersection.

Responsibilities
----------------
- Own a junction
- Execute reasoning cycle
- Coordinate capabilities
- Interface with the simulator

Actual intelligence is implemented inside capabilities.
"""

from __future__ import annotations

import logging

from agents.base.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class JunctionAgent(BaseAgent):
    """
    Intelligent traffic junction agent.

    One JunctionAgent controls exactly one SUMO junction.

    The agent itself contains very little logic.
    Intelligence is delegated to capabilities.

    Reasoning Cycle
    ---------------

    Observe

        ↓

    Understand

        ↓

    Predict

        ↓

    Plan

        ↓

    Communicate

        ↓

    Execute

        ↓

    Learn
    """

    def __init__(
        self,
        junction_id: str,
    ) -> None:

        super().__init__(
            agent_id=f"agent_{junction_id}",
            junction_id=junction_id,
        )

        logger.info(
            "Created JunctionAgent for %s",
            junction_id,
        )

    # =====================================================
    # Hooks
    # =====================================================

    def before_step(self) -> None:
        """
        Executed before capabilities.

        Child projects may override this.
        """

        logger.debug(
            "[%s] Starting reasoning cycle",
            self.agent_id,
        )

    def after_step(self) -> None:
        """
        Executed after capabilities.

        Child projects may override this.
        """

        logger.debug(
            "[%s] Finished reasoning cycle",
            self.agent_id,
        )

    # =====================================================
    # Information
    # =====================================================

    @property
    def junction(self) -> str:
        """
        Junction identifier.
        """
        return self.junction_id

    @property
    def capability_names(self) -> list[str]:
        """
        Names of installed capabilities.
        """

        return [
            capability.name
            for capability in self.capabilities
        ]

    # =====================================================
    # Debug
    # =====================================================

    def print_summary(self) -> None:

        print()

        print("=" * 60)

        print(" Junction Agent")

        print("=" * 60)

        print(f"Agent      : {self.agent_id}")

        print(f"Junction   : {self.junction}")

        print(f"Status     : {self.state.status.value}")

        print(f"Step       : {self.state.current_step}")

        print(f"Capabilities ({len(self)})")

        for capability in self.capabilities:

            print(f"   • {capability.name}")

        print("=" * 60)

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:

        return (
            f"JunctionAgent("
            f"junction='{self.junction}', "
            f"capabilities={len(self)}, "
            f"status='{self.state.status.value}')"
        )