# Effect broker evidence: read-only source excerpts

Captured UTC: 2026-09-11T12:17:09.3249376Z
These excerpts describe files read from a mutable working tree; they are not a deployed-process attestation. Each block names the source SHA-256 at capture. No project code or tests were executed.

## backend/server.py
Source SHA-256: 1d3ed8ca8c7d019f03d2e8410c46644f377a1bb6b03e6c94b6060330764e5536
```text
42: class RunTaskRequest(BaseModel):
43:     """Body for POST /run_task."""
44: 
45:     tool: str = Field(..., description="Tool name, e.g. read_file, run_shell")
46:     args: dict[str, Any] = Field(default_factory=dict, description="Tool arguments")
47: 
48: 
49: class RunTaskResponse(BaseModel):
50:     """Uniform Success/Failure envelope."""
51: 
52:     ok: bool
53:     tool: str
54:     result: dict[str, Any] | None = None
55:     error: str | None = None
56: 
57: 
58: @app.get("/health")
59: def health() -> dict[str, Any]:
60:     """Liveness probe."""
61:     return {
62:         "ok": True,
63:         "service": "mag-backend",
64:         "tools": sorted(TOOL_MAP),
65:         "version": "1.0.0",
66:     }
67: 
68: 
69: @app.post("/api/v1/cast/launch")
70: def cast_launch() -> dict[str, Any]:
71:     """APPROVAL-FREE launch of the LAN voice/dashboard server (the operator's 'just do shit' — the
72:     op is a REST route the backend executes, never a terminal prompt). Spawns the cast server
73:     headless (CREATE_NO_WINDOW, detached) so the phone can reach /voice at http://<PC-IP>:8765."""
74:     try:
75:         import subprocess
76:         flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
77:         proc = subprocess.Popen(
78:             [sys.executable, "-m", "mag.cast_launch", "launch", "--host", "0.0.0.0", "--port", "8765"],
79:             cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
80:             creationflags=flags, close_fds=True)
81:         return {"ok": True, "service": "mag-backend", "pid": proc.pid,
82:                 "url": "http://<PC-LAN-IP>:8765/voice",
83:                 "note": "LAN voice/dashboard launched headless via the backend REST route (no prompt)"}
84:     except Exception as e:  # noqa: BLE001
85:         return {"ok": False, "service": "mag-backend", "error": str(e)[:160]}
86: 
87: 
88: @app.post("/run_task", response_model=RunTaskResponse)
89: def run_task(req: RunTaskRequest) -> RunTaskResponse:
90:     """Dispatch a tool call. Returns Success/Failure JSON envelope."""
91:     if req.tool not in TOOL_MAP:
92:         return RunTaskResponse(
93:             ok=False,
94:             tool=req.tool,
95:             error=f"unknown tool: {req.tool}",
96:             result={"tools": sorted(TOOL_MAP)},
97:         )
98:     try:
99:         result = tool_dispatch(req.tool, req.args or {})
100:         ok = bool(result.get("ok", False))
101:         return RunTaskResponse(ok=ok, tool=req.tool, result=result)
102:     except Exception as e:  # noqa: BLE001
103:         return RunTaskResponse(
104:             ok=False,
105:             tool=req.tool,
106:             error=str(e),
107:             result={"exception": True},
108:         )
```

## tools/__init__.py
Source SHA-256: 7e64c6e96d509d10eaf8f138b23306fc5b8ca054720576390c58e2a4a13dadc8
```text
147: def dispatch(name: str, args: dict | None = None) -> dict:
148:     if name not in TOOL_MAP:
149:         return {"ok": False, "exit_code": 127, "error": f"unknown tool: {name}", "tools": list(TOOL_MAP)}
150:     args = _normalize_args(name, args)
151:     try:
152:         return TOOL_MAP[name](**args)
153:     except TypeError as e:
154:         # Convert the cryptic binding error into an actionable shape error so
155:         # the model recovers on the FIRST attempt instead of looping until the
156:         # collapse detector fires (bug #2 in the 2026-08-03 12h sovereign run).
157:         return {
158:             "ok": False,
159:             "exit_code": 2,
160:             "error": (
161:                 f"bad arguments for {name}: {e}. "
162:                 f"Expected flat named parameters: {_expected_params(name)}. "
163:                 "Emit ONE <parameter name='X'> element per argument as SIBLINGS — "
164:                 "never nest them under a single 'arguments' blob."
165:             ),
166:             "expected_params": _expected_params(name),
167:             "received_args": sorted(args),
168:         }
```

## mag/effect_broker.py
Source SHA-256: 79311798f029231ba495747d53cefef4c98afed1e6ea2c4c544639ca3f126864
```text
184: def _commit_receipt(rec: dict) -> dict:
185:     rec["status"] = "RECEIPT_COMMITTED"
186:     rec["committed_ts"] = _now()
187:     _ensure_dirs()
188:     slug = f"{rec['event_id'].replace(':', '_')}_{rec['effect']}"
189:     # unique filename
190:     ts = time.strftime("%Y%m%d_%H%M%S")
191:     path = RECEIPTS_DIR / f"{slug}_{ts}.json"
192:     for i in range(100):
193:         if not path.exists():
194:             break
195:         path = RECEIPTS_DIR / f"{slug}_{ts}_{i}.json"
196:     path.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
197:     rec["receipt_path"] = str(path.relative_to(ROOT))
198:     return rec
199: 
200: 
201: # ---------------------------------------------------------------------------
202: # Authority pre-check
203: # ---------------------------------------------------------------------------
204: 
205: def _authority_ok(authority: dict, effect: str) -> tuple[bool, str]:
206:     # The switchboard changes a grant to EXECUTING before handing it here.
207:     # Reject everything else, but do not reject the intended in-flight state.
208:     if authority.get("status") not in {"AUTHORIZED", "EXECUTING"}:
209:         return False, f"status={authority.get('status')} not executable"
210:     caps = authority.get("granted_capabilities", [])
211:     if effect not in caps:
212:         return False, f"effect {effect} not in granted_capabilities"
213:     # Deep check via policy_engine if available
214:     pe = _load_policy_engine()
215:     if pe:
216:         verdict = pe.validate_authority(authority, effect)
217:         if not verdict.get("ok"):
218:             return False, verdict.get("reason", "policy_engine denied")
219:     return True, ""
```

## mag/effect_broker.py
Source SHA-256: 79311798f029231ba495747d53cefef4c98afed1e6ea2c4c544639ca3f126864
```text
318: def _broker_fs_write(params: dict, authority: dict) -> dict:
319:     path = Path(params.get("path", ""))
320:     content = params.get("content", "")
321:     mode = params.get("mode", "write")  # write | append
322:     # allowlist check
323:     path_real = str(path.resolve())
324:     allowed = False
325:     for prefix in FS_ALLOWLIST:
326:         prefix_real = str(Path(prefix).resolve())
327:         if path_real.startswith(prefix_real):
328:             allowed = True
329:             break
330:     if not allowed:
331:         return {"ok": False, "error": f"path {path} not in FS_ALLOWLIST"}
332:     try:
333:         path.parent.mkdir(parents=True, exist_ok=True)
334:         if mode == "append":
335:             with path.open("a", encoding="utf-8") as f:
336:                 f.write(content)
337:         else:
338:             path.write_text(content, encoding="utf-8")
339:         return {"ok": True, "path": str(path), "bytes_written": len(content.encode("utf-8"))}
340:     except Exception as e:
341:         return {"ok": False, "error": repr(e)}
```

## mag/effect_broker.py
Source SHA-256: 79311798f029231ba495747d53cefef4c98afed1e6ea2c4c544639ca3f126864
```text
369: def execute(effect: str, params: dict, authority: dict) -> dict:
370:     """Execute an effect through the broker.  Returns a RECEIPT_COMMITTED dict.
371: 
372:     Receipt state machine:
373:         ENQUEUED → RUNNING → (COMPLETED | FAILED) → RECEIPT_COMMITTED
374:     """
375:     event_id = authority.get("event_id", params.get("event_id", f"anon-{int(time.time())}"))
376: 
377:     # 1. ENQUEUED
378:     rec = _receipt(event_id, effect, "ENQUEUED", params, {})
379: 
380:     # 2. Authority gate
381:     ok, reason = _authority_ok(authority, effect)
382:     if not ok:
383:         rec["status"] = "FAILED"
384:         rec["error"] = f"authority check failed: {reason}"
385:         return _commit_receipt(rec)
386: 
387:     # Validation is intentionally a non-mutating preflight.  Consume one
388:     # budget unit only after the authority gate passes and before the effect
389:     # can run; otherwise a budget existed only in prose and unlimited calls
390:     # slipped through the broker.
391:     pe = _load_policy_engine()
392:     # board_write has a second, policy-aware reference-monitor implementation
393:     # in switchboard_v2.write_board_note(); it validates and charges its own
394:     # budget after the broker preflight. Leave that effect to its owner so a
395:     # central pre-charge cannot make the owner's revalidation reject call 3.
396:     if pe is not None and effect != "board_write":
397:         budget_ok, remaining = pe.check_budget(authority, effect, decrement=True)
398:         rec["budget_remaining"] = remaining
399:         if not budget_ok:
400:             rec["status"] = "FAILED"
401:             rec["error"] = "budget exhausted"
402:             return _commit_receipt(rec)
403: 
404:     # 3. RUNNING
405:     rec["status"] = "RUNNING"
406:     rec["pre_state"] = _pre_state(effect, params)
407: 
408:     broker = BROKERS.get(effect)
409:     if broker is None:
410:         rec["status"] = "FAILED"
411:         rec["error"] = f"unknown effect: {effect}"
412:         return _commit_receipt(rec)
413: 
414:     try:
415:         result = broker(params, authority)
416:     except Exception as e:
417:         rec["status"] = "FAILED"
418:         rec["error"] = repr(e)
419:         rec["post_state"] = _post_state(effect, params, {})
420:         return _commit_receipt(rec)
421: 
422:     rec["result"] = result
423:     rec["post_state"] = _post_state(effect, params, result)
424: 
425:     if result.get("ok"):
426:         rec["status"] = "COMPLETED"
427:     else:
428:         rec["status"] = "FAILED"
429:         rec["error"] = result.get("error", "broker returned ok=False")
430: 
431:     # 4. Postcondition evidence
432:     rec["postcondition_evidence"] = _postcondition_evidence(effect, params, result)
433: 
434:     return _commit_receipt(rec)
435: 
436: 
437: def get_receipt(event_id: str, effect: str | None = None) -> dict | None:
438:     """Load the most recent receipt for an event_id / effect."""
439:     _ensure_dirs()
440:     candidates = []
441:     for p in RECEIPTS_DIR.glob("*.json"):
442:         try:
443:             data = json.loads(p.read_text(encoding="utf-8"))
444:             if data.get("event_id") == event_id:
445:                 if effect is None or data.get("effect") == effect:
446:                     candidates.append(data)
447:         except Exception:
448:             pass
449:     if not candidates:
```

## tools/filesystem.py
Source SHA-256: 1f5b46a24daf52891ef723595e2444c4dff7984cad1785530d1a240169d5bced
```text
145: def write_file(
146:     path: str,
147:     content: str | None = None,
148:     search: str | None = None,
149:     replace: str | None = None,
150:     snapshot: str | None = None,
151: ) -> dict:
152:     """Write a file, or surgically edit it.
153: 
154:     Manifesto Phase 2 semantics:
155:       - content only            -> full write (legacy, but discouraged)
156:       - search + replace        -> diff-based edit; `search` must appear exactly once
157:       - snapshot provided       -> current on-disk sha256 must match or write is rejected
158:     Returns ok=False with a precise reason when the edit would clobber or drift.
159:     """
160:     try:
161:         p = _resolve(path)
162: 
163:         # Snapshot drift guard (Base + Drift): reject if the file changed since we read it.
164:         if snapshot is not None:
165:             if not p.is_file():
166:                 return {"ok": False, "exit_code": 1, "error": "snapshot given but file missing", "path": str(p)}
167:             cur = _file_digest(p)
168:             if cur != snapshot:
169:                 return {
170:                     "ok": False,
171:                     "exit_code": 1,
172:                     "error": "DRIFT: file changed since snapshot (external edit). Re-read before writing.",
173:                     "path": str(p),
174:                     "sha256_now": cur,
175:                     "sha256_snapshot": snapshot,
176:                 }
177: 
178:         if search is not None:
179:             # diff-based edit
180:             if not p.is_file():
181:                 return {"ok": False, "exit_code": 1, "error": "search given but file missing (create with content= instead)", "path": str(p)}
182:             if replace is None:
183:                 return {"ok": False, "exit_code": 1, "error": "replace missing for search-mode edit", "path": str(p)}
184:             old = p.read_text(encoding="utf-8", errors="replace")
185:             n = old.count(search)
186:             if n == 0:
187:                 return {"ok": False, "exit_code": 1, "error": f"search text not found ({len(search)} chars)", "path": str(p)}
188:             if n > 1:
189:                 return {"ok": False, "exit_code": 1, "error": f"search text ambiguous: found {n} occurrences (use a longer anchor)", "path": str(p)}
190:             new = old.replace(search, replace, 1)
191:             p.write_text(new, encoding="utf-8")
```

## tools/filesystem.py
Source SHA-256: 1f5b46a24daf52891ef723595e2444c4dff7984cad1785530d1a240169d5bced
```text
217:         # full write (content)
218:         if content is None:
219:             return {"ok": False, "exit_code": 1, "error": "write_file needs content= or search=+replace=", "path": str(p)}
220:         p.parent.mkdir(parents=True, exist_ok=True)
221:         p.write_text(content, encoding="utf-8")
222:         result = {
223:             "ok": True,
224:             "exit_code": 0,
225:             "path": str(p),
226:             "mode": "full",
227:             "bytes": len(content.encode("utf-8")),
228:             "sha256": _file_digest(p),
229:         }
230:         if p.suffix.lower() == ".py":
231:             verified, err = _verify_py(p)
232:             result["verified"] = verified
233:             if not verified:
234:                 result["compile_error"] = err
235:                 result["output"] = f"write ok, but py_compile FAILED: {err}"
236:         return result
237:     except Exception as e:
238:         return {"ok": False, "exit_code": 1, "error": str(e)}
```

## mag/switchboard_v2.py
Source SHA-256: 7bfb9bd9ca2a3602830ee6fd93faec4cb83f3d36470d6d134b892a61fc60cc04
```text
566: def write_board_note(note: dict, authority: dict, *, budget_consumed: bool = False) -> dict:
567:     """Effect broker: write a blackboard note, fail closed unless authorized.
568: 
569:     Now re-validates the authority through policy_engine at execution time so a
570:     revoked/expired-but-cached authority cannot write after the fact.
571:     """
572:     effect = "board_write"
573:     verdict = policy_engine.validate_authority(authority, effect)
574:     if not verdict["ok"]:
575:         return {"ok": False, "err": verdict.get("reason", "denied"), "authority": authority,
576:                 "policy_check": verdict}
577:     if "board_write" not in authority.get("granted_capabilities", []):
578:         return {"ok": False, "err": "capability board_write not granted", "authority": authority}
579: 
580:     pol = policy_engine.load_policy()
581:     # Direct callers still consume a budget unit here.  The unified effect
582:     # broker consumes it immediately before dispatching this effect, so it
583:     # marks the call as already charged to avoid double-decrementing.
584:     if budget_consumed:
585:         budget = authority.get("budget") or {}
586:         used = budget.get("used") if isinstance(budget.get("used"), dict) else {}
587:         remaining = int(budget.get("max_calls", pol.get("default_budget", {}).get("max_calls", 3))) - int(used.get(effect, 0))
588:     else:
589:         budget_ok, remaining = policy_engine.check_budget(authority, effect, pol, decrement=True)
590:         if not budget_ok:
591:             return {"ok": False, "err": "board_write budget exhausted", "authority": authority,
592:                     "budget_remaining": remaining}
593: 
594:     # max_board_notes cap
595:     max_notes = int(pol.get("max_board_notes", 1000))
596:     if BB.exists():
597:         existing_count = len(list(BB.glob("bb-*.json")))
598:         if existing_count >= max_notes:
599:             return {"ok": False, "err": f"max_board_notes({max_notes}) reached", "authority": authority}
600: 
601:     try:
602:         BB.mkdir(parents=True, exist_ok=True)
603:         existing = sorted(BB.glob("bb-*.json"))
604:         seq = 0
605:         if existing:
606:             try:
607:                 seq = int(existing[-1].stem.split("-")[1])
608:             except Exception:
609:                 seq = len(existing)
610:         for _ in range(5):
611:             seq += 1
612:             path = BB / f"bb-{seq:05d}.json"
613:             if path.exists():
614:                 continue
615:             payload = {
616:                 "schema": "swarm_tools.v1",
617:                 "tool": "swarm_blackboard",
618:                 "seq": seq,
619:                 "ts": note.get("ts", _now()),
620:                 "owner": note.get("owner", "switchboard"),
621:                 "kind": note.get("kind", "finding"),
622:                 "pinned": False,
623:                 "text": note.get("text", ""),
624:                 "authority": authority,
625:                 "event": note.get("event", ""),
626:                 "step_ok": note.get("step_ok", {}),
627:             }
628:             path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
629:             return {"ok": True, "path": str(path.relative_to(ROOT)), "seq": seq,
630:                     "budget_remaining": remaining}
631:         return {"ok": False, "err": "seq collision x5"}
632:     except Exception as e:
633:         return {"ok": False, "err": repr(e)}
634: 
635: 
636: # ---------------------------------------------------------------------------
637: # Trail
638: # ---------------------------------------------------------------------------
639: 
640: def trail_append(decision: dict):
641:     """Durable receipt-chain log. Ensures receipt_status field is always present."""
642:     record = dict(decision)
643:     record.setdefault("receipt_status", record.get("status", "UNKNOWN"))
644:     TRAIL.parent.mkdir(parents=True, exist_ok=True)
645:     with TRAIL.open("a", encoding="utf-8") as f:
646:         f.write(json.dumps(record, ensure_ascii=False) + "\n")
```

## mag/policy_engine.py
Source SHA-256: 37e286e8d6681198ce835623001ac98bf3ddbc8592d313a9d983f4a7448c09e5
```text
198: def check_budget(authority: dict, effect: str, policy: dict | None = None,
199:                  decrement: bool = True) -> tuple[bool, int]:
200:     """Check (and optionally decrement) the budget counter for `effect`.
201: 
202:     Budget lives on the authority record (`authority.budget`). Each effect call
203:     decrements the counter; returns (ok, remaining) where ok is True only while
204:     remaining > 0 after the decrement. If the authority has no budget field, a
205:     default budget is created (backward compat). Thread-safe decrement.
206:     """
207:     pol = policy or load_policy()
208:     default = pol.get("default_budget", {"max_calls": 3})
209:     with _budget_lock:
210:         budget = authority.get("budget")
211:         if budget is None:
212:             budget = dict(default)
213:             authority["budget"] = budget
214:         max_calls = int(budget.get("max_calls", default.get("max_calls", 3)))
215: 
216:         # per-effect counters map effect -> calls consumed
217:         used = int(budget.get("used", {}).get(effect, 0)) if isinstance(budget.get("used"), dict) else 0
218: 
219:         if decrement:
220:             # A max_calls=3 budget permits calls 1, 2, and 3.  The previous
221:             # ``remaining > 0`` return rejected call 3 and made the harness
222:             # report a false budget failure.
223:             if used >= max_calls:
224:                 return False, 0
225:             used += 1
226:             budget.setdefault("used", {})[effect] = used
227:             remaining = max_calls - used
228:             return True, remaining
229: 
230:         remaining = max_calls - used
231:         return remaining > 0, remaining
```

## mag/verkle_knot.py
Source SHA-256: 908c9624aff227a9d944db2f21c163337bb3ce6c762adea41a529ac46a2b7777
```text
69: #
70: # Forensics: 1,044 chain rows referenced knot files that no longer existed.
71: # Cause: amend unlinks the old knot file, then rewrites the WHOLE chain file;
72: # a concurrent append (read chain → append one line) clobbered that rewrite,
73: # leaving the chain pointing at the deleted filename. Every mutator below now
74: # holds this lock, so chain read-modify-write, knot unlink and pointer write
75: # are atomic with respect to each other, process-wide and seat-wide.
76: #
77: # O_CREAT|O_EXCL create is atomic on Windows and POSIX. Stale locks (crashed
78: # holder) are broken after _LOCK_STALE_SECONDS.
79: # ───────────────────────────────────────────────────────────────────────────
80: 
81: # Amends run _rewrite_chain, which uses an incremental O(n log n) prefix-root
82: # calculation. The stale threshold must exceed the worst legitimate holder or
83: # we'd re-introduce the race.
84: _LOCK_STALE_SECONDS = 900.0
85: _LOCK_POLL_SECONDS = 0.05
86: 
87: 
88: @contextlib.contextmanager
89: def verkle_lock(timeout: float = 60.0):
90:     """Cross-process single-writer lock for the verkle chain/knots/pointers."""
91:     deadline = time.time() + timeout
92:     fd = None
93:     while True:
94:         try:
95:             fd = os.open(str(LOCK), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
96:             break
97:         except FileExistsError:
98:             try:
99:                 stale = time.time() - LOCK.stat().st_mtime > _LOCK_STALE_SECONDS
100:                 # A crashed writer can leave a fresh-looking marker behind (for
101:                 # example after a test/process is terminated).  Do not wait the
102:                 # full 15-minute safety window when the recorded owner is gone.
103:                 if not stale:
104:                     try:
105:                         owner = int(LOCK.read_text(encoding="utf-8", errors="replace").split()[0])
106:                     except (OSError, ValueError, IndexError):
107:                         owner = 0
108:                     if owner and owner != os.getpid():
109:                         try:
110:                             os.kill(owner, 0)
111:                         except ProcessLookupError:
112:                             stale = True
113:                         except PermissionError:
114:                             # Cannot prove the owner is dead; preserve the lock.
115:                             stale = False
116:                         except SystemError:
117:                             # CPython on some Windows builds surfaces a missing
118:                             # PID as SystemError (WinError 87) instead of OSError.
119:                             stale = True
120:                         except OSError:
121:                             # Windows may report a generic missing-process error.
122:                             stale = True
123:                 if stale:
124:                     LOCK.unlink()  # crashed holder — break the stale lock
125:             except OSError:
126:                 pass
127:             if time.time() > deadline:
128:                 raise TimeoutError(f"verkle_lock timeout after {timeout}s (holder pid: "
129:                                    f"{LOCK.read_text(encoding='utf-8', errors='replace')[:16] if LOCK.is_file() else '?'})")
130:             time.sleep(_LOCK_POLL_SECONDS)
131:     try:
132:         os.write(fd, f"{os.getpid()} {datetime.now(timezone.utc).isoformat()}".encode("utf-8"))
133:         yield
134:     finally:
135:         try:
136:             os.close(fd)
137:         finally:
138:             with contextlib.suppress(OSError):
139:                 LOCK.unlink()
140: 
```

## mag/verkle_knot.py
Source SHA-256: 908c9624aff227a9d944db2f21c163337bb3ce6c762adea41a529ac46a2b7777
```text
552: def _write_tip_atomic(tip: dict[str, Any]) -> None:
553:     """Replace the small tip pointer atomically while holding ``verkle_lock``."""
554:     TIP.parent.mkdir(parents=True, exist_ok=True)
555:     tmp = TIP.with_name(f"{TIP.name}.{os.getpid()}.tmp")
556:     try:
557:         tmp.write_text(json.dumps(tip, indent=2) + "\n", encoding="utf-8")
558:         os.replace(tmp, TIP)
559:     finally:
560:         with contextlib.suppress(OSError):
561:             tmp.unlink()
562: 
```

## mag/verkle_knot.py
Source SHA-256: 908c9624aff227a9d944db2f21c163337bb3ce6c762adea41a529ac46a2b7777
```text
606: def _append_verkle_knot_unlocked(dossier: dict[str, Any], pdf_path: str | None = None) -> dict[str, Any]:
607:     """
608:     Write/update one leaf per session (amend in place).
609: 
610:     Same session_id → replace existing chain row + knot file (no bloat).
611:     New session_id → append. Same leaf_hash → skip.
612: 
613:     INTEGRITY GATE (2026-08-16, party_subchain pattern): refuse to extend an unverified chain.
614:     """
615:     ok, why = _verify_chain_consistent()
616:     if not ok:
617:         return {"ok": False, "schema": SCHEMA, "error": "refusing to extend an unverified verkle chain",
618:                 "verify": why}
619:     KNOTS.mkdir(parents=True, exist_ok=True)
620:     leaf = build_leaf_from_dossier(dossier)
621:     fname = knot_filename(
622:         start_minute_iso=leaf.get("start_minute"),
623:         dominant_theme=leaf.get("dominant_theme"),
624:         session_id=str(leaf.get("session_id") or ""),
625:         commit_hex=str(leaf.get("dossier_commit") or leaf.get("leaf_hash") or ""),
626:         chord_slug=leaf.get("chord_commitment"),
627:     )
628:     leaf["filename"] = fname
629:     if pdf_path:
630:         leaf["pdf_path"] = pdf_path
631: 
632:     sid = str(leaf.get("session_id") or "unknown")
633:     rows = _load_chain_rows()
634:     existing_i = next(
635:         (i for i, r in enumerate(rows) if str(r.get("session_id") or "") == sid),
636:         None,
637:     )
638: 
639:     # identical content already recorded for this session
640:     if existing_i is not None and rows[existing_i].get("leaf_hash") == leaf["leaf_hash"]:
641:         tip = json.loads(TIP.read_text(encoding="utf-8")) if TIP.is_file() else {}
642:         return {
643:             "ok": True,
644:             "skipped": True,
645:             "amended": False,
646:             "filename": fname,
647:             "leaf_hash": leaf["leaf_hash"],
648:             "verkle_root": tip.get("root"),
649:             "path": str(KNOTS / fname),
650:             "n_leaves": tip.get("n_leaves") or len(rows),
651:         }
652: 
653:     # drop old knot file for this session if filename changed
654:     if existing_i is not None:
655:         old_name = rows[existing_i].get("filename")
656:         if old_name and old_name != fname:
657:             old_path = KNOTS / str(old_name)
658:             if old_path.is_file():
659:                 try:
660:                     old_path.unlink()
661:                 except OSError:
662:                     pass
663: 
664:     path = KNOTS / fname
665:     path.write_text(json.dumps(leaf, indent=2), encoding="utf-8")
666:     pointer_doc = {"filename": fname, "leaf_hash": leaf["leaf_hash"], "session_id": sid,
667:                    "schema": "verkle_session_pointer.v2"}
668:     _safe_sid = re.sub(r"[^A-Za-z0-9._-]+", "-", sid)[:12]
669:     (KNOTS / f"by-session_{_safe_sid}.json").write_text(
670:         json.dumps(pointer_doc, indent=2), encoding="utf-8"
671:     )
672:     session_pointer_v2(sid).write_text(json.dumps(pointer_doc, indent=2), encoding="utf-8")
673: 
674:     chain_row = {
675:         "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
676:         "filename": fname,
677:         "leaf_hash": leaf["leaf_hash"],
678:         "session_id": leaf.get("session_id"),
679:         "start_minute": leaf.get("start_minute"),
680:         "end_minute": leaf.get("end_minute"),
681:         "dominant_theme": leaf.get("dominant_theme"),
682:         "theme_vector_normalized": leaf.get("theme_vector_normalized"),
683:         "tension_index": leaf.get("tension_index"),
684:         "dossier_commit": leaf.get("dossier_commit"),
685:         "amended": existing_i is not None,
686:     }
687:     if existing_i is not None:
688:         # PRESERVE repair/custom fields across amend (2026-08-25): a flagged
689:         # evidence_lost row being re-folded must NOT silently lose its flag.
690:         # The canary (chain_guard) caught exactly this — flags dropped
691:         # 1,039 -> 1,029 as normal folds amended flagged sessions. The fresh
692:         # chain_row below is built from a fixed field set, so carry forward
693:         # any repair fields present on the row being replaced.
694:         for _k in ("evidence_lost", "repaired_from_pointer"):
695:             if rows[existing_i].get(_k) is not None:
696:                 chain_row[_k] = rows[existing_i][_k]
697:         rows[existing_i] = chain_row
698:         amended = True
699:         # AMEND (2026-08-16): history changes -> full rewrite is correct (rare, on re-summarize).
700:         all_hashes = _rewrite_chain(rows)
701:     else:
702:         rows.append(chain_row)
703:         amended = False
704:         # PURE APPEND (2026-08-16, Option A incremental): a new leaf does NOT require rewriting
705:         # every row's merkle root. Compute the new root ONCE (O(n), not O(n^2)) and append one line.
706:         # This was the 65s O(n^2) landmine (5,874 leaves -> ~34M sha256 on every append).
707:         all_hashes = [r.get("leaf_hash") for r in rows if r.get("leaf_hash")]
708:         root = _merkle_root(all_hashes) if all_hashes else _h(b"empty")
709:         parent_root = _merkle_root(all_hashes[:-1]) if len(all_hashes) > 1 else _h(b"empty")
710:         chain_row["index"] = len(all_hashes) - 1
711:         chain_row["n_leaves"] = len(all_hashes)
712:         chain_row["parent_verkle_root"] = parent_root
713:         chain_row["verkle_root"] = root
714:         CHAIN.parent.mkdir(parents=True, exist_ok=True)
715:         with CHAIN.open("a", encoding="utf-8") as fh:
716:             fh.write(json.dumps(chain_row, ensure_ascii=False) + "\n")
717:         root = chain_row["verkle_root"]
718: 
719:     root = _merkle_root(all_hashes) if all_hashes else _h(b"empty")
720:     parent_root = (
721:         _merkle_root(all_hashes[:-1]) if len(all_hashes) > 1 else _h(b"empty")
722:     )
723: 
724:     tip = {
725:         "schema": "verkle_tip.v1",
726:         "root": root,
727:         "n_leaves": len(all_hashes),
728:         "last_filename": fname,
729:         "last_leaf_hash": leaf["leaf_hash"],
730:         "last_session_id": leaf.get("session_id"),
731:         "updated_minute": leaf.get("end_minute") or leaf.get("start_minute"),
732:         "note": "One leaf per session; amend in place on re-summarize. Merkle–Verkle hybrid tip.",
733:     }
734:     TIP.write_text(json.dumps(tip, indent=2), encoding="utf-8")
735:     (BIO / "latest.knot.json").write_text(json.dumps(leaf, indent=2), encoding="utf-8")
736: 
737:     _update_topic_evolution(leaf, root, len(all_hashes), amend_session=sid)
738: 
739:     return {
740:         "ok": True,
741:         "amended": amended,
742:         "filename": fname,
743:         "path": str(path),
744:         "leaf_hash": leaf["leaf_hash"],
745:         "verkle_root": root,
746:         "parent_verkle_root": parent_root,
747:         "n_leaves": len(all_hashes),
748:         "chain": str(CHAIN),
749:         "tip": str(TIP),
750:         "evolution": str(EVOLUTION),
751:     }
752: 
753: 
754: def append_verkle_knot(dossier: dict[str, Any], pdf_path: str | None = None) -> dict[str, Any]:
755:     """Locked entry point — see _append_verkle_knot_unlocked for the real body.
756: 
757:     Single-writer lock makes chain read-modify-write + knot unlink + pointer
758:     write atomic against concurrent seats (the 2026-08-25 lost-update fix).
759:     """
760:     with verkle_lock():
761:         return _append_verkle_knot_unlocked(dossier, pdf_path)
```

## mag/verkle_lance.py
Source SHA-256: 1c7dc9b8a88d0f3b3dd634e03dbaebb03e03f5794e4918387de770df5c4e0d71
```text
148: def link(event: str, *, when: str = "") -> dict[str, Any]:
149:     """Tie an event temporally: the knot at/before its time and the verkle root at that point.
150: 
151:     This is the 'map to events tying them together temporally' op: given an event (a label/flow or
152:     an ISO time), find the chain position it lands in and the root that anchors it.
153:     """
154:     rows = _load_chain()
155:     if not rows:
156:         return {"ok": True, "schema": SCHEMA, "event": event, "found": False}
157:     # direct session/theme match first
158:     matched = [r for r in rows if _matches(event, r)]
159:     if matched:
160:         h = matched[-1]
161:         return {"ok": True, "schema": SCHEMA, "event": event, "found": True,
162:                 "knot": _knot_meta(h), "verkle_root": h.get("verkle_root"),
163:                 "n_knots_at_point": (h.get("index") or 0) + 1}
164:     # else temporal anchor: nearest knot by time
165:     tgt = None
166:     if when:
167:         try:
168:             tgt = datetime.fromisoformat(when.replace("Z", "+00:00"))
169:         except ValueError:
170:             tgt = None
171:     if tgt:
172:         best = None
173:         for r in rows:
174:             ts = r.get("ts") or r.get("start_minute")
175:             if not ts:
176:                 continue
177:             try:
178:                 dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
179:             except ValueError:
180:                 continue
181:             if dt <= tgt:
182:                 best = r
183:             else:
184:                 break
185:         if best:
186:             return {"ok": True, "schema": SCHEMA, "event": event, "found": True,
187:                     "knot": _knot_meta(best), "verkle_root": best.get("verkle_root"),
188:                     "temporal": "nearest_at_or_before"}
189:     return {"ok": True, "schema": SCHEMA, "event": event, "found": False,
190:             "note": "no session/theme match and no time anchor given; see temporal()"}
```
