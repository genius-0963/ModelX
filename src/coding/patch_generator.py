"""Patch generator for creating code changes from plans."""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from .planner import ExecutionPlan, ExecutionStep, StepType
from .code_editor import FileChange


@dataclass
class GeneratedPatch:
    """Generated code patch."""
    file_changes: List[FileChange] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'file_changes': [
                {
                    'file_path': fc.file_path,
                    'operation': fc.operation,
                    'content': fc.content,
                    'line_start': fc.line_start,
                    'line_end': fc.line_end,
                    'old_content': fc.old_content,
                    'new_content': fc.new_content
                }
                for fc in self.file_changes
            ],
            'metadata': self.metadata,
            'confidence': self.confidence
        }


class PatchGenerator:
    """Generates code patches from execution plans."""

    def __init__(self, repository_path: str):
        self.repository_path = repository_path

    def generate_patch(self, plan: ExecutionPlan, context: Optional[Dict] = None) -> GeneratedPatch:
        """Generate patches from an execution plan."""
        context = context or {}
        patch = GeneratedPatch()
        patch.metadata = {
            'task_type': plan.task_type.value,
            'goal': plan.goal,
            'complexity': plan.complexity,
            'estimated_steps': plan.estimated_steps
        }

        # Generate patches based on plan steps
        for step in plan.steps:
            if step.step_type == StepType.GENERATE:
                file_changes = self._generate_from_step(step, context)
                patch.file_changes.extend(file_changes)
            elif step.step_type == StepType.APPLY:
                # APPLY steps typically reference previously generated content
                pass

        # Calculate confidence based on plan completeness
        patch.confidence = self._calculate_confidence(plan, patch)

        return patch

    def _generate_from_step(self, step: ExecutionStep, context: Dict) -> List[FileChange]:
        """Generate file changes from a single step."""
        file_changes = []

        # This is a placeholder for actual AI-based code generation
        # In production, this would integrate with an LLM or code generation model
        if step.parameters.get('focus') == 'test_generation':
            file_changes.append(FileChange(
                file_path=step.file_path or "tests/test_generated.py",
                operation='create',
                content=self._generate_test_stub(step.description)
            ))
        elif step.parameters.get('focus') == 'error_analysis':
            # Analysis step - no file changes
            pass
        else:
            # Generic code generation
            if step.file_path:
                file_changes.append(FileChange(
                    file_path=step.file_path,
                    operation='patch',
                    old_content="",
                    new_content=self._generate_code_stub(step.description)
                ))

        return file_changes

    def _generate_test_stub(self, description: str) -> str:
        """Generate a test file stub."""
        return f'''"""Generated test for: {description}"""

import pytest


def test_generated():
    """Test generated from task: {description}"""
    # TODO: Implement test logic
    assert True
'''

    def _generate_code_stub(self, description: str) -> str:
        """Generate a code stub."""
        return f'''# Generated code for: {description}
# TODO: Implement logic based on requirements
'''

    def _calculate_confidence(self, plan: ExecutionPlan, patch: GeneratedPatch) -> float:
        """Calculate confidence score for the generated patch."""
        confidence = 0.5  # Base confidence

        # Increase confidence if plan has clear structure
        if plan.estimated_steps > 0:
            confidence += 0.1

        # Increase confidence if file changes are generated
        if len(patch.file_changes) > 0:
            confidence += 0.2

        # Increase confidence if context is provided
        if plan.context:
            confidence += 0.1

        # Cap at 1.0
        return min(confidence, 1.0)

    def generate_bug_fix_patch(self, error_message: str, file_path: str, context: Dict) -> GeneratedPatch:
        """Generate a patch for bug fixing."""
        patch = GeneratedPatch()
        patch.metadata = {
            'task_type': 'bug_fix',
            'error_message': error_message,
            'file_path': file_path
        }

        # Generate fix based on error
        fix_code = self._generate_fix_for_error(error_message, context)
        
        patch.file_changes.append(FileChange(
            file_path=file_path,
            operation='patch',
            old_content=context.get('current_code', ''),
            new_content=fix_code
        ))

        patch.confidence = 0.7
        return patch

    def generate_feature_patch(self, feature_description: str, file_path: str, context: Dict) -> GeneratedPatch:
        """Generate a patch for feature development."""
        patch = GeneratedPatch()
        patch.metadata = {
            'task_type': 'feature_development',
            'feature_description': feature_description,
            'file_path': file_path
        }

        # Generate feature implementation
        feature_code = self._generate_feature_code(feature_description, context)
        
        patch.file_changes.append(FileChange(
            file_path=file_path,
            operation='patch',
            old_content=context.get('current_code', ''),
            new_content=feature_code
        ))

        patch.confidence = 0.6
        return patch

    def generate_refactor_patch(self, refactor_description: str, file_path: str, context: Dict) -> GeneratedPatch:
        """Generate a patch for refactoring."""
        patch = GeneratedPatch()
        patch.metadata = {
            'task_type': 'refactoring',
            'refactor_description': refactor_description,
            'file_path': file_path
        }

        # Generate refactored code
        refactored_code = self._generate_refactored_code(refactor_description, context)
        
        patch.file_changes.append(FileChange(
            file_path=file_path,
            operation='patch',
            old_content=context.get('current_code', ''),
            new_content=refactored_code
        ))

        patch.confidence = 0.65
        return patch

    def _generate_fix_for_error(self, error_message: str, context: Dict) -> str:
        """Generate fix code based on error message."""
        # Placeholder for actual error analysis and fix generation
        # In production, this would use pattern matching and code analysis
        current_code = context.get('current_code', '')
        
        # Simple heuristic: if it's a NameError, add the missing variable
        if 'NameError' in error_message:
            missing_name = error_message.split("'")[1]
            return f"{missing_name} = None\n{current_code}"
        
        # If it's an IndexError, add bounds checking
        if 'IndexError' in error_message:
            return f"""# Added bounds check
if len(data) > 0:
    {current_code}
else:
    raise ValueError("Index out of bounds")
"""
        
        # Default: return original code with comment
        return f"# Fix for: {error_message}\n{current_code}"

    def _generate_feature_code(self, feature_description: str, context: Dict) -> str:
        """Generate feature implementation code."""
        current_code = context.get('current_code', '')
        
        # Placeholder for actual feature generation
        return f"""# Feature: {feature_description}
{current_code}

# New feature implementation
def new_feature():
    '''Implement: {feature_description}'''
    # TODO: Implement feature logic
    pass
"""

    def _generate_refactored_code(self, refactor_description: str, context: Dict) -> str:
        """Generate refactored code."""
        current_code = context.get('current_code', '')
        
        # Placeholder for actual refactoring
        return f"""# Refactored: {refactor_description}
# Improved code structure and readability

{current_code}
"""
