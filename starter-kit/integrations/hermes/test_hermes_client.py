#!/usr/bin/env python3
"""test_hermes_client - the budget laws, proven offline.

Run: python test_hermes_client.py   (or python -m unittest, stdlib only)

NO live spend: every fire rides a mocked transport returning canned
response bytes; the DNS fence is tested with a patched getaddrinfo; the
only thing that touches a network here is nothing.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import hermes_client as hc


def ok_response(content="the deliverable body", pin=100, pout=50,
                finish="stop", reasoning_tokens=None):
    usage = {"prompt_tokens": pin, "completion_tokens": pout}
    if reasoning_tokens is not None:
        usage["completion_tokens_details"] = {"reasoning_tokens": reasoning_tokens}
    return {"choices": [{"message": {"content": content},
                         "finish_reason": finish}],
            "usage": usage}


def burned_response(pout=12000, reasoning_tokens=12000):
    """The EMPTY_REASONING shape: whole budget spent on hidden reasoning,
    content channel empty, finish=length."""
    return {"choices": [{"message": {"content": None},
                         "finish_reason": "length"}],
            "usage": {"prompt_tokens": 500, "completion_tokens": pout,
                      "completion_tokens_details":
                          {"reasoning_tokens": reasoning_tokens}}}


class Recorder:
    """A bank that keeps rows in memory (the ledger law, offline shape)."""

    def __init__(self):
        self.rows = []

    def __call__(self, row):
        self.rows.append(row)


class PlanCallTest(unittest.TestCase):
    def test_small_floor_applies(self):
        plan = hc.plan_call(model="anthropic/claude-sonnet-5.5",
                            prompt_chars=100, requested_max_tokens=500)
        self.assertEqual(plan.shape, "small")
        self.assertEqual(plan.max_tokens, 8000)  # requested 500 lifted to floor

    def test_review_floor_applies(self):
        plan = hc.plan_call(model="anthropic/claude-sonnet-5.5",
                            prompt_chars=hc.REVIEW_SHAPE_CHARS + 1,
                            requested_max_tokens=2000)
        self.assertEqual(plan.shape, "review")
        self.assertEqual(plan.max_tokens, 24000)

    def test_deepseek_explicit_thinking_off(self):
        plan = hc.plan_call(model="deepseek-v4.1-flash", prompt_chars=10)
        self.assertEqual(plan.extra_body.get("thinking"),
                         {"type": "disabled"})
        self.assertEqual(plan.max_tokens, 2000)  # deepseek small floor

    def test_glm_flash_uncaps_and_omits_key(self):
        plan = hc.plan_call(model="glm-5.3-flash", prompt_chars=10)
        self.assertIsNone(plan.max_tokens)
        body = hc.build_body(plan, "glm-5.3-flash", [{"role": "user",
                                                      "content": "hi"}])
        self.assertNotIn("max_tokens", body)  # uncapped = key omitted
        self.assertEqual(body["thinking"], {"type": "enabled"})
        self.assertEqual(body["reasoning_effort"], "low")

    def test_nous_primes_reasoning_rail(self):
        plan = hc.plan_call(model="glm-5.3-prime", prompt_chars=10)
        self.assertEqual(plan.extra_body.get("reasoning"), {"max_tokens": 6000})

    def test_forbidden_keys_stripped(self):
        plan = hc.plan_call(model="qwen3.7-flash", prompt_chars=10,
                            ask_extra={"reasoning": {"enabled": False},
                                       "temperature": 0.2})
        self.assertNotIn("reasoning", plan.extra_body)  # qwen 400s on it
        self.assertEqual(plan.extra_body.get("temperature"), 0.2)

    def test_plan_cannot_rewrite_model_or_messages(self):
        plan = hc.plan_call(model="deepseek-v4.1-flash", prompt_chars=10,
                            ask_extra={"model": "evil", "messages": []})
        body = hc.build_body(plan, "deepseek-v4.1-flash",
                             [{"role": "user", "content": "real"}])
        self.assertEqual(body["model"], "deepseek-v4.1-flash")
        self.assertEqual(body["messages"], [{"role": "user",
                                             "content": "real"}])

    def test_default_recipe_floors(self):
        plan = hc.plan_call(model="totally-unknown-animal", prompt_chars=10)
        self.assertEqual(plan.recipe_key, "default")
        self.assertEqual(plan.max_tokens, 8000)


class EndpointFenceTest(unittest.TestCase):
    def test_fence_rejects_foreign_shapes_before_dns(self):
        with mock.patch.object(hc.socket, "getaddrinfo",
                               side_effect=OSError("no network in tests")):
            # fence order: allowlist check runs BEFORE the DNS probe, so an
            # unreachable network still cannot sneak a foreign host through
            with self.assertRaises(RuntimeError):
                hc.fence_endpoint("http://inference-api.nousresearch.com/v1")  # not https
            with self.assertRaises(RuntimeError):
                hc.fence_endpoint("https://evil.example.com/v1/chat/completions")
            with self.assertRaises(RuntimeError):
                hc.fence_endpoint("https://inference-api.nousresearch.com:8443/v1")

    def test_public_dns_required(self):
        def fake_getaddrinfo(host, port, **kw):
            return [(2, 1, 6, "", ("127.0.0.1", 443))]
        with mock.patch.object(hc.socket, "getaddrinfo",
                               side_effect=fake_getaddrinfo):
            with self.assertRaisesRegex(RuntimeError, "non-public"):
                hc.fence_endpoint(hc.DEFAULT_ENDPOINT)

    def test_real_shape_returns_host_port_path(self):
        with mock.patch.object(hc.socket, "getaddrinfo",
                               return_value=[(2, 1, 6, "",
                                              ("93.184.216.34", 443))]):
            host, port, path = hc.fence_endpoint(hc.DEFAULT_ENDPOINT)
        self.assertEqual((host, port, path),
                         (hc.ENDPOINT_HOST, 443, "/v1/chat/completions"))


class FireTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ask_dir = Path(self.tmp.name)
        self.rec = Recorder()

    def tearDown(self):
        self.tmp.cleanup()

    def test_happy_path_banks_and_returns(self):
        calls = []

        def mock_transport(host, port, path, key, body_bytes, timeout):
            calls.append(json.loads(body_bytes))
            return ok_response(content="a real deliverable")

        out = hc.fire("anthropic/claude-haiku-4.5",
                      [{"role": "user", "content": "small ask"}],
                      key="sk-test", bank=self.rec, ask_dir=self.ask_dir,
                      ask_id="A1", transport=mock_transport, retries=0)
        self.assertTrue(out["ok"])
        # haiku has no FAMILY_TABLE row (only opus-5.5 and fable do among
        # the anthropic SKUs), so it rides the default recipe honestly
        self.assertEqual(out["recipe_key"], "default")
        # plan rode the wire: small floor 8000, not the requested nothing
        self.assertEqual(calls[0]["max_tokens"], 8000)
        self.assertEqual(calls[0]["model"], "anthropic/claude-haiku-4.5")
        # the burn banked with a cost
        self.assertEqual(len(self.rec.rows), 1)
        row = self.rec.rows[0]
        self.assertTrue(row["ok"])
        self.assertEqual(row["cost_usd"],
                         round(100 * 0.000001 + 50 * 0.000005, 4))

    def test_empty_reasoning_is_terminal(self):
        mock_transport = lambda *a, **k: burned_response()
        with self.assertRaises(hc.TerminalEmpty) as ctx:
            hc.fire("anthropic/claude-fable-5.1",
                    [{"role": "user", "content": "x" * 30}],
                    key="sk-test", bank=self.rec, ask_dir=self.ask_dir,
                    ask_id="B1", transport=mock_transport, retries=0)
        self.assertIn("hidden reasoning", ctx.exception.cause)
        # the marker minted; same params would skip on sight forever
        marker = self.ask_dir / hc.MARKER_NAME
        self.assertTrue(marker.is_file())
        self.assertIn("NEVER refires", marker.read_text(encoding="utf-8"))
        # the burn banked as data (ok False, empty_reasoning flag)
        self.assertEqual(len(self.rec.rows), 1)
        self.assertFalse(self.rec.rows[0]["ok"])
        self.assertTrue(self.rec.rows[0]["empty_reasoning"])

    def test_terminal_ask_skips_on_sight(self):
        (self.ask_dir / hc.MARKER_NAME).write_text("pre-existing", encoding="utf-8")
        def must_not_fire(*a, **k):
            raise AssertionError("a terminal ask reached the transport")
        out = hc.fire("anthropic/claude-fable-5.1",
                      [{"role": "user", "content": "x"}], key="sk-test",
                      bank=self.rec, ask_dir=self.ask_dir, ask_id="B1",
                      transport=must_not_fire)
        self.assertTrue(out["skipped"])
        self.assertEqual(self.rec.rows, [])

    def test_transport_failure_banks_data_row(self):
        def failing_transport(*a, **k):
            raise hc.TransportFailure("HTTP 402: insufficient credits")
        with self.assertRaises(hc.TransportFailure):
            hc.fire("anthropic/claude-haiku-4.5",
                    [{"role": "user", "content": "x"}], key="sk-test",
                    bank=self.rec, ask_dir=self.ask_dir, ask_id="W1",
                    transport=failing_transport, retries=0)
        self.assertEqual(len(self.rec.rows), 1)
        self.assertFalse(self.rec.rows[0]["ok"])
        self.assertIn("402", self.rec.rows[0]["transport_error"])

    def test_no_key_refuses_before_any_network(self):
        def must_not_fire(*a, **k):
            raise AssertionError("fired without a key")
        with self.assertRaisesRegex(RuntimeError, "no API key"):
            hc.fire("anthropic/claude-haiku-4.5",
                    [{"role": "user", "content": "x"}], key="",
                    bank=self.rec, ask_dir=self.ask_dir, transport=must_not_fire)

    def test_no_bank_refuses(self):
        with self.assertRaisesRegex(RuntimeError, "bank is required"):
            hc.fire("anthropic/claude-haiku-4.5",
                    [{"role": "user", "content": "x"}], key="sk-test",
                    bank=None, ask_dir=self.ask_dir,
                    transport=lambda *a, **k: ok_response())

    def test_unknown_model_fails_closed_before_firing(self):
        def must_not_fire(*a, **k):
            raise AssertionError("unknown model reached the wire")
        with self.assertRaisesRegex(ValueError, "add pricing first"):
            hc.fire("mystery/animal", [{"role": "user", "content": "x"}],
                    key="sk-test", bank=self.rec, ask_dir=self.ask_dir,
                    transport=must_not_fire)

    def test_refusal_banks_and_raises(self):
        resp = {"choices": [{"message": {"content": None,
                                         "refusal": "cannot help with that"},
                             "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 0}}
        with self.assertRaises(hc.Refused):
            hc.fire("anthropic/claude-haiku-4.5",
                    [{"role": "user", "content": "x"}], key="sk-test",
                    bank=self.rec, ask_dir=self.ask_dir, ask_id="R1",
                    transport=lambda *a, **k: resp, retries=0)
        self.assertIn("refused", self.rec.rows[0])


class GuardTerminalUnitTest(unittest.TestCase):
    def test_classify_empty_matrix(self):
        u = {"completion_tokens": 12000,
             "completion_tokens_details": {"reasoning_tokens": 12000}}
        self.assertEqual(hc.classify_empty("length", u, None),
                         hc.EMPTY_REASONING)
        self.assertEqual(hc.classify_empty("stop", u, "real content"),
                         hc.NOT_EMPTY)
        self.assertEqual(hc.classify_empty("stop", {"completion_tokens": 0},
                                           None), hc.EMPTY_OTHER)
        # burn evidence without a separate reasoning_tokens report
        self.assertEqual(hc.classify_empty("length",
                                           {"completion_tokens": 1500}, ""),
                         hc.EMPTY_REASONING)
        # sub-floor completion with no reasoning report is not burn evidence
        self.assertEqual(hc.classify_empty("length",
                                           {"completion_tokens": 40}, ""),
                         hc.EMPTY_OTHER)


if __name__ == "__main__":
    unittest.main(verbosity=2)
