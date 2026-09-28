#!/usr/bin/env python3
"""Pure decimal checks and calculations for a normalized local estimate model."""

from __future__ import annotations

import argparse
import json
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path
from typing import Any

MONEY = Decimal("0.01")


def dec(value: Any, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError(f"{field} must be a decimal number") from exc
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


def money(value: Decimal) -> str:
    return format(value.quantize(MONEY, rounding=ROUND_HALF_UP), "f")


def validate_price(payload: dict) -> dict:
    evidence = payload["evidence"]
    expected = payload["expected"]
    errors = []
    for field in ("code", "zone_id", "period_id"):
        if evidence.get(field) != expected.get(field):
            errors.append(f"{field}: expected {expected.get(field)!r}, got {evidence.get(field)!r}")
    if evidence.get("status") != "complete":
        errors.append(f"status: expected 'complete', got {evidence.get('status')!r}")
    if evidence.get("resolved_price") is None:
        errors.append("resolved_price is missing")
    return {"valid": not errors, "errors": errors}


def resource(payload: dict) -> dict:
    quantity = dec(payload["quantity"], "quantity")
    price = dec(payload["resolved_price"], "resolved_price")
    if quantity < 0 or price < 0:
        raise ValueError("quantity and resolved_price must be nonnegative")
    return {"quantity": str(quantity), "resolved_price": str(price), "cost": money(quantity * price)}


def position(payload: dict) -> dict:
    ot = dec(payload.get("ot", 0), "ot")
    em = dec(payload.get("em", 0), "em")
    materials = dec(payload.get("materials", 0), "materials")
    other = dec(payload.get("other", 0), "other")
    otm = dec(payload.get("otm", 0), "otm")
    nr_rate = dec(payload.get("nr_rate", 0), "nr_rate")
    sp_rate = dec(payload.get("sp_rate", 0), "sp_rate")
    if any(value < 0 for value in (ot, em, materials, other, otm, nr_rate, sp_rate)):
        raise ValueError("costs and rates must be nonnegative")
    direct = ot + em + materials + other
    fot = ot + otm
    nr = fot * nr_rate / Decimal(100)
    sp = fot * sp_rate / Decimal(100)
    return {
        "direct_cost": money(direct),
        "fot": money(fot),
        "overheads": money(nr),
        "estimated_profit": money(sp),
        "total": money(direct + nr + sp),
        "otm_in_direct_cost": False,
    }


def calculate(payload: dict) -> dict:
    action = payload.get("action")
    if action == "validate_price":
        return validate_price(payload)
    if action == "resource":
        return resource(payload)
    if action == "position":
        return position(payload)
    raise ValueError("action must be validate_price, resource or position")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="JSON input file")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(calculate(payload), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
