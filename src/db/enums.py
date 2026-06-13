"""
Database enumerations for the Autonomous Agent Platform.

These Python enums map directly to PostgreSQL ENUM types created via
SQLAlchemy's ``Enum`` column type. Each enum value is stored as its
lowercase string representation in the database.
"""

from __future__ import annotations

import enum


class SessionStatus(str, enum.Enum):
    """Lifecycle status of an agent session."""

    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskStatus(str, enum.Enum):
    """Lifecycle status of an individual task within a session."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class ExecutionStatus(str, enum.Enum):
    """Status of a single agent execution attempt."""

    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class MemoryType(str, enum.Enum):
    """Classification of memory entries in the memory subsystem."""

    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"


class SourceType(str, enum.Enum):
    """Origin type for knowledge documents."""

    ARXIV = "arxiv"
    WEB = "web"
    WIKIPEDIA = "wikipedia"
    PDF = "pdf"
    MANUAL = "manual"


class ReflectionType(str, enum.Enum):
    """Scope of a reflection record."""

    TASK = "task"
    SESSION = "session"
    STRATEGY = "strategy"


class Priority(str, enum.Enum):
    """Task priority levels, ordered from lowest to highest."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class TaskType(str, enum.Enum):
    """Categorization of agent tasks for strategy selection."""

    RESEARCH = "research"
    CODING = "coding"
    PLANNING = "planning"
    WRITING = "writing"
    ANALYSIS = "analysis"
    AUTOMATION = "automation"
    DATA_PROCESSING = "data_processing"
    MULTI_STEP_REASONING = "multi_step_reasoning"


class StrategyStatus(str, enum.Enum):
    """Lifecycle status of a learned strategy."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    TESTING = "testing"


class MetricType(str, enum.Enum):
    """Types of performance metrics tracked for analytics."""

    SUCCESS_RATE = "success_rate"
    TOKEN_USAGE = "token_usage"
    EXECUTION_LATENCY = "execution_latency"
    MEMORY_HIT_RATE = "memory_hit_rate"
    STRATEGY_EFFECTIVENESS = "strategy_effectiveness"
    REFLECTION_QUALITY = "reflection_quality"
    TOOL_UTILIZATION = "tool_utilization"


class SkillStatus(str, enum.Enum):
    """Lifecycle status of a reusable skill."""

    ACTIVE = "active"
    DRAFT = "draft"
    DEPRECATED = "deprecated"


class ResearchTrackStatus(str, enum.Enum):
    """Lifecycle status of a research track."""

    PROPOSED = "proposed"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    TERMINATED = "terminated"


class PortfolioStatus(str, enum.Enum):
    """Lifecycle status of a research portfolio."""

    ACTIVE = "active"
    ARCHIVED = "archived"


class GoalStatus(str, enum.Enum):
    """Lifecycle status of an autonomously generated goal."""

    GENERATED = "generated"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    ACHIEVED = "achieved"
    FAILED = "failed"
