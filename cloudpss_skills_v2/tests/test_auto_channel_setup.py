"""Tests for cloudpss_skills_v2.tools.auto_channel_setup."""

from cloudpss_skills_v2.tools.auto_channel_setup import AutoChannelSetupTool


class TestAutoChannelSetupTool:
    def test_validate_requires_channel_request(self):
        tool = AutoChannelSetupTool()
        valid, errors = tool.validate({"channels": {}, "sampling": {"frequency": 50}})
        assert valid is False
        assert "at least one channel type must be requested" in errors

    def test_build_helpers_create_expected_channel_types(self):
        tool = AutoChannelSetupTool()
        voltage = tool._build_voltage_channel("Bus1", 110, 100)
        current = tool._build_current_channel("Line1", "A", 100)
        power = tool._build_power_channel("Gen1", "Q", 100)
        frequency = tool._build_frequency_channel("Bus1", 50)

        assert voltage["type"] == "voltage"
        assert current["id"] == "I_Line1_A"
        assert power["power_type"] == "Q"
        assert frequency["unit"] == "Hz"

    def test_group_and_output_config(self):
        tool = AutoChannelSetupTool()
        channels = [
            tool._build_voltage_channel("Bus1"),
            tool._build_current_channel("Line1", "A"),
            tool._build_voltage_channel("Bus2"),
        ]
        grouped = tool._group_channels_by_type(channels)
        output = tool._generate_output_config(channels)

        assert len(grouped["voltage"]) == 2
        assert output["channel_count"] == 3
        assert "V_Bus1" in list(output["enabled"])

    def test_run_generates_all_requested_channels(self):
        tool = AutoChannelSetupTool()
        config = {
            "channels": {
                "voltage": {"buses": [{"name": "Bus1", "v_base": 220}]},
                "current": {"components": [{"component": "Line1", "pins": ["A", "B"]}]},
                "power": {"components": [{"component": "Gen1", "power_types": ["P", "Q"]}]},
                "frequency": {"buses": ["Bus1"]},
            },
            "sampling": {"frequency": 200},
        }
        result = tool.run(config)

        assert result.status.value == "success"
        assert result.data["output_config"]["channel_count"] == 6
        assert result.metrics["channel_count"] == 6
        assert result.logs[0].message == "Auto channel setup completed"

    def test_run_fails_for_invalid_power_type(self):
        tool = AutoChannelSetupTool()
        config = {
            "channels": {"power": {"components": [{"component": "Gen1", "power_types": ["invalid"]}]}},
            "sampling": {"frequency": 50},
        }
        result = tool.run(config)

        assert result.status.value == "failed"
        assert "power_type" in result.error
