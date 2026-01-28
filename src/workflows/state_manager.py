"""
Workflow state manager - tracks progress and supports resumption
"""
import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

from .config import WorkflowConfig


class StateManager:
    """Manages workflow state to allow resumption after errors"""
    
    def __init__(self, state_file: str = None):
        self.state_file = state_file or WorkflowConfig.STATE_FILE
        self.state = self._load_state()
    
    def _load_state(self) -> Dict[str, Any]:
        """Load state from file if exists"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._create_empty_state()
    
    def _create_empty_state(self) -> Dict[str, Any]:
        """Create a new empty state"""
        return {
            "current_step": 0,
            "completed_steps": [],
            "step_data": {},
            "last_updated": None,
            "started_at": None,
            "errors": []
        }
    
    def save(self) -> None:
        """Save current state to file"""
        self.state["last_updated"] = datetime.now().isoformat()
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def mark_step_started(self, step: int) -> None:
        """Mark a step as started"""
        self.state["current_step"] = step
        if not self.state["started_at"]:
            self.state["started_at"] = datetime.now().isoformat()
        self.save()
    
    def mark_step_completed(self, step: int, data: Any = None) -> None:
        """Mark a step as completed with its output data"""
        if step not in self.state["completed_steps"]:
            self.state["completed_steps"].append(step)
        self.state["step_data"][str(step)] = data
        self.state["current_step"] = step + 1
        self.save()
    
    def is_step_completed(self, step: int) -> bool:
        """Check if a step is completed"""
        return step in self.state["completed_steps"]
    
    def get_step_data(self, step: int) -> Optional[Any]:
        """Get output data from a completed step"""
        return self.state["step_data"].get(str(step))
    
    def set_partial_data(self, step: int, data: Any) -> None:
        """Save partial progress within a step"""
        key = f"{step}_partial"
        self.state["step_data"][key] = data
        self.save()
    
    def get_partial_data(self, step: int) -> Optional[Any]:
        """Get partial progress data for a step"""
        key = f"{step}_partial"
        return self.state["step_data"].get(key)
    
    def clear_partial_data(self, step: int) -> None:
        """Clear partial progress data after step completion"""
        key = f"{step}_partial"
        if key in self.state["step_data"]:
            del self.state["step_data"][key]
            self.save()
    
    def log_error(self, step: int, error: str) -> None:
        """Log an error for a step"""
        self.state["errors"].append({
            "step": step,
            "error": error,
            "timestamp": datetime.now().isoformat()
        })
        self.save()
    
    def reset(self) -> None:
        """Reset entire workflow state"""
        self.state = self._create_empty_state()
        self.save()
    
    def reset_from_step(self, step: int) -> None:
        """Reset workflow from a specific step onwards"""
        self.state["completed_steps"] = [s for s in self.state["completed_steps"] if s < step]
        self.state["current_step"] = step
        
        # Remove data for reset steps
        keys_to_remove = [k for k in self.state["step_data"].keys() if int(k.split("_")[0]) >= step]
        for key in keys_to_remove:
            del self.state["step_data"][key]
        
        self.save()
    
    def get_resume_point(self) -> int:
        """Get the step number to resume from"""
        if not self.state["completed_steps"]:
            return 1
        return max(self.state["completed_steps"]) + 1