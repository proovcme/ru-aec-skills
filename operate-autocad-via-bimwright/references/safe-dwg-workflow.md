# Safe DWG workflow

## Target identity

Before a write phase, record:

- selected AutoCAD target and process identity when exposed;
- full `Database.Filename` rather than only the document/tab name;
- model or paper space and current layout;
- drawing units;
- baseline entity counts relevant to the task.

Repeat the identity check after any document switch, Save As, restart, timeout, or recovery. Two documents can share the same display name.

Complete the capability preflight before this write phase. When the full path or another required invariant depends on `dwg_send_code`, a disabled advanced channel is a configuration blocker, not permission to proceed on the basis of a tab caption.

## Source and reference protection

- Inspect a reference drawing without saving it.
- Prefer a working copy for destructive analysis or cleanup.
- Before modifying an existing output, create a timestamped or otherwise unique backup without overwriting an earlier backup.
- Do not promote a copy over a file that AutoCAD still has open. Wait until the file handle is released and preserve the previous version.
- Where practical, compare source size, modification time, hash, or object counts before and after the operation.

## Bounded writes and idempotence

- Group changes by a semantic unit such as one block group, one floor, one table, or one layout.
- Capture returned handles immediately and maintain a mapping from logical IDs to DWG handles.
- Verify counts and representative properties after each group.
- Give generated layers, blocks, layouts, and semantic IDs deterministic names so a resumed run can distinguish existing work from missing work.
- On timeout, perform read-only checks before deciding whether to retry. Never assume rollback.

## Saving

For a new deliverable, save to a distinct output path. After the save:

1. query the exact active database filename;
2. confirm the intended output exists and is no longer zero-length;
3. read the required entities back from the active drawing;
4. when risk justifies it, create a second verification copy or reopen the output in a fresh AutoCAD session and repeat readback.

`dwg_save_drawing` can create a file without switching the active database. Save As commands dispatched asynchronously can also leave the original active. Treat both path identity and readback as mandatory evidence.

If saving to the current active path returns a filer error, a native queued `QSAVE` may succeed, but verify the file timestamp and `Database.Filename` afterward. Do not replace the target at the filesystem level while it is open.

## Timeouts and recovery

- A plugin read timeout does not prove failure; the AutoCAD UI thread may still be executing the write.
- Stop issuing mutations until read-only status can be obtained.
- If AutoCAD is unresponsive, record the target path and last verified batch before any restart.
- After restart, open only the intended output, re-establish MCP capability, verify the exact path, inspect counts, and resume from the first missing semantic unit.
- Do not start another AutoCAD COM instance as a diagnostic shortcut; it can make the MCP and diagnostics observe different processes.

## Evidence hierarchy

Strong evidence is, in order: exact active path, native entity readback, block/attribute or table-cell readback, saved file state, and visual capture. A PNG alone proves only what was rendered, not the underlying DWG semantics.
