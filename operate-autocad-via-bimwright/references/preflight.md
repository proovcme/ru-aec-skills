# AutoCAD MCP capability preflight

Run this preflight before modifying a DWG and repeat the affected checks after an AutoCAD restart, MCP reconnect, target switch, document open, or Save As. Its purpose is to expose missing configuration before work depends on it.

## 1. Classify the requested work

Use **typed mode** when every required operation has a dedicated MCP tool, for example layers, ordinary geometry, text/MText, insertion of an existing block, block attributes, dimensions, tables supported by the connected release, entity queries, capture, and save.

Use **advanced mode** when any required invariant or operation is absent from the typed tools. Common cases are exact `Database.Filename` readback, layout and page-setup creation, floating viewport configuration, paper-space enumeration, new attributed block definitions, cloning definitions between open databases, and native table-cell inspection.

Do not enable advanced mode merely because it is available. It permits arbitrary AutoCAD .NET code and should be requested only when the deliverable actually needs it.

## 2. Probe the connection before work

1. Confirm that the expected `dwg_*` tools are exposed by the MCP client.
2. Call `dwg_list_available_targets`, select the intended AutoCAD process when there is more than one, and confirm it with `dwg_get_current_target`.
3. Call `dwg_get_drawing_info`. Record the document name, current layout/space, units, and target identity.
4. If the task needs advanced mode, call `dwg_send_code` with a harmless read-only probe that returns `db.Filename` and no database changes. Do this before creating an output copy or any CAD entity.
5. Compare the returned full path with the intended source or output. A tab caption, document name, successful Save As response, or file existing on disk is not enough.

For a new output, perform any write probe only after the working copy is active. Create one disposable entity with a typed tool, read its handle and properties back, erase that exact handle, and confirm it is gone. Never use a user source or reference DWG for this probe.

## 3. Interpret advanced-mode failure

`dwg_send_code` has two independent opt-ins:

- the MCP server must be started with `--enable-send-code`;
- the current AutoCAD session must be opted in with the AutoCAD command `MCPENABLECODE`.

If the tool reports `send_code is disabled`, do not guess which side is missing. Inspect the server launch configuration when it is safely readable, then tell the user which setting is confirmed and which remains to be enabled. Do not silently change this security setting through UI automation.

Use a concise early notice such as:

> AutoCAD MCP is connected and typed tools work, but this task also needs advanced layout/block operations. Before I modify the drawing, start the MCP server with `--enable-send-code` and run `MCPENABLECODE` once in the current AutoCAD session. I will then repeat a read-only path probe. Until that succeeds I will not substitute a simplified sheet without your agreement.

If typed tools completely cover the requested result, state that advanced mode is unavailable but non-blocking and continue. If advanced mode is required, pause that part of the work instead of silently degrading an attributed block, layout, viewport, native table, or verification step into plain lines/text or an image.

## 4. Readiness result

Before mutation, record one of these outcomes:

- `READY_TYPED`: target, drawing identity, and every required typed capability passed;
- `READY_ADVANCED`: typed checks passed and the read-only `dwg_send_code` path probe returned the exact intended full path;
- `BLOCKED_CONFIGURATION`: specify the missing server flag, AutoCAD opt-in, tool, target, or identity evidence and the exact user action needed;
- `BLOCKED_TARGET_AMBIGUITY`: more than one plausible AutoCAD process or drawing exists and the intended database cannot be proven.

Do not call a task ready merely because the server process started. Readiness requires an actual tool call through the client to the selected AutoCAD instance.

## 5. Recheck boundaries

- After Save As, re-read the active full path. Some save tools create the destination file while leaving the source database active.
- After opening another drawing or changing target, repeat identity, space/layout, and capability checks.
- After restarting AutoCAD, assume the AutoCAD-side advanced opt-in is off until the read-only probe proves otherwise.
- After restarting the MCP server, assume the server-side flag is unknown until its configuration or the probe confirms it.
- After a timeout, do not use a second write as a probe. First establish whether the previous mutation committed.

