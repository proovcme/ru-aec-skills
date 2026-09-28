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
        {"ot": 100, "em": 50, "otm": 10, "materials": 25, "nr_rate": 100, "sp_rate": 50}
    )
    assert result == {
        "direct_cost": "175.00",
        "fot": "110.00",
        "overheads": "110.00",
        "estimated_profit": "55.00",
        "total": "340.00",
        "otm_in_direct_cost": False,
    }


def test_price_context_mismatch_fails_validation():
    result = MODULE.validate_price(
        {
            "expected": {"code": "x", "zone_id": 206, "period_id": 427},
            "evidence": {"code": "x", "zone_id": 206, "period_id": 426, "status": "complete", "resolved_price": 1},
        }
    )
    assert result["valid"] is False
    assert "period_id" in result["errors"][0]
