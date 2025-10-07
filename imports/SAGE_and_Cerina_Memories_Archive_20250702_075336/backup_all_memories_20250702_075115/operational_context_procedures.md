# Operational Context Management Procedures

1. **Start of Conversation**
- Check active context using get_current_config
- Load relevant memories based on initial user query
- Establish baseline context for current session

2. **During Operations**
- Call think_about_task_adherence before any significant action
- Use think_about_collected_information after gathering data
- Call think_about_whether_you_are_done before concluding tasks

3. **Context Switching Protocol**
- Save current context state before switching
- Load relevant context for new task
- Maintain awareness of context stack

4. **Memory Updates**
- Write new memories for reusable information
- Update existing memories when new patterns emerge
- Cross-reference related memories

5. **Error Prevention**
- Never reconstruct context from conversation summaries
- Always maintain active context awareness
- Use proper context management tools instead of inference

6. **Recovery Steps**
- If context is unclear, check active configuration
- If memory access is needed, use list_memories and read_memory
- If context is lost, rebuild using proper tools rather than inference