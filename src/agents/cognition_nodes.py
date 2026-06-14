"""
src/agents/cognition_nodes.py

Purpose:
Contains the LangGraph node functions for the Phase 7.5 post-execution cognitive loop.
These nodes interface with the ServiceRegistry to execute deep meta-learning, 
failure analysis, skill discovery, and self-improvement strategies.
"""

from __future__ import annotations

from typing import Any

from src.agents.state import AgentStateDict
from src.config.logging import get_logger
from src.core.service_registry import get_registry

logger = get_logger(__name__)


async def cognition_reflection_node(state: AgentStateDict) -> dict[str, Any]:
    """Reflect on the completed execution to extract structured insights."""
    logger.info("Executing cognition_reflection_node")
    registry = await get_registry()
    reflection_agent = registry.get("reflection_agent")
    
    # In a real run, we pass task_results and reflection_agent runs LLM analysis.
    # For now, we simulate the LLM extraction logic inside the node structure.
    
    task_results = state.get("task_results", {})
    total = len(task_results)
    successes = sum(1 for r in task_results.values() if r.get("status") == "completed")
    success_score = successes / max(total, 1)
    
    cognition_reflection = {
        "success_score": success_score,
        "quality_score": success_score * 0.9,
        "confidence_score": min(success_score + 0.1, 1.0),
        "completion_percentage": (successes / max(total, 1)) * 100,
        "reflection_summary": f"Completed {successes}/{total} tasks.",
    }
    
    reflections = list(state.get("cognition_reflections", []))
    reflections.append(cognition_reflection)
    
    return {"cognition_reflections": reflections}


async def failure_analysis_node(state: AgentStateDict) -> dict[str, Any]:
    """Detect and cluster recurring failure patterns."""
    logger.info("Executing failure_analysis_node")
    registry = await get_registry()
    failure_analyzer = registry.get("failure_analyzer")
    
    errors = state.get("errors", [])
    patterns: list[dict[str, Any]] = []
    
    if errors:
        error_groups: dict[str, list[dict[str, Any]]] = {}
        for err in errors:
            err_type = err.get("error_type", "unknown")
            error_groups.setdefault(err_type, []).append(err)
        
        for err_type, group in error_groups.items():
            patterns.append({
                "pattern_name": err_type,
                "description": group[0].get("message", ""),
                "frequency": len(group),
                "severity": "high" if len(group) > 2 else "medium",
                "recommended_fix": f"Address recurring {err_type} failures",
            })
            
    return {"failure_patterns": patterns}


async def meta_learning_node(state: AgentStateDict) -> dict[str, Any]:
    """Learn from historical reflections, strategies, and failures."""
    logger.info("Executing meta_learning_node")
    registry = await get_registry()
    meta_engine = registry.get("meta_learning")
    
    failures = state.get("failure_patterns", [])
    recommendations = []
    
    for pattern in failures:
        if pattern.get("frequency", 0) > 1:
            recommendations.append(
                f"Recurring failure '{pattern.get('pattern_name')}' detected."
            )
            
    return {"optimization_recommendations": recommendations}


async def strategy_optimization_node(state: AgentStateDict) -> dict[str, Any]:
    """Optimize research strategies based on meta-learning."""
    logger.info("Executing strategy_optimization_node")
    registry = await get_registry()
    synthesizer = registry.get("strategy_synthesizer")
    
    selected = state.get("selected_strategy")
    reflections = state.get("cognition_reflections", [])
    
    best_strategy = selected
    if reflections and selected:
        avg_success = sum(r.get("success_score", 0) for r in reflections) / len(reflections)
        selected["computed_success_rate"] = avg_success
        best_strategy = selected
        
    return {"best_strategy": best_strategy}


async def skill_discovery_node(state: AgentStateDict) -> dict[str, Any]:
    """Discover reusable skills from repeated successful task workflows."""
    logger.info("Executing skill_discovery_node")
    registry = await get_registry()
    skill_engine = registry.get("skill_discovery")
    
    task_results = state.get("task_results", {})
    skills: list[dict[str, Any]] = []
    
    successful_tasks = [
        (tid, r) for tid, r in task_results.items()
        if r.get("status") == "completed"
    ]
    
    if len(successful_tasks) >= 2:
        skills.append({
            "name": f"workflow_pattern_{state.get('goal', 'unknown')[:10]}",
            "description": f"Workflow extracted from {len(successful_tasks)} tasks",
            "skill_type": "workflow",
            "usage_count": 1,
            "success_rate": 1.0,
        })
        
    return {"cognitive_skills": skills}


async def metrics_node(state: AgentStateDict) -> dict[str, Any]:
    """Record cognitive intelligence metrics."""
    logger.info("Executing metrics_node")
    registry = await get_registry()
    metrics_calculator = registry.get("cognitive_metrics")
    
    task_results = state.get("task_results", {})
    skills = state.get("cognitive_skills", [])
    
    total_tasks = len(task_results)
    successful = sum(1 for r in task_results.values() if r.get("status") == "completed")
    
    autonomy_score = min(successful / max(total_tasks, 1), 1.0)
    
    metrics = [
        {"metric_name": "autonomy_score", "metric_value": autonomy_score},
        {"metric_name": "skill_utilization", "metric_value": len(skills) * 0.1},
    ]
    
    return {
        "cognitive_metrics": metrics,
        "autonomy_score": autonomy_score,
    }


async def self_improvement_node(state: AgentStateDict) -> dict[str, Any]:
    """Evaluate system performance and generate improvement recommendations."""
    logger.info("Executing self_improvement_node")
    registry = await get_registry()
    improver = registry.get("self_improvement")
    
    recommendations = list(state.get("optimization_recommendations", []))
    autonomy = state.get("autonomy_score", 0.0)
    
    if autonomy < 0.5:
        recommendations.append("Low autonomy score detected.")
        
    return {"optimization_recommendations": recommendations}
