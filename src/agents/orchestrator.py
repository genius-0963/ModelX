"""
Orchestrator Agent — The central coordinator for the multi-agent workflow.

Implements a LangGraph StateGraph that:
1. Analyzes high-level goals
2. Decomposes goals into executable tasks
3. Routes tasks to specialist agents
4. Tracks progress and handles failures
5. Triggers reflection after completion
6. Generates summary reports
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph

from src.agents.state import AgentStateDict, TaskSpec
from src.config.logging import get_logger
from src.config.settings import get_settings

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# System prompts for the orchestrator's different roles
# ---------------------------------------------------------------------------

GOAL_ANALYSIS_PROMPT = """You are an expert goal analyst. Analyze the following goal and provide a structured analysis.

Goal: {goal}
{context}

Provide your analysis as JSON with the following structure:
{{
    "intent": "What the user wants to achieve",
    "scope": "small | medium | large",
    "domain": "The primary domain (e.g., 'research', 'coding', 'analysis')",
    "constraints": ["Any constraints or limitations"],
    "success_criteria": ["How to measure success"],
    "required_capabilities": ["research", "execution", "memory"],
    "estimated_complexity": 1-10,
    "risks": ["Potential risks or challenges"]
}}

Respond ONLY with valid JSON, no additional text."""

TASK_DECOMPOSITION_PROMPT = """You are an expert task planner. Decompose the following goal into executable tasks.

Goal: {goal}
Analysis: {analysis}
Available Memories: {memories}

Create a list of tasks as JSON array. Each task should have:
{{
    "id": "unique_id (use task_1, task_2, etc.)",
    "title": "Short task title",
    "description": "Detailed description of what needs to be done",
    "agent_type": "research | execution | memory",
    "priority": 1-5 (1 = highest),
    "dependencies": ["ids of tasks this depends on"]
}}

Rules:
- Order tasks logically (research before execution)
- Mark dependencies correctly
- Use "research" for information gathering
- Use "execution" for code/file/API operations
- Use "memory" for storing/recalling information
- Keep tasks atomic and focused
- Aim for 3-10 tasks total

Respond ONLY with a valid JSON array, no additional text."""

INTEGRATION_PROMPT = """You are a results integrator. Review the task results and determine next steps.

Goal: {goal}
Completed Tasks: {completed}
Current Task Result: {current_result}
Remaining Tasks: {remaining}
Errors: {errors}

Determine:
1. Was the current task successful?
2. Should we continue with the next task, retry, or stop?
3. Do any remaining tasks need modification based on results?

Respond as JSON:
{{
    "current_task_assessment": "success | partial | failure",
    "action": "continue | retry | stop | reflect",
    "modifications": ["Any task modifications needed"],
    "reasoning": "Why this action"
}}

Respond ONLY with valid JSON."""

REPORT_GENERATION_PROMPT = """You are a report generator. Create a comprehensive summary report.

Goal: {goal}
Task Results: {results}
Reflection: {reflection}

Generate a clear, structured report in Markdown format covering:
1. **Goal**: What was requested
2. **Approach**: How it was tackled
3. **Results**: What was accomplished
4. **Key Findings**: Important discoveries or outputs
5. **Challenges**: Any issues encountered
6. **Recommendations**: Next steps or improvements

Be concise but thorough."""


class OrchestratorAgent:
    """
    Central orchestrator that coordinates the multi-agent workflow using LangGraph.

    The orchestrator manages the lifecycle of goal execution:
    goal → analysis → decomposition → routing → execution → reflection → report
    """

    def __init__(
        self,
        memory_agent: Any = None,
        research_agent: Any = None,
        execution_agent: Any = None,
        reflection_agent: Any = None,
        strategy_engine: Any = None,
        task_classifier: Any = None,
        learning_engine: Any = None,
        experience_replay: Any = None,
    ) -> None:
        """
        Initialize the orchestrator with specialist agents.

        Args:
            memory_agent: Agent for memory operations.
            research_agent: Agent for research tasks.
            execution_agent: Agent for code execution tasks.
            reflection_agent: Agent for post-execution reflection.
        """
        settings = get_settings()
        self.llm = ChatAnthropic(
            model=settings.anthropic_model,
            api_key=settings.anthropic_api_key.get_secret_value(),
            temperature=settings.llm_temperature,
            max_tokens=settings.llm_max_tokens,
        )
        self.memory_agent = memory_agent
        self.research_agent = research_agent
        self.execution_agent = execution_agent
        self.reflection_agent = reflection_agent
        self.strategy_engine = strategy_engine
        self.task_classifier = task_classifier
        self.learning_engine = learning_engine
        self.experience_replay = experience_replay
        self._graph = self._build_graph()

    # -----------------------------------------------------------------------
    # Graph construction
    # -----------------------------------------------------------------------

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph StateGraph for the orchestration workflow."""
        graph = StateGraph(AgentStateDict)

        # Register nodes
        graph.add_node("analyze_goal", self._analyze_goal)
        graph.add_node("recall_memories", self._recall_memories)
        graph.add_node("replay_experiences", self._replay_experiences)
        graph.add_node("decompose_tasks", self._decompose_tasks)
        graph.add_node("classify_task", self._classify_task)
        graph.add_node("select_strategy", self._select_strategy)
        graph.add_node("route_task", self._route_task)
        graph.add_node("execute_research", self._execute_research)
        graph.add_node("execute_task", self._execute_task)
        graph.add_node("execute_memory_op", self._execute_memory_op)
        graph.add_node("integrate_results", self._integrate_results)
        graph.add_node("dynamic_replan", self._dynamic_replan)
        graph.add_node("reflect", self._reflect)
        graph.add_node("extract_learnings", self._extract_learnings)
        graph.add_node("update_strategies", self._update_strategies)
        
        # Phase 6 Autonomous Research Nodes
        graph.add_node("knowledge_gap_detection", self._knowledge_gap_detection)
        graph.add_node("goal_generation", self._goal_generation)
        graph.add_node("curiosity_evaluation", self._curiosity_evaluation)
        graph.add_node("research_director", self._research_director)
        graph.add_node("research_portfolio", self._research_portfolio)
        graph.add_node("knowledge_graph_update", self._knowledge_graph_update)
        
        graph.add_node("generate_report", self._generate_report)

        # Define edges
        graph.add_edge(START, "analyze_goal")
        graph.add_edge("analyze_goal", "recall_memories")
        graph.add_edge("recall_memories", "replay_experiences")
        graph.add_edge("replay_experiences", "decompose_tasks")
        graph.add_edge("decompose_tasks", "classify_task")
        graph.add_edge("classify_task", "select_strategy")
        graph.add_edge("select_strategy", "route_task")

        # Conditional routing based on task type
        graph.add_conditional_edges(
            "route_task",
            self._routing_decision,
            {
                "research": "execute_research",
                "execution": "execute_task",
                "memory": "execute_memory_op",
                "reflect": "reflect",
                "complete": "generate_report",
            },
        )

        # All execution paths lead to integration
        graph.add_edge("execute_research", "integrate_results")
        graph.add_edge("execute_task", "integrate_results")
        graph.add_edge("execute_memory_op", "integrate_results")

        # Integration decides next step
        graph.add_conditional_edges(
            "integrate_results",
            self._completion_check,
            {
                "continue": "dynamic_replan",
                "reflect": "reflect",
                "failed": "reflect",
            },
        )

        graph.add_edge("dynamic_replan", "classify_task")
        graph.add_edge("reflect", "extract_learnings")
        graph.add_edge("extract_learnings", "update_strategies")
        graph.add_edge("update_strategies", "generate_report")
        graph.add_edge("generate_report", END)

        return graph

    def compile(self, checkpointer: Any = None) -> Any:
        """
        Compile the graph with optional checkpointer for persistence.

        Args:
            checkpointer: LangGraph checkpointer for state persistence.

        Returns:
            Compiled LangGraph graph ready for execution.
        """
        kwargs: dict[str, Any] = {}
        if checkpointer:
            kwargs["checkpointer"] = checkpointer
        return self._graph.compile(**kwargs)

    # -----------------------------------------------------------------------
    # Node implementations
    # -----------------------------------------------------------------------

    async def _analyze_goal(self, state: AgentStateDict) -> dict[str, Any]:
        """Analyze the user's goal to understand intent, scope, and requirements."""
        logger.info("Analyzing goal", goal=state["goal"][:100])
        start_time = time.monotonic()

        context_str = ""
        if state.get("goal_analysis") and isinstance(state["goal_analysis"], dict):
            context_str = f"\nAdditional Context: {json.dumps(state['goal_analysis'])}"

        prompt = GOAL_ANALYSIS_PROMPT.format(
            goal=state["goal"],
            context=context_str,
        )

        response = await self.llm.ainvoke([
            SystemMessage(content="You are an expert goal analyst. Respond only with valid JSON."),
            HumanMessage(content=prompt),
        ])

        try:
            analysis = json.loads(response.content)
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            content = str(response.content)
            start = content.find("{")
            end = content.rfind("}") + 1
            if start >= 0 and end > start:
                analysis = json.loads(content[start:end])
            else:
                analysis = {
                    "intent": state["goal"],
                    "scope": "medium",
                    "domain": "general",
                    "constraints": [],
                    "success_criteria": ["Goal completed successfully"],
                    "required_capabilities": ["research", "execution"],
                    "estimated_complexity": 5,
                    "risks": [],
                }

        duration_ms = int((time.monotonic() - start_time) * 1000)
        logger.info("Goal analysis complete", duration_ms=duration_ms, scope=analysis.get("scope"))

        return {
            "goal_analysis": analysis,
            "status": "planning",
        }

    async def _recall_memories(self, state: AgentStateDict) -> dict[str, Any]:
        """Recall relevant memories from previous sessions."""
        logger.info("Recalling relevant memories")

        memories: list[dict[str, Any]] = []

        if self.memory_agent:
            try:
                recalled = await self.memory_agent.recall(
                    query=state["goal"],
                    user_id=state["user_id"],
                    limit=5,
                )
                memories = [
                    {
                        "id": str(m.get("id", "")),
                        "content": m.get("content", ""),
                        "memory_type": m.get("memory_type", ""),
                        "importance_score": m.get("importance_score", 0.0),
                        "relevance_score": m.get("relevance_score", 0.0),
                    }
                    for m in recalled
                ]
                logger.info("Memories recalled", count=len(memories))
            except Exception as e:
                logger.warning("Memory recall failed, continuing without memories", error=str(e))

        return {"retrieved_memories": memories}

    async def _replay_experiences(self, state: AgentStateDict) -> dict[str, Any]:
        """Replay past experiences for context."""
        logger.info("Replaying past experiences")
        
        experiences = []
        if self.experience_replay:
            try:
                # We fetch some generic past successes/failures related to the goal
                experiences = await self.experience_replay.get_similar_experiences(
                    task=state["goal"], limit=3
                )
            except Exception as e:
                logger.warning("Experience replay failed", error=str(e))
                
        context = ""
        if experiences:
            context = "Past relevant experiences:\n" + "\n".join([e.context_summary for e in experiences])
            
        return {"experience_context": context}

    async def _decompose_tasks(self, state: AgentStateDict) -> dict[str, Any]:
        """Decompose the goal into executable tasks."""
        logger.info("Decomposing goal into tasks")
        start_time = time.monotonic()

        memories_str = json.dumps(state.get("retrieved_memories", [])[:3])
        analysis_str = json.dumps(state.get("goal_analysis", {}))

        prompt = TASK_DECOMPOSITION_PROMPT.format(
            goal=state["goal"],
            analysis=analysis_str,
            memories=memories_str,
        )

        response = await self.llm.ainvoke([
            SystemMessage(content="You are an expert task planner. Respond only with a valid JSON array."),
            HumanMessage(content=prompt),
        ])

        try:
            tasks = json.loads(response.content)
        except json.JSONDecodeError:
            content = str(response.content)
            start = content.find("[")
            end = content.rfind("]") + 1
            if start >= 0 and end > start:
                tasks = json.loads(content[start:end])
            else:
                # Fallback: create a single research task
                tasks = [{
                    "id": "task_1",
                    "title": "Research and execute goal",
                    "description": state["goal"],
                    "agent_type": "research",
                    "priority": 1,
                    "dependencies": [],
                }]

        # Validate and normalize tasks
        validated_tasks = []
        for task in tasks:
            validated_tasks.append({
                "id": task.get("id", f"task_{len(validated_tasks) + 1}"),
                "title": task.get("title", "Unnamed Task"),
                "description": task.get("description", ""),
                "agent_type": task.get("agent_type", "research"),
                "priority": task.get("priority", 3),
                "dependencies": task.get("dependencies", []),
                "status": "pending",
            })

        duration_ms = int((time.monotonic() - start_time) * 1000)
        logger.info(
            "Task decomposition complete",
            task_count=len(validated_tasks),
            duration_ms=duration_ms,
        )

        return {
            "task_plan": validated_tasks,
            "current_task_index": 0,
            "status": "executing",
        }

    async def _classify_task(self, state: AgentStateDict) -> dict[str, Any]:
        """Classify the current task type."""
        task_plan = state.get("task_plan", [])
        current_idx = state.get("current_task_index", 0)
        
        if current_idx >= len(task_plan):
            return {"task_classification": None}
            
        current_task = task_plan[current_idx]
        logger.info("Classifying task", task_id=current_task.get("id"))
        
        classification = None
        if self.task_classifier:
            try:
                classification = await self.task_classifier.classify(
                    task_description=current_task.get("description", ""),
                    context=state.get("goal", ""),
                )
            except Exception as e:
                logger.error("Task classification failed", error=str(e))
                
        return {"task_classification": classification}

    async def _select_strategy(self, state: AgentStateDict) -> dict[str, Any]:
        """Select the best execution strategy for the task."""
        classification = state.get("task_classification")
        if not classification or not self.strategy_engine:
            return {"selected_strategy": None}
            
        logger.info("Selecting strategy for task type", task_type=classification.get("task_type"))
        
        strategy = None
        try:
            # We would normally convert Enum to string or pass directly
            task_type = classification.get("task_type")
            task_plan = state.get("task_plan", [])
            current_idx = state.get("current_task_index", 0)
            current_task = task_plan[current_idx] if current_idx < len(task_plan) else {}
            
            # get_best_strategy uses semantic search
            strategy = await self.strategy_engine.get_best_strategy(
                task_type=task_type,
                context=current_task.get("description", ""),
            )
        except Exception as e:
            logger.error("Strategy selection failed", error=str(e))
            
        strategy_dict = None
        if strategy:
            strategy_dict = {
                "id": str(strategy.id),
                "name": strategy.name,
                "steps": strategy.steps,
            }
            logger.info("Strategy selected", strategy_name=strategy.name)
            
        return {"selected_strategy": strategy_dict}

    async def _route_task(self, state: AgentStateDict) -> dict[str, Any]:
        """Route the current task to the appropriate agent."""
        task_plan = state.get("task_plan", [])
        current_idx = state.get("current_task_index", 0)

        if current_idx >= len(task_plan):
            logger.info("All tasks completed, moving to reflection")
            return {"next_agent": "reflect"}

        current_task = task_plan[current_idx]

        # Check if dependencies are satisfied
        completed_ids = set(state.get("task_results", {}).keys())
        deps = current_task.get("dependencies", [])
        unsatisfied = [d for d in deps if d not in completed_ids]

        if unsatisfied:
            logger.warning(
                "Task has unsatisfied dependencies, skipping",
                task_id=current_task["id"],
                unsatisfied=unsatisfied,
            )
            # Skip to next task
            return {
                "current_task_index": current_idx + 1,
                "next_agent": current_task.get("agent_type", "research"),
            }

        agent_type = current_task.get("agent_type", "research")
        logger.info(
            "Routing task",
            task_id=current_task["id"],
            task_title=current_task["title"],
            agent_type=agent_type,
        )

        return {"next_agent": agent_type}

    def _routing_decision(self, state: AgentStateDict) -> str:
        """Determine which agent to route to based on state."""
        next_agent = state.get("next_agent", "reflect")
        task_plan = state.get("task_plan", [])
        current_idx = state.get("current_task_index", 0)
        iteration = state.get("iteration_count", 0)
        max_iter = state.get("max_iterations", 20)

        # Safety: prevent infinite loops
        if iteration >= max_iter:
            logger.warning("Max iterations reached, forcing reflection", iteration=iteration)
            return "reflect"

        if current_idx >= len(task_plan):
            return "reflect"

        if next_agent == "reflect":
            return "reflect"

        # Map agent types to node names
        routing_map = {
            "research": "research",
            "execution": "execution",
            "memory": "memory",
        }
        return routing_map.get(next_agent, "research")

    async def _execute_research(self, state: AgentStateDict) -> dict[str, Any]:
        """Execute a research task using the research agent."""
        task_plan = state.get("task_plan", [])
        current_idx = state.get("current_task_index", 0)
        current_task = task_plan[current_idx] if current_idx < len(task_plan) else {}

        logger.info("Executing research task", task_id=current_task.get("id"))
        start_time = time.monotonic()

        result: dict[str, Any]
        if self.research_agent:
            try:
                result = await self.research_agent.execute(
                    task=current_task,
                    context={
                        "goal": state["goal"],
                        "previous_results": state.get("task_results", {}),
                        "memories": state.get("retrieved_memories", []),
                    },
                )
            except Exception as e:
                logger.error("Research agent failed", error=str(e))
                result = {"status": "failed", "error": str(e)}
        else:
            # Fallback: use the LLM directly for research
            response = await self.llm.ainvoke([
                SystemMessage(content="You are a research assistant. Provide thorough, well-sourced answers."),
                HumanMessage(content=f"Research the following:\n\n{current_task.get('description', state['goal'])}"),
            ])
            result = {
                "status": "completed",
                "output": str(response.content),
                "source": "llm_fallback",
            }

        duration_ms = int((time.monotonic() - start_time) * 1000)
        task_id = current_task.get("id", f"task_{current_idx}")

        task_results = dict(state.get("task_results", {}))
        task_results[task_id] = {
            **result,
            "task_id": task_id,
            "duration_ms": duration_ms,
        }

        return {
            "task_results": task_results,
            "iteration_count": state.get("iteration_count", 0) + 1,
        }

    async def _execute_task(self, state: AgentStateDict) -> dict[str, Any]:
        """Execute a computational task using the execution agent."""
        task_plan = state.get("task_plan", [])
        current_idx = state.get("current_task_index", 0)
        current_task = task_plan[current_idx] if current_idx < len(task_plan) else {}

        logger.info("Executing computational task", task_id=current_task.get("id"))
        start_time = time.monotonic()

        result: dict[str, Any]
        if self.execution_agent:
            try:
                result = await self.execution_agent.execute(
                    task=current_task,
                    context={
                        "goal": state["goal"],
                        "previous_results": state.get("task_results", {}),
                    },
                )
            except Exception as e:
                logger.error("Execution agent failed", error=str(e))
                result = {"status": "failed", "error": str(e)}
        else:
            # Fallback: use the LLM to generate a response
            response = await self.llm.ainvoke([
                SystemMessage(content="You are a technical execution assistant. Provide actionable solutions."),
                HumanMessage(content=f"Execute the following task:\n\n{current_task.get('description', state['goal'])}"),
            ])
            result = {
                "status": "completed",
                "output": str(response.content),
                "source": "llm_fallback",
            }

        duration_ms = int((time.monotonic() - start_time) * 1000)
        task_id = current_task.get("id", f"task_{current_idx}")

        task_results = dict(state.get("task_results", {}))
        task_results[task_id] = {
            **result,
            "task_id": task_id,
            "duration_ms": duration_ms,
        }

        return {
            "task_results": task_results,
            "iteration_count": state.get("iteration_count", 0) + 1,
        }

    async def _execute_memory_op(self, state: AgentStateDict) -> dict[str, Any]:
        """Execute a memory operation (store or recall)."""
        task_plan = state.get("task_plan", [])
        current_idx = state.get("current_task_index", 0)
        current_task = task_plan[current_idx] if current_idx < len(task_plan) else {}

        logger.info("Executing memory operation", task_id=current_task.get("id"))

        result: dict[str, Any]
        if self.memory_agent:
            try:
                result = await self.memory_agent.execute(
                    task=current_task,
                    context={
                        "goal": state["goal"],
                        "previous_results": state.get("task_results", {}),
                        "user_id": state["user_id"],
                    },
                )
            except Exception as e:
                logger.error("Memory agent failed", error=str(e))
                result = {"status": "failed", "error": str(e)}
        else:
            result = {"status": "completed", "output": "Memory operation skipped (no memory agent)"}

        task_id = current_task.get("id", f"task_{current_idx}")
        task_results = dict(state.get("task_results", {}))
        task_results[task_id] = {**result, "task_id": task_id}

        return {
            "task_results": task_results,
            "iteration_count": state.get("iteration_count", 0) + 1,
        }

    async def _integrate_results(self, state: AgentStateDict) -> dict[str, Any]:
        """Integrate task results and determine next steps."""
        task_plan = state.get("task_plan", [])
        current_idx = state.get("current_task_index", 0)
        task_results = state.get("task_results", {})

        current_task = task_plan[current_idx] if current_idx < len(task_plan) else {}
        task_id = current_task.get("id", f"task_{current_idx}")
        current_result = task_results.get(task_id, {})

        logger.info(
            "Integrating results",
            task_id=task_id,
            status=current_result.get("status", "unknown"),
        )

        # Move to next task
        new_index = current_idx + 1

        # Check if current task failed
        errors = list(state.get("errors", []))
        if current_result.get("status") == "failed":
            errors.append({
                "task_id": task_id,
                "agent_type": current_task.get("agent_type", "unknown"),
                "error_type": "task_failure",
                "message": current_result.get("error", "Unknown error"),
                "recoverable": True,
            })

        return {
            "current_task_index": new_index,
            "errors": errors,
        }

    async def _dynamic_replan(self, state: AgentStateDict) -> dict[str, Any]:
        """Dynamically adjust the plan if tasks fail or new discoveries are made."""
        logger.info("Evaluating dynamic replan")
        # In Phase 5, this would use LLM to check if remaining tasks need adjusting
        # For now, it simply tracks the replan count and proceeds.
        return {
            "replan_count": state.get("replan_count", 0) + 1
        }

    def _completion_check(self, state: AgentStateDict) -> str:
        """Check if all tasks are complete or if we should continue."""
        task_plan = state.get("task_plan", [])
        current_idx = state.get("current_task_index", 0)
        iteration = state.get("iteration_count", 0)
        max_iter = state.get("max_iterations", 20)
        errors = state.get("errors", [])

        # Safety check
        if iteration >= max_iter:
            logger.warning("Max iterations reached during completion check")
            return "reflect"

        # All tasks done
        if current_idx >= len(task_plan):
            return "reflect"

        # Too many errors
        if len(errors) > len(task_plan) * 2:
            logger.warning("Too many errors, forcing reflection")
            return "failed"

        return "continue"

    async def _reflect(self, state: AgentStateDict) -> dict[str, Any]:
        """Run the reflection agent to analyze the session."""
        logger.info("Starting reflection phase")

        reflection: dict[str, Any]
        if self.reflection_agent:
            try:
                reflection = await self.reflection_agent.execute(
                    goal=state["goal"],
                    task_plan=state.get("task_plan", []),
                    task_results=state.get("task_results", {}),
                    errors=state.get("errors", []),
                )
            except Exception as e:
                logger.error("Reflection agent failed", error=str(e))
                reflection = {
                    "successes": [],
                    "failures": [str(e)],
                    "root_causes": ["Reflection agent error"],
                    "improvements": [],
                    "confidence_score": 0.0,
                }
        else:
            # Fallback: LLM-based reflection
            task_results = state.get("task_results", {})
            successes = [tid for tid, r in task_results.items() if r.get("status") == "completed"]
            failures = [tid for tid, r in task_results.items() if r.get("status") == "failed"]

            reflection = {
                "successes": [f"Task {tid} completed successfully" for tid in successes],
                "failures": [f"Task {tid} failed: {task_results[tid].get('error', 'unknown')}" for tid in failures],
                "root_causes": [],
                "improvements": [],
                "confidence_score": len(successes) / max(len(task_results), 1),
            }

        return {
            "reflection": reflection,
            "status": "reflecting",
        }

    async def _extract_learnings(self, state: AgentStateDict) -> dict[str, Any]:
        """Extract learnings from reflection."""
        logger.info("Extracting learnings from reflection")
        
        learnings = []
        if self.learning_engine and state.get("reflection"):
            try:
                # We need a session ID, fallback to uuid4 if None
                session_id = uuid.UUID(state.get("session_id")) if state.get("session_id") else uuid.uuid4()
                learnings = await self.learning_engine.extract_learnings(
                    session_id=session_id,
                    reflections=[state.get("reflection")],
                    task_results=state.get("task_results", {}),
                )
                logger.info("Extracted learnings", count=len(learnings))
            except Exception as e:
                logger.error("Learning extraction failed", error=str(e))
                
        return {"learnings": learnings}

    async def _update_strategies(self, state: AgentStateDict) -> dict[str, Any]:
        """Update strategies based on the new learnings."""
        logger.info("Updating strategies")
        # Logic to update strategy confidence happens here or via the LearningEngine
        return {}

    # -----------------------------------------------------------------------
    # Phase 6 Autonomous Research Nodes
    # ---------------------------------------------------------------------------

    async def _knowledge_gap_detection(self, state: AgentStateDict) -> dict[str, Any]:
        """Detect knowledge gaps across the system."""
        logger.info("Detecting knowledge gaps")
        return {"knowledge_gaps": []}

    async def _goal_generation(self, state: AgentStateDict) -> dict[str, Any]:
        """Generate goals based on gaps."""
        logger.info("Generating autonomous goals")
        return {"generated_goals": []}

    async def _curiosity_evaluation(self, state: AgentStateDict) -> dict[str, Any]:
        """Evaluate curiosity scores for goals."""
        logger.info("Evaluating curiosity for goals")
        return {}

    async def _research_director(self, state: AgentStateDict) -> dict[str, Any]:
        """Manage research tracks and allocate tasks."""
        logger.info("Director reviewing goals and tracks")
        return {"research_tracks": []}

    async def _research_portfolio(self, state: AgentStateDict) -> dict[str, Any]:
        """Update research portfolios."""
        logger.info("Updating research portfolios")
        return {"portfolio_summary": {}}

    async def _knowledge_graph_update(self, state: AgentStateDict) -> dict[str, Any]:
        """Update the Neo4j knowledge graph with new concepts."""
        logger.info("Updating Knowledge Graph")
        return {}

    async def _generate_report(self, state: AgentStateDict) -> dict[str, Any]:
        """Generate a summary report of the goal execution."""
        logger.info("Generating final report")

        prompt = REPORT_GENERATION_PROMPT.format(
            goal=state["goal"],
            results=json.dumps(state.get("task_results", {}), default=str)[:4000],
            reflection=json.dumps(state.get("reflection", {}), default=str)[:2000],
        )

        response = await self.llm.ainvoke([
            SystemMessage(content="You are a concise report generator. Use Markdown formatting."),
            HumanMessage(content=prompt),
        ])

        return {
            "final_report": str(response.content),
            "status": "complete",
        }

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    async def execute_goal(
        self,
        goal: str,
        user_id: str,
        session_id: str | None = None,
        max_iterations: int = 20,
        context: str | None = None,
        checkpointer: Any = None,
    ) -> dict[str, Any]:
        """
        Execute a goal through the full agent pipeline.

        Args:
            goal: High-level goal description.
            user_id: User identifier.
            session_id: Optional session ID for persistence.
            max_iterations: Maximum agent loop iterations.
            context: Additional context for the goal.
            checkpointer: Optional LangGraph checkpointer.

        Returns:
            Final state dictionary with results and report.
        """
        if not session_id:
            session_id = str(uuid.uuid4())

        initial_state: AgentStateDict = {
            "goal": goal,
            "goal_analysis": {"context": context} if context else None,
            "task_plan": [],
            "current_task_index": 0,
            "messages": [],
            "task_results": {},
            "errors": [],
            "retrieved_memories": [],
            "retrieved_knowledge": [],
            "reflection": None,
            "session_id": session_id,
            "user_id": user_id,
            "iteration_count": 0,
            "max_iterations": max_iterations,
            "status": "planning",
            "next_agent": None,
            "task_classification": None,
            "selected_strategy": None,
            "strategy_executions": {},
            "experience_context": None,
            "learnings": [],
            "replan_count": 0,
            "final_report": None,
        }

        compiled = self.compile(checkpointer=checkpointer)

        config = {"configurable": {"thread_id": session_id}}

        logger.info(
            "Starting goal execution",
            session_id=session_id,
            goal=goal[:100],
            max_iterations=max_iterations,
        )

        final_state = await compiled.ainvoke(initial_state, config=config)

        logger.info(
            "Goal execution complete",
            session_id=session_id,
            status=final_state.get("status"),
            tasks_completed=len(final_state.get("task_results", {})),
        )

        return dict(final_state)
