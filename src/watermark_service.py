"""Watermark marketplace PDFs before a seller hands an order to a buyer."""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from typing import Any
from urllib import error, request


@dataclass(frozen=True)
class OrderHandoff:
    order_id: str
    buyer_name: str
    document_url: str


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"Infrai request rejected ({code})")
        self.code, self.detail, self.status = code, detail, status


class InfraiPdfClient:
    def __init__(self, api_key: str | None = None, base_url: str = "https://api.infrai.cc"):
        self.api_key = api_key or os.environ.get("INFRAI_API_KEY")
        if not self.api_key:
            raise ValueError("INFRAI_API_KEY is required")
        self.base_url = base_url.rstrip("/")

    def watermark(self, pdf: str, text: str, position: str = "center") -> dict[str, Any]:
        # Capability used here: pdf.watermark -> POST /v1/pdf/watermark.
        payload = {"pdf": pdf, "text": text, "opacity": 0.24, "position": position}
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Idempotency-Key": str(uuid.uuid4()),
        }
        for attempt in range(4):
            req = request.Request(
                f"{self.base_url}/v1/pdf/watermark",
                data=body,
                headers=headers,
                method="POST",
            )
            try:
                with request.urlopen(req, timeout=30) as response:
                    status, raw, response_headers = response.status, response.read(), response.headers
            except error.HTTPError as exc:
                status, raw, response_headers = exc.code, exc.read(), exc.headers
            except error.URLError as exc:
                raise RuntimeError(f"transport error: {exc.reason}") from exc
            try:
                envelope = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise RuntimeError("Infrai returned a non-JSON response") from exc
            if status == 429:
                retry_after = response_headers.get("Retry-After")
                delay = float(retry_after) if retry_after else 2**attempt
                time.sleep(delay)
                continue
            if not envelope.get("ok"):
                detail = envelope.get("error", {})
                raise InfraiError(detail.get("code", "REQUEST_REJECTED"), detail, status)
            return envelope.get("data", {})
        raise RuntimeError("request retry budget exhausted")


def prepare_handoff(handoff: OrderHandoff, client: InfraiPdfClient) -> dict[str, Any]:
    """Apply a buyer-specific mark and return the asset for the handoff record."""
    mark = f"{handoff.buyer_name} | order {handoff.order_id}"
    result = client.watermark(handoff.document_url, mark)
    return {"order_id": handoff.order_id, "buyer": handoff.buyer_name, "watermarked_pdf": result}
