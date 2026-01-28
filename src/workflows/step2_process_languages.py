"""
Step 2: Process languages
"""
from typing import List, Dict, Any, Optional

from .config import WorkflowConfig
from .state_manager import StateManager

STEP_NUMBER = 2


def run(
    state_manager: StateManager,
    year: int,
    languages: List[str],
    titles: Optional[List[str]] = None,
    force: bool = False
) -> Dict[str, Any]:
    """
    Execute the language processing step
    
    Args:
        state_manager: State manager instance
        year: Target year
        languages: List of language codes
        titles: Titles from step 1 (optional, loaded from state if not provided)
        force: Force re-execution
    
    Returns:
        Dictionary of editors per language
    """
    step_config = WorkflowConfig.get_step(STEP_NUMBER)
    
    # Check if already completed
    if not force and state_manager.is_step_completed(STEP_NUMBER):
        print(f"[Step {STEP_NUMBER}] Already completed, loading cached results...")
        return state_manager.get_step_data(STEP_NUMBER)
    
    # Verify previous step is completed
    if not state_manager.is_step_completed(1):
        raise RuntimeError("Step 1 must be completed before running Step 2")
    
    # Load titles from state if not provided
    if titles is None:
        titles = state_manager.get_step_data(1)
    
    print(f"[Step {STEP_NUMBER}] Starting: {step_config.name}")
    print(f"[Step {STEP_NUMBER}] Processing {len(languages)} languages...")
    state_manager.mark_step_started(STEP_NUMBER)
    
    try:
        all_editors = _process_languages(year, languages, titles, state_manager)
        
        state_manager.clear_partial_data(STEP_NUMBER)
        state_manager.mark_step_completed(STEP_NUMBER, all_editors)
        
        print(f"[Step {STEP_NUMBER}] Completed")
        return all_editors
        
    except Exception as e:
        state_manager.log_error(STEP_NUMBER, str(e))
        raise


def _process_languages(
    year: int,
    languages: List[str],
    titles: List[str],
    state_manager: StateManager
) -> Dict[str, Any]:
    """
    Core logic for processing languages
    Supports partial resumption per language
    """
    # Load partial progress
    partial = state_manager.get_partial_data(STEP_NUMBER) or {
        "processed": [],
        "editors": {}
    }
    
    processed_langs = partial["processed"]
    all_editors = partial["editors"]
    
    for lang in languages:
        # Skip already processed languages
        if lang in processed_langs:
            print(f"  [Skip] {lang} (already processed)")
            continue
        
        print(f"  [Processing] {lang}")
        
        try:
            # TODO: Implement actual language processing logic here
            editors_for_lang = _process_single_language(lang, year, titles)
            
            all_editors[lang] = editors_for_lang
            processed_langs.append(lang)
            
            # Save checkpoint after each language
            state_manager.set_partial_data(STEP_NUMBER, {
                "processed": processed_langs,
                "editors": all_editors
            })
            
        except Exception as e:
            print(f"  [Error] {lang}: {e}")
            raise
    
    return all_editors


def _process_single_language(lang: str, year: int, titles: List[str]) -> Dict[str, Any]:
    """
    Process a single language
    
    Args:
        lang: Language code
        year: Target year
        titles: List of titles to process
    
    Returns:
        Editor data for this language
    """
    # TODO: Implement actual processing logic
    return {}