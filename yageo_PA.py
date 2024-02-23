# Values not that common - not recommended.




import common
import values
import component


tolerance_labels = {
    '0.5%' : 'D',
    '1.0%' : 'F',
    '5.0%' : 'J'
}

packaging_labels = {
    'Paper taping reel (PA0100~PA1206)': 'R',
    'Embossed taping reel (PA2010/PA2512)': 'K',
}

tcr_labels = {
    '50ppm/°C' : 'E',
    '75ppm/°C' : 'M',
    '100ppm/°C' : 'F',
    '150ppm/°C' : 'L',
    '200ppm/°C' : 'G',
    '300ppm/°C' : 'I',
}

def gen_resistance_label(resistance):
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
    
def gen_pn(size, tolerance, packaging, tcr, power_label, resistance):
    tolerance_label = tolerance_labels[tolerance]
    packaging_label = packaging_labels[packaging]
    tcr_label = tcr_labels[tcr]
    resistance_label = gen_resistance_label(resistance)
    if size in ['1206', '1210', '2512']:
        default_code = 'Z'
    else:
        default_code = 'L'
    return f'PA{size}{tolerance_label}{packaging_label}{tcr_label}{power_label}{resistance_label}{default_code}'

def gen_component_dict(
    resistance,
    value_series_str,
    tolerance,
    size,
    tcr,
    power_rating,
    power_label,
    packaging
):
    """
    Generate component object that represents a specific resistor by this manufacturer
    """
    resistance_label = gen_resistance_label(resistance)
    if resistance == 0:
        description = f"{resistance_label} Jumper, {size}, {power_rating}"
    else:
        description = f"{resistance_label} Resistor, {tolerance}, {size}, {power_rating}"

    return component.ChipComponent(
        value=resistance_label,
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
            tcr=tcr,
            power_label=power_label,
            resistance=resistance,
        ),
        symbol_path=common.SYMBOL_PATH,
        symbol_ref='Resistor',
        footprint_path=common.FOOTPRINT_PATH,
        footprint_ref=size,
        construction=f'TCR={tcr}',
    ).to_dict()

def gen_component_dicts_in_range(
    min_value,
    max_value,
    accepted_series_list,
    tolerance,
    size,
    tcr,
    power_rating,
    power_label,
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
                resistance=value,
                value_series_str=values.gen_series_str(series_list),
                tolerance=tolerance,
                size=size,
                tcr=tcr,
                power_rating=power_rating,
                power_label=power_label,
                packaging=packaging,
            )
        )
    return component_list

    
            

def gen_all_components():
    # Generate all components
    component_list = []

    # 0603
    for power_config in [
        ('1/10W', '07'),
        ('1/5W', '7W'),
        ('1/3W', '7T'),
        ('2/5W', '47'),
        ('1/2W', '57'),
    ]:
        for tcr in [
            '50ppm/°C',
            # '75ppm/°C',
            # '100ppm/°C',
            # '150ppm/°C',
            # '200ppm/°C',
            # '300ppm/°C',
        ]:
            power_rating = power_config[0]
            power_label = power_config[1]

            component_list += gen_component_dicts_in_range(
                min_value=10e-3,
                max_value=20e-3,
                accepted_series_list=[values.E6],#[values.E24],#, values.E96], # Assumed available, not yet verified
                tolerance='0.5%',
                size='0603',
                tcr=tcr,
                power_rating=power_rating,
                power_label=power_label,
                packaging='Paper taping reel (PA0100~PA1206)',
            )

    return component_list

# import pandas as pd
# df = pd.DataFrame(gen_all_components())
# print(df)