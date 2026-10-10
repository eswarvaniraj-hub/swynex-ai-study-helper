"""
Unit Tests for AI Study Helper - Text Processing & JSON Response Parsing
SWYNEX Internship Task 4 Final AI Project

NOTE: These tests use explicitly labeled test data fixtures and do NOT call any external API.
"""

import json
import unittest
from ai_service import (
    parse_and_validate_json,
    generate_study_materials,
    StudyHelperResponse,
    MalformedResponseError,
    MissingAPIKeyError,
    InputValidationError,
)

# ==============================================================================
# LABELED TEST FIXTURES (TEST DATA ONLY - NOT REAL MODEL OUTPUT)
# ==============================================================================
VALID_TEST_JSON_FIXTURE = """
{
  "summary": "Photosynthesis is the process used by plants and other organisms to convert light energy into chemical energy stored in carbohydrate molecules such as glucose. It takes place primarily in chloroplasts using chlorophyll, consuming water and carbon dioxide while producing oxygen as a vital byproduct.",
  "key_points": [
    "Photosynthesis occurs inside specialized plant organelles called chloroplasts.",
    "Chlorophyll is the primary green pigment responsible for capturing sunlight.",
    "The core chemical inputs are sunlight, water (H2O), and carbon dioxide (CO2).",
    "Glucose is produced as chemical energy to nourish the plant.",
    "Oxygen (O2) is released into the atmosphere as a beneficial byproduct."
  ],
  "quiz": [
    {
      "question": "Which organelle is the primary site of photosynthesis in plant cells?",
      "options": [
        "A) Mitochondria",
        "B) Chloroplast",
        "C) Ribosome",
        "D) Golgi apparatus"
      ],
      "correct_answer": "B",
      "explanation": "Chloroplasts contain chlorophyll and the biochemical machinery necessary for photosynthesis."
    },
    {
      "question": "What are the primary chemical reactants consumed during photosynthesis?",
      "options": [
        "A) Glucose and oxygen",
        "B) Carbon dioxide and water",
        "C) Nitrogen and methane",
        "D) Hydrogen and ozone"
      ],
      "correct_answer": "B",
      "explanation": "Photosynthesis consumes carbon dioxide and water to produce glucose and oxygen."
    },
    {
      "question": "Why is oxygen released during photosynthesis?",
      "options": [
        "A) It is a metabolic byproduct of water splitting",
        "B) It is consumed to create carbon dioxide",
        "C) It is stored for night respiration only",
        "D) It is absorbed directly through roots"
      ],
      "correct_answer": "A",
      "explanation": "When water molecules are split in the light reactions, oxygen is released as a byproduct."
    }
  ]
}
"""

MARKDOWN_WRAPPED_TEST_FIXTURE = f"""```json
{VALID_TEST_JSON_FIXTURE.strip()}
```"""

MALFORMED_SYNTAX_FIXTURE = """
{
  "summary": "This JSON is broken because of a missing closing brace and quote
  "key_points": ["Broken"]
"""

MISSING_QUIZ_FIELD_FIXTURE = """
{
  "summary": "Photosynthesis summary text.",
  "key_points": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"]
}
"""

EMPTY_KEY_POINTS_FIXTURE = """
{
  "summary": "Photosynthesis summary text.",
  "key_points": [],
  "quiz": [
    {
      "question": "Test question?",
      "options": ["A) 1", "B) 2", "C) 3", "D) 4"],
      "correct_answer": "A",
      "explanation": "Explanation"
    }
  ]
}
"""


class TestTextProcessingAndJSONParsing(unittest.TestCase):
    """Test suite verifying JSON parsing, Pydantic validation, and error guards."""

    def test_parse_valid_json_fixture(self):
        """Valid JSON fixture should deserialize into a StudyHelperResponse object."""
        result = parse_and_validate_json(VALID_TEST_JSON_FIXTURE)
        self.assertIsInstance(result, StudyHelperResponse)
        self.assertTrue(len(result.summary) > 20)
        self.assertEqual(len(result.key_points), 5)
        self.assertEqual(len(result.quiz), 3)

        # Verify first quiz item structure
        first_q = result.quiz[0]
        self.assertEqual(first_q.correct_answer, "B")
        self.assertEqual(len(first_q.options), 4)
        self.assertIn("Chloroplast", first_q.options[1])

    def test_parse_markdown_fenced_json(self):
        """Responses wrapped in ```json ... ``` markdown code fences should parse cleanly."""
        result = parse_and_validate_json(MARKDOWN_WRAPPED_TEST_FIXTURE)
        self.assertIsInstance(result, StudyHelperResponse)
        self.assertEqual(len(result.key_points), 5)
        self.assertEqual(len(result.quiz), 3)

    def test_malformed_syntax_raises_error(self):
        """Invalid JSON syntax should trigger MalformedResponseError."""
        with self.assertRaises(MalformedResponseError) as ctx:
            parse_and_validate_json(MALFORMED_SYNTAX_FIXTURE)
        self.assertIn("not valid JSON", str(ctx.exception))

    def test_empty_string_raises_error(self):
        """Empty string input should trigger MalformedResponseError."""
        with self.assertRaises(MalformedResponseError) as ctx:
            parse_and_validate_json("")
        self.assertIn("empty response", str(ctx.exception).lower())

    def test_missing_quiz_field_raises_error(self):
        """JSON missing required fields must fail schema validation and raise MalformedResponseError."""
        with self.assertRaises(MalformedResponseError) as ctx:
            parse_and_validate_json(MISSING_QUIZ_FIELD_FIXTURE)
        self.assertIn("validation failed", str(ctx.exception).lower())

    def test_empty_key_points_raises_error(self):
        """JSON with empty key points list should be rejected as incomplete."""
        with self.assertRaises(MalformedResponseError) as ctx:
            parse_and_validate_json(EMPTY_KEY_POINTS_FIXTURE)
        self.assertIn("empty", str(ctx.exception).lower())

    def test_missing_api_key_raises_exception_without_calling_network(self):
        """Ensures generate_study_materials raises MissingAPIKeyError before making any API call."""
        valid_notes = (
            "Photosynthesis is the process by which green plants, algae, and cyanobacteria "
            "convert light energy into chemical energy stored in carbohydrate molecules such as glucose."
        )
        with self.assertRaises(MissingAPIKeyError) as ctx:
            generate_study_materials(notes=valid_notes, api_key="")
        self.assertIn("API key not found", str(ctx.exception))

    def test_invalid_notes_caught_before_api_call(self):
        """Input validation failures are caught locally before any network invocation."""
        with self.assertRaises(InputValidationError) as ctx:
            generate_study_materials(notes="Too short", api_key="dummy_test_key")
        self.assertIn("too short", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main()
