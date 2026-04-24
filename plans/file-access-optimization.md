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

## Review Notes (Prickett)

### Identity Resolution

**Issue**: The plan uses `event.message_obj.self_id` for persona identification. However, `self_id` is a social platform account identifier (e.g., QQ number), not the persona name.

**Solution**: Instead reference from `astr_main_agent.py`:
```python
# How astrbot resolves the current persona
from astrbot.core.star.persona_manager import PersonaManager
persona_id = await plugin_context.persona_manager.resolve_selected_persona(
    umo=event.unified_msg_origin,
    conversation_persona_id=req.conversation.persona_id,
    ...
)
```
For now, since there's only one persona ("prickett"), this can be simplified to a configured default value `self.default_persona`.

### Replace Monkey-Patch with `on_req_llm`

**Issue**: The current implementation monkey-patches `_ensure_persona_and_skills` in `astr_main_agent.py`, which is fragile and hard to maintain.

**Solution**: Use the standard `on_req_llm` hook (as seen in `long_term_memory.py:151`):
```python
async def on_req_llm(self, event: AstrMessageEvent, req: ProviderRequest) -> None:
    """当触发 LLM 请求前，调用此方法修改 req"""
    # Read self_prompt.md and inject into req.system_prompt
    self_prompt_path = self._get_persona_file_path(event, "self_prompt.md")
    if self_prompt_path.exists():
        content = self_prompt_path.read_text(encoding='utf-8').strip()
        if content:
            req.system_prompt += f"\n# Self Instructions\n\n{content}\n"
```
This eliminates:
- The fragile monkey-patch
- The `initialize`/`terminate` patch/restore logic
- Direct dependency on `astr_main_agent` internals

### Deprecate `get_self_prompt_file_path`

- Keep the old tool but change its return to a deprecation warning
- Remove it entirely in the next major version

### Updated Acceptance Criteria
- [ ] `read_self_prompt` tool allows reading without specifying a path
- [ ] `update_self_prompt` tool handles `replace`/`append`/`prepend` modes
- [ ] Files stored in `plugin_data/astrbot-memory-plugin/memory/<persona>/self_prompt.md`
- [ ] Warning logs on missing self prompt (not auto-create)
- [ ] Self prompt injection via `on_req_llm` instead of monkey-patch
- [ ] `get_self_prompt_file_path` returns deprecation warning
- [ ] Backward compatibility maintained for existing tools
