import importlib.util
from pathlib import Path


PATH = Path(__file__).parents[1] / "prepare-local-cost-estimate" / "scripts" / "estimate_calculator.py"
SPEC = importlib.util.spec_from_file_location("estimate_calculator", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_resource_uses_resolved_price():
    assert MODULE.resource({"quantity": "0.64", "resolved_price": "89238.27"})["cost"] == "57112.49"


def test_position_does_not_double_count_machine_labor():
    result = MODULE.position(
        {"ot": 100, "em": 50, "otm": 10, "materials": 25, "nr_rate": 100, "sp_rate": 50,
         "em_includes_otm": True}
    )
    assert result == {
        "direct_cost": "175.00",
        "fot": "110.00",
        "overheads": "110.00",
        "estimated_profit": "55.00",
        "total": "340.00",
        "em_includes_otm": True,
        "otm_added_to_direct_cost": False,
    }


def test_position_adds_machine_labor_when_machine_cost_excludes_it():
    result = MODULE.position(
        {"ot": 100, "em": 50, "otm": 10, "materials": 25, "nr_rate": 100, "sp_rate": 50,
         "em_includes_otm": False}
    )
    assert result == {
        "direct_cost": "185.00",
        "fot": "110.00",
        "overheads": "110.00",
        "estimated_profit": "55.00",
        "total": "350.00",
        "em_includes_otm": False,
        "otm_added_to_direct_cost": True,
    }


def test_position_requires_explicit_machine_cost_semantics():
    try:
        MODULE.position({"ot": 100, "em": 50, "otm": 10})
    except ValueError as exc:
        assert "em_includes_otm" in str(exc)
    else:
        raise AssertionError("position must reject an implicit EM/OTm assumption")


def test_project_quantity_is_not_silently_zeroed():
    try:
        MODULE.resource({"quantity": "П", "resolved_price": 1})
    except ValueError as exc:
        assert "project_quantity" in str(exc)
    else:
        raise AssertionError("project-defined quantity must remain unresolved")


def test_machine_labor_uses_driver_codes_and_current_wages():
    result = MODULE.machine_labor(
        {
            "machines": [
                {
                    "machine_code": "91.05.05-015",
                    "machine_hours": "0.09",
                    "labour_mach": "1",
                    "driver_code": "4-100-060",
                    "current_salary": "814.34",
                },
                {
                    "machine_code": "91.14.02-001",
                    "machine_hours": "0.09",
                    "labour_mach": "1",
                    "driver_code": "4-100-040",
                    "current_salary": "606.23",
                },
            ]
        }
    )
    assert result["labor_hours"] == "0.18"
    assert result["labor_cost"] == "127.85"
    assert result["weighted_hourly_rate"] == "710.29"


def test_machine_without_crew_has_zero_machine_labor():
    result = MODULE.machine_labor(
        {
            "machines": [
                {
                    "machine_code": "91.17.04-194",
                    "machine_hours": "0.91",
                    "labour_mach": "0",
                    "current_salary": "0",
                }
            ]
        }
    )
    assert result["labor_hours"] == "0.00"
    assert result["labor_cost"] == "0.00"


def test_price_context_mismatch_fails_validation():
    result = MODULE.validate_price(
        {
            "expected": {"code": "x", "zone_id": 206, "period_id": 427},
            "evidence": {"code": "x", "zone_id": 206, "period_id": 426, "status": "complete", "resolved_price": 1},
        }
    )
    assert result["valid"] is False
    assert "period_id" in result["errors"][0]
