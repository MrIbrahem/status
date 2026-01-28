# Workflow Separation Plan

## Overview

This plan outlines the separation of the three main workflow steps into independent files within a `workflow/` directory, with full resume support for error recovery.

---

## Objectives

1. **Separate each step into its own file** for better maintainability
2. **Implement state management** to track progress and enable resumption
3. **Support partial resumption** within each step (checkpoint system)
4. **Centralize configuration** in a single config file
5. **Update all documentation** and AI assistant instructions

---

## Directory Structure

```
workflow/
├── __init__.py
├── config.py
├── state_manager.py
├── step1_retrieve_titles.py
├── step2_process_languages.py
├── step3_generate_reports.py
└── runner.py
```

---

## Implementation Tasks

### Phase 1: Core Infrastructure

| Task | File | Description |
|------|------|-------------|
| 1.1 | `workflow/config.py` | Create central configuration with step definitions and file paths |
| 1.2 | `workflow/state_manager.py` | Implement state persistence with JSON storage |
| 1.3 | `workflow/__init__.py` | Export public API |

### Phase 2: Step Separation

| Task | File | Description |
|------|------|-------------|
| 2.1 | `workflow/step1_retrieve_titles.py` | Extract title retrieval logic with checkpoint support |
| 2.2 | `workflow/step2_process_languages.py` | Extract language processing with per-language checkpoints |
| 2.3 | `workflow/step3_generate_reports.py` | Extract report generation logic |

### Phase 3: Orchestration

| Task | File | Description |
|------|------|-------------|
| 3.1 | `workflow/runner.py` | Implement workflow orchestrator with resume capability |

### Phase 4: Documentation Updates

| Task | File | Description |
|------|------|-------------|
| 4.1 | `README.md` | Update main readme with workflow usage instructions |
| 4.2 | `docs/workflow.md` | Create detailed workflow documentation |
| 4.3 | `docs/configuration.md` | Document all configuration options |
| 4.4 | `docs/error_handling.md` | Document error recovery procedures |
| 4.5 | `.github/copilot-instructions.md` | Update Copilot instructions for workflow changes |
| 4.6 | `CLAUDE.md` | Update Claude instructions for workflow changes |

---

## File Specifications

### config.py

```python
# Central configuration containing:
# - STATE_FILE: Path to state JSON file
# - OUTPUT_DIR: Output directory path
# - STEPS: Dictionary mapping step numbers to StepConfig objects
#   - StepConfig: number, name, module_name
```

### state_manager.py

```python
# StateManager class providing:
# - load/save state to JSON
# - mark_step_started(step)
# - mark_step_completed(step, data)
# - is_step_completed(step)
# - get_step_data(step)
# - set_partial_data(step, data) - for checkpoints within steps
# - get_partial_data(step)
# - log_error(step, error)
# - reset() / reset_from_step(step)
# - get_resume_point()
```

### Step Files (step1, step2, step3)

```python
# Each step file contains:
# - STEP_NUMBER constant
# - run(state_manager, **kwargs) - main entry point
# - _internal_logic() - actual implementation
# - validate_output() - output validation
```

### runner.py

```python
# WorkflowRunner class providing:
# - run_all(year, languages, resume=True, force_from_step=None)
# - run_step(step, **kwargs)
# - status() - display current state
# - reset(from_step=None)
```

---

## State File Schema

```json
{
  "current_step": 2,
  "completed_steps": [1],
  "step_data": {
    "1": ["title1", "title2"],
    "2_partial": {
      "processed": ["ar", "en"],
      "editors": {}
    }
  },
  "last_updated": "2026-01-28T10:30:00",
  "started_at": "2026-01-28T10:00:00",
  "errors": [
    {
      "step": 2,
      "error": "Connection timeout",
      "timestamp": "2026-01-28T10:25:00"
    }
  ]
}
```

---

## Documentation Updates

### README.md Updates

Add new section:

```markdown
## Workflow Usage

### Running the Complete Workflow

from workflow import WorkflowRunner

runner = WorkflowRunner()
runner.run_all(year=2024, languages=["ar", "en", "fr"])

### Resuming After Error

# Automatically resumes from last checkpoint
runner.run_all(year=2024, languages=["ar", "en", "fr"], resume=True)

### Checking Status

runner.status()

### Resetting Workflow

runner.reset()  # Full reset
runner.reset(from_step=2)  # Reset from step 2
```

### docs/workflow.md (New File)

Create comprehensive documentation covering:

1. **Architecture Overview**
   - Step separation rationale
   - State management design
   - Checkpoint system

2. **Step Details**
   - Step 1: Retrieve Titles
   - Step 2: Process Languages
   - Step 3: Generate Reports

3. **Resume Capabilities**
   - Automatic resume on restart
   - Partial step resumption
   - Manual reset options

4. **Error Handling**
   - Error logging
   - Recovery procedures
   - Troubleshooting guide

### .github/copilot-instructions.md Updates

Add section:

```markdown
## Workflow Module

The workflow is split into three independent steps in the `workflow/` directory:

- `step1_retrieve_titles.py` - Retrieves medicine titles
- `step2_process_languages.py` - Processes multiple languages
- `step3_generate_reports.py` - Generates final reports

Key classes:
- `WorkflowRunner` - Main orchestrator
- `StateManager` - Handles persistence and resume
- `WorkflowConfig` - Central configuration

When modifying workflow:
1. Update the relevant step file
2. Update config.py if adding new steps
3. Update state_manager.py if changing state schema
4. Run tests for affected steps
```

### CLAUDE.md Updates

Add section:

```markdown
## Workflow System

### Structure
- All workflow code is in `workflow/` directory
- Configuration is centralized in `workflow/config.py`
- State is persisted in `workflow_state.json`

### Key Patterns
- Each step has a `run()` function as entry point
- Steps use `state_manager.set_partial_data()` for checkpoints
- Steps verify previous step completion before running

### Adding New Steps
1. Create `workflow/stepN_name.py`
2. Add step to `WorkflowConfig.STEPS` in config.py
3. Update `runner.py` to include new step
4. Update documentation
```

---

## Testing Plan

| Test | Description |
|------|-------------|
| Unit: StateManager | Test all state management functions |
| Unit: Each Step | Test step logic in isolation |
| Integration: Full Run | Test complete workflow execution |
| Integration: Resume | Test resume after simulated failure |
| Integration: Partial Resume | Test checkpoint recovery within steps |

---

## Migration Steps

1. Create `workflow/` directory
2. Implement `config.py` and `state_manager.py`
3. Extract step logic to individual files
4. Implement `runner.py`
5. Update imports in existing code
6. Run tests
7. Update all documentation
8. Update AI assistant instructions

---

## Rollback Plan

If issues arise:
1. Keep original code in separate branch
2. State file can be deleted to start fresh
3. Individual steps can be reverted independently

---

## Success Criteria

- [ ] All three steps execute independently
- [ ] Workflow resumes correctly after interruption
- [ ] Partial progress within steps is preserved
- [ ] All documentation is updated
- [ ] AI assistant instructions are current
- [ ] All tests pass