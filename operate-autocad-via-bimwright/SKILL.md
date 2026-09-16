---
name: operate-autocad-via-bimwright
description: Operate native AutoCAD DWG files through the bimwright/dwg-mcp toolset, including inspection, safe editing, reusable block authoring, sheet production, layouts, tables, saving, visual checks, and object readback. Use for any discipline when the requested result must exist as verified AutoCAD objects rather than an image or exchange-format substitute.
---

# Operate AutoCAD through bimwright/dwg-mcp

Use the MCP tools exposed by `bimwright/dwg-mcp`; do not assume a particular AI client, MCP server alias, AutoCAD release, installation directory, workspace path, PID, locale, or drawing template. Resolve those facts at runtime.

## Operating contract

1. Run the capability preflight in [references/preflight.md](references/preflight.md) before promising or starting CAD mutations. Classify the task as typed-tool-only or advanced, test the required execution path, and tell the user immediately when AutoCAD or the MCP server needs configuration.
2. Discover the available MCP tools and AutoCAD targets. Select a target explicitly when more than one exists.
3. Inspect the active drawing before mutation: units, current space/layout, layers, blocks, and relevant objects.
4. Establish the exact full path of the active database before every write phase. `dwg_get_drawing_info` may expose only a document name; use a read-only `dwg_send_code` query for `Database.Filename` when necessary. If the target is ambiguous, do not write.
5. Treat user drawings and reference drawings as immutable unless the user explicitly chose one as the output. Create a separate working/output DWG and preserve the source.
6. Prefer typed MCP tools for ordinary CAD objects. Use `dwg_send_code` only for a capability absent from the typed toolset or for a read-only invariant that typed tools cannot expose.
7. Work in bounded batches. After each meaningful batch, read the affected entities back and compare their types, layers, geometry, text, block names, attributes, and counts with the intended result.
8. Save through AutoCAD, then independently verify the output path, file existence, active database identity, and object readback. A successful tool response or a file appearing on disk is not sufficient by itself.
9. Perform a visual check after object-level verification. A screenshot is supporting evidence, not a substitute for DWG readback.

For detailed tool selection, read [references/tool-routing.md](references/tool-routing.md). For source protection, saving, timeouts, and recovery, read [references/safe-dwg-workflow.md](references/safe-dwg-workflow.md).

- For a composed paper-space deliverable, read [references/sheet-production.md](references/sheet-production.md).
- For creating or repairing reusable block definitions, read [references/block-authoring.md](references/block-authoring.md).
- Read [references/advanced-autocad.md](references/advanced-autocad.md) only when the task requires layouts, viewports, external definitions, native tables, or custom .NET code not covered by typed tools.

## Mutation rules

- Do not drive AutoCAD through a second COM instance, shell automation, or UI macros when the MCP connection is the requested execution path.
- Never infer the active file from the tab caption alone.
- Do not use a reference DWG as a block library while it is open for editing. Work from a closed source file or clone definitions between already-open databases with a narrowly scoped AutoCAD .NET operation.
- Do not rasterize editable deliverables. Create native DWG entities: `BlockReference`, attributes, text/MText, polylines, dimensions, tables, layouts, and viewports as appropriate.
- Preserve object semantics: symbols should be blocks, repeated data should be attributes or table cells, and connections should be real lines/polylines on meaningful layers.
- Treat a sheet as a coordinated deliverable: plot settings, printable area, frame/title block, viewports, scale, annotation, and revision data must agree.
- Treat a block as a reusable API: stable name, meaningful base point, correct units, controlled layer/color behavior, documented attributes, and verified insertion behavior.
- Do not retry a timed-out write blindly. First determine whether the previous operation committed; otherwise a retry may duplicate geometry.
- Keep source and output paths explicit in the completion report. State which checks were object-level and which were visual.

## Completion gate

Do not report a CAD task as complete until all applicable conditions hold:

- the intended DWG is the verified target;
- requested objects exist as native AutoCAD entities;
- representative handles and properties were read back through MCP;
- required blocks and attributes are present;
- layouts/viewports/tables were verified when used;
- AutoCAD saved the output to the intended path;
- a visual inspection found no obvious clipping, overlap, illegibility, or empty viewport;
- the source/reference files were not modified.

Return a concise verification record containing the output path, target identity, entity counts by type/layer, representative handles, block/attribute checks, layout checks, save evidence, visual evidence, and any capability gaps.
