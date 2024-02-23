import common
import values
import component

tolerance_labels = {
    '5.0%' : 'J',
    '10.0%' : 'K',
    '20.0%' : 'M',
}

packaging_labels = {
    'Paper/PE taping reel; Reel 7 inch': 'R',
    'Blister taping reel; Reel 7 inch': 'K',
    'Paper/PE taping reel; Reel 13 inch': 'P',
    'Blister taping reel; Reel 13 inch': 'F',
}

rated_voltage_labels = {
    '6.3V' : '5',
    '10V' : '6',
    '16V' : '7',
    '25V' : '8',
    '50V' : '9',
    '100V' : '0',
    '200V' : 'A',
    '250V' : 'Y',
}

def gen_capacitance_label(capacitance):
    significand, exponent = values.val_to_scinot(capacitance)
    significand2_str = str(round(significand*10))
    return f"{significand2_str}{exponent+11}"

def gen_capacitance_common_str(capacitance):
    significand, exponent = values.val_to_scinot(capacitance)
    significand3_str = str(round(significand*100))
    pivot = (exponent % 3) + 1
    a = significand3_str[:pivot]
    b = significand3_str[pivot:].rstrip('0')
    if b:
        b = f".{b}"
    if exponent < -9:
        return f"{a}{b}pF"
    elif exponent < -6:
        return f"{a}{b}nF"
    elif exponent < -3:
        return f"{a}{b}uF"
    
def gen_pn(size, tolerance, packaging, rated_voltage, capacitance):
    tolerance_label = tolerance_labels[tolerance]
    packaging_label = packaging_labels[packaging]
    rated_voltage_label = rated_voltage_labels[rated_voltage]
    capacitance_label = gen_capacitance_label(capacitance)
    return f'CC{size}{tolerance_label}{packaging_label}X7R{rated_voltage_label}BB{capacitance_label}'

def gen_component_dict(
    capacitance,
    value_series_str,
    tolerance,
    size,
    rated_voltage,
    packaging,
):
    """
    Generate component object that represents a specific resistor by this manufacturer
    """
    # capacitance_label = gen_capacitance_label(capacitance)
    capacitance_common_str = gen_capacitance_common_str(capacitance)
    description = f"{capacitance_common_str} Capacitor, {tolerance}, {size}, {rated_voltage}, X7R"

    return component.ChipComponent(
        value=capacitance_common_str,
        series=value_series_str,
        tolerance=tolerance,
        size=size,
        rated_voltage=rated_voltage,
        power_rating='',
        description=description,
        comment='=Value',
        manufacturer='Yageo',
        manufacturer_pn=gen_pn(
            size=size,
            tolerance=tolerance,
            packaging=packaging,
            rated_voltage=rated_voltage,
            capacitance=capacitance,
        ),
        symbol_path=common.SYMBOL_PATH,
        symbol_ref='Capacitor',
        footprint_path=common.FOOTPRINT_PATH,
        footprint_ref=size,
        construction='X7R',
    ).to_dict()

def gen_component_dicts_in_range(
    min_value,
    max_value,
    accepted_series_list,
    tolerance,
    size,
    rated_voltage,
    packaging,
):
    # Generate list of possible values from max and min
    values_map = values.ValueSeries.gen_values_map_in_range(
        min_value=min_value,
        max_value=max_value,
        accepted_series_list=accepted_series_list
    )

    # Generate component for each value
    component_list = []
    for value, series_list in values_map.items():
        component_list.append(
            gen_component_dict(
                capacitance=value,
                value_series_str=values.gen_series_str(series_list),
                tolerance=tolerance,
                size=size,
                rated_voltage=rated_voltage,
                packaging=packaging,
            )
        )
    return component_list

    
            

def gen_all_components():
    # Generate all components
    component_list = []

    # 0603
    size = '0603'
    packaging = 'Paper/PE taping reel; Reel 7 inch'
    for tolerance in tolerance_labels.keys():
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=4.7e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='6.3V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=2.2e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='10V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=2.2e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='16V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=1e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='25V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=1e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='50V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=100e-9,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='100V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=220e-12,
            max_value=22e-9,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='200V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=220e-12,
            max_value=22e-9,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='250V',
            packaging=packaging,
        )

    # 0805
    size = '0805'
    packaging = 'Paper/PE taping reel; Reel 7 inch'
    for tolerance in tolerance_labels.keys():
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=10e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='6.3V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=10e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='10V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=10e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='16V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=4.7e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='25V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=2.2e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='50V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=1e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='100V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=47e-9,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='200V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=100e-12,
            max_value=47e-9,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='250V',
            packaging=packaging,
        )

    # 1206
    size = '1206'
    packaging = 'Paper/PE taping reel; Reel 7 inch'
    for tolerance in tolerance_labels.keys():
        component_list += gen_component_dicts_in_range(
            min_value=220e-12,
            max_value=22e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='6.3V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=220e-12,
            max_value=22e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='10V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=220e-12,
            max_value=22e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='16V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=220e-12,
            max_value=10e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='25V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=220e-12,
            max_value=4.7e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='50V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=220e-12,
            max_value=2.2e-6,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='100V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=220e-12,
            max_value=100e-9,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='200V',
            packaging=packaging,
        )
        component_list += gen_component_dicts_in_range(
            min_value=220e-12,
            max_value=100e-9,
            accepted_series_list=[values.E6],
            tolerance=tolerance,
            size=size,
            rated_voltage='250V',
            packaging=packaging,
        )

    return component_list

# print(gen_capacitance_common_str(1.2e-7))
import pandas as pd
df = pd.DataFrame(gen_all_components())
print(df)