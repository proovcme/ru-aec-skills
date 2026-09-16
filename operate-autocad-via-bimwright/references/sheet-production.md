# Sheet production

Use this workflow when the requested result is a plotted sheet, not merely model-space geometry.

When the deliverable is governed by ESKD or SPDS, also apply the sibling skill `../../apply-eskd-spds-to-drawings/SKILL.md`. This file controls AutoCAD mechanics; the sibling skill controls which form, title block, notation, table, and revision rules are applicable.

## Establish the sheet contract

Derive the contract from the user's template, reference DWG, or stated standard. Record:

- paper size, orientation, and drawing units in paper space;
- plotter/media name, printable area, plot style, lineweight policy, and output scale;
- frame and title-block definition, insertion point, and attribute tags;
- required views, viewport scales, clipping, layer states, and annotation scale;
- sheet number, title, stage/status, revision, authorship fields, and issue date;
- required schedules, legends, notes, key plans, and continuation references.

Do not invent an organizational title block when a template is expected. If no template exists, create a clearly identified neutral frame/title block and report that it is provisional.

## Build order

1. Inspect existing layouts, page setups, title blocks, named views, scales, text/dimension styles, and plot settings.
2. Reuse or clone a matching layout when that preserves the template correctly; otherwise create a new named layout.
3. Apply a valid device/media pair and orientation before placing the frame. Do not hardcode localized media names: enumerate what the current installation exposes.
4. Insert the frame/title block at 1:1 in paper space and populate attributes through tags, not coordinate-dependent text replacement.
5. Create only the viewports needed for the sheet. Set model view, custom scale, twist, clipping, visual style, and per-viewport layer state; then lock each viewport.
6. Add paper-space annotations, tables, legends, and revision data. Keep model annotations in model space only when the drawing's annotation strategy requires it.
7. Regenerate and activate the layout before final inspection.

## Composition checks

- All intended content lies inside the printable frame and outside title-block reserved zones.
- Viewport scales match their labels and are locked.
- No unintended model objects, construction layers, frozen references, or duplicate viewports are visible.
- Text, dimensions, symbols, hatches, and lineweights are legible at plotted size.
- View titles, section/detail references, sheet references, drawing title, and revision status are mutually consistent.
- Schedules and tables fit without clipped cells or unreadable row height.
- The layout contains native editable objects rather than a rasterized sheet.

## MCP readback

Verify at minimum:

- layout name and paper-space block table record;
- plot device, canonical media, orientation, plot type, scale, and style sheet when available;
- frame/title-block reference name, handle, insertion point, scale, and attribute values;
- floating viewport count, numbers, bounds, `On`, lock state, model view center, view height, custom scale, and clipping boundary;
- extents of tables and major annotations relative to the frame;
- absence of unexpected OLE or raster objects when an editable CAD sheet was requested.

Capture the active layout for visual review. If the MCP capture omits a floating viewport's contents, verify the viewport object and capture the corresponding model view separately; do not interpret a blank capture as conclusive.

## Sheet-set consistency

For multiple sheets, derive shared values once and apply them consistently. Check unique layout/sheet numbers, ordered numbering, common title-block revision, matching project metadata, continuation references, and a coherent list of drawings. Do not duplicate a layout and leave stale attributes or viewport targets.

