# CFMBT v5 — Conflict-First Municipal Bond Transparency
Spec for Build. Locked sitting: 2026-09-22.
Target class: public-suite civic (pattern-lab method stays off the public surface).
Lane: civic
One product sentence: a one-page conflict audit that shows the vote, the yearly General Fund hit, advisor conflicts, and a threshold self-disclosure check — without publishing a live list of natural-person bondholders.

Operating version: AOS v5.0.
Protocol: GVCP 4 (Ground, Verify, Correct, Predict). Protocol, not four desks.
Honesty labels: we-have-a-record / not-proven / people-disagree.
Incomplete beats fake-complete. Human final call.
Shareable output is identity-agnostic. Local names bind on the host at run time only.

---

## 0. Done-when lock
Build is finished when all of the following are true:

1. A single public page (or printable pack) answers three questions in ten minutes:
   - How much does this debt cost the General Fund per year?
   - Who was paid to advise or underwrite the issue?
   - Did any covered official, vendor, or family member self-disclose holdings above the threshold?
2. The page never lists natural-person beneficial owners from DTC / Cede & Co.
3. Every number and document link carries a source and a score: we-have-a-record / not-proven / people-disagree.
4. Placeholders `{{COUNTY}}`, `{{PROJECT}}`, `{{SERIES}}`, `{{YEAR}}`, `{{DEBT_SERVICE_Y1}}`, `{{ISSUE_SIZE}}`, `{{PROJECT_COST}}` are the only local tokens in the public tree.
5. No secrets, no PII, no host folder map, no git, no public bind.

If any of those five fail, lock: fail. Do not ship.

---

## 1. Method (the rule)
Disclose the conflict file and the budget line at the speed of the decision.
Publish fund-level positions where the market already allows it.
Require self-disclosure from officials, project vendors, and their families above a threshold.
Do not build a live public list of every beneficial owner — the market was never built to produce one, and privacy law will not permit it.

This combination has not been tried as one standing framework. That is the product.

---

## 2. Why this is the product (not a full owner registry)
Existing work aims at the wrong layer.

- Beneficial-ownership transparency (Tax Justice Network REBOT 2023; Open Ownership Principles 2023) targets company shells, not municipal bondholders. The 2022 CJEU ruling (joined cases C-37/20 and C-601/20) struck down general-public access to those registers as a disproportionate privacy interference.
- FDTA 2022 makes existing muni filings machine-readable. It does not add owner identity.
- SEC Rule 15c2-12 (2019) puts private bank loans on EMMA. Still no owner names.
- Dubrow & Hiteshew / ProMarket 2024 improve official-statement readability. Not ownership.
- GFOA speaks only to beneficial owners of *defaulted* bonds.
- NFMA 2015 maps transaction-participant conflicts. Advisory, not a county rule.
- Activest (~2018) is buy-side responsible investing.

Gap CFMBT fills: decision-speed conflict file + fund-level sunlight + threshold self-disclosure, while refusing an open natural-person holder list.

Tower Amendment (Exchange Act §15B(d)) bars SEC/MSRB from forcing issuer filings. It does not bar a county from an ethics rule for its own officials and vendors.

---

## 3. Three pillars

### Pillar A — Conflict file and budget line (decision-speed)
Public at the vote, or assembled from the public record immediately after.

Must show:
- Vote to borrow (date, roll call, ordinance / resolution number)
- Contract and dollar amount
- “General Fund pays about $X a year”
- What else that fund pays, and what is squeezed
- Official statement and latest audit (links)
- Underwriter, municipal advisor, bond counsel, and conflicts already disclosed under MSRB Rule G-17 (make those taxpayer-visible)
- Campaign finance, procurement, and ethics filings for officials who voted

Source of truth: county records + EMMA. No new private data collection.

### Pillar B — Fund-level positions (market sunlight)
Sunlight without naming private people.

Show:
- CUSIP(s)
- EMMA trade summary (volume, price range, last trade date)
- Any public 13F / N-PORT hit that names the CUSIP or the issuer
- Registered owner fact: Cede & Co., nominee of DTC
- Plain sentence: no public beneficial-owner list exists

Do not request or display DTC participant beneficial-owner files.
Fund-level means “Fund Family X reports a muni sleeve.” It does not mean “Resident Y holds $50,000.”

### Pillar C — Threshold self-disclosure (influence rule)
The piece that has not been run as a standing local rule.

Design:
- Threshold: interest above $5,000 in a fiscal year, **or** 5% or more of an entity that holds the bonds. Model language from common municipal conflict statutes (e.g. NY GML-style dollar and percentage tests). Local ethics code is the hook, not a new federal regime.
- Covered persons: elected officials who vote on the borrowing; county manager and finance director; project vendors and their principals; spouse and dependent children.
- Trigger: at issuance, at material amendment, annually while outstanding.
- Filing: short sworn statement to the clerk. Yes / No + amount band. No SSN, no account numbers, no exact individual position size.
- Publication: the yes/no and amount band sit next to the budget line. Non-response is published as “no response received” + date.
- Enforcement: existing ethics-commission penalties.

Typical holders are national funds. Local capture usually shows in campaign finance, procurement, advisors, and ethics filings. Pillar C catches the one case where a local actor holds the paper they approved.

---

## 4. Privacy architecture (non-negotiable)
Public surface never publishes a natural-person bondholder registry.

| Risk | Rule |
|---|---|
| CJEU 22 Nov 2022, C-37/20 & C-601/20 | No general-public natural-person holder list. Legitimate-interest access only (press, research, oversight with a stated purpose). |
| DTC book-entry | Accept it. Work around it with A–C. Do not pierce. |
| Broker KYC / BSA-AML | Stays with institutions and regulators. Not a county website feed. |
| Public-records law | Publish conflict + fund-level + budget line. Exempt personal financial detail that is not a covered-person threshold filing. |
| Over-collection | Pillar C = yes/no + amount band only. |

Design line: collect what is needed to detect influence, publish what is needed to deter it, never publish what identifies a private investor who is not a covered person.

---

## 5. Integrity kernel (every field)
Each fact on the page:

- Label: we-have-a-record / not-proven / people-disagree
- Basis: Evidence / Inference / Assumption
- Primary record beats commentary
- Software never auto-truths
- Blank is allowed. Invented complete is not.

Predict-only forecasts (what a refinance might save) stay labeled Forecast, never Record.

---

## 6. MVP — one page, four sections

Public product title (agnostic):
**County Bond Conflict Audit — {{PROJECT}} ({{SERIES}})**

### Section 1 — Decision file (Pillar A)
Fields:
- Issuer: {{COUNTY}}
- Project: {{PROJECT}}
- Series: {{SERIES}}
- Project cost: {{PROJECT_COST}}
- Bonded amount: {{ISSUE_SIZE}}
- First-year debt service: {{DEBT_SERVICE_Y1}}
- Payment source: General Fund
- Vote date / roll call / instrument number
- Use of proceeds
- Opportunity-cost note (what else the General Fund pays)
- Links: official statement (EMMA), audit, budget page
- Transaction parties: underwriter, municipal advisor, bond counsel, paying agent / trustee
- G-17 / official-statement conflict excerpts (quoted, sourced)

### Section 2 — Conflict check (Pillar C)
- Threshold printed in plain words
- Covered-person roster (roles, not home addresses)
- Request date
- Each row: Role | Name-or-seat | Response (Yes / No / No response) | Amount band | Date | Source
- Template of the sworn statement (one page, copy-ready)

Amount bands (fixed):
- None / below threshold
- $5,000–$24,999
- $25,000–$99,999
- $100,000+
- Indirect via entity ≥ 5%

### Section 3 — Fund-level sunlight (Pillar B)
- CUSIP list
- Registered owner: Cede & Co. (DTC)
- EMMA trade snapshot
- Public fund filings (if any). If none: “not-proven — no public fund filing names this CUSIP as of {{RETRIEVE_DATE}}”
- Explicit refusal of a live beneficial-owner list

### Section 4 — Method statement
Short, public, no shop codes:
The county borrowed in public and pays from the General Fund in public. Current lenders sit behind a book-entry market built in the 1980s and 1990s. Sunlight that matches the speed of county government is the vote, the yearly payment, the advisor file, and a targeted conflict rule — not a claim that nothing is known until every bond fund is named.

Cite on this section only:
- CJEU 2022 privacy boundary
- Tower Amendment federal-filing boundary
- “If a covered person fails to disclose and is later shown to hold the bonds, that is an ethics violation, not a missing owner registry.”

---

## 7. What Build must produce
One tree. No second product.

Suggested public tree (tokenized):

```
work/civic/cfmbt/
  README.md                 # this spec, trimmed of operator notes
  app/
    index.html              # the one-page audit (print-friendly)
    styles.css
    app.js                  # loads data/case.json only
  data/
    case.json               # placeholders only in the public copy
    sources.json            # url, retrieve date, score, basis
    schema.json             # field list + allowed scores
  forms/
    self-disclosure.md      # sworn statement template
  legal/
    privacy-posture.md      # Pillar B/C rules, CJEU, Tower
  conversation/
    beats.md                # six spoken beats, public-safe
```

Host bind file (not in the public copy, not committed, not pasted to chat):

```
work/civic/cfmbt/local/bind.json
```

`bind.json` is the only place local names and live dollar figures from the operator’s case may sit. Build reads bind.json on the host to fill placeholders. If bind.json is missing, the page renders placeholders and marks figures not-proven.

Do not put bind.json in a shareable zip.

---

## 8. case.json schema (public copy uses nulls)
```json
{
  "county": null,
  "project": null,
  "series": null,
  "year": null,
  "project_cost": null,
  "issue_size": null,
  "debt_service_y1": null,
  "payment_source": "General Fund",
  "vote": { "date": null, "instrument": null, "roll_call": [] },
  "parties": {
    "underwriter": null,
    "municipal_advisor": null,
    "bond_counsel": null,
    "paying_agent": null
  },
  "cusips": [],
  "registered_owner": "Cede & Co., nominee of DTC",
  "emma_os_url": null,
  "audit_url": null,
  "budget_url": null,
  "retrieve_date": null
}
```

Every non-null field in a live bind must have a matching sources.json row.

---

## 9. Conversation beats (public-safe)
Use these in the app’s “Explain this page” drawer and in spoken briefings.

1. Anchor: “This fund pays about {{DEBT_SERVICE_Y1}} a year for {{PROJECT}}. Who collects that interest?”
2. Structure, not villain: “Not a conspiracy. Book-entry. Munis live at DTC under Cede & Co. The county cannot see beneficial owners because the system was built for settlement speed.”
3. Priority: “The first question is what we can see at the speed of the vote — the roll call, the contract, the yearly hit, what else that fund pays.”
4. Influence: “Local capture shows up in campaign checks, vendor contracts, advisor fees, ethics filings. The threshold rule catches the rare case where a local actor holds the paper.”
5. Privacy: “No public list of every private holder. European courts already blocked open natural-person ownership registers. Fund-level is allowed. Private names are not, unless they are covered persons who must self-disclose.”
6. Close: “Borrowed in public, paid in public, lenders behind a 1980s–90s market. Demand the conflict file and the budget line first, a targeted disclosure rule second.”

No shop codes, no desk names, no helper names on this surface.

---

## 10. Out of scope
- Repealing the Tower Amendment
- Calling the underlying project illegitimate
- Asking DTC, the paying agent, or the trustee for beneficial-owner lists
- Federal mandate
- Pattern-lab chrome, meme desks, or private lore in the public UI
- Live trading, payments, or outbound mail
- Scraping non-official owner lists and presenting them as a record
- Storing operator identity, phone, mail, or handle in the tree

---

## 11. Build rules (host)
- who: Lead
- lane: civic
- One tree: `%HIVE_ROOT%\work\civic\cfmbt`
- Inputs: this spec file; operator bind values only if present in local/bind.json
- No git
- No public bind unless the operator says yes after Review lock: pass
- Map a tool before installing it. Tokens are not a ship.
- If a figure is missing, leave it blank and score not-proven.
- Review lock fails if inputs are blank, if Implement does not echo inputs touched, or if the done-when lock in section 0 is unmet.

Implement echo required:
```
spec: CFMBT-v5-SPEC
inputs touched: <list or none>
wrote: <paths or description>
stopped because: <done-when lock met / missing spec / asked before irreversible>
unknown: <or none>
```

---

## 12. Team routing
- Lead: file-bus only. Append this job. Do not invent product.
- Spec: this file is the Spec. Do not expand scope.
- Implement / Build: write the tree from this file.
- Review: lock pass/fail against section 0.
- Logger: dated line + optional sha256 seal of the spec bytes. A seal is not a truth score.
- Tracker: one open loop — “host PC on → Build runs civic/cfmbt.”
- Draft: public copy only after Review lock: pass.
- Queue: holds any send of the pack until operator YES.
- Analyst / Scout: used only if a live figure must be pulled from EMMA or the official statement. They do not conclude.
- Foreman: no roster change in this job.
- Inbox / Calendar: not in this job.

---

## 13. Operator bind (host only — do not copy into public product)
The originating sitting concerned a sheriff-headquarters capital issue financed with non-ad valorem capital-improvement bonds, paid from a General Fund, first-year debt service on the order of low single-digit millions, inside a larger multi-purpose issue, official registered owner Cede & Co.

Bind those live names and exact figures on the host in `local/bind.json` at run time. Until then, the app shows placeholders.

Do not treat outline figures as we-have-a-record until the official statement, budget book, or council minutes are attached as sources.

---

## 14. Sources (framework, not the local case)
- Tax Justice Network, Roadmap to Effective Beneficial Ownership Transparency (2023)
- Open Ownership, Principles for Effective Beneficial Ownership Disclosure (January 2023); Guide to Implementing BOT (2021)
- CJEU, joined cases C-37/20 and C-601/20, 22 November 2022
- Financial Data Transparency Act of 2022, Title LVIII, NDAA FY2023 (Pub. L. 117-263)
- Tower Amendment, 15 U.S.C. §78o-4(d)
- SEC Rule 15c2-12 and 2019 amendments
- Dubrow & Hiteshew, ProMarket, 23 October 2024
- NFMA, Conflicts of Interest in the Municipal Securities Market (2015)
- MSRB Rule G-17
- GFOA, communicating with beneficial owners of defaulted municipal securities
- MSRB EMMA (emma.msrb.org)

---

## 15. First slice (if Build must cut)
If time is short, ship only:
- index.html + styles.css
- data/schema.json + data/case.json (nulls)
- forms/self-disclosure.md
- legal/privacy-posture.md
- README.md with the three taxpayer questions

Fund-level lookup and live EMMA pulls can wait. Blank + not-proven is a valid first slice.

---

America First | Truth-Seeking
