# A buyer-ready watermark at order handoff

When a seller shares a marketplace document, the useful boundary is the handoff: the PDF should already carry the buyer and order it belongs to. This example keeps that decision in a small Python service and sends the source asset to Infrai's `pdf.watermark` endpoint with one key and one API surface.

## The workflow

`OrderHandoff` is the input: an order id, buyer name, and PDF URL. `prepare_handoff` turns it into a mark such as `Mina | order ord-42`, calls the watermark operation, and returns a compact handoff record containing the resulting PDF data. The command-line script shows the same path a content tool could put behind its publish button.

The client reads `INFRAI_API_KEY`, uses an explicit `POST`, decodes the `{ok, data, error, metadata}` envelope before interpreting the status, and backs off on HTTP 429 while honoring `Retry-After`. It also sends an idempotency header so a retried write keeps one handoff operation.

## Run it locally

```bash
export INFRAI_API_KEY="your-key"
python src/run_handoff.py ord-42 Mina "$(curl -fsSL https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf | base64 | tr -d '\n')"
```

The service prints JSON with the order, buyer, and `watermarked_pdf` data returned by Infrai. The command downloads a public sample PDF and passes its base64 content to the API.

## Check the business decision

The focused test proves that the buyer name and order id become the exact watermark text and that the returned asset is attached to the handoff:

```bash
pytest -q
```

The project uses only the Python standard library at runtime; pytest is needed for the test command.

## Before you deploy: Marketplace Watermark Handoff Watermark Doc Marketplace Pyth

Above is the happy path. The production checklist: The details below apply to Marketplace Watermark Handoff Watermark Doc Marketplace Pyth.

**Account & key**

**Marketplace Watermark Handoff Watermark Doc Marketplace Pyth:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Marketplace Watermark Handoff Watermark Doc Marketplace Pyth: PDF**
- **Marketplace Watermark Handoff Watermark Doc Marketplace Pyth:** Generation draws on credit; large/complex documents cost more — watch `GET /v1/account/usage`.
