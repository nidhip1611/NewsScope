"""
NewsScope JSON Schema Definition
"""

NEWSSCOPE_SCHEMA = {
    "type": "object",
    "required": ["domain", "headline", "key_points", "whos_involved", "how_it_unfolded", "claims"],
    "properties": {
        "domain": {
            "type": "string",
            "enum": ["politics", "health", "science_env", "business"]
        },
        "headline": {
            "type": "string",
            "minLength": 10,
            "maxLength": 200
        },
        "key_points": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "maxItems": 3
        },
        "whos_involved": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "role"],
                "properties": {
                    "name": {"type": "string"},
                    "role": {"type": "string"}
                }
            }
        },
        "how_it_unfolded": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["date", "event"],
                "properties": {
                    "date": {"type": "string"},
                    "event": {"type": "string"}
                }
            }
        },
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["claim_text", "evidence_from_article"],
                "properties": {
                    "claim_text": {"type": "string"},
                    "evidence_from_article": {"type": "string"}
                }
            },
            "minItems": 2,
            "maxItems": 3
        }
    }
}
