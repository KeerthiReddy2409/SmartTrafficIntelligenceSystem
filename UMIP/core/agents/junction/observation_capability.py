"""
Observation Capability

This capability is responsible for making the agent aware of the
current traffic situation.

Unlike traditional implementations, the CityState has already been
constructed by the simulator before the agent executes.

Therefore this capability simply validates the available state and
computes analytics.

Pipeline
--------

Simulation
      ↓
CityState
      ↓
ObservationCapability
      ↓
AnalyticsEngine
      ↓
AgentContext
"""

from __future__ import annotations

import logging

from analytics.analytics_engine import AnalyticsEngine

from core.agents.base.capability import Capability

logger = logging.getLogger(__name__)


class ObservationCapability(Capability):
    """
    Observation capability.

    Responsibilities
    ----------------
    1. Read current CityState
    2. Compute traffic analytics
    3. Store analytics inside AgentContext
    """

    def __init__(self) -> None:

        super().__init__()

        self.analytics_engine = AnalyticsEngine()

    @property
    def name(self) -> str:
        return "Observation"

    def initialize(self, context) -> None:

        super().initialize(context)

        logger.info(
            "[%s] ObservationCapability initialized.",
            context.agent_id,
        )

    def execute(self, context) -> None:
        """
        Execute one observation cycle.
        """

        city = context.city_state

        if city is None:

            logger.warning(
                "[%s] CityState not available.",
                context.agent_id,
            )

            return

        tracker = None

        if context.toolbox is not None:

            tracker = getattr(
                context.toolbox,
                "vehicle_tracker",
                None,
            )

        analytics = self.analytics_engine.compute(
            city,
            tracker=tracker,
        )

        context.analytics = analytics

        logger.debug(
            "[%s] Observation complete.",
            context.agent_id,
        )

    def shutdown(self, context) -> None:

        logger.info(
            "[%s] ObservationCapability shutdown.",
            context.agent_id,
        )