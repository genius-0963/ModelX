"""
Voice Assistant Integration - Connects Voice Assistant to ModelX Cognitive Modules
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from src.cognition.cognitive_bus import (
    CognitiveBus, CognitiveEventType, get_cognitive_bus, initialize_cognitive_bus
)
from src.reasoning.planner import Planner
from src.reasoning.drift_detector import EnvironmentalDriftDetector
from src.reasoning.reactive_replanner import ReactiveRePlanner
from src.memory.memory_fabric import MemoryFabric
from src.memory.working_memory import WorkingMemory
from src.memory.context_compressor import ContextCompressor
from src.cognition.hierarchical_agent_registry import HierarchicalAgentRegistry
from src.cognition.delegation_protocol import DelegationProtocol
from src.cognition.swarm import HierarchicalSwarm
from src.tools.mcp_client import MCPClient
from src.tools.mcp_discovery import discover_mcp_capabilities
from src.tools.base import MCPTool
from src.autonomous_development.architecture_evolver import ArchitectureEvolver
from src.config.settings import get_settings

logger = logging.getLogger(__name__)


@dataclass
class VoiceAssistantContext:
    """Context passed between voice assistant and cognitive modules"""
    user_id: str = "voice_user"
    session_id: str = ""
    conversation_history: List[Dict[str, str]] = None
    active_plan_id: Optional[str] = None
    working_memory: List[Dict] = None

    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []
        if self.working_memory is None:
            self.working_memory = []


class VoiceAssistantIntegration:
    """
    Integrates Voice Assistant with all ModelX cognitive modules.
    Acts as the bridge between voice I/O and the AGI brain.
    """

    def __init__(self, settings: Any = None):
        self.settings = settings or get_settings()
        self.context = VoiceAssistantContext()

        # Core cognitive modules (lazy initialized)
        self._cognitive_bus: Optional[CognitiveBus] = None
        self._planner: Optional[Planner] = None
        self._drift_detector: Optional[EnvironmentalDriftDetector] = None
        self._replanner: Optional[ReactiveRePlanner] = None
        self._memory_fabric: Optional[MemoryFabric] = None
        self._working_memory: Optional[WorkingMemory] = None
        self._context_compressor: Optional[ContextCompressor] = None
        self._agent_registry: Optional[HierarchicalAgentRegistry] = None
        self._delegation_protocol: Optional[DelegationProtocol] = None
        self._swarm: Optional[HierarchicalSwarm] = None
        self._mcp_client: Optional[MCPClient] = None
        self._architecture_evolver: Optional[ArchitectureEvolver] = None

        # Tool registry
        self._tools: Dict[str, Any] = {}

        # State
        self._initialized = False
        self._running = False

    async def initialize(self):
        """Initialize all cognitive modules"""
        if self._initialized:
            return

        logger.info("Initializing Voice Assistant Integration...")

        # 1. Cognitive Bus (central event hub)
        self._cognitive_bus = await initialize_cognitive_bus()

        # 2. Memory Systems
        await self._init_memory()

        # 3. Reasoning & Planning
        await self._init_reasoning()

        # 4. Multi-Agent System
        await self._init_multi_agent()

        # 5. Tools & MCP
        await self._init_tools()

        # 6. Self-Improvement
        await self._init_self_improvement()

        # Register event handlers
        self._register_handlers()

        self._initialized = True
        logger.info("Voice Assistant Integration ready!")

    async def _init_memory(self):
        """Initialize memory systems"""
        from src.memory.memory_fabric import MemoryFabric
        from src.memory.working_memory import WorkingMemory
        from src.memory.context_compressor import ContextCompressor

        # Memory fabric (uses vector store + graph + episodic)
        self._memory_fabric = MemoryFabric(
            qdrant_client=self._get_qdrant_client(),
        )
        await self._memory_fabric.initialize()

        # Working memory for current session
        self._working_memory = WorkingMemory(
            ttl=300
        )

        # Context compressor for long conversations
        self._context_compressor = ContextCompressor(
            llm_client=self._get_llm_client(),
            vector_store=self._memory_fabric.qdrant_client,
            memory_fabric=self._memory_fabric
        )

    async def _init_reasoning(self):
        """Initialize reasoning and planning"""
        from src.reasoning.planner import Planner

        llm = self._get_llm_client()

        self._planner = Planner(llm_client=llm, memory_fabric=self._memory_fabric)
        await self._planner.initialize(enable_drift_detection=True)

        # Drift detector and replanner are initialized inside planner
        self._drift_detector = self._planner._drift_detector
        self._replanner = self._planner._replanner

    async def _init_multi_agent(self):
        """Initialize hierarchical multi-agent system"""
        from src.cognition.hierarchical_agent_registry import HierarchicalAgentRegistry
        from src.cognition.delegation_protocol import DelegationProtocol
        from src.cognition.swarm import HierarchicalSwarm, create_default_swarm

        # Agent registry with Neo4j
        self._agent_registry = HierarchicalAgentRegistry(
            neo4j_client=self._get_neo4j_client(),
            embedding_model=self._get_embedding_model()
        )
        await self._agent_registry.initialize()

        # Delegation protocol
        self._delegation_protocol = DelegationProtocol(
            agent_registry=self._agent_registry,
            message_broker=self._get_message_broker()
        )

        # Create default swarm
        self._swarm = await create_default_swarm(
            agent_registry=self._agent_registry,
            delegation_protocol=self._delegation_protocol,
            cognitive_bus=self._cognitive_bus
        )

    async def _init_tools(self):
        """Initialize MCP tools and ModelX tools"""
        from src.tools.mcp_client import MCPClient
        from src.tools.mcp_discovery import discover_mcp_capabilities, MCPCatalogManager
        from src.tools.base import MCPTool

        self._mcp_client = MCPClient()

        # Connect to configured MCP servers (if any)
        mcp_servers = getattr(self.settings, 'mcp_servers', [])
        for server_config in mcp_servers:
            await self._mcp_client.connect_server(server_config)

        # Discover and register MCP tools
        mcp_tools = await discover_mcp_capabilities(self._mcp_client)
        for tool_schema in mcp_tools:
            mcp_tool = self._mcp_client.get_tool_schema(
                tool_schema.metadata["server"],
                tool_schema.metadata["original_name"]
            )
            if mcp_tool:
                wrapper = MCPTool.create_from_mcp(
                    self._mcp_client,
                    tool_schema.metadata["server"],
                    mcp_tool
                )
                self._tools[wrapper.name] = wrapper

        # Also register built-in ModelX tools
        await self._register_builtin_tools()

    async def _init_self_improvement(self):
        """Initialize architecture evolver for self-improvement"""
        if self.settings.agi_architecture_evolution:
            from src.autonomous_development.architecture_evolver import ArchitectureEvolver

            self._architecture_evolver = ArchitectureEvolver(
                llm_client=self._get_llm_client(),
                repo_root=".",
                test_runner=self._run_tests,
                approval_callback=self._request_approval,
                auto_apply_safe=self.settings.agi_auto_apply_safe
            )
            await self._architecture_evolver.initialize()

    def _register_handlers(self):
        """Register cognitive bus event handlers"""
        self._cognitive_bus.subscribe(
            CognitiveEventType.USER_SPEECH,
            self._handle_user_speech
        )
        self._cognitive_bus.subscribe(
            CognitiveEventType.PLAN_COMPLETED,
            self._handle_plan_completed
        )
        self._cognitive_bus.subscribe(
            CognitiveEventType.DRIFT_DETECTED,
            self._handle_drift_detected
        )
        self._cognitive_bus.subscribe(
            CognitiveEventType.MEMORY_COMPRESSED,
            self._handle_memory_compressed
        )

    async def process_user_input(self, text: str) -> str:
        """
        Main entry point: process user speech/text and generate response.
        This orchestrates all cognitive modules.
        """
        # 1. Add to conversation history
        self.context.conversation_history.append({
            "role": "user",
            "content": text
        })

        # 2. Store in working memory
        await self._working_memory.add({
            "type": "user_input",
            "content": text,
            "timestamp": asyncio.get_event_loop().time()
        })

        # 3. Emit to cognitive bus
        await self._cognitive_bus.emit(self._cognitive_bus.create_event(
            event_type=CognitiveEventType.USER_SPEECH,
            source="voice_assistant",
            payload={"text": text, "user_id": self.context.user_id}
        ))

        # 4. Determine response strategy
        response = await self._generate_response(text)

        # 5. Add to conversation history
        self.context.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        # 6. Store assistant response
        await self._working_memory.add({
            "type": "assistant_response",
            "content": response,
            "timestamp": asyncio.get_event_loop().time()
        })

        # 7. Check if context compression needed
        await self._maybe_compress_context()

        return response

    async def _generate_response(self, user_input: str) -> str:
        """Generate response using appropriate cognitive module"""

        # Check if this is a task requiring planning
        if await self._is_planning_task(user_input):
            return await self._handle_planning_task(user_input)

        # Check if this requires delegation to agents
        if await self._is_delegation_task(user_input):
            return await self._handle_delegation_task(user_input)

        # Check if this is a tool use request
        if await self._is_tool_task(user_input):
            return await self._handle_tool_task(user_input)

        # Default: conversational response with context
        return await self._handle_conversation(user_input)

    async def _is_planning_task(self, text: str) -> bool:
        """Determine if input requires planning"""
        planning_keywords = [
            "plan", "schedule", "organize", "steps", "how to",
            "create a plan", "roadmap", "timeline", "milestones"
        ]
        text_lower = text.lower()
        return any(kw in text_lower for kw in planning_keywords)

    async def _handle_planning_task(self, text: str) -> str:
        """Handle planning requests"""
        # Create plan
        plan = await self._planner.create_plan(
            goal=text,
            context={"user_id": self.context.user_id, "conversation": self.context.conversation_history[-5:]}
        )

        self.context.active_plan_id = plan.plan_id

        # Execute plan with drift monitoring
        async def state_getter():
            return await self._get_execution_state()

        async def context_getter():
            return {"goal": text, "user_id": self.context.user_id}

        success = await self._planner.execute_plan(
            plan.plan_id,
            get_state_func=state_getter,
            get_context_func=context_getter
        )

        if success:
            return f"I've created and executed a plan for: {text}. The task is complete."
        else:
            return f"I created a plan but encountered issues during execution. Let me know if you'd like me to adjust."

    async def _is_delegation_task(self, text: str) -> bool:
        """Determine if input requires agent delegation"""
        delegation_keywords = [
            "delegate", "assign", "have someone", "get an agent",
            "team", "specialist", "expert"
        ]
        text_lower = text.lower()
        return any(kw in text_lower for kw in delegation_keywords)

    async def _handle_delegation_task(self, text: str) -> str:
        """Handle multi-agent delegation"""
        result = await self._swarm.execute_hierarchical_task(
            goal=text,
            required_capabilities=["general_reasoning", "task_execution"]
        )
        return f"Task delegated and completed: {result}"

    async def _is_tool_task(self, text: str) -> bool:
        """Determine if input requires tool use"""
        # Check if any tool matches
        for tool_name, tool in self._tools.items():
            if tool_name.lower() in text.lower():
                return True
        return False

    async def _handle_tool_task(self, text: str) -> str:
        """Execute tool based on user request"""
        # Simple tool matching - in production, use LLM to select tool
        for tool_name, tool in self._tools.items():
            if tool_name.lower() in text.lower():
                try:
                    # Extract parameters from text (simplified)
                    params = await self._extract_tool_params(text, tool)
                    result = await tool.execute(**params)
                    return f"Tool {tool_name} result: {result}"
                except Exception as e:
                    return f"Error using {tool_name}: {e}"
        return "I couldn't find the right tool for that request."

    async def _handle_conversation(self, text: str) -> str:
        """Handle general conversation with full context"""
        # Build rich context
        context = await self._build_rich_context(text)

        # Use LLM with context
        llm = self._get_llm_client()
        prompt = self._build_conversation_prompt(text, context)

        response = await llm.ainvoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)

    async def _build_rich_context(self, current_input: str) -> Dict:
        """Build context from all memory systems"""
        # Get relevant memories
        memories = await self._memory_fabric.retrieve(
            query=current_input,
            limit=5
        )

        # Get working memory
        wm = await self._working_memory.get_recent(10)

        # Get active plan status
        plan_status = None
        if self.context.active_plan_id:
            plan = self._planner.get_plan(self.context.active_plan_id)
            if plan:
                plan_status = {
                    "plan_id": plan.plan_id,
                    "goal": plan.goal,
                    "status": plan.status.value,
                    "progress": f"{len([a for a in plan.actions if a.status == 'completed'])}/{len(plan.actions)}"
                }

        return {
            "memories": memories,
            "working_memory": wm,
            "active_plan": plan_status,
            "conversation_history": self.context.conversation_history[-10:],
            "available_tools": list(self._tools.keys()),
            "available_agents": await self._agent_registry.list_agents()
        }

    def _build_conversation_prompt(self, user_input: str, context: Dict) -> str:
        """Build prompt for conversational response"""
        memory_str = "\n".join([f"- {m['content'][:200]}" for m in context.get("memories", [])])
        wm_str = "\n".join([f"- {m['content'][:100]}" for m in context.get("working_memory", [])])
        plan_str = ""
        if context.get("active_plan"):
            p = context["active_plan"]
            plan_str = f"\nActive Plan: {p['goal']} ({p['progress']} steps done)"

        history = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in context.get("conversation_history", [])
        ])

        return f"""You are a helpful AI assistant with access to planning, tools, and a team of agents.

Context:
Recent Memories:
{memory_str or "None"}

Working Memory:
{wm_str or "None"}

{plan_str}

Conversation History:
{history}

Current User Input: {user_input}

Respond naturally and helpfully. If the user needs a plan, tool, or delegation, acknowledge and I'll handle it."""

    async def _extract_tool_params(self, text: str, tool: Any) -> Dict:
        """Extract tool parameters from user text using LLM"""
        llm = self._get_llm_client()
        prompt = f"""Extract parameters for tool '{tool.name}' from user request.

Tool: {tool.name}
Description: {tool.description}
Parameters: {tool.parameters}

User: {text}

Return JSON with parameters:"""
        response = await llm.ainvoke(prompt)
        import json
        try:
            return json.loads(response.content)
        except:
            return {}

    async def _get_execution_state(self) -> Dict:
        """Get current execution state for drift detection"""
        return {
            "executed": [],
            "current_step": 0,
            "resources": {},
            "timestamp": asyncio.get_event_loop().time()
        }

    async def _maybe_compress_context(self):
        """Compress working memory if it gets too large"""
        stats = await self._working_memory.get_stats()
        if stats["token_usage"] / stats["max_tokens"] > 0.8:
            await self._context_compressor.compress(
                agent_id=self.context.user_id,
                working_memories=await self._working_memory.get_all()
            )
            await self._cognitive_bus.emit(self._cognitive_bus.create_event(
                event_type=CognitiveEventType.MEMORY_COMPRESSED,
                source="voice_assistant",
                payload={"agent_id": self.context.user_id}
            ))

    # Event handlers
    async def _handle_user_speech(self, event):
        """Handle user speech event"""
        logger.info(f"User speech received: {event.payload.get('text')}")

    async def _handle_plan_completed(self, event):
        """Handle plan completion"""
        logger.info(f"Plan completed: {event.payload}")
        self.context.active_plan_id = None

    async def _handle_drift_detected(self, event):
        """Handle environmental drift"""
        logger.warning(f"Drift detected: {event.payload}")
        # Could trigger proactive replanning

    async def _handle_memory_compressed(self, event):
        """Handle memory compression"""
        logger.info(f"Memory compressed: {event.payload}")

    # Dependency getters (override in subclass or configure)
    def _get_llm_client(self):
        """Get LLM client - integrate with your LLM setup"""
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=self.settings.anthropic_model,
            api_key=self.settings.anthropic_api_key.get_secret_value(),
            max_tokens=4096
        )

    def _get_embedding_model(self):
        """Get embedding model"""
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model=self.settings.embedding_model,
            api_key=self.settings.openai_api_key.get_secret_value()
        )

    def _get_neo4j_client(self):
        """Get Neo4j client"""
        from neo4j import AsyncGraphDatabase
        return AsyncGraphDatabase.driver(
            self.settings.neo4j_uri,
            auth=(self.settings.neo4j_user, self.settings.neo4j_password.get_secret_value())
        )

    def _get_qdrant_client(self):
        """Get Qdrant client"""
        from qdrant_client import AsyncQdrantClient
        return AsyncQdrantClient(url=self.settings.qdrant_url)

    def _get_message_broker(self):
        """Get message broker (Redis/RabbitMQ)"""
        import redis.asyncio as redis
        return redis.from_url(self.settings.redis_url)

    async def _register_builtin_tools(self):
        """Register built-in ModelX tools"""
        from src.tools.file_operations import FileOperationsTool
        from src.tools.shell_tool import ShellTool
        from src.tools.python_executor import PythonExecutorTool
        from src.tools.web_search import WebSearchTool

        tools = [
            FileOperationsTool(),
            ShellTool(),
            PythonExecutorTool(),
            WebSearchTool(),
        ]
        for tool in tools:
            self._tools[tool.name] = tool

    async def _run_tests(self, patch_id: str) -> Dict:
        """Test runner for architecture evolver"""
        import subprocess
        result = subprocess.run(
            ["pytest", "tests/", "-v", "--tb=short"],
            capture_output=True, text=True, timeout=300
        )
        return {
            "passed": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr
        }

    async def _request_approval(self, patch) -> bool:
        """Request human approval for patches"""
        # In production, integrate with UI/notification system
        logger.info(f"Approval requested for patch: {patch.patch_id}")
        return False  # Default: require explicit approval

    async def shutdown(self):
        """Clean shutdown"""
        self._running = False
        if self._cognitive_bus:
            await self._cognitive_bus.stop()
        if self._mcp_client:
            await self._mcp_client.disconnect_all()
        logger.info("Voice Assistant Integration shutdown complete")


# Factory function
async def create_voice_assistant_integration(settings: Any = None) -> VoiceAssistantIntegration:
    """Create and initialize voice assistant integration"""
    integration = VoiceAssistantIntegration(settings)
    await integration.initialize()
    return integration