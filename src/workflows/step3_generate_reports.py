"""
Step 3: Generate global reports
"""
from typing import Dict, Any, Optional

from .config import WorkflowConfig
from .state_manager import StateManager

STEP_NUMBER = 3


def run(
    state_manager: StateManager,
    year: int,
    all_editors: Optional[Dict[str, Any]] = None,
    force: bool = False
) -> Dict[str, Any]:
    """
    Execute the report generation step
    
    Args:
        state_manager: State manager instance
        year: Target year
        all_editors: Editor data from step 2 (optional)
        force: Force re-execution
    
    Returns:
        Report generation summary
    """
    step_config = WorkflowConfig.get_step(STEP_NUMBER)
    
    # Check if already completed
    if not force and state_manager.is_step_completed(STEP_NUMBER):
        print(f"[Step {STEP_NUMBER}] Already completed")
        return state_manager.get_step_data(STEP_NUMBER)
    
    # Verify previous step is completed
    if not state_manager.is_step_completed(2):
        raise RuntimeError("Step 2 must be completed before running Step 3")
    
    # Load editor data from state if not provided
    if all_editors is None:
        all_editors = state_manager.get_step_data(2)
    
    print(f"[Step {STEP_NUMBER}] Starting: {step_config.name}")
    state_manager.mark_step_started(STEP_NUMBER)
    
    try:
        report_summary = _generate_reports(all_editors, year, state_manager)
        
        state_manager.clear_partial_data(STEP_NUMBER)
        state_manager.mark_step_completed(STEP_NUMBER, report_summary)
        
        print(f"[Step {STEP_NUMBER}] Completed: Workflow finished successfully!")
        return report_summary
        
    except Exception as e:
        state_manager.log_error(STEP_NUMBER, str(e))
        raise


def _generate_reports(
    all_editors: Dict[str, Any],
    year: int,
    state_manager: StateManager
) -> Dict[str, Any]:
    """
    Core logic for generating reports
    """
    # Load partial progress
    partial = state_manager.get_partial_data(STEP_NUMBER) or {
        "generated": [],
        "reports": []
    }
    
    generated = partial["generated"]
    reports = partial["reports"]
    
    # TODO: Implement actual report generation logic
    # Example:
    #
    # for lang, editors in all_editors.items():
    #     if lang in generated:
    #         continue
    #     
    #     report = create_report(lang, editors, year)
    #     reports.append(report)
    #     generated.append(lang)
    #     
    #     state_manager.set_partial_data(STEP_NUMBER, {
    #         "generated": generated,
    #         "reports": reports
    #     })
    
    return {
        "year": year,
        "total_languages": len(all_editors),
        "reports_generated": reports,
        "status": "completed"
    }