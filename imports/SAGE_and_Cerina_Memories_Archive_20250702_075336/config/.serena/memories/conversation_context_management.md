# Conversation Context Management Guidelines

1. **Active Context Tracking**
- Always maintain awareness of current conversation thread
- Use active context flags instead of reconstructing from summaries
- Track conversation state changes in real-time

2. **Context Transition Rules**
- When switching topics, explicitly acknowledge the transition
- Preserve relevant context from previous topic if related
- Clear irrelevant context to prevent confusion

3. **Memory Integration**
- Use short-term memory for current conversation flow
- Convert important short-term context to long-term memories when appropriate
- Reference existing memories instead of reconstructing context

4. **Task Continuity**
- Maintain clear understanding of current task state
- Track progress through multi-step operations
- Keep track of user preferences and decisions within the current session