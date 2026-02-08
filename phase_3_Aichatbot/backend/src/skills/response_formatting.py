"""
Response formatting skill for the AI Agent Platform
Formats agent responses for consistent presentation
"""
from typing import Dict, Any
from .base_skill import BaseSkill, SkillResult
from ..utils.logging import Logger
import re
import html


class ResponseFormattingSkill(BaseSkill):
    """
    The response formatting skill is responsible for:
    1. Standardizing response format across different agents
    2. Ensuring consistent presentation of responses
    3. Applying formatting rules for different intent types
    4. Sanitizing content for safe display
    """

    def __init__(self):
        # Define formatting rules for different intents
        self.formatting_rules = {
            "greeting": {
                "prefix": "",
                "suffix": "",
                "capitalize": True,
                "newline_after": False
            },
            "help": {
                "prefix": "📋 Help: ",
                "suffix": "\n\nHow else can I assist you?",
                "capitalize": True,
                "newline_after": True
            },
            "task_management": {
                "prefix": "✅ Task: ",
                "suffix": "",
                "capitalize": True,
                "newline_after": True
            },
            "question": {
                "prefix": "",
                "suffix": "",
                "capitalize": True,
                "newline_after": False
            },
            "general": {
                "prefix": "",
                "suffix": "",
                "capitalize": True,
                "newline_after": False
            }
        }

        # Define formatting options
        self.options = {
            "max_line_length": 80,
            "sanitize_html": True,
            "preserve_code_blocks": True,
            "add_markdown_support": True
        }

    def get_skill_name(self) -> str:
        """Return the name of the skill"""
        return "response_formatting"

    def get_required_params(self) -> list:
        """Get the list of required parameters for this skill"""
        return ["content"]

    def get_optional_params(self) -> list:
        """Get the list of optional parameters for this skill"""
        return ["intent", "options"]

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Execute the response formatting

        Args:
            params: Parameters for the skill execution, must include 'content', optionally 'intent' and 'options'

        Returns:
            SkillResult: Result of the response formatting
        """
        try:
            # Validate parameters
            if "content" not in params or not isinstance(params["content"], str):
                return SkillResult(
                    success=False,
                    error="Missing or invalid 'content' parameter"
                )

            content = params["content"]
            intent = params.get("intent", "general")
            options = params.get("options", {})

            # Apply formatting based on intent
            formatted_content = self._apply_formatting(content, intent, options)

            # Sanitize the content for safe display
            sanitized_content = self._sanitize_content(formatted_content)

            # Apply additional formatting options
            final_content = self._apply_options(sanitized_content, options)

            # Prepare result data
            result_data = {
                "original_content": content,
                "formatted_content": final_content,
                "intent": intent,
                "formatting_applied": True
            }

            Logger.info(f"Response formatting completed", extra={
                "intent": intent,
                "original_length": len(content),
                "formatted_length": len(final_content)
            })

            return SkillResult(
                success=True,
                data=result_data
            )

        except Exception as e:
            Logger.error(f"Error in response formatting skill: {str(e)}")
            return SkillResult(
                success=False,
                error=f"Failed to format response: {str(e)}"
            )

    def _apply_formatting(self, content: str, intent: str, options: Dict[str, Any]) -> str:
        """
        Apply formatting rules based on intent

        Args:
            content: Original content to format
            intent: Intent type for formatting
            options: Additional formatting options

        Returns:
            str: Formatted content
        """
        # Get formatting rule for the intent
        rule = self.formatting_rules.get(intent, self.formatting_rules["general"])

        # Apply prefix and suffix
        formatted = f"{rule['prefix']}{content}{rule['suffix']}"

        # Capitalize if required
        if rule.get("capitalize", False):
            formatted = self._capitalize_sentences(formatted)

        return formatted

    def _sanitize_content(self, content: str) -> str:
        """
        Sanitize content for safe display

        Args:
            content: Content to sanitize

        Returns:
            str: Sanitized content
        """
        if not self.options.get("sanitize_html", True):
            return content

        # Escape HTML entities to prevent XSS
        sanitized = html.escape(content)

        # Be more specific about code blocks to preserve them
        # This preserves code blocks while sanitizing other content
        code_block_pattern = r'(```.*?```|`.*?`)'
        code_blocks = re.findall(code_block_pattern, sanitized, re.DOTALL)

        # Temporarily replace code blocks with placeholders
        temp_content = re.sub(code_block_pattern, '<CODE_BLOCK_{}>', sanitized, flags=re.DOTALL)

        # Sanitize the rest of the content
        temp_sanitized = html.escape(temp_content)

        # Restore code blocks
        result = temp_sanitized
        for i, code_block in enumerate(code_blocks):
            result = result.replace(f'<CODE_BLOCK_{i}>', code_block)

        return result

    def _apply_options(self, content: str, options: Dict[str, Any]) -> str:
        """
        Apply additional formatting options

        Args:
            content: Content to apply options to
            options: Formatting options to apply

        Returns:
            str: Content with options applied
        """
        result = content

        # Apply line wrapping if requested
        max_line_length = options.get("max_line_length", self.options["max_line_length"])
        if max_line_length and max_line_length > 0:
            result = self._wrap_lines(result, max_line_length)

        # Apply other options as needed
        return result

    def _capitalize_sentences(self, text: str) -> str:
        """
        Capitalize the first letter of each sentence

        Args:
            text: Text to capitalize

        Returns:
            str: Capitalized text
        """
        # Split text into sentences and capitalize the first letter of each
        sentences = re.split(r'([.!?]+)', text)
        result = []

        for i, part in enumerate(sentences):
            if i % 2 == 0:  # This is a sentence (not punctuation)
                # Strip leading/trailing whitespace and capitalize first letter
                stripped = part.strip()
                if stripped:
                    result.append(stripped[0].upper() + stripped[1:] if len(stripped) > 1 else stripped.upper())
                else:
                    result.append(part)  # Preserve original whitespace
            else:  # This is punctuation
                result.append(part)

        # Join back together, preserving original spacing
        return "".join(result)

    def _wrap_lines(self, text: str, max_length: int) -> str:
        """
        Wrap lines to a maximum length

        Args:
            text: Text to wrap
            max_length: Maximum line length

        Returns:
            str: Wrapped text
        """
        if max_length <= 0:
            return text

        lines = []
        for paragraph in text.split('\n'):
            if len(paragraph) <= max_length:
                lines.append(paragraph)
            else:
                # Wrap the paragraph
                wrapped_paragraph = self._wrap_single_line(paragraph, max_length)
                lines.extend(wrapped_paragraph.split('\n'))

        return '\n'.join(lines)

    def _wrap_single_line(self, line: str, max_length: int) -> str:
        """
        Wrap a single line to a maximum length

        Args:
            line: Line to wrap
            max_length: Maximum line length

        Returns:
            str: Wrapped line
        """
        if len(line) <= max_length:
            return line

        words = line.split(' ')
        lines = []
        current_line = ""

        for word in words:
            # Check if adding this word would exceed the max length
            if len(current_line) + len(word) + (1 if current_line else 0) <= max_length:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                # Start a new line
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return '\n'.join(lines)

    def add_formatting_rule(self, intent: str, rule: Dict[str, Any]):
        """
        Add a custom formatting rule for an intent

        Args:
            intent: Intent name for the rule
            rule: Formatting rule dictionary
        """
        self.formatting_rules[intent] = rule

    def update_options(self, new_options: Dict[str, Any]):
        """
        Update formatting options

        Args:
            new_options: Dictionary of new options
        """
        self.options.update(new_options)