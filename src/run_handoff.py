import json
import sys

from watermark_service import InfraiPdfClient, OrderHandoff, prepare_handoff


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: python src/run_handoff.py ORDER_ID BUYER_NAME PDF_URL")
    handoff = OrderHandoff(sys.argv[1], sys.argv[2], sys.argv[3])
    print(json.dumps(prepare_handoff(handoff, InfraiPdfClient()), indent=2))


if __name__ == "__main__":
    main()

