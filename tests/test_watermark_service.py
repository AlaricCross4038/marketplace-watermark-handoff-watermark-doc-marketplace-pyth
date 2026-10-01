import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from watermark_service import OrderHandoff, prepare_handoff


class RecordingClient:
    def __init__(self):
        self.calls = []

    def watermark(self, pdf, text, position="center"):
        self.calls.append((pdf, text, position))
        return {"url": "https://files.example/watermarked.pdf"}


def test_handoff_marks_the_buyer_and_order():
    client = RecordingClient()
    handoff = OrderHandoff("ord-42", "Mina", "https://files.example/source.pdf")
    result = prepare_handoff(handoff, client)
    assert client.calls == [("https://files.example/source.pdf", "Mina | order ord-42", "center")]
    assert result["watermarked_pdf"]["url"].endswith("watermarked.pdf")
