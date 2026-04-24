# File Access Optimization Plan

## Goal
Simplify the process of reading and updating persona-specific configuration files (specifically `self_prompt`) to reduce the number of tool calls and manual path management for the LLM.

## Proposed Changes

### 1. Persona-Based Path Architecture
Transition from a flat file structure based on `self_id` to a directory-based structure per persona to allow for future expansion (e.g., adding short-term memory files).
- **Current**: `self.self_prompt_path / f"{self_id}.md"`
- **Proposed**: `self.memory_path / <persona_id> / "self_prompt.md"`
- **Identity Mapping**: Use `event.message_obj.self_id` as the `<persona_id>` for now to maintain identity consistency.

### 2. New Simplified Tools
Implement high-level tools that abstract away path discovery.

#### `read_self_prompt(event)`
- Resolve the persona path based on the event.
- Read the content of `self_prompt.md`.
- **Error Handling**: If the file is missing, output a warning log and return a message indicating the prompt is not yet defined.

#### `update_self_prompt(event, mode, content)`
- **Arguments**: 
    - `mode`: `replace` | `append` | `prepend`
    - `content`: The text to write.
- Resolve the persona path.
- Implement update logic:
    - `replace`: Overwrite the file with new content.
    - `append`: Append content to the end of the file.
    - `prepend`: Insert content at the beginning of the file.
- Ensure parent directories are created automatically.

### 3. Refactoring & Integration
- **Centralized Path Utility**: Create a private helper method `_get_persona_file_path(event, filename)` to ensure consistent path resolution across the plugin.
- **Update Initialization**: Modify the monkey-patch for `_ensure_persona_and_skills` to use the new persona-based path structure.
- **Backward Compatibility**: Maintain existing `retrieve_memory` and `store_memory` tools for general-purpose relative path access.

## Acceptance Criteria
- [ ] `read_self_prompt` tool allows reading without specifying a path.
- [ ] `update_self_prompt` tool correctly handles all three modes (`replace`, `append`, `prepend`).
- [ ] Files are stored in `plugin_data/astrbot-memory-plugin/memory/<persona>/self_prompt.md`.
- [ ] Warning logs are triggered when attempting to read a non-existent self prompt.
- [ ] The system prompt is successfully injected into the agent's context using the new pathing.
