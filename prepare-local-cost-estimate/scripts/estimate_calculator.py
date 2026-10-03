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
    if str(payload.get("quantity", "")).strip().upper() in {"П", "P"}:
        raise ValueError("quantity is project-defined; keep status project_quantity and exclude it from confirmed totals")
    quantity = dec(payload["quantity"], "quantity")
    price = dec(payload["resolved_price"], "resolved_price")
    if quantity < 0 or price < 0:
        raise ValueError("quantity and resolved_price must be nonnegative")
    return {"quantity": str(quantity), "resolved_price": str(price), "cost": money(quantity * price)}


def machine_labor(payload: dict) -> dict:
    machines = payload.get("machines")
    if not isinstance(machines, list) or not machines:
        raise ValueError("machines must be a non-empty list")

    total_hours = Decimal(0)
    total_cost = Decimal(0)
    components = []
    for index, item in enumerate(machines):
        machine_hours = dec(item["machine_hours"], f"machines[{index}].machine_hours")
        labour_mach = dec(item.get("labour_mach", 0), f"machines[{index}].labour_mach")
        salary = dec(item.get("current_salary", 0), f"machines[{index}].current_salary")
        if machine_hours < 0 or labour_mach < 0 or salary < 0:
            raise ValueError("machine hours, labour_mach and current_salary must be nonnegative")
        labor_hours = machine_hours * labour_mach
        cost = labor_hours * salary
        total_hours += labor_hours
        total_cost += cost
        components.append(
            {
                "machine_code": item.get("machine_code"),
                "driver_code": item.get("driver_code"),
                "labor_hours": str(labor_hours),
                "current_salary": str(salary),
                "cost": money(cost),
            }
        )

    weighted_rate = total_cost / total_hours if total_hours else Decimal(0)
    return {
        "labor_hours": str(total_hours),
        "labor_cost": money(total_cost),
        "weighted_hourly_rate": money(weighted_rate),
        "components": components,
    }


def position(payload: dict) -> dict:
    if "applicability_status" not in payload:
        raise ValueError("applicability_status is required for every position")
    status = str(payload["applicability_status"]).strip().upper()
    allowed_statuses = {
        "ТОЧНАЯ НОРМА",
        "ПРИМЕНИМО С ОГРАНИЧЕНИЯМИ",
        "ОТДЕЛЬНАЯ КАЛЬКУЛЯЦИЯ",
        "НЕ ПОДТВЕРЖДЕНО",
    }
    if status not in allowed_statuses:
        raise ValueError(f"unsupported applicability_status: {payload['applicability_status']!r}")
    if "included_in_confirmed_total" not in payload or not isinstance(payload["included_in_confirmed_total"], bool):
        raise ValueError("included_in_confirmed_total must be an explicit boolean")
    included = payload["included_in_confirmed_total"]
    matrix_complete = payload.get("comparison_matrix_complete") is True
    if status == "ПРИМЕНИМО С ОГРАНИЧЕНИЯМИ" and included and not matrix_complete:
        raise ValueError("restricted norm cannot enter confirmed total until comparison_matrix_complete is true")
    if status == "НЕ ПОДТВЕРЖДЕНО" and included:
        raise ValueError("unconfirmed position cannot enter confirmed total")

    ot = dec(payload.get("ot", 0), "ot")
    em = dec(payload.get("em", 0), "em")
    materials = dec(payload.get("materials", 0), "materials")
    other = dec(payload.get("other", 0), "other")
    otm = dec(payload.get("otm", 0), "otm")
    nr_rate = dec(payload.get("nr_rate", 0), "nr_rate")
    sp_rate = dec(payload.get("sp_rate", 0), "sp_rate")
    if "em_includes_otm" not in payload or not isinstance(payload["em_includes_otm"], bool):
        raise ValueError("em_includes_otm must be an explicit boolean supported by the source representation")
    em_includes_otm = payload["em_includes_otm"]
    if any(value < 0 for value in (ot, em, materials, other, otm, nr_rate, sp_rate)):
        raise ValueError("costs and rates must be nonnegative")
    otm_direct_component = Decimal(0) if em_includes_otm else otm
    direct = ot + em + otm_direct_component + materials + other
    fot = ot + otm
    nr = fot * nr_rate / Decimal(100)
    sp = fot * sp_rate / Decimal(100)
    return {
        "direct_cost": money(direct),
        "fot": money(fot),
        "overheads": money(nr),
        "estimated_profit": money(sp),
        "total": money(direct + nr + sp),
        "em_includes_otm": em_includes_otm,
        "otm_added_to_direct_cost": not em_includes_otm,
        "applicability_status": status,
        "included_in_confirmed_total": included,
    }


def calculate(payload: dict) -> dict:
    action = payload.get("action")
    if action == "validate_price":
        return validate_price(payload)
    if action == "resource":
        return resource(payload)
    if action == "machine_labor":
        return machine_labor(payload)
    if action == "position":
        return position(payload)
    raise ValueError("action must be validate_price, resource, machine_labor or position")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="JSON input file")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(calculate(payload), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
