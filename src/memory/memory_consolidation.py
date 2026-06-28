'''memory_consolidation.py

Coordinates consolidation of memories across the hierarchy.
Provides a high‑level API that invokes the consolidation, abstraction, and forgetting engines.
''' 

import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from src.config.logging import get_logger
from src.db.repositories.memory_repo import MemoryRepository
from src.db.enums import MemoryType
from src.rag.embeddings import EmbeddingService

logger = get_logger(__name__)

class MemoryConsolidation:
    """Orchestrates the consolidation process.
    
    * Merges duplicate episodic entries.
    * Abstracts high‑level concepts into semantic memory.
    * Prunes low‑utility items via the forgetting engine.
    """

    def __init__(self, db_session, memory_repo: MemoryRepository, embedding_service: EmbeddingService):
        self.db_session = db_session
        self.memory_repo = memory_repo
        self.embedder = embedding_service
        self.similarity_threshold = 0.85
        self.consolidation_batch_size = 100

    async def run(self, user_id: uuid.UUID) -> Dict[str, int]:
        """Run the full memory consolidation pipeline.
        
        Returns:
            Dictionary with consolidation statistics.
        """
        logger.info(f"Running memory consolidation pipeline for user {user_id}")
        
        stats = {
            "consolidated": 0,
            "abstracted": 0,
            "forgotten": 0,
            "errors": 0
        }
        
        try:
            # Step 1: Consolidate duplicate episodic memories
            consolidated = await self._consolidation_engine(user_id)
            stats["consolidated"] = consolidated
            
            # Step 2: Abstract high-level concepts to semantic memory
            abstracted = await self._abstraction_engine(user_id)
            stats["abstracted"] = abstracted
            
            # Step 3: Prune low-utility memories
            forgotten = await self._forgetting_engine(user_id)
            stats["forgotten"] = forgotten
            
            logger.info(f"Memory consolidation complete: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error during memory consolidation: {e}")
            stats["errors"] += 1
            return stats

    async def _consolidation_engine(self, user_id: uuid.UUID) -> int:
        """Merge duplicate episodic memories based on semantic similarity."""
        consolidated_count = 0
        
        # Get recent episodic memories
        episodic_memories = await self.memory_repo.get_by_user_and_type(
            user_id, MemoryType.EPISODIC, limit=self.consolidation_batch_size
        )
        
        # Group by similarity
        for i, mem1 in enumerate(episodic_memories):
            for mem2 in episodic_memories[i+1:]:
                similarity = await self._compute_similarity(mem1.content, mem2.content)
                
                if similarity >= self.similarity_threshold:
                    # Merge memories - keep the one with higher importance
                    primary = mem1 if mem1.importance_score >= mem2.importance_score else mem2
                    secondary = mem2 if mem1.importance_score >= mem2.importance_score else mem1
                    
                    # Update primary with combined metadata
                    combined_metadata = {
                        **primary.metadata or {},
                        "consolidated_from": str(secondary.id),
                        "consolidation_date": datetime.now(timezone.utc).isoformat()
                    }
                    
                    await self.memory_repo.update(primary.id, metadata=combined_metadata)
                    await self.memory_repo.delete(secondary.id)
                    
                    consolidated_count += 1
                    logger.debug(f"Consolidated memory {secondary.id} into {primary.id}")
        
        return consolidated_count

    async def _abstraction_engine(self, user_id: uuid.UUID) -> int:
        """Extract high-level concepts from episodic memories and store as semantic."""
        abstracted_count = 0
        
        # Get episodic memories that haven't been abstracted
        episodic_memories = await self.memory_repo.get_by_user_and_type(
            user_id, MemoryType.EPISODIC, limit=50
        )
        
        for mem in episodic_memories:
            if not mem.metadata or not mem.metadata.get("abstracted"):
                # Create semantic abstraction
                abstract_content = await self._generate_abstraction(mem.content)
                
                if abstract_content:
                    await self.memory_repo.store_memory(
                        user_id=user_id,
                        content=abstract_content,
                        memory_type=MemoryType.SEMANTIC,
                        metadata={
                            "source_episodic_id": str(mem.id),
                            "abstraction_date": datetime.now(timezone.utc).isoformat()
                        },
                        importance_score=mem.importance_score * 0.9
                    )
                    
                    # Mark episodic as abstracted
                    await self.memory_repo.update(
                        mem.id, 
                        metadata={**(mem.metadata or {}), "abstracted": True}
                    )
                    
                    abstracted_count += 1
        
        return abstracted_count

    async def _forgetting_engine(self, user_id: uuid.UUID) -> int:
        """Prune low-utility memories based on importance and access patterns."""
        forgotten_count = 0
        
        # Get low-importance memories with low access count
        all_memories = await self.memory_repo.get_by_user(user_id, limit=200)
        
        for mem in all_memories:
            # Forgetting criteria:
            # - Low importance (< 0.3)
            # - Low access count (< 2)
            # - Old (created > 30 days ago)
            age_days = (datetime.now(timezone.utc) - mem.created_at).days
            
            if (mem.importance_score < 0.3 and 
                mem.access_count < 2 and 
                age_days > 30):
                
                await self.memory_repo.delete(mem.id)
                forgotten_count += 1
                logger.debug(f"Forgotten memory {mem.id} (importance: {mem.importance_score})")
        
        return forgotten_count

    async def _compute_similarity(self, text1: str, text2: str) -> float:
        """Compute semantic similarity between two texts using embeddings."""
        try:
            emb1 = await self.embedder.embed_text(text1)
            emb2 = await self.embedder.embed_text(text2)
            
            # Cosine similarity
            dot_product = sum(a * b for a, b in zip(emb1, emb2))
            magnitude1 = sum(a * a for a in emb1) ** 0.5
            magnitude2 = sum(b * b for b in emb2) ** 0.5
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            return dot_product / (magnitude1 * magnitude2)
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0

    async def _generate_abstraction(self, content: str) -> Optional[str]:
        """Generate a high-level abstraction from episodic content.
        
        This is a simplified implementation. In production, this would use
        an LLM to extract key concepts and patterns.
        """
        # Simplified abstraction: extract first sentence and key terms
        sentences = content.split('.')
        if sentences:
            return sentences[0].strip() + "."
        return content[:200] + "..."

    def __repr__(self):
        return "MemoryConsolidation()"
