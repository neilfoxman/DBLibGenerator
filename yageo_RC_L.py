import common
import values
import component

tolerance_labels = {
    '0.1%' : 'B',
    '0.5%' : 'D',
    '1.0%' : 'F',
    '5.0%' : 'J' # Also for jumpers
}

packaging_labels = {
    'Paper taping reel': 'R',
    'Embossed taping reel': 'K',
    'ESD safe reel (0075/0100 only)': 'S'
}

reel_power_labels = {
    '7 inch dia. Reel & Standard power': '07',
    '10 inch dia. Reel': '10',
    '13 inch dia. Reel': '13',
    '7 inch dia. Reel & 2 x standard power': '7W',
    '7 inch dia. Reel, ESD safe reel (0075/0100 only)': '7N',
    '13 inch dia. Reel & 2 x standard power': '3W'
}

def gen_resistance_str(resistance):
    significand, exponent = values.val_to_scinot(resistance)
    significand3_str = str(round(significand*100))
    
    # Determine resistance string
    if exponent < -3:
        return f"0U{'0'*(-1*(exponent+4))}{significand3_str.rstrip('0')}"
    elif exponent < 0:
        return f"0R{'0'*(-1*(exponent+1))}{significand3_str.rstrip('0')}"
    elif exponent < 3:
        return f"{significand3_str[:exponent+1]}R{significand3_str[exponent+1:].rstrip('0')}"
    elif exponent < 6:
        return f"{significand3_str[:exponent-2]}K{significand3_str[exponent-2:].rstrip('0')}"
    elif exponent < 9:
        return f"{significand3_str[:exponent-5]}M{significand3_str[exponent-5:].rstrip('0')}"
    
def gen_pn(size, tolerance, packaging, reel_power, resistance):
    tolerance_label = tolerance_labels[tolerance]
    packaging_label = packaging_labels[packaging]
    reel_power_label = reel_power_labels[reel_power]
    resistance_label = gen_resistance_str(resistance)
    return f'RC{size}{tolerance_label}{packaging_label}-{reel_power_label}{resistance_label}L'

def gen_component_dict(
    resistance,
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
    resistance_str = gen_resistance_str(resistance)
    if resistance == 0:
        description = f"{resistance_str} Jumper, {size}, {power_rating}"
    else:
        description = f"{resistance_str} Resistor, {tolerance}, {size}, {power_rating}"

    return component.ChipComponent(
        value=resistance_str,
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
                value_series_str=values.gen_series_str(series_list),
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

import pandas as pd
df = pd.DataFrame(gen_all_components())
print(df)