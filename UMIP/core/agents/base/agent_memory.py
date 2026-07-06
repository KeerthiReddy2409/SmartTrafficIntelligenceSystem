"""
agent_memory.py
===============

Persistent memory for an intelligent traffic agent.

Unlike AgentContext, which only stores information for the
current reasoning cycle, AgentMemory stores information across
the entire lifetime of the agent.

Future extensions:
------------------
- Reinforcement Learning
- Experience Replay
- Long-Term Memory
- LangGraph Memory
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, Dict, Optional


@dataclass(slots=True)
class AgentMemory:
    """
    Persistent memory of an intelligent agent.

    Parameters
    ----------
    history_size:
        Maximum number of historical records to keep.
    """

    history_size: int = 100

    # ==========================================================
    # Internal History
    # ==========================================================

    state_history: Deque[Any] = field(init=False)

    analytics_history: Deque[Any] = field(init=False)

    prediction_history: Deque[Any] = field(init=False)

    plan_history: Deque[Any] = field(init=False)

    action_history: Deque[Any] = field(init=False)

    reward_history: Deque[float] = field(init=False)

    message_history: Deque[Any] = field(init=False)

    # ==========================================================
    # Long-Term Knowledge
    # ==========================================================

    knowledge: Dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Initialization
    # ==========================================================

    def __post_init__(self) -> None:

        self.state_history = deque(maxlen=self.history_size)

        self.analytics_history = deque(maxlen=self.history_size)

        self.prediction_history = deque(maxlen=self.history_size)

        self.plan_history = deque(maxlen=self.history_size)

        self.action_history = deque(maxlen=self.history_size)

        self.reward_history = deque(maxlen=self.history_size)

        self.message_history = deque(maxlen=self.history_size)

    # ==========================================================
    # State Memory
    # ==========================================================

    def remember_state(self, state: Any) -> None:
        self.state_history.append(state)

    @property
    def latest_state(self) -> Optional[Any]:

        if not self.state_history:
            return None

        return self.state_history[-1]

    # ==========================================================
    # Analytics Memory
    # ==========================================================

    def remember_analytics(self, analytics: Any) -> None:
        self.analytics_history.append(analytics)

    @property
    def latest_analytics(self) -> Optional[Any]:

        if not self.analytics_history:
            return None

        return self.analytics_history[-1]

    # ==========================================================
    # Prediction Memory
    # ==========================================================

    def remember_prediction(self, prediction: Any) -> None:
        self.prediction_history.append(prediction)

    @property
    def latest_prediction(self) -> Optional[Any]:

        if not self.prediction_history:
            return None

        return self.prediction_history[-1]

    # ==========================================================
    # Plan Memory
    # ==========================================================

    def remember_plan(self, plan: Any) -> None:
        self.plan_history.append(plan)

    @property
    def latest_plan(self) -> Optional[Any]:

        if not self.plan_history:
            return None

        return self.plan_history[-1]

    # ==========================================================
    # Action Memory
    # ==========================================================

    def remember_action(self, action: Any) -> None:
        self.action_history.append(action)

    @property
    def latest_action(self) -> Optional[Any]:

        if not self.action_history:
            return None

        return self.action_history[-1]

    # ==========================================================
    # Reward Memory
    # ==========================================================

    def remember_reward(self, reward: float) -> None:
        self.reward_history.append(reward)

    @property
    def latest_reward(self) -> float:

        if not self.reward_history:
            return 0.0

        return self.reward_history[-1]

    @property
    def average_reward(self) -> float:

        if not self.reward_history:
            return 0.0

        return sum(self.reward_history) / len(self.reward_history)

    # ==========================================================
    # Message Memory
    # ==========================================================

    def remember_message(self, message: Any) -> None:
        self.message_history.append(message)

    # ==========================================================
    # Knowledge Store
    # ==========================================================

    def store(self, key: str, value: Any) -> None:
        """
        Store long-term knowledge.
        """

        self.knowledge[key] = value

    def retrieve(self, key: str, default: Any = None) -> Any:
        """
        Retrieve long-term knowledge.
        """

        return self.knowledge.get(key, default)

    def contains(self, key: str) -> bool:
        """
        Check whether a key exists.
        """

        return key in self.knowledge

    def remove(self, key: str) -> None:
        """
        Remove stored knowledge.
        """

        self.knowledge.pop(key, None)

    # ==========================================================
    # Statistics
    # ==========================================================

    @property
    def state_count(self) -> int:
        return len(self.state_history)

    @property
    def prediction_count(self) -> int:
        return len(self.prediction_history)

    @property
    def action_count(self) -> int:
        return len(self.action_history)

    @property
    def plan_count(self) -> int:
        return len(self.plan_history)

    @property
    def reward_count(self) -> int:
        return len(self.reward_history)

    @property
    def message_count(self) -> int:
        return len(self.message_history)

    # ==========================================================
    # Maintenance
    # ==========================================================

    def clear_history(self) -> None:

        self.state_history.clear()

        self.analytics_history.clear()

        self.prediction_history.clear()

        self.plan_history.clear()

        self.action_history.clear()

        self.reward_history.clear()

        self.message_history.clear()

    def clear_knowledge(self) -> None:
        self.knowledge.clear()

    def clear(self) -> None:
        """
        Completely reset memory.
        """

        self.clear_history()

        self.clear_knowledge()

    # ==========================================================
    # Export
    # ==========================================================

    def snapshot(self) -> Dict[str, Any]:
        """
        Return memory statistics.
        """

        return {
            "states": self.state_count,
            "analytics": len(self.analytics_history),
            "predictions": self.prediction_count,
            "plans": self.plan_count,
            "actions": self.action_count,
            "messages": self.message_count,
            "knowledge": len(self.knowledge),
            "average_reward": self.average_reward,
        }

    def __len__(self) -> int:
        return self.state_count

    def __repr__(self) -> str:

        return (
            f"AgentMemory("
            f"states={self.state_count}, "
            f"predictions={self.prediction_count}, "
            f"actions={self.action_count}, "
            f"knowledge={len(self.knowledge)})"
        )