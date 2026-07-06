"""
planning_capability.py
======================

Planning Capability

Responsible for selecting the best signal action for the
current simulation step.

The capability itself contains no planning logic.
It simply coordinates the Planning Engine.

Pipeline
--------

CityState
      ↓
Analytics
      ↓
Prediction
      ↓
Planning Engine
      ↓
Selected Plan
      ↓
Selected Action
      ↓
Agent Context
"""

from __future__ import annotations

import logging

from core.agents.base.capability import Capability

logger = logging.getLogger(__name__)


class PlanningCapability(Capability):
    """
    Planning capability.

    This capability asks the planning engine to evaluate the
    current traffic situation and choose the best action.

    Future Planning Engines
    -----------------------

    - Rule Based Planner
    - Optimization Planner
    - Reinforcement Learning Planner
    - LLM Planner
    """

    def __init__(self) -> None:

        super().__init__()

    @property
    def name(self) -> str:
        return "Planning"

    def initialize(self, context) -> None:

        super().initialize(context)

        logger.info(
            "[%s] PlanningCapability initialized.",
            context.agent_id,
        )

    def execute(self, context) -> None:
        """
        Execute one planning cycle.
        """

        if context.city_state is None:

            logger.warning(
                "[%s] CityState missing.",
                context.agent_id,
            )

            return

        engine = None

        if context.toolbox is not None:

            engine = context.toolbox.planning_engine

        if engine is None:

            logger.debug(
                "[%s] Planning engine not available.",
                context.agent_id,
            )

            return

        result = engine.plan(
            city_state=context.city_state,
            analytics=context.analytics,
            prediction=context.prediction,
            memory=context.memory,
        )

        if result is None:

            logger.debug(
                "[%s] Planning engine returned no plan.",
                context.agent_id,
            )

            return

        # ----------------------------------------------------
        # Expected Return Format
        #
        # {
        #     "plan": ...,
        #     "action": ...
        # }
        # ----------------------------------------------------

        context.current_plan = result.get("plan")

        context.selected_action = result.get("action")

        logger.debug(
            "[%s] Planning completed.",
            context.agent_id,
        )

    def shutdown(self, context) -> None:

        logger.info(
            "[%s] PlanningCapability shutdown.",
            context.agent_id,
        )