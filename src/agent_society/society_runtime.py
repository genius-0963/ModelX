"""
Society Runtime - Manages agent society and collaboration

The SocietyRuntime is responsible for:
- Managing agent society lifecycle
- Facilitating agent collaboration
- Coordinating multi-agent tasks
- Managing society resources
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


logger = logging.getLogger(__name__)


class SocietyStatus(Enum):
    """Status of agent society"""
    FORMING = "forming"
    ACTIVE = "active"
    DISSOLVING = "dissolving"
    DISSOLVED = "dissolved"


@dataclass
class Society:
    """An agent society"""
    society_id: str
    name: str
    members: Set[str]
    purpose: str
    status: SocietyStatus = SocietyStatus.FORMING
    created_at: float = field(default_factory=lambda: datetime.now().timestamp())
    resources: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_member(self, agent_id: str) -> None:
        """Add a member to the society"""
        self.members.add(agent_id)
    
    def remove_member(self, agent_id: str) -> None:
        """Remove a member from the society"""
        self.members.discard(agent_id)
    
    def is_member(self, agent_id: str) -> bool:
        """Check if an agent is a member"""
        return agent_id in self.members


@dataclass
class Collaboration:
    """A collaboration between agents"""
    collaboration_id: str
    participants: Set[str]
    task: str
    society_id: Optional[str] = None
    started_at: float = field(default_factory=lambda: datetime.now().timestamp())
    ended_at: Optional[float] = None
    status: str = "active"
    results: Dict[str, Any] = field(default_factory=dict)


class SocietyRuntime:
    """
    Runtime for agent society management.
    
    Provides:
    - Society creation and management
    - Agent collaboration coordination
    - Resource sharing
    - Society lifecycle management
    """
    
    def __init__(self):
        self._societies: Dict[str, Society] = {}
        self._agent_societies: Dict[str, Set[str]] = defaultdict(set)
        self._collaborations: Dict[str, Collaboration] = {}
        
        # Statistics
        self._societies_created = 0
        self._collaborations_started = 0
        self._collaborations_completed = 0
    
    async def initialize(self) -> None:
        """Initialize the society runtime"""
        logger.info("SocietyRuntime initialized")
    
    async def create_society(
        self,
        name: str,
        purpose: str,
        initial_members: Optional[List[str]] = None,
        resources: Optional[Dict[str, Any]] = None,
    ) -> Society:
        """
        Create a new agent society.
        
        Args:
            name: Society name
            purpose: Society purpose
            initial_members: Initial member agent IDs
            resources: Initial resources
            
        Returns:
            Created society
        """
        society_id = f"society_{datetime.now().timestamp()}"
        
        society = Society(
            society_id=society_id,
            name=name,
            members=set(initial_members or []),
            purpose=purpose,
            resources=resources or {},
            status=SocietyStatus.ACTIVE,
        )
        
        self._societies[society_id] = society
        
        # Track agent memberships
        for member_id in society.members:
            self._agent_societies[member_id].add(society_id)
        
        self._societies_created += 1
        
        logger.info(f"Created society {society_id}: {name} with {len(society.members)} members")
        return society
    
    async def dissolve_society(self, society_id: str) -> bool:
        """
        Dissolve a society.
        
        Args:
            society_id: Society identifier
            
        Returns:
            True if dissolved successfully
        """
        if society_id not in self._societies:
            logger.warning(f"Society {society_id} not found")
            return False
        
        society = self._societies[society_id]
        society.status = SocietyStatus.DISSOLVED
        
        # Remove agent memberships
        for member_id in society.members:
            self._agent_societies[member_id].discard(society_id)
        
        logger.info(f"Dissolved society {society_id}")
        return True
    
    async def add_to_society(
        self,
        society_id: str,
        agent_id: str,
    ) -> bool:
        """
        Add an agent to a society.
        
        Args:
            society_id: Society identifier
            agent_id: Agent identifier
            
        Returns:
            True if added successfully
        """
        if society_id not in self._societies:
            logger.warning(f"Society {society_id} not found")
            return False
        
        society = self._societies[society_id]
        society.add_member(agent_id)
        self._agent_societies[agent_id].add(society_id)
        
        logger.debug(f"Added agent {agent_id} to society {society_id}")
        return True
    
    async def remove_from_society(
        self,
        society_id: str,
        agent_id: str,
    ) -> bool:
        """
        Remove an agent from a society.
        
        Args:
            society_id: Society identifier
            agent_id: Agent identifier
            
        Returns:
            True if removed successfully
        """
        if society_id not in self._societies:
            logger.warning(f"Society {society_id} not found")
            return False
        
        society = self._societies[society_id]
        society.remove_member(agent_id)
        self._agent_societies[agent_id].discard(society_id)
        
        logger.debug(f"Removed agent {agent_id} from society {society_id}")
        return True
    
    async def start_collaboration(
        self,
        participants: List[str],
        task: str,
        society_id: Optional[str] = None,
    ) -> Collaboration:
        """
        Start a collaboration between agents.
        
        Args:
            participants: List of participant agent IDs
            task: Task to collaborate on
            society_id: Optional society ID
            
        Returns:
            Collaboration object
        """
        collaboration_id = f"collab_{datetime.now().timestamp()}"
        
        collaboration = Collaboration(
            collaboration_id=collaboration_id,
            participants=set(participants),
            task=task,
            society_id=society_id,
        )
        
        self._collaborations[collaboration_id] = collaboration
        self._collaborations_started += 1
        
        logger.info(f"Started collaboration {collaboration_id} with {len(participants)} agents")
        return collaboration
    
    async def end_collaboration(
        self,
        collaboration_id: str,
        results: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        End a collaboration.
        
        Args:
            collaboration_id: Collaboration identifier
            results: Collaboration results
            
        Returns:
            True if ended successfully
        """
        if collaboration_id not in self._collaborations:
            logger.warning(f"Collaboration {collaboration_id} not found")
            return False
        
        collaboration = self._collaborations[collaboration_id]
        collaboration.ended_at = datetime.now().timestamp()
        collaboration.status = "completed"
        collaboration.results = results or {}
        
        self._collaborations_completed += 1
        
        logger.info(f"Ended collaboration {collaboration_id}")
        return True
    
    def get_society(self, society_id: str) -> Optional[Society]:
        """Get a society by ID"""
        return self._societies.get(society_id)
    
    def get_agent_societies(self, agent_id: str) -> List[Society]:
        """Get all societies for an agent"""
        society_ids = self._agent_societies.get(agent_id, set())
        return [
            self._societies[sid]
            for sid in society_ids
            if sid in self._societies
        ]
    
    def get_collaboration(self, collaboration_id: str) -> Optional[Collaboration]:
        """Get a collaboration by ID"""
        return self._collaborations.get(collaboration_id)
    
    def get_active_collaborations(self) -> List[Collaboration]:
        """Get all active collaborations"""
        return [
            collab for collab in self._collaborations.values()
            if collab.status == "active"
        ]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get society runtime metrics"""
        return {
            "societies_created": self._societies_created,
            "active_societies": sum(
                1 for s in self._societies.values()
                if s.status == SocietyStatus.ACTIVE
            ),
            "collaborations_started": self._collaborations_started,
            "collaborations_completed": self._collaborations_completed,
            "active_collaborations": len(self.get_active_collaborations()),
            "total_members": sum(len(s.members) for s in self._societies.values()),
        }
