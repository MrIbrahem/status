"""
Main workflow runner - orchestrates step execution with resume support
"""
import importlib
from typing import List, Optional

from .config import WorkflowConfig
from .state_manager import StateManager


class WorkflowRunner:
    """Orchestrates workflow execution with automatic resume capability"""
    
    def __init__(self, state_file: str = None):
        self.state_manager = StateManager(state_file)
        self._step_modules = {}
    
    def _get_step_module(self, step_number: int):
        """Dynamically load step module"""
        if step_number not in self._step_modules:
            module_name = WorkflowConfig.get_module_name(step_number)
            self._step_modules[step_number] = importlib.import_module(
                f".{module_name}", package="workflow"
            )
        return self._step_modules[step_number]
    
    def run_all(
        self,
        year: int,
        languages: List[str],
        resume: bool = True,
        force_from_step: Optional[int] = None
    ) -> None:
        """
        Run all workflow steps
        
        Args:
            year: Target year for processing
            languages: List of language codes to process
            resume: Whether to resume from last checkpoint (default: True)
            force_from_step: Force restart from a specific step
        """
        print("=" * 50)
        print("Starting Workflow")
        print("=" * 50)
        
        # Determine starting point
        if force_from_step:
            self.state_manager.reset_from_step(force_from_step)
            start_step = force_from_step
        elif resume:
            start_step = self.state_manager.get_resume_point()
            if start_step > 1:
                print(f"Resuming from step {start_step}")
        else:
            self.state_manager.reset()
            start_step = 1
        
        try:
            # Step 1: Retrieve titles
            if start_step <= 1:
                step1 = self._get_step_module(1)
                titles = step1.run(self.state_manager)
            else:
                titles = self.state_manager.get_step_data(1)
            
            # Step 2: Process languages
            if start_step <= 2:
                step2 = self._get_step_module(2)
                all_editors = step2.run(
                    self.state_manager, year, languages, titles
                )
            else:
                all_editors = self.state_manager.get_step_data(2)
            
            # Step 3: Generate reports
            if start_step <= 3:
                step3 = self._get_step_module(3)
                step3.run(self.state_manager, year, all_editors)
            
            print("\n" + "=" * 50)
            print("Workflow completed successfully!")
            print("=" * 50)
            
        except Exception as e:
            print(f"\nWorkflow stopped due to error: {e}")
            print(f"Resume later with: runner.run_all(..., resume=True)")
            raise
    
    def run_step(self, step: int, **kwargs) -> None:
        """Run a specific step only"""
        step_config = WorkflowConfig.get_step(step)
        print(f"Running step {step}: {step_config.name}")
        
        module = self._get_step_module(step)
        module.run(self.state_manager, **kwargs)
    
    def status(self) -> None:
        """Display current workflow status"""
        print("\nWorkflow Status:")
        print("-" * 30)
        
        for step_num in range(1, WorkflowConfig.TOTAL_STEPS + 1):
            step_config = WorkflowConfig.get_step(step_num)
            
            if self.state_manager.is_step_completed(step_num):
                status = "Completed"
                icon = "[x]"
            elif self.state_manager.state["current_step"] == step_num:
                status = "In Progress"
                icon = "[~]"
            else:
                status = "Pending"
                icon = "[ ]"
            
            print(f"  {icon} Step {step_num}: {step_config.name} - {status}")
        
        errors = self.state_manager.state["errors"]
        if errors:
            print(f"\nErrors logged: {len(errors)}")
    
    def reset(self, from_step: Optional[int] = None) -> None:
        """Reset workflow state"""
        if from_step:
            self.state_manager.reset_from_step(from_step)
            print(f"Reset from step {from_step}")
        else:
            self.state_manager.reset()
            print("Full reset completed")


if __name__ == "__main__":
    runner = WorkflowRunner()
    runner.status()