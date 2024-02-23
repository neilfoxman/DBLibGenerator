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
    if exponent < -9:
        return f"{a}p{b}"
    elif exponent < -6:
        return f"{a}n{b}"
    elif exponent < -3:
        return f"{a}u{b}"
    
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
    power_rating,
    packaging,
    reel_power
):
    """
    Generate component object that represents a specific resistor by this manufacturer
    """
    capacitance_label = gen_capacitance_label(capacitance)
    description = f"{capacitance_label} Capacitor ({capacitance_label}), {tolerance}, {size}, {power_rating}"

    return component.ChipComponent(
        value=capacitance_label,
        series=value_series_str,
        tolerance=tolerance,
        size=size,
        power_rating=power_rating,
        description=description,
        comment='=Value',
        manufacturer='Yageo',
        manufacturer_pn=gen_pn(
            size=size,
            tolerance=tolerance,
            packaging=packaging,
            reel_power=reel_power,
            resistance=resistance,
        ),
        symbol_path=common.SYMBOL_PATH,
        symbol_ref='Resistor',
        footprint_path=common.FOOTPRINT_PATH,
        footprint_ref=size,
        construction='Thick Film',
    ).to_dict()

def gen_component_dicts_in_range(
    min_value,
    max_value,
    accepted_series_list,
    tolerance,
    size,
    power_rating,
    packaging,
    reel_power
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
                resistance=value,
                value_series_str=gen_series_str(series_list),
                tolerance=tolerance,
                size=size,
                power_rating=power_rating,
                packaging=packaging,
                reel_power=reel_power
            )
        )
    return component_list

    
            

def gen_all_components():
    # Some common parameters to use for generating all resistors
    packaging = 'Paper taping reel'
    reel_power = '7 inch dia. Reel & Standard power'

    # Generate all components
    component_list = []

    # 0603
    component_list.append(
        gen_component_dict(
            resistance=0,
            value_series_str='Jumper',
            tolerance='5.0%',
            size='0603',
            power_rating='1A Rated, 2A Max',
            packaging=packaging,
            reel_power=reel_power
        )
    )
    component_list += gen_component_dicts_in_range(
        min_value=1,
        max_value=10e6,
        accepted_series_list=[values.E24, values.E96],
        tolerance='1.0%',
        size='0603',
        power_rating='1/10W',
        packaging=packaging,
        reel_power=reel_power
    )


    # 0805
    component_list.append(
        gen_component_dict(
            resistance=0,
            value_series_str='Jumper',
            tolerance='5.0%',
            size='0805',
            power_rating='2A Rated, 5A Max',
            packaging=packaging,
            reel_power=reel_power
        )
    )
    component_list += gen_component_dicts_in_range(
        min_value=1,
        max_value=10e6,
        accepted_series_list=[values.E24, values.E96],
        tolerance='1.0%',
        size='0805',
        power_rating='1/8W',
        packaging=packaging,
        reel_power=reel_power
    )

    # 1206
    component_list.append(
        gen_component_dict(
            resistance=0,
            value_series_str='Jumper',
            tolerance='5.0%',
            size='1206',
            power_rating='2A Rated, 10A Max',
            packaging=packaging,
            reel_power=reel_power
        )
    )
    component_list += gen_component_dicts_in_range(
        min_value=1,
        max_value=10e6,
        accepted_series_list=[values.E24, values.E96],
        tolerance='1.0%',
        size='1206',
        power_rating='1/4W',
        packaging=packaging,
        reel_power=reel_power
    )

    return component_list

print(gen_capacitance_common_str(1e-6))