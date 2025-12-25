---
title: Cognitive Planning with Large Language Models (LLMs)
sidebar_label: Chapter 2 - Cognitive Planning with LLMs
description: Using LLMs to map natural language commands to robot actions in VLA systems
---

# Cognitive Planning with Large Language Models (LLMs)

## Introduction to LLMs in Robotics

Large Language Models (LLMs) such as GPT-3, GPT-3.5, and GPT-4 represent a significant advancement in natural language understanding and generation. In the context of Vision-Language-Action (VLA) systems, LLMs serve as cognitive planners that interpret natural language commands and translate them into structured action sequences that robots can execute.

### Key Capabilities of LLMs for Robotics
- **Natural Language Understanding**: Interpret complex, nuanced commands
- **Context Awareness**: Consider environmental context and previous interactions
- **Reasoning**: Apply logical reasoning to determine appropriate actions
- **Knowledge Integration**: Leverage pre-trained knowledge for task planning
- **Adaptability**: Handle novel situations through generalization

## Setting Up LLM Integration

### API Access and Configuration
To use LLMs for cognitive planning, you'll need to set up your environment:

```python
import openai
import os
import json
from typing import Dict, List, Any

# Set your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class LLMCognitivePlanner:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.3):
        self.model = model
        self.temperature = temperature
        self.conversation_history = []

    def set_model_parameters(self, model: str, temperature: float = 0.3):
        """Update model parameters"""
        self.model = model
        self.temperature = temperature
```

### Structured Prompting for Action Mapping
The key to effective LLM integration is creating well-structured prompts that guide the model to produce consistent, actionable outputs:

```python
def create_action_mapping_prompt(self, command: str, robot_capabilities: List[str],
                                environment_context: Dict[str, Any] = None) -> str:
    """
    Create a structured prompt for mapping natural language to robot actions
    """
    capabilities_str = "\n".join([f"- {cap}" for cap in robot_capabilities])

    context_str = ""
    if environment_context:
        context_str = f"""
Environment Context:
- Objects present: {environment_context.get('objects', [])}
- Robot location: {environment_context.get('location', 'unknown')}
- Previous actions: {environment_context.get('previous_actions', [])}
"""

    prompt = f"""
You are a cognitive planner for a robot. Your task is to interpret natural language commands and convert them into specific robot actions.

Robot Capabilities:
{capabilities_str}

{context_str}

Command: "{command}"

Please respond in the following JSON format:
{{
    "action_sequence": [
        {{
            "action": "action_name",
            "parameters": {{"param_name": "param_value", ...}},
            "confidence": 0.0-1.0
        }}
    ],
    "reasoning": "Brief explanation of your interpretation",
    "safety_check": "Whether the action sequence is safe to execute"
}}

Only respond with the JSON object, nothing else.
"""
    return prompt

# Example usage
planner = LLMCognitivePlanner()
capabilities = [
    "move_forward(distance_meters)",
    "move_backward(distance_meters)",
    "turn_left(degrees)",
    "turn_right(degrees)",
    "pick_up_object(object_name)",
    "place_object(object_name, location)",
    "detect_object(object_name)",
    "navigate_to(location)"
]

prompt = planner.create_action_mapping_prompt(
    "Pick up the red ball and place it in the blue box",
    capabilities,
    {"objects": ["red ball", "blue box"], "location": "room center"}
)
```

## Advanced Prompting Techniques

### Role-Based Prompting
Define the role and context for the LLM to improve response quality:

```python
def create_role_based_prompt(self, command: str, robot_capabilities: List[str]) -> str:
    """
    Create a role-based prompt that establishes context for the LLM
    """
    capabilities_str = "\n".join([f"- {cap}" for cap in robot_capabilities])

    prompt = f"""You are an expert cognitive planner for a humanoid robot. Your role is to interpret human commands and generate safe, executable action sequences.

Your approach:
1. Understand the intent behind the command
2. Consider the robot's capabilities and limitations
3. Generate a step-by-step action sequence
4. Include safety checks
5. Provide reasoning for your decisions

Robot Capabilities:
{capabilities_str}

Command: "{command}"

Respond in JSON format with action_sequence, reasoning, and safety_check as specified.
"""
    return prompt
```

### Few-Shot Learning Examples
Provide examples to guide the LLM's behavior:

```python
def create_few_shot_prompt(self, command: str, robot_capabilities: List[str]) -> str:
    """
    Create a prompt with few-shot examples for better action mapping
    """
    capabilities_str = "\n".join([f"- {cap}" for cap in robot_capabilities])

    examples = """
Example 1:
Input: "Move forward 2 meters"
Output: {
    "action_sequence": [
        {"action": "move_forward", "parameters": {"distance_meters": 2.0}, "confidence": 0.95}
    ],
    "reasoning": "User wants to move forward by 2 meters, which is within robot capabilities",
    "safety_check": "safe"
}

Example 2:
Input: "Pick up the green cube from the table"
Output: {
    "action_sequence": [
        {"action": "detect_object", "parameters": {"object_name": "green cube"}, "confidence": 0.85},
        {"action": "navigate_to", "parameters": {"location": "table"}, "confidence": 0.90},
        {"action": "pick_up_object", "parameters": {"object_name": "green cube"}, "confidence": 0.92}
    ],
    "reasoning": "User wants to pick up a specific object. Need to detect it first, then navigate to it, then pick it up.",
    "safety_check": "safe"
}
"""

    prompt = f"""
You are a cognitive planner for a robot. Your task is to interpret natural language commands and convert them into specific robot actions.

Robot Capabilities:
{capabilities_str}

{examples}

Now process this command: "{command}"

Respond in the same JSON format as the examples.
"""
    return prompt
```

## Processing Natural Language to Actions

### Basic Action Mapping
Here's how to process commands using the LLM:

```python
import json
import re

class LLMActionMapper:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model

    def map_command_to_actions(self, command: str, capabilities: List[str],
                             environment: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Map a natural language command to a sequence of robot actions
        """
        prompt = self.create_mapping_prompt(command, capabilities, environment)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a robot cognitive planner. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )

            # Extract and parse the response
            response_text = response.choices[0].message.content.strip()

            # Clean up any markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove ```

            result = json.loads(response_text)
            return result

        except json.JSONDecodeError:
            return {
                "action_sequence": [],
                "reasoning": "Could not parse LLM response",
                "safety_check": "error"
            }
        except Exception as e:
            return {
                "action_sequence": [],
                "reasoning": f"Error processing command: {str(e)}",
                "safety_check": "error"
            }

    def create_mapping_prompt(self, command: str, capabilities: List[str],
                           environment: Dict[str, Any] = None) -> str:
        """Create a structured prompt for action mapping"""
        capabilities_str = "\n".join([f"- {cap}" for cap in capabilities])

        context_str = ""
        if environment:
            env_parts = []
            if "objects" in environment:
                env_parts.append(f"Objects present: {', '.join(environment['objects'])}")
            if "location" in environment:
                env_parts.append(f"Current location: {environment['location']}")
            if "robot_state" in environment:
                env_parts.append(f"Robot state: {environment['robot_state']}")

            if env_parts:
                context_str = "Environment context:\n" + "\n".join([f"- {part}" for part in env_parts]) + "\n\n"

        prompt = f"""You are a cognitive planner for a robot. Convert the user command to a sequence of actions.

Available capabilities:
{capabilities_str}

{context_str}
Command: "{command}"

Respond with JSON containing:
- action_sequence: array of action objects with action, parameters, and confidence
- reasoning: brief explanation
- safety_check: safe/unsafe/error

Example format:
{{
    "action_sequence": [
        {{"action": "move_forward", "parameters": {{"distance_meters": 1.0}}, "confidence": 0.95}}
    ],
    "reasoning": "Moving forward to approach target",
    "safety_check": "safe"
}}"""

        return prompt

# Example usage
mapper = LLMActionMapper(os.getenv("OPENAI_API_KEY"))
capabilities = [
    "move_forward(distance_meters)",
    "move_backward(distance_meters)",
    "turn_left(degrees)",
    "turn_right(degrees)",
    "pick_up_object(object_name)",
    "place_object(object_name, location)",
    "detect_object(object_name)",
    "navigate_to(location)"
]

result = mapper.map_command_to_actions(
    "Please go to the kitchen and bring me the red apple",
    capabilities,
    {"objects": ["red apple", "blue cup"], "location": "living room"}
)

print(json.dumps(result, indent=2))
```

## Context and Memory Integration

### Maintaining Conversation Context
For complex interactions, it's important to maintain context across multiple commands:

```python
class ContextualLLMPlanner:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        self.conversation_history = []
        self.robot_state = {}

    def add_to_history(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        # Keep only the last 10 exchanges to manage token usage
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

    def process_command_with_context(self, command: str, capabilities: List[str]) -> Dict[str, Any]:
        """
        Process a command with access to conversation history and robot state
        """
        # Create system message with context
        system_message = f"""
You are a cognitive planner for a robot. Use the conversation history and robot state to inform your decisions.

Robot Capabilities:
{chr(10).join([f"- {cap}" for cap in capabilities])}

Current Robot State:
{json.dumps(self.robot_state, indent=2)}
"""

        # Build the message sequence
        messages = [
            {"role": "system", "content": system_message}
        ]

        # Add conversation history
        messages.extend(self.conversation_history)

        # Add the current command
        messages.append({"role": "user", "content": f"Command: {command}"})

        # Add instructions for response format
        messages.append({
            "role": "user",
            "content": "Respond in JSON format with action_sequence, reasoning, and safety_check."
        })

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )

            response_text = response.choices[0].message.content.strip()

            # Clean up markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            result = json.loads(response_text)

            # Update conversation history
            self.add_to_history("user", command)
            self.add_to_history("assistant", json.dumps(result))

            return result

        except Exception as e:
            error_result = {
                "action_sequence": [],
                "reasoning": f"Error processing command with context: {str(e)}",
                "safety_check": "error"
            }
            self.add_to_history("user", command)
            self.add_to_history("assistant", json.dumps(error_result))
            return error_result
```

## Safety and Validation

### Safety Validation Layer
Implement a safety layer to validate LLM-generated actions:

```python
class SafetyValidator:
    def __init__(self):
        self.forbidden_actions = [
            "harm", "injure", "damage", "destroy", "break",
            "attack", "hit", "fight", "hurt", "unsafe"
        ]
        self.safety_keywords = ["safe", "careful", "cautious", "carefully"]

    def validate_action_sequence(self, action_sequence: List[Dict],
                               robot_capabilities: List[str]) -> Dict[str, Any]:
        """
        Validate an action sequence for safety and feasibility
        """
        validation_result = {
            "is_safe": True,
            "is_feasible": True,
            "issues": [],
            "suggestions": []
        }

        # Check if actions are in robot capabilities
        capability_names = [cap.split('(')[0] for cap in robot_capabilities]

        for action in action_sequence:
            action_name = action.get("action", "")

            # Check if action is supported
            if action_name not in capability_names:
                validation_result["is_feasible"] = False
                validation_result["issues"].append(f"Action '{action_name}' not supported")

            # Check for potentially unsafe actions
            if any(forbidden in action_name.lower() for forbidden in self.forbidden_actions):
                validation_result["is_safe"] = False
                validation_result["issues"].append(f"Potentially unsafe action: {action_name}")

        # Additional safety checks could include:
        # - Physical constraints (movement limits)
        # - Environmental constraints (obstacles)
        # - Object properties (fragile items)

        return validation_result

    def enhance_with_safety(self, original_result: Dict[str, Any],
                           robot_capabilities: List[str]) -> Dict[str, Any]:
        """
        Enhance the LLM result with safety validation
        """
        # Validate the action sequence
        validation = self.validate_action_sequence(
            original_result.get("action_sequence", []),
            robot_capabilities
        )

        # Update the result with validation
        result = original_result.copy()
        result["validation"] = validation

        # Update safety_check based on validation
        if not validation["is_safe"]:
            result["safety_check"] = "unsafe"
        elif not validation["is_feasible"]:
            result["safety_check"] = "infeasible"

        return result

# Example usage
safety_validator = SafetyValidator()
capabilities = [
    "move_forward(distance_meters)",
    "move_backward(distance_meters)",
    "pick_up_object(object_name)",
    "place_object(location)"
]

# Example result from LLM
llm_result = {
    "action_sequence": [
        {"action": "move_forward", "parameters": {"distance_meters": 2.0}, "confidence": 0.95}
    ],
    "reasoning": "Moving forward to approach target",
    "safety_check": "safe"
}

validated_result = safety_validator.enhance_with_safety(llm_result, capabilities)
print(json.dumps(validated_result, indent=2))
```

## Advanced Cognitive Planning

### Hierarchical Task Planning
For complex commands, implement hierarchical planning:

```python
class HierarchicalPlanner:
    def __init__(self, api_key: str):
        self.action_mapper = LLMActionMapper(api_key)
        self.safety_validator = SafetyValidator()

    def decompose_task(self, high_level_command: str, capabilities: List[str]) -> Dict[str, Any]:
        """
        Decompose a high-level command into subtasks
        """
        # First, get a plan from the LLM
        result = self.action_mapper.map_command_to_actions(
            high_level_command,
            capabilities
        )

        # Then, validate the plan
        validated_result = self.safety_validator.enhance_with_safety(
            result, capabilities
        )

        # If the plan is complex, decompose further
        if len(validated_result.get("action_sequence", [])) > 5:  # Arbitrary threshold
            validated_result["decomposition"] = self.identify_subtasks(
                validated_result["action_sequence"]
            )

        return validated_result

    def identify_subtasks(self, action_sequence: List[Dict]) -> List[Dict]:
        """
        Identify logical groupings of actions as subtasks
        """
        subtasks = []
        current_subtask = []

        for action in action_sequence:
            current_subtask.append(action)

            # Group actions by type or logical separation
            if action["action"] in ["navigate_to", "pick_up_object", "place_object"]:
                if current_subtask:
                    subtasks.append({
                        "name": self.generate_subtask_name(current_subtask),
                        "actions": current_subtask,
                        "description": self.generate_subtask_description(current_subtask)
                    })
                    current_subtask = []

        # Add any remaining actions as a final subtask
        if current_subtask:
            subtasks.append({
                "name": self.generate_subtask_name(current_subtask),
                "actions": current_subtask,
                "description": self.generate_subtask_description(current_subtask)
            })

        return subtasks

    def generate_subtask_name(self, actions: List[Dict]) -> str:
        """Generate a descriptive name for a subtask"""
        if not actions:
            return "Empty Subtask"

        first_action = actions[0]["action"]
        if first_action == "navigate_to":
            return "Navigation Subtask"
        elif first_action == "pick_up_object":
            return "Object Pickup Subtask"
        elif first_action == "place_object":
            return "Object Placement Subtask"
        else:
            return f"{first_action.title()} Subtask"

    def generate_subtask_description(self, actions: List[Dict]) -> str:
        """Generate a description for a subtask"""
        if not actions:
            return "No actions in subtask"

        action_names = [action["action"] for action in actions]
        return f"Sequence of {len(actions)} actions: {', '.join(action_names[:3])}{'...' if len(actions) > 3 else ''}"

# Example usage
hierarchical_planner = HierarchicalPlanner(os.getenv("OPENAI_API_KEY"))
result = hierarchical_planner.decompose_task(
    "Go to the kitchen, pick up the red cup, and bring it to the living room table",
    capabilities
)
print(json.dumps(result, indent=2))
```

## Error Handling and Fallback Strategies

### Handling Ambiguous Commands
Implement strategies for handling unclear or ambiguous commands:

```python
class RobustLLMPlanner:
    def __init__(self, api_key: str):
        self.action_mapper = LLMActionMapper(api_key)
        self.safety_validator = SafetyValidator()

    def handle_ambiguous_command(self, command: str, capabilities: List[str],
                               environment: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Handle commands that might be ambiguous
        """
        # Try the original command first
        result = self.action_mapper.map_command_to_actions(
            command, capabilities, environment
        )

        # If confidence is low or safety check fails, try to clarify
        action_sequence = result.get("action_sequence", [])
        if not action_sequence or result.get("safety_check") != "safe":
            clarification_result = self.request_clarification(
                command, capabilities, environment
            )
            return clarification_result

        # Validate the result
        validated_result = self.safety_validator.enhance_with_safety(
            result, capabilities
        )

        return validated_result

    def request_clarification(self, command: str, capabilities: List[str],
                            environment: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate a clarification request when command is ambiguous
        """
        prompt = f"""
The user said: "{command}"

This command seems ambiguous or unclear. Please respond with:
1. What information is needed to clarify the command
2. A question to ask the user for clarification

Respond in JSON format:
{{
    "needs_clarification": true,
    "clarification_needed": "What specific information is unclear",
    "question_for_user": "What would you ask the user",
    "suggested_interpretation": "What the command might mean"
}}
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that identifies unclear commands and suggests clarifications."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300,
                response_format={"type": "json_object"}
            )

            response_text = response.choices[0].message.content.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            clarification = json.loads(response_text)
            return {
                "action_sequence": [],
                "reasoning": "Command needs clarification",
                "safety_check": "pending_clarification",
                "clarification": clarification
            }
        except Exception as e:
            return {
                "action_sequence": [],
                "reasoning": f"Could not process ambiguous command: {str(e)}",
                "safety_check": "error"
            }

# Example usage
robust_planner = RobustLLMPlanner(os.getenv("OPENAI_API_KEY"))
result = robust_planner.handle_ambiguous_command(
    "Do something with that thing over there",
    capabilities
)
print(json.dumps(result, indent=2))
```

## Integration with VLA Pipeline

### Complete Cognitive Planning Pipeline
Here's how to integrate cognitive planning into the broader VLA system:

```python
class VLACognitivePlanner:
    def __init__(self, api_key: str):
        self.robust_planner = RobustLLMPlanner(api_key)
        self.safety_validator = SafetyValidator()

    def process_command(self, command: str, capabilities: List[str],
                       environment: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Complete pipeline: Command -> LLM Processing -> Validation -> Action Sequence
        """
        # Step 1: Process with LLM
        llm_result = self.robust_planner.handle_ambiguous_command(
            command, capabilities, environment
        )

        # Step 2: Validate safety and feasibility
        if llm_result.get("safety_check") != "pending_clarification":
            validated_result = self.safety_validator.enhance_with_safety(
                llm_result, capabilities
            )
        else:
            validated_result = llm_result  # Already has clarification request

        # Step 3: Add metadata for the VLA system
        validated_result["timestamp"] = time.time()
        validated_result["source"] = "llm_cognitive_planner"
        validated_result["model_used"] = "gpt-3.5-turbo"  # or whatever model was used

        return validated_result

# Example usage in VLA system
vla_planner = VLACognitivePlanner(os.getenv("OPENAI_API_KEY"))

# Example command processing
capabilities = [
    "move_forward(distance_meters)",
    "move_backward(distance_meters)",
    "turn_left(degrees)",
    "turn_right(degrees)",
    "pick_up_object(object_name)",
    "place_object(object_name, location)",
    "detect_object(object_name)",
    "navigate_to(location)"
]

environment = {
    "objects": ["red ball", "blue box", "green cube"],
    "location": "room center",
    "robot_state": {"battery": 0.85, "gripper": "empty"}
}

result = vla_planner.process_command(
    "Pick up the red ball and place it in the blue box",
    capabilities,
    environment
)

print("VLA Cognitive Planning Result:")
print(json.dumps(result, indent=2))
```

## Academic and Research Applications

LLMs have revolutionized cognitive planning in robotics:

### Research Papers and References
- Brown, T., et al. (2020). "Language Models are Few-Shot Learners" (GPT-3 paper)
- Achiam, J., et al. (2023). "GPT-4 Technical Report"
- Recent papers on LLMs in robotics and human-robot interaction
- Studies on instruction following and action mapping

### Research Applications
- Instruction following for complex robot tasks
- Natural language interfaces for robotics
- Few-shot learning for new robot capabilities
- Commonsense reasoning for robotics applications

## Performance Optimization

### Caching and Efficiency
For better performance, implement caching for common commands:

```python
import hashlib
from functools import lru_cache

class OptimizedLLMPlanner:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.model = "gpt-3.5-turbo"
        self.cache = {}
        self.max_cache_size = 100

    @lru_cache(maxsize=128)
    def get_cached_action_sequence(self, command_hash: str) -> Dict[str, Any]:
        """Get cached action sequence for a command hash"""
        return self.cache.get(command_hash, None)

    def process_command_with_caching(self, command: str, capabilities: List[str],
                                   environment: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process command with caching for repeated commands
        """
        # Create a hash of the command and relevant context
        cache_key = hashlib.md5(
            f"{command}:{str(environment)}:{str(sorted(capabilities))}".encode()
        ).hexdigest()

        # Check cache first
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            cached_result["from_cache"] = True
            return cached_result

        # If not in cache, process with LLM
        result = self.process_command_uncached(command, capabilities, environment)

        # Add to cache
        if len(self.cache) < self.max_cache_size:
            self.cache[cache_key] = result

        return result

    def process_command_uncached(self, command: str, capabilities: List[str],
                               environment: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process command without using cache
        """
        # Implementation similar to previous examples
        mapper = LLMActionMapper(os.getenv("OPENAI_API_KEY"))
        result = mapper.map_command_to_actions(command, capabilities, environment)
        return result
```

## Summary

Large Language Models provide powerful cognitive planning capabilities for VLA systems, enabling robots to understand and interpret complex natural language commands. By implementing proper prompting techniques, safety validation, and context management, we can create robust cognitive planning systems. The next chapter will explore how to integrate visual information with language processing for complete multimodal understanding.