"""
execution_capability.py
=======================

Execution Capability

Responsible for executing the action selected by the planner.

This capability never decides WHAT to do.
It only executes the selected action using the configured
Execution Engine.

Pipeline
--------

Planning
      ↓
Selected Action
      ↓
Execution Engine
      ↓
SUMO / Signal Controller
"""

from __future__ import annotations

import logging

from core.agents.base.capability import Capability

logger = logging.getLogger(__name__)


class ExecutionCapability(Capability):
    """
    Execution capability.

    Responsibilities
    ----------------
    1. Read selected action.
    2. Execute action.
    3. Record execution result.
    """

    def __init__(self) -> None:

        super().__init__()

    @property
    def name(self) -> str:
        return "Execution"

    def initialize(self, context) -> None:

        super().initialize(context)

        logger.info(
            "[%s] ExecutionCapability initialized.",
            context.agent_id,
        )

    def execute(self, context) -> None:
        """
        Execute selected traffic signal action.
        """

        if context.selected_action is None:

            logger.debug(
                "[%s] No action selected.",
                context.agent_id,
            )

            return

        if context.toolbox is None:

            logger.warning(
                "[%s] Toolbox unavailable.",
                context.agent_id,
            )

            return

        engine = context.toolbox.execution_engine

        if engine is None:

            logger.debug(
                "[%s] Execution engine unavailable.",
                context.agent_id,
            )

            return

        try:

            result = engine.execute(
                junction_id=context.junction_id,
                action=context.selected_action,
                city_state=context.city_state,
            )

            context.put(
                "execution_result",
                result,
            )

            logger.debug(
                "[%s] Action executed successfully.",
                context.agent_id,
            )

        except Exception:

            logger.exception(
                "[%s] Failed to execute action.",
                context.agent_id,
            )

            raise

    def shutdown(self, context) -> None:

        logger.info(
            "[%s] ExecutionCapability shutdown.",
            context.agent_id,
        )