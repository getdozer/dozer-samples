#!/usr/bin/env python3
"""Top-level unittest runner alias (`python -m unittest test_sample.py`)."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent
TESTS_DIR = ROOT / "tests"
APP_DIR = ROOT / "app"
for p in (TESTS_DIR, APP_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from test_banking_chatbot import TestDozerBankingChatbotSample  # noqa: F401

if __name__ == "__main__":
    unittest.main(verbosity=2)
