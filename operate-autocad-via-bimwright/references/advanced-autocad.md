# Advanced AutoCAD operations

Read this only for operations not reliably covered by typed MCP tools.

## `dwg_send_code`

The tool is intentionally guarded twice: the MCP server must allow code execution and the current AutoCAD session must opt in. Respect both controls. Use it for small, reviewable AutoCAD .NET operations and return structured readback data. Avoid long UI-bound workflows or document switching from background code.

## Layouts and viewports

- Layout manager and editor APIs can be sensitive to AutoCAD's UI thread.
- Prefer native queued AutoCAD commands for creating or activating a layout when direct background API calls produce thread-affinity or invalid-input errors.
- Create paper-space geometry transactionally in the layout's block table record.
- A viewport created only as a database object may have an invalid number until its layout is activated. Activate each layout before validating viewport number, `On`, lock state, model view center, and view height.
- Preserve the system paper-space viewport. Removing every viewport can make image capture fail with a null object identifier.
- Paper-space capture can omit the model view rendered inside a valid floating viewport. Verify viewport properties through object readback and, if needed, capture the corresponding model-space view separately.

## Native tables

- Use an AutoCAD `Table` when the deliverable must stay editable; do not embed a raster or OLE spreadsheet as a substitute.
- Configure plot settings and create/populate a large table in separate transactions if a combined transaction is unstable.
- Read back row/column counts and representative cell contents. Check the table extents against the printable frame.

## External blocks

- `dwg_insert_block` can import a definition from a closed external DWG and then reuse it by name.
- An external DWG already open in AutoCAD can produce a sharing violation when passed as `block_path`.
- For two already-open databases, clone only the required block table records with `WblockCloneObjects`; do not activate or save the source merely to obtain its definitions.
- Inspect a candidate symbol's extents and complexity before repeated insertion. A plan symbol is not automatically suitable as a rack elevation or facade symbol.
- Insert complex blocks in small groups, set the correct layer at creation when possible, save, and verify extents/counts after each group.

## Command dispatch and document operations

- Asynchronous command dispatch may finish after the MCP call returns. Poll using read-only checks rather than immediately sending another write.
- Opening a DWG and switching `MdiActiveDocument` from background code can block the AutoCAD UI thread. Prefer selecting/opening the intended drawing outside the background callback, then verify its exact database path through MCP.
- Never treat the appearance of a target file or a changed tab caption as proof that Save As or document switching completed.
