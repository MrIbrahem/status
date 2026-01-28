"""
Workflow configuration settings
"""
from dataclasses import dataclass
from typing import Dict


@dataclass
class StepConfig:
    """Configuration for a single workflow step"""
    number: int
    name: str
    module_name: str


class WorkflowConfig:
    """Central configuration for the workflow system"""
    
    # File paths
    STATE_FILE = "workflow_state.json"
    OUTPUT_DIR = "output"
    
    # Step definitions
    STEPS: Dict[int, StepConfig] = {
        1: StepConfig(
            number=1,
            name="retrieve_titles",
            module_name="step1_retrieve_titles"
        ),
        2: StepConfig(
            number=2,
            name="process_languages",
            module_name="step2_process_languages"
        ),
        3: StepConfig(
            number=3,
            name="generate_reports",
            module_name="step3_generate_reports"
        ),
    }
    
    # Step count
    TOTAL_STEPS = len(STEPS)
    
    @classmethod
    def get_step(cls, step_number: int) -> StepConfig:
        """Get step configuration by number"""
        if step_number not in cls.STEPS:
            raise ValueError(f"Invalid step number: {step_number}")
        return cls.STEPS[step_number]
    
    @classmethod
    def get_module_name(cls, step_number: int) -> str:
        """Get module name for a step"""
        return cls.get_step(step_number).module_name