"""Tests for cloudpss_skills_v2.tools.component_catalog."""

from cloudpss_skills_v2.tools.component_catalog import ComponentCatalogTool, ComponentInfo


def _servers():
    return [
        {
            "name": "main",
            "components": [
                {
                    "rid": "comp/main/bus",
                    "name": "AC Bus",
                    "category": "network",
                    "data_class": "Bus",
                    "description": "Three phase bus",
                },
                {
                    "rid": "comp/main/line",
                    "name": "Line",
                    "category": "network",
                    "data_class": "Branch",
                    "description": "Transmission line",
                },
            ],
        },
        {
            "name": "public",
            "components": [
                {
                    "rid": "comp/public/pv",
                    "name": "PV Source",
                    "category": "renewable",
                    "data_class": "Generator",
                    "description": "Photovoltaic source",
                }
            ],
        },
    ]


class TestComponentCatalogTool:
    def test_component_info_defaults(self):
        info = ComponentInfo()
        assert info.rid == ""
        assert info.data_class is None

    def test_validate_requires_servers_and_rid_for_resolution(self):
        tool = ComponentCatalogTool()
        valid, errors = tool.validate({"action": "resolve_rid", "servers": _servers()})
        assert valid is False
        assert "rid is required" in errors[0]

    def test_iter_components_adds_server_metadata(self):
        tool = ComponentCatalogTool()
        components = tool._iter_components(_servers())
        assert len(components) == 3
        assert components[0]["server"] == "main"
        assert components[0]["data_class"] == "Bus"

    def test_search_matches_category_description_and_name(self):
        tool = ComponentCatalogTool()
        components = tool._iter_components(_servers())
        assert [item["name"] for item in tool._search(components, "renewable")] == ["PV Source"]
        assert [item["name"] for item in tool._search(components, "line")] == ["Line"]

    def test_run_list_search_and_resolve_rid(self):
        tool = ComponentCatalogTool()
        list_result = tool.run({"action": "list", "servers": _servers()})
        search_result = tool.run({"action": "search", "query": "bus", "servers": _servers()})
        resolve_result = tool.run({"action": "resolve_rid", "rid": "comp/public/pv", "servers": _servers()})

        assert list_result.status.value == "success"
        assert list_result.metrics["component_count"] == 3
        assert search_result.data["components"][0]["name"] == "AC Bus"
        assert resolve_result.data["component"]["server"] == "public"
