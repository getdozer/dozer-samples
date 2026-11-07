#!/usr/bin/env python3
"""Interactive / One-Command Demo for the Dozer + Vector DB + LangChain Banking Chatbot."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
APP_DIR = ROOT / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from banking_chatbot import main

if __name__ == "__main__":
    # Run Customer C001 demo followed by C003 Real-Time CDC simulation if no CLI args passed
    if len(sys.argv) == 1:
        rc = main(
            [
                "--offline-fixture",
                "--customer",
                "C001",
                "--question",
                "Which card is best for travel and dining rewards?",
            ]
        )
        if rc != 0:
            raise SystemExit(rc)
        print()
        raise SystemExit(
            main(
                [
                    "--offline-fixture",
                    "--customer",
                    "C003",
                    "--simulate-realtime-tx",
                ]
            )
        )
    raise SystemExit(main())
