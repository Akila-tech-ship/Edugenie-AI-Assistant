from __future__ import annotations

from typing import Any, Iterable

DEFAULT_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
]


def _normalize_model_name(model_name: str | None) -> str | None:
    if model_name is None:
        return None
    normalized = model_name.strip()
    if not normalized:
        return None
    if normalized.startswith("models/"):
        normalized = normalized.split("/", 1)[1]
    if normalized.startswith("model/"):
        normalized = normalized.split("/", 1)[1]
    return normalized or None


def list_available_models(client: Any) -> list[str]:
    """Return model names exposed by the Gemini API when available."""
    try:
        model_objects = client.models.list()
    except Exception:
        return []

    names: list[str] = []
    for model in model_objects:
        model_name = getattr(model, "name", None)
        if not model_name and isinstance(model, dict):
            model_name = model.get("name")
        if not model_name:
            continue
        normalized = _normalize_model_name(model_name.split("/")[-1])
        if normalized and normalized not in names:
            names.append(normalized)
    return names


def get_model_candidates(preferred_model: str | None = None, available_models: Iterable[str] | None = None) -> list[str]:
    """Return the configured model first, then all supported fallback candidates."""
    ordered: list[str] = []
    seen: set[str] = set()

    for candidate in [preferred_model, *list(available_models or []), *DEFAULT_MODELS]:
        normalized = _normalize_model_name(candidate)
        if not normalized or normalized in seen:
            continue
        ordered.append(normalized)
        seen.add(normalized)

    return ordered


def generate_with_fallback(
    client: Any,
    prompt: str,
    preferred_model: str | None = None,
    *,
    response_schema: Any | None = None,
):
    """Try the preferred model and then the supported Gemini fallbacks."""
    last_error: Exception | None = None
    candidate_models = get_model_candidates(preferred_model)

    for model_name in candidate_models:
        try:
            request_kwargs: dict[str, Any] = {
                "model": model_name,
                "contents": prompt,
            }
            if response_schema is not None:
                request_kwargs["config"] = {
                    "response_mime_type": "application/json",
                    "response_schema": response_schema,
                }
            return client.models.generate_content(**request_kwargs)
        except Exception as exc:  # pragma: no cover - depends on the live Gemini API
            last_error = exc
            if _should_try_next_model(exc):
                continue
            raise

    if last_error is not None:
        raise last_error

    raise RuntimeError("No valid Gemini model could be resolved for this app.")


def _should_try_next_model(exc: Exception) -> bool:
    status_code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
    if status_code in {404, 429, 500, 502, 503, 504}:
        return True

    message = str(exc).lower()
    return any(
        marker in message
        for marker in ("not found", "model", "unsupported", "404", "429", "503", "unavailable")
    )
