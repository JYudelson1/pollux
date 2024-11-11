# Pollux: A Coherent AI Agent Architecture

Pollux is an AI agent architecture designed to maintain coherent, long-running assistance through a combination of memory, scheduled interactions, and dynamic task management. It uses Claude (Anthropic's AI model) as its core, augmented with tools and scaffolding to enable persistent, contextual interactions.

## Core Philosophy

The architecture is built around a few key insights:
- AI assistance is most valuable when it maintains context and coherence over time
- The agent should learn and adapt through interaction, not just execute commands
- Tools should enhance natural conversation, not replace it
- Memory should inform both understanding and action

## Key Features

### Memory System
- Persistent storage of learned preferences and patterns
- Importance-based retrieval
- Regular reflection and synthesis of new learnings
- Used to inform future interactions

### Task Management
- Tracks user commitments and todos
- Integrates with iOS reminders for practical usage
- Natural language task descriptions
- Flexible scheduling and reprioritization

### Wakeup System
- Allows agent to schedule future interactions
- Maintains context across conversations
- Enables proactive assistance
- Coordinates with task system for timely reminders

### Tool Development
The agent can propose new tools when it identifies gaps in its capabilities. This follows a structured process:
1. Discuss need with user
2. Propose XML interface
3. Implement after approval

### Communication
- Seamless switching between chat and SMS
- Context-aware channel selection
- Natural conversation style
- Regular reflection during longer conversations

## Technical Architecture

### Core Components
- Claude API integration
- XML-based tool interface
- File and memory persistence
- Task and wakeup scheduling
- SMS capabilities (via Twilio)

### Scaffolding Features
- Ongoing reflection during conversations
- Morning routine planning
- Context preservation between sessions
- Structured tool proposal system

## What This Is Good For

- Personal assistance that learns and adapts
- Task management with natural interaction
- Projects requiring sustained context
- Systems that benefit from proactive help
- Applications needing both automation and flexibility

## What This Isn't

- Not a general automation framework
- Not designed for multi-user interactions
- Not meant for real-time/latency-critical tasks
- Not a replacement for dedicated specialized tools

## Implementation Notes

The system requires:
- Anthropic API access
- Twilio for SMS
- iOS integration capabilities
- Python 3.8+
- Storage for memories, tasks, and files

## For Future Architects

The key to this system is coherence - each component exists to help the agent maintain a consistent understanding and provide better assistance over time. When adding features:

1. Favor natural language over rigid structures
2. Keep tools simple and composable
3. Preserve context whenever possible
4. Allow the agent to learn from interactions
5. Maintain the balance between proactive help and user autonomy

The architecture is designed to be extensible but intentionally minimal. New capabilities should be added through the tool proposal system rather than architectural changes when possible.

## Getting Started

[Implementation details to come]