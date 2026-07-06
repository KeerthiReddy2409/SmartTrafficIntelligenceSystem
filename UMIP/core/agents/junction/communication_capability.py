"""
communication_capability.py
===========================

Communication Capability

Responsible for exchanging information between neighbouring
junction agents.

This capability does not implement communication itself.
It delegates the work to the configured Communication Engine.
"""

from __future__ import annotations

import logging

from core.agents.base.capability import Capability

logger = logging.getLogger(__name__)


class CommunicationCapability(Capability):
    """
    Communication capability.

    Responsibilities
    ----------------
    1. Send outgoing messages.
    2. Receive incoming messages.
    3. Update AgentContext.

    Future message types
    --------------------
    - Queue Length
    - Predicted Queue
    - Predicted Flow
    - Emergency Vehicle
    - Congestion Alert
    - Green Wave Coordination
    """

    def __init__(self) -> None:

        super().__init__()

    @property
    def name(self) -> str:
        return "Communication"

    def initialize(self, context) -> None:

        super().initialize(context)

        logger.info(
            "[%s] CommunicationCapability initialized.",
            context.agent_id,
        )

    def execute(self, context) -> None:
        """
        Execute one communication cycle.
        """

        if context.toolbox is None:
            return

        engine = context.toolbox.communication_engine

        if engine is None:

            logger.debug(
                "[%s] Communication engine unavailable.",
                context.agent_id,
            )

            return

        # -------------------------------------------------
        # Receive new messages
        # -------------------------------------------------

        incoming = engine.receive(
            agent_id=context.agent_id,
            junction_id=context.junction_id,
        )

        if incoming:

            context.incoming_messages.extend(
                incoming
            )

        # -------------------------------------------------
        # Send queued messages
        # -------------------------------------------------

        if context.outgoing_messages:

            engine.send(
                sender=context.agent_id,
                junction=context.junction_id,
                messages=context.outgoing_messages,
            )

            context.outgoing_messages.clear()

        logger.debug(
            "[%s] Communication completed.",
            context.agent_id,
        )

    def shutdown(self, context) -> None:

        logger.info(
            "[%s] CommunicationCapability shutdown.",
            context.agent_id,
        )