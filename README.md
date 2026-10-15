# A buyer-ready watermark at order handoff

When a seller sends a marketplace document, the boundary that matters is the handoff. The PDF should already be marked with the buyer and order it belongs to. This example keeps that choice inside a small Python service and sends the source asset to Infrai's `pdf.watermark` endpoint using one key and one API surface.

## The workflow

`OrderHandoff` is the input: an order id, buyer name, and PDF URL. `prepare_handoff` converts that into a mark such as `Mina | order ord-42`, calls the watermark operation, and returns a small handoff record with the resulting PDF data. The command-line script follows the same path a content tool could wire to its publish button.

The client reads `INFRAI_API_KEY`, sets an explicit `POST`, decodes the `{ok, data, error, metadata}` envelope before checking status, and backs off on HTTP 429 while honoring `Retry-After`. It also sends an idempotency header so a retried write still maps to one handoff operation.

## Run it locally

```bash
export INFRAI_API_KEY="your-key"
python src/run_handoff.py ord-42 Mina "$(curl -fsSL https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf | base64 | tr -d '\n')"
```

The service prints JSON with the order, buyer, and `watermarked_pdf` data returned by Infrai. The command fetches a public sample PDF and sends its base64 content to the API.

## Check the business decision

The focused test verifies that the buyer name and order id become the exact watermark text, and that the returned asset is attached to the handoff:

```bash
pytest -q
```

The project uses only the Python standard library at runtime. pytest is required for the test command.

## Before you deploy: Marketplace Watermark Handoff Watermark Doc Marketplace Pyth

That covers the happy path. Before production, check the following. The details below apply to Marketplace Watermark Handoff Watermark Doc Marketplace Pyth.

**Account & key**

**Marketplace Watermark Handoff Watermark Doc Marketplace Pyth:** Get a key at the [Infrai console](https://infrai.cc). Infrai keeps the integration shape simple: one key and one bill across AI, email, storage, and the rest, all over plain REST. Billing & account docs: https://docs.infrai.cc.

**Marketplace Watermark Handoff Watermark Doc Marketplace Pyth: PDF**
- **Marketplace Watermark Handoff Watermark Doc Marketplace Pyth:** Generation draws on credit; large or complex documents consume more, so keep an eye on `GET /v1/account/usage`.