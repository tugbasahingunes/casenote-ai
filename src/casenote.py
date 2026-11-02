"""CaseNote AI: turn a home-visit note into structured, evidence-quoted flags.

The criteria live in a separate JSON file, so the same code can serve another
country or client group. Every flag must quote the note; quotes that do not
appear in the note are removed and reported.

Works with two model providers, so their results can be compared:
    CASENOTE_PROVIDER=anthropic  (needs ANTHROPIC_API_KEY)
    CASENOTE_PROVIDER=gemini     (needs GEMINI_API_KEY)

Never write an API key in code or commit it. Set it as an environment variable.

Usage:
    python src/casenote.py "Text of a home-visit note"
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CRITERIA = ROOT / "config" / "criteria_fi_older_people.json"

LEVELS = ["record", "human_review", "urgent_human_review"]


def load_criteria(path=DEFAULT_CRITERIA):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def output_schema(criteria):
    """JSON schema the model must fill in (passed as a tool definition)."""
    domain_ids = [int(d) for d in criteria["domains"]]
    flag = {
        "type": "object",
        "properties": {
            "domain": {"type": "integer", "enum": domain_ids},
            "level": {"type": "string", "enum": LEVELS},
            "quote": {"type": "string", "description": "exact words copied from the note"},
            "source": {"type": "string", "enum": ["person_said", "professional_observed", "relative_said"]},
        },
        "required": ["domain", "level", "quote", "source"],
    }

    def area_flag(areas):
        return {
            "type": "object",
            "properties": {
                "area": {"type": "string", "enum": list(areas)},
                "level": {"type": "string", "enum": LEVELS},
                "quote": {"type": "string"},
            },
            "required": ["area", "level", "quote"],
        }

    return {
        "type": "object",
        "properties": {
            "person": {"type": "array", "items": flag},
            "caregiver": {"type": "array", "items": area_flag(criteria["caregiver_areas"])},
            "young_carer": {"type": "array", "items": area_flag(criteria["young_carer_areas"])},
            "no_info": {"type": "array", "items": {"type": "integer", "enum": domain_ids}},
            "said_vs_observed": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "said": {"type": "string"},
                        "observed": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["said", "observed"],
                },
            },
        },
        "required": ["person", "caregiver", "young_carer", "no_info", "said_vs_observed"],
    }


def build_system_prompt(criteria):
    domains = "\n".join(
        f"{k}. {v['name']}: {v['signals']}" for k, v in criteria["domains"].items()
    )
    carer = "\n".join(f"- {k}: {v}" for k, v in criteria["caregiver_areas"].items())
    young = "\n".join(f"- {k}: {v}" for k, v in criteria["young_carer_areas"].items())
    levels = "\n".join(f"- {k}: {v}" for k, v in criteria["levels"].items())
    rules = "\n".join(f"- {r}" for r in criteria["rules"])
    return f"""You support social care professionals by structuring home-visit notes.
You produce a draft for a professional to review. You do not decide anything.

Setting: {criteria['name']}

Assessment domains:
{domains}

Family carer areas:
{carer}

Young carer areas:
{young}

Review levels:
{levels}

Rules:
{rules}

Return your answer only by calling the record_flags tool."""


def _norm(text):
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()


def quote_in_note(quote, note):
    """True if the quote (or each part split by '...') appears in the note."""
    parts = [p for p in re.split(r"\.\.\.|…", quote) if p.strip()]
    n = _norm(note)
    return bool(parts) and all(_norm(p).strip(" \"'") in n for p in parts)


def verify_quotes(result, note):
    """Remove flags whose quote is not in the note. Return (clean_result, removed)."""
    removed = []
    for key in ("person", "caregiver", "young_carer"):
        kept = []
        for f in result.get(key, []):
            (kept if quote_in_note(f.get("quote", ""), note) else removed).append(f)
        result[key] = kept
    return result, removed


def _call_anthropic(note, criteria, model, client=None):
    import anthropic

    client = client or anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=build_system_prompt(criteria),
        tools=[{
            "name": "record_flags",
            "description": "Record structured, evidence-quoted flags for one home-visit note.",
            "input_schema": output_schema(criteria),
        }],
        tool_choice={"type": "tool", "name": "record_flags"},
        messages=[{"role": "user", "content": f"Home-visit note:\n\n{note}"}],
    )
    return next(b.input for b in response.content if b.type == "tool_use")


def _gemini_schema(schema):
    """Gemini accepts a subset of JSON Schema: replace integer enums with a range."""
    if isinstance(schema, dict):
        if schema.get("type") == "integer" and "enum" in schema:
            return {"type": "integer", "minimum": min(schema["enum"]), "maximum": max(schema["enum"])}
        return {k: _gemini_schema(v) for k, v in schema.items()}
    if isinstance(schema, list):
        return [_gemini_schema(v) for v in schema]
    return schema


def _call_gemini(note, criteria, model, client=None):
    from google import genai
    from google.genai import types

    client = client or genai.Client()  # reads GEMINI_API_KEY
    system = build_system_prompt(criteria).replace(
        "Return your answer only by calling the record_flags tool.",
        "Return your answer only as JSON matching the given schema.")
    response = client.models.generate_content(
        model=model,
        contents=f"Home-visit note:\n\n{note}",
        config=types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
            response_json_schema=_gemini_schema(output_schema(criteria)),
        ),
    )
    return json.loads(response.text)


PROVIDERS = {
    "anthropic": (_call_anthropic, "claude-sonnet-5-5"),
    "gemini": (_call_gemini, "gemini-3.8-flash"),
}


def analyze_note(note, criteria=None, client=None, provider=None, model=None):
    """Send one note to the model and return verified, structured flags."""
    provider = provider or os.environ.get("CASENOTE_PROVIDER", "anthropic")
    call, default_model = PROVIDERS[provider]
    model = model or os.environ.get("CASENOTE_MODEL", default_model)
    criteria = criteria or load_criteria()
    raw = call(note, criteria, model, client)
    result, removed = verify_quotes(raw, note)
    result["removed_unverified_quotes"] = removed
    result["model"] = model
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: python src/casenote.py "note text"')
    print(json.dumps(analyze_note(sys.argv[1]), indent=2, ensure_ascii=False))
