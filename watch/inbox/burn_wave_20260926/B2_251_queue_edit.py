"""B2-251 checkbox truth audit: queue edit pass 1.

Flips unearned checked Open rows back to unchecked with dated no-erase
annotations, and attaches resolvable receipt pointers to landed rows whose
text never named their own landing receipt. Every action is keyed on a unique
line prefix; the script aborts without writing if any key matches zero lines.
Append-only on row text: nothing is erased.
"""
import sys

QUEUE = 'watch/inbox/burn_wave_20260926/QUEUE.md'
RECEIPT = 'watch/inbox/burn_wave_20260926/B2_251_checkbox_audit_20260926.md'

FLIP_ANNOTATION = (
    ' (2026-09-26 B2-251 checkbox audit: [x] flipped to [ ], no resolvable'
    ' landing receipt on disk at audit time; no bytes erased, prior checked'
    ' state recorded in ' + RECEIPT + ')'
)

# (unique row key, extra honesty clause or '')
# note: the B2-255 double-spend sweep landed mid-audit and renumbered the
# second claimants, so the flips target the new ids (renumbered briefs carry
# the same subjects; verified before the edit).
FLIPS = [
    ('- [x] B2-247 Reconcile collected-files vs disk-candidates gap', ''),
    ('- [x] B2-286 model-null hole in chat_provider',
     ' providers.yaml z_ai2/z_ai3 still carry no default_model'),
    ('- [x] B2-287 live re-verify of the reasoning floor',
     ' no own-lane receipt on disk'),
    ('- [x] B2-288 pre-existing test debt stash-proven',
     ' the drift_dashboard half is provable only as the tools/drift_dashboard.py'
     ' receipt comment'),
    ('- [x] B2-297 living-downgrade detector',
     ' no detector code in mag/shared_surface.py'),
    ('- [x] B2-298 drift-patrol prompt persistence',
     ' no repo-side prompt copy found'),
    ('- [x] B2-299 fold verify cwd trap',
     ' index_fold_host.mjs verify still resolves items against cwd'),
]

# (unique row key, receipt basename). Rows already naming their own receipt
# basename are skipped automatically.
ATTACH_SUBJECT = [
    ('- [x] B2-215 Census freshness tripwire', 'B2_215_census_tripwire_20260926.md'),
    ('- [x] B2-216 Collected-vs-executed delta', 'B2_216_collect_delta_20260926.md'),
    ('- [x] B2-221 Living-law census owed', 'B2_221_prefix_editor_20260926.md'),
    ('- [x] B2-222 Register the hot unregistered', 'B2_222_hot_living_20260926.md'),
    ('- [x] B2-223 mimo_watch.jsonl living re-registration', 'B2_223_mimo_living_20260926.md'),
    ('- [x] B2-236 mimo probe 403 retest', 'B2_236_mimo_retest_20260926.md'),
    ('- [x] B2-237 Attribute the 13:53:18Z', 'B2_237_touch_law_20260926.md'),
    ('- [x] B2-242 QUANTITY substring false exclusions', 'B2_242_quantity_bounds_20260926.md'),
    ('- [x] B2-243 Caption ledger residual bucket audit', 'B2_243_bucket_audit_20260926.md'),
    ('- [x] B2-244 Census carrier collected-count drift', 'B2_244_collect_deep_20260926.md'),
    ('- [x] B2-285 Guard-class regression pin', 'B2_244_guard_pin_20260926.md'),
    ('- [x] B2-246 Schedule the --collect deep check', 'B2_246_collect_schedule_20260926.md'),
    ('- [x] B2-250 Shared-file edit claim convention', 'B2_250_file_claims_20260926.md'),
    ('- [x] B2-254 Living re-classification regression', 'B2_254_living_regression_20260926.md'),
    ('- [x] B2-256 Caption ledger guard pin for the B2-243 classes', 'B2_256_class_pin_20260926.md'),
    ('- [x] B2-257 Year-inference ladder', 'B2_257_year_ladder_20260926.md'),
    ('- [x] B2-258 Year-first month-day extraction', 'B2_258_yearfirst_20260926.md'),
]

# id-keyed batch for the pre-law wave receipts (attach only if still checked
# and the basename is not already named in the row)
ATTACH_IDS = {
    11: 'B2_11_mimosa_close_20260926.md',
    12: 'B2_12_caption_ledger_20260926.md',
    13: 'B2_13_scenario_cards_20260926.md',
    14: 'B2_14_qdrop874_20260926.md',
    15: 'B2_15_xintel_dig_20260926.md',
    16: 'B2_16_uf_sweep_20260926.md',
    17: 'B2_17_adventure2d6_20260926.md',
    18: 'B2_18_stone2b_20260926.md',
    19: 'B2_19_improve_backlog_20260926.md',
    20: 'B2_20_loop_gaps_20260926.md',
    21: 'B2_21_doctor_probe_20260926.md',
    22: 'B2_22_fts5_spike_20260926.md',
    23: 'B2_23_seed_flip_card_20260926.md',
    24: 'B2_24_carrier_scan_20260926.md',
    25: 'B2_25_envelope_remeasure_20260926.md',
    26: 'B2_26_links_sha_backfill_20260926.md',
    27: 'B2_27_scout_checkgate_20260926.md',
    28: 'B2_28_schema_split_20260926.md',
    29: 'B2_29_rbxlx_rebuild_20260926.md',
    30: 'B2_30_shadowledger_live_20260926.md',
    31: 'B2_31_poll_tripwire_20260926.md',
    32: 'B2_32_cascade_wire_20260926.md',
    33: 'B2_33_rejection_recount_20260926.md',
    34: 'B2_34_cluster_detectors_20260926.md',
    35: 'B2_35_groq_surgery_20260926.md',
    36: 'B2_36_cerebras_reclassify_20260926.md',
    37: 'B2_37_provider_health_close_20260926.md',
    40: 'B2_40_fold_poison_guard_20260926.md',
    41: 'B2_41_hash_freshness_20260926.md',
    42: 'B2_42_events_hygiene_20260926.md',
    50: 'B2_50_missing_triage_20260926.md',
    51: 'B2_51_autorun_autopsy_20260926.md',
    52: 'B2_52_bridge_card_20260926.md',
    53: 'B2_53_grok_fire_card_20260926.md',
    54: 'B2_54_cron_arm_card_20260926.md',
    55: 'B2_55_buildlane_flip_20260926.md',
    56: 'B2_56_returncode_law_20260926.md',
    57: 'B2_57_uf_promotion_20260926.md',
    58: 'B2_58_prompt_amendments_20260926.md',
    59: 'B2_59_miprov2_dig_20260926.md',
    60: 'B2_60_judge_independence_20260926.md',
    61: 'B2_61_roster_purge_20260926.md',
    62: 'B2_62_zai_backoff_20260926.md',
    63: 'B2_63_gemini_auth_20260926.md',
    64: 'B2_64_drift_dashboard_20260926.md',
    65: 'B2_65_registry_revival_20260926.md',
    66: 'B2_66_aging_guard_20260926.md',
    67: 'B2_67_qvision_fixes_20260926.md',
    68: 'B2_68_fraction_guard_20260926.md',
    69: 'B2_69_test_census_20260926.md',
    70: 'B2_70_referee_refresh_20260926.md',
    71: 'B2_71_hill_build_20260926.md',
    72: 'B2_72_order_sensitivity_20260926.md',
    145: 'B2_145_phantom_paths_20260926.md',
    146: 'B2_146_unregistered_files_20260926.md',
    156: 'B2_156_living_hash_law_20260926.md',
    157: 'B2_157_prefix_case_20260926.md',
    197: 'B2_197_living_census_20260926.md',
    198: 'B2_198_owed_receipt_20260926.md',
    199: 'B2_199_patrol_living_20260926.md',
    219: 'B2_219_misdate_classes_20260926.md',
    220: 'B2_220_dotted_guards_20260926.md',
    238: 'B2_238_checkbox_law_20260926.md',
    235: 'B2_235_mimo_revival_20260926.md',
    252: 'B2_252_error_capture_20260926.md',
    253: 'B2_253_transport_decision_20260926.md',
    259: 'B2_259_pin_law_20260926.md',
    260: 'B2_260_verifier_gate_20260926.md',
}


def main():
    with open(QUEUE, encoding='utf-8', newline='') as f:
        raw = f.read()
    lines = raw.split('\n')
    actions = []
    abort = []

    def find_rows(prefix):
        return [i for i, l in enumerate(lines) if l.startswith(prefix)]

    # flips
    for key, extra in FLIPS:
        hits = find_rows(key)
        if len(hits) != 1:
            abort.append(f'FLIP key matched {len(hits)} lines: {key}')
            continue
        i = hits[0]
        line = lines[i]
        clause = FLIP_ANNOTATION
        if extra:
            clause = clause[:-1] + ';' + extra + ')'
        lines[i] = '- [ ]' + line[5:] + clause
        actions.append(f'FLIP line {i+1}: {key[7:60]}')

    # subject-keyed attachments
    for key, base in ATTACH_SUBJECT:
        hits = find_rows(key)
        if len(hits) != 1:
            abort.append(f'ATTACH key matched {len(hits)} lines: {key}')
            continue
        i = hits[0]
        if base in lines[i]:
            actions.append(f'SKIP (already named) line {i+1}: {base}')
            continue
        if not lines[i].startswith('- [x]'):
            actions.append(f'SKIP (now unchecked) line {i+1}: {key[7:50]}')
            continue
        lines[i] = lines[i] + f' (receipt attachment 2026-09-26, B2-251 audit: watch/inbox/burn_wave_20260926/{base})'
        actions.append(f'ATTACH line {i+1}: {base}')

    # id-keyed attachments
    for bid, base in sorted(ATTACH_IDS.items()):
        for state in ('- [x]', '- [ ]'):
            key = f'{state} B2-{bid} '
            hits = find_rows(key)
            if hits:
                break
        else:
            abort.append(f'ATTACH id B2-{bid} matched no row')
            continue
        if len(hits) != 1:
            abort.append(f'ATTACH id B2-{bid} matched {len(hits)} rows')
            continue
        i = hits[0]
        if base in lines[i]:
            actions.append(f'SKIP (already named) line {i+1}: {base}')
            continue
        if not lines[i].startswith('- [x]'):
            actions.append(f'SKIP (now unchecked) line {i+1}: B2-{bid}')
            continue
        lines[i] = lines[i] + f' (receipt attachment 2026-09-26, B2-251 audit: watch/inbox/burn_wave_20260926/{base})'
        actions.append(f'ATTACH line {i+1}: B2-{bid} {base}')

    if abort:
        print('ABORT, no bytes written:')
        for a in abort:
            print('  ' + a)
        sys.exit(2)

    with open(QUEUE, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(lines))
    for a in actions:
        print(a)
    print(f'total actions: {len(actions)}')


if __name__ == '__main__':
    main()
