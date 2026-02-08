"""
Intent analysis skill for the AI Agent Platform
Analyzes user messages to determine the intent
"""
from typing import Dict, Any
from .base_skill import BaseSkill, SkillResult
from ..utils.logging import Logger
import re
import json


class IntentAnalysisSkill(BaseSkill):
    """
    The intent analysis skill is responsible for:
    1. Analyzing user input to determine intent
    2. Providing confidence scores for detected intents
    3. Identifying keywords and entities in the input
    """

    def __init__(self):
        # Define intent patterns and keywords
        self.intent_patterns = {
            "greeting": [
                r"\b(hello|hi|hey|greetings|good morning|good afternoon|good evening)\b",
                r"\bhowdy\b"
            ],
            "goodbye": [
                r"\b(goodbye|bye|see you|farewell|take care|later)\b",
                r"\b(catch you later|talk to you later)\b"
            ],
            "help": [
                r"\b(help|assist|support|what can you do|how do i|instructions)\b",
                r"\b(tutorial|guide|assistance)\b"
            ],
            "task_management": [
                r"\b(add|create|make|new)\s+(task|todo|item)\b",
                r"\b(list|show|view)\s+(tasks|todos|items)\b",
                r"\b(delete|remove|finish|complete)\s+(task|todo|item)\b",
                r"\b(update|change|modify)\s+(task|todo|item)\b"
            ],
            "question": [
                r"\b(what|who|when|where|why|how|can|could|would|is|are|do|does)\b.*\?$",
                r".*\?$"  # Any sentence ending with question mark
            ],
            "general": [
                # General intent will be the fallback
            ]
        }

        # Define common entities that might be extracted
        self.entity_patterns = {
            "datetime": [
                r"\b\d{1,2}[/:]\d{1,2}[/:]\d{2,4}\b",  # Date: MM/DD/YYYY or DD/MM/YYYY
                r"\b\d{1,2}:\d{2}(?:\s?(?:AM|PM|am|pm))?\b",  # Time: HH:MM
                r"\b(today|tomorrow|yesterday|tonight|now)\b",  # Relative time
                r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",  # Days of week
                r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\b"  # Months
            ],
            "number": [
                r"\b\d+\b"  # Numbers
            ],
            "email": [
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"  # Email addresses
            ]
        }

    def get_skill_name(self) -> str:
        """Return the name of the skill"""
        return "intent_analysis"

    def get_required_params(self) -> list:
        """Get the list of required parameters for this skill"""
        return ["message"]

    async def execute(self, params: Dict[str, Any]) -> SkillResult:
        """
        Execute the intent analysis

        Args:
            params: Parameters for the skill execution, must include 'message'

        Returns:
            SkillResult: Result of the intent analysis
        """
        try:
            # Validate parameters
            if "message" not in params or not isinstance(params["message"], str):
                return SkillResult(
                    success=False,
                    error="Missing or invalid 'message' parameter"
                )

            message = params["message"].strip().lower()

            if not message:
                return SkillResult(
                    success=False,
                    error="Message cannot be empty"
                )

            # Perform intent analysis
            detected_intent, confidence = self._analyze_intent(message)
            entities = self._extract_entities(message)

            # Prepare result data
            result_data = {
                "detected_intent": detected_intent,
                "confidence": confidence,
                "entities": entities,
                "original_message": params["message"],
                "processed_message": message
            }

            Logger.info(f"Intent analysis completed", extra={
                "intent": detected_intent,
                "confidence": confidence,
                "entities": entities
            })

            return SkillResult(
                success=True,
                data=result_data
            )

        except Exception as e:
            Logger.error(f"Error in intent analysis skill: {str(e)}")
            return SkillResult(
                success=False,
                error=f"Failed to analyze intent: {str(e)}"
            )

    def _analyze_intent(self, message: str) -> tuple[str, float]:
        """
        Analyze the message to determine the intent

        Args:
            message: The message to analyze

        Returns:
            tuple[str, float]: (detected intent, confidence score)
        """
        scores = {}

        # Calculate scores for each intent based on pattern matches
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, message, re.IGNORECASE)
                score += len(matches)

            scores[intent] = score

        # Normalize scores and calculate confidence
        total_score = sum(scores.values())

        if total_score == 0:
            # If no patterns match, default to 'general' intent
            return "general", 0.1

        # Find the intent with the highest score
        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]

        # Calculate confidence as percentage of total score
        confidence = best_score / total_score if total_score > 0 else 0.0

        # Cap confidence at 0.95 to acknowledge uncertainty
        confidence = min(confidence, 0.95)

        # Boost confidence slightly if we have a strong match
        if best_score >= 2:
            confidence = min(confidence + 0.1, 0.95)

        return best_intent, confidence

    def _extract_entities(self, message: str) -> Dict[str, list]:
        """
        Extract entities from the message

        Args:
            message: The message to extract entities from

        Returns:
            Dict[str, list]: Dictionary mapping entity types to lists of found entities
        """
        entities = {}

        for entity_type, patterns in self.entity_patterns.items():
            found_entities = []
            for pattern in patterns:
                matches = re.findall(pattern, message, re.IGNORECASE)
                found_entities.extend(matches)

            # Remove duplicates while preserving order
            unique_entities = list(dict.fromkeys(found_entities))
            entities[entity_type] = unique_entities

        return entities

    def add_intent_pattern(self, intent_name: str, patterns: list):
        """
        Add custom patterns for an intent

        Args:
            intent_name: Name of the intent
            patterns: List of regex patterns for the intent
        """
        if intent_name not in self.intent_patterns:
            self.intent_patterns[intent_name] = []

        self.intent_patterns[intent_name].extend(patterns)

    def get_supported_intents(self) -> list:
        """
        Get a list of supported intents

        Returns:
            list: List of supported intent names
        """
        return list(self.intent_patterns.keys())