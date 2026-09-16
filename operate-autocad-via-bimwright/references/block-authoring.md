# Block authoring

Use this workflow to create reusable native AutoCAD block definitions, not merely grouped geometry or a one-off symbol.

## Define the block contract first

Record:

- semantic purpose and stable block name;
- insertion units and intended drawing scale;
- meaningful base point and default orientation;
- extents, connection points, clearances, and expected insertion contexts;
- geometry layers and color/linetype/lineweight inheritance policy;
- attribute tags, prompts, defaults, visibility, text style, justification, and whether values must remain unique per instance;
- whether annotative, dynamic, visibility-state, lookup, or nested behavior is actually required.

Do not add dynamic behavior unless the requested variants justify it and the MCP/.NET path can verify it. Prefer several clear static definitions over an unverified opaque dynamic block.

## Geometry and property rules

- Author geometry at 1:1 in the block's declared units.
- Put reusable symbol geometry on layer `0` with `ByBlock` or `ByLayer` properties when instances must inherit host-layer graphics. Use dedicated internal layers only when the template intentionally controls subcomponents that way.
- Choose a base point that supports placement: centerline intersection, mounting corner, connector, or another documented datum. Avoid arbitrary world coordinates.
- Keep construction geometry out of the final definition.
- Use closed polylines only where closure is semantically correct. Keep text orientation and hatch scale valid under expected rotation and mirroring.
- Avoid deep nesting and excessive anonymous geometry. Inspect extents and entity counts before approving the block for mass insertion.

## Attribute definitions

- Use stable uppercase tags without spaces; treat tags as the external data contract.
- Separate user-facing prompt/default text from the tag.
- Define constant attributes only for values shared by every instance. Use editable attributes for identifiers, marks, addresses, equipment types, or quantities that vary.
- Position and justify attribute definitions relative to the block base point. Decide explicitly whether each attribute should be invisible, preset, verifiable, or locked in position.
- After inserting a reference, create its attribute references from the definitions, apply instance values by tag, and synchronize existing references when definitions change.

## Creation paths

Use a typed block-definition tool if the connected release provides one. Otherwise, use a narrowly scoped `dwg_send_code` transaction:

1. validate that the target block name does not collide with an incompatible existing definition;
2. create or open the `BlockTableRecord` with the correct origin/units;
3. append native geometry and `AttributeDefinition` objects;
4. commit, insert one test `BlockReference`, and instantiate attributes;
5. regenerate and read the definition/reference back.

For a reusable library file, write the approved definition to its own DWG or a controlled library DWG with `Wblock`/clone semantics. Do not make the production drawing the only copy of a reusable definition.

## Validation

Test at least:

- insertion at the origin and at a non-zero point;
- rotation and every scale mode that the contract allows;
- host-layer/color inheritance;
- attribute enumeration and update by tag;
- extents and base-point behavior;
- repeated insertion without duplicating or renaming the definition;
- save, reopen, and readback;
- import into a separate clean DWG from the closed library file.

Read back both the definition and representative references: names, handles, nested entity types/counts, units, origin, reference transform, layer, dynamic status if any, and all attribute tag/value pairs. Capture an isolated test insertion and a realistic in-context insertion.

## Updating an existing block

Before redefining a block, inventory all references and dynamic/attribute data, then back up the DWG. Preserve the existing data contract unless the user requested a migration. After redefinition, synchronize attributes deliberately and verify that instance values, transforms, and visibility remain correct. Never assume redefining geometry alone updates every reference safely.

