

def ComponentCategory():
    '''ComponentCategory'''
    pass


def ComponentRegistry():
    '''ComponentRegistry'''
    pass


def register_component(rid, data_class, args_mapping, pins_mapping, category, default_fields):
    '''
    Decorator to register a component with custom parser.

    Usage:
        @register_component("model/CloudPSS/_newBus_3p", BusData)
        def parse_bus(component, node_to_bus):
            args = component.get("args", {})
            pins = component.get("pins", {})
            return BusData(
                name=args.get("Name", ""),
                voltage_kv=float(args.get("VBase", 0)),
            )
    '''
    pass


def _setup_builtin_mappings():
    '''Setup built-in component mappings.'''
    pass

