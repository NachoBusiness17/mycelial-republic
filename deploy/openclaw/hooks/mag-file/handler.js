"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const BOARD = process.env.MAG_BOARD || "/board";

function append(name, rec) {
  try {
    fs.mkdirSync(BOARD, { recursive: true });
    fs.appendFileSync(path.join(BOARD, name), JSON.stringify(rec) + "\n");
  } catch (_e) {
    /* never stall the gateway */
  }
}

function appendTrajectory(rec) {
  try {
    fs.mkdirSync(BOARD, { recursive: true });
    const target = path.join(BOARD, "openclaw_traj.jsonl");
    const body = JSON.stringify(rec);
    const bodyBytes = Buffer.from(body + "\n", "utf8");
    const startByte = fs.existsSync(target) ? fs.statSync(target).size : 0;
    // Count physical JSONL lines, including blank/malformed legacy lines.
    // Filtering empty strings shifts every later lineRange after a damaged
    // append, making an otherwise valid span impossible to dereference.
    let previous = 0;
    if (fs.existsSync(target)) {
      const existing = fs.readFileSync(target);
      previous = existing.length ? existing.toString("utf8").split("\n").length - 1 : 0;
      if (existing.length && existing[existing.length - 1] !== 0x0a) previous += 1;
    }
    const bounded = {
      ...rec,
      metadata: {
        schema: "trajectory_span.v1",
        spanId: crypto.randomUUID(),
        lineRange: [previous + 1, previous + 1],
        // byteRange describes the serialized bounded record that is actually
        // appended, not the unbounded pre-metadata input record.
        byteRange: [startByte, 0],
        bodySha256: crypto.createHash("sha256").update(bodyBytes).digest("hex"),
        pathsTouched: Array.isArray(rec.pathsTouched) ? rec.pathsTouched : [],
        tokenCount: Number(rec.tokensAfter || 0),
      },
    };
    // The byte range is part of the serialized record, so its digit count can
    // change the record length.  Iterate to a fixed point before appending;
    // stamping it once with a placeholder produces stale/zero end offsets.
    let endByte = startByte;
    let finalBytes = Buffer.alloc(0);
    for (let i = 0; i < 8; i += 1) {
      bounded.metadata.byteRange = [startByte, endByte];
      finalBytes = Buffer.from(JSON.stringify(bounded) + "\n", "utf8");
      const nextEnd = startByte + finalBytes.length;
      if (nextEnd === endByte) break;
      endByte = nextEnd;
    }
    bounded.metadata.byteRange = [startByte, endByte];
    finalBytes = Buffer.from(JSON.stringify(bounded) + "\n", "utf8");
    if (startByte + finalBytes.length !== endByte) {
      bounded.metadata.byteRange[1] = startByte + finalBytes.length;
      finalBytes = Buffer.from(JSON.stringify(bounded) + "\n", "utf8");
    }
    fs.appendFileSync(target, finalBytes);
  } catch (_e) {
    /* trajectory evidence must never stall the gateway */
  }
}

async function handler(event) {
  const ctx = event.context || {};
  const rec = {
    ts: new Date().toISOString(),
    seat: "claw",
    event: [event.type, event.action].filter(Boolean).join(":"),
    thread: String(event.sessionKey || "main").slice(0, 60),
    text: String(ctx.content || ctx.reason || event.type || "").slice(0, 2000),
  };
  const toolName = ctx.toolName || ctx.tool || ctx.name;
  if (toolName || /tool/i.test(rec.event)) {
    rec.event = "tool";
    rec.tool = String(toolName || rec.event).slice(0, 40);
    const payload = String(ctx.content || ctx.params || ctx.input || rec.text || "").slice(0, 500);
    rec.text = ">tool " + rec.tool + (payload ? "\n>" + payload.replace(/\n/g, "\n>") : "");
  }
  if (ctx.success === false) rec.status = "unverified";
  append("room.jsonl", rec);
  if (event.type === "session" && String(event.action || "").indexOf("compact") !== -1) {
    appendTrajectory({
      ts: rec.ts,
      session: rec.thread,
      tokensBefore: ctx.tokensBefore,
      tokensAfter: ctx.tokensAfter,
      compactedCount: ctx.compactedCount,
      pathsTouched: ctx.pathsTouched,
    });
  }
}

module.exports = handler;
module.exports.default = handler;
