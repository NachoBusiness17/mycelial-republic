from scripts.build_agent_state_layers import build


def test_layers_are_a_projection_not_a_new_chain():
    result = build(recent=8)
    assert result["schema"] == "agent_state_layers.v1"
    assert set(result["layers"]) == {"L0_viewport", "L1_continuity", "L2_history", "L3_evidence"}
    assert "preserve" in result["repair_policy"]
