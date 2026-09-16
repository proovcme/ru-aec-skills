# Tool routing

Use the schemas exposed by the connected server as the authority; releases may add or rename tools. Match by capability instead of assuming a client-specific namespace or MCP server alias.

Before routing any mutation, run [preflight.md](preflight.md). In particular, test `dwg_send_code` with a read-only call before relying on it for layouts, blocks, tables, or identity checks.

## Start and inspect

- Discover instances with `dwg_list_available_targets` and select one with `dwg_switch_target` when needed.
- Confirm the selected instance with `dwg_get_current_target` and inspect the drawing with `dwg_get_drawing_info`.
- Inventory layers and block definitions with `dwg_list_layers` and `dwg_list_blocks`.
- Inspect content with `dwg_query_entities`, `dwg_count_entities`, and `dwg_get_entity_properties`. Request geometry only when the task needs it; large unfiltered reads are expensive.

## Create and modify

- Prefer the typed create tools for layers, lines, polylines, text, MText, blocks, dimensions, and tables.
- Insert an existing definition by name. Import a definition from a closed external DWG with `dwg_insert_block(block_path=...)` when the tool schema supports it.
- Set block attributes through the dedicated attribute tool after insertion, then read the instance back.
- Use `dwg_change_layer` and other modify tools on small, verified handle sets. Assign the correct layer during creation when possible.
- Use `dwg_batch_execute` only after one representative direct call succeeds. Batch argument shapes can differ from the direct tool schema.
- Use `dwg_erase_entities` only with exact handles gathered from the current verified drawing, followed by a count/readback check.

## Verify and publish

- Use `dwg_query_entities(include_geometry=true)` for geometric verification and `dwg_get_entity_properties` for detailed spot checks.
- Use `dwg_zoom_extents` and `dwg_capture_view_image` for visual review after object verification.
- Use `dwg_save_drawing` for a new output or verification copy when appropriate. Re-check which database remains active afterward; saving a copy does not necessarily switch the active document.
- If baked tools are used, inventory them first with `dwg_list_baked_tools`. Treat project-specific baked tools as optional accelerators, not prerequisites for this skill.

## Escalate to `dwg_send_code` only when necessary

Suitable cases include reading the exact database filename, enumerating layouts not exposed by typed tools, creating/configuring layouts and viewports, cloning block definitions between open databases, and inspecting native table cells. Keep code minimal, transaction-scoped, and return a small structured result. Mutation code requires both server-side and in-AutoCAD opt-in; never attempt to bypass either control.

If the preflight reports that advanced mode is disabled, do not discover that halfway through production and quietly replace semantic objects with drafting primitives. Report the missing opt-in before mutation and either continue in typed mode only when it fully satisfies the requested deliverable or wait for the required configuration.
