"""
NewsScope JSON Output Validator
"""

import json
from typing import Dict, Any, List, Optional, Tuple

try:
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError
    HAS_JSONSCHEMA = True
except Exception:
    HAS_JSONSCHEMA = False

from .schema import NEWSSCOPE_SCHEMA


class NewscopeValidator:
    def __init__(self, schema: Optional[Dict[str, Any]] = None):
        self.schema = schema or NEWSSCOPE_SCHEMA

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        if HAS_JSONSCHEMA:
            try:
                validate(instance=data, schema=self.schema)
                return True, []
            except ValidationError as e:
                return False, [str(e.message)]
        return self._validate_manual(data)

    def _validate_manual(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        required = ["domain", "headline", "key_points", "whos_involved", "how_it_unfolded", "claims"]
        for k in required:
            if k not in data:
                errors.append(f"Missing required field: {k}")
        if errors:
            return False, errors

        if data.get("domain") not in ["politics", "health", "science_env", "business"]:
            errors.append("Invalid domain")

        headline = data.get("headline", "")
        if not (10 <= len(headline) <= 200):
            errors.append("headline length must be 10-200")

        kp = data.get("key_points", [])
        if not (isinstance(kp, list) and len(kp) == 3 and all(isinstance(x, str) for x in kp)):
            errors.append("key_points must be a list of exactly 3 strings")

        claims = data.get("claims", [])
        if not (isinstance(claims, list) and 2 <= len(claims) <= 3):
            errors.append("claims must be a list of 2-3 items")

        for i, c in enumerate(claims if isinstance(claims, list) else []):
            if "claim_text" not in c:
                errors.append(f"claims[{i}] missing claim_text")
            if "evidence_from_article" not in c:
                errors.append(f"claims[{i}] missing evidence_from_article")

        return (len(errors) == 0), errors

    def repair_json(self, text: str) -> Tuple[Optional[Dict[str, Any]], str]:
        # strip code fences
        if "```" in text:
            parts = text.split("```")
            text = parts[1] if len(parts) >= 2 else text

        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end <= start:
            return None, "No JSON object found"

        s = text[start:end]
        try:
            return json.loads(s), ""
        except json.JSONDecodeError:
            s = s.replace(",}", "}")
            s = s.replace(",]", "]")
            try:
                return json.loads(s), ""
            except json.JSONDecodeError as e:
                return None, f"JSON parse error: {e}"


def validate_output(raw_text: str) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
    v = NewscopeValidator()
    data, err = v.repair_json(raw_text)
    if data is None:
        return False, None, [err]
    ok, errors = v.validate(data)
    return ok, data, errors
