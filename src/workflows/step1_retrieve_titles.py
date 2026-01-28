"""
Step 1: Retrieve medicine titles
"""
from typing import List

from .config import WorkflowConfig
from .state_manager import StateManager

STEP_NUMBER = 1


def run(state_manager: StateManager, force: bool = False) -> List[str]:
    """
    Execute the title retrieval step
    
    Args:
        state_manager: State manager instance
        force: Force re-execution even if completed
    
    Returns:
        List of retrieved titles
    """
    step_config = WorkflowConfig.get_step(STEP_NUMBER)
    
    # Check if already completed
    if not force and state_manager.is_step_completed(STEP_NUMBER):
        print(f"[Step {STEP_NUMBER}] Already completed, loading cached results...")
        return state_manager.get_step_data(STEP_NUMBER)
    
    print(f"[Step {STEP_NUMBER}] Starting: {step_config.name}")
    state_manager.mark_step_started(STEP_NUMBER)
    
    try:
        titles = _retrieve_medicine_titles(state_manager)
        
        # Clear partial data and save final results
        state_manager.clear_partial_data(STEP_NUMBER)
        state_manager.mark_step_completed(STEP_NUMBER, titles)
        
        print(f"[Step {STEP_NUMBER}] Completed: Retrieved {len(titles)} titles")
        return titles
        
    except Exception as e:
        state_manager.log_error(STEP_NUMBER, str(e))
        raise


def _retrieve_medicine_titles(state_manager: StateManager) -> List[str]:
    """
    Core logic for retrieving medicine titles
    Supports partial resumption
    """
    # Load partial progress if exists
    partial = state_manager.get_partial_data(STEP_NUMBER) or {
        "titles": [],
        "last_offset": 0
    }
    
    titles = partial["titles"]
    offset = partial["last_offset"]
    
    # TODO: Implement actual retrieval logic here
    # Example structure with checkpointing:
    #
    # while has_more_data:
    #     batch = fetch_batch(offset)
    #     titles.extend(batch)
    #     offset += len(batch)
    #     
    #     # Save checkpoint periodically
    #     state_manager.set_partial_data(STEP_NUMBER, {
    #         "titles": titles,
    #         "last_offset": offset
    #     })
    
    return titles


def validate_output(titles: List[str]) -> bool:
    """Validate step output"""
    return isinstance(titles, list)