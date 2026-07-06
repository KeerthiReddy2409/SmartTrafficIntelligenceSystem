"""
prediction_capability.py
========================

Prediction Capability

Responsible for generating future traffic predictions for the
current junction.

Pipeline
--------

CityState
      ↓
Analytics
      ↓
Prediction Engine
      ↓
Prediction State
      ↓
Agent Context
"""

from __future__ import annotations

import logging

from core.agents.base.capability import Capability

logger = logging.getLogger(__name__)


class PredictionCapability(Capability):
    """
    Prediction capability.

    This capability generates traffic predictions using the
    configured prediction engine.

    Initially this is only a wrapper around the prediction engine.
    Later it can support:

    - Queue Prediction
    - Waiting Time Prediction
    - Lane Flow Prediction
    - Congestion Prediction
    - Travel Time Prediction
    """

    def __init__(self) -> None:

        super().__init__()

    @property
    def name(self) -> str:
        return "Prediction"

    def initialize(self, context) -> None:

        super().initialize(context)

        logger.info(
            "[%s] PredictionCapability initialized.",
            context.agent_id,
        )

    def execute(self, context) -> None:
        """
        Execute one prediction cycle.
        """

        if context.city_state is None:

            logger.warning(
                "[%s] CityState missing.",
                context.agent_id,
            )

            return

        if context.analytics is None:

            logger.warning(
                "[%s] Analytics missing.",
                context.agent_id,
            )

            return

        engine = None

        if context.toolbox is not None:

            engine = context.toolbox.prediction_engine

        if engine is None:

            logger.debug(
                "[%s] Prediction engine not available.",
                context.agent_id,
            )

            return

        prediction = engine.predict(
            city_state=context.city_state,
            analytics=context.analytics,
            memory=context.memory,
        )

        context.prediction = prediction

        logger.debug(
            "[%s] Prediction completed.",
            context.agent_id,
        )

    def shutdown(self, context) -> None:

        logger.info(
            "[%s] PredictionCapability shutdown.",
            context.agent_id,
        )