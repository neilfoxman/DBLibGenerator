import common
import values
import component

class Yageo_RC_L:
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
        if exponent < 3:
            return f"{significand3_str[:exponent+1]}R{significand3_str[exponent+1:].rstrip('0')}"
        elif exponent < 6:
            return f"{significand3_str[:exponent-2]}K{significand3_str[exponent-2:].rstrip('0')}"
        elif exponent < 9:
            return f"{significand3_str[:exponent-5]}M{significand3_str[exponent-5:].rstrip('0')}"
        
    def gen_pn(size, tolerance, packaging, reel_power, resistance):
        tolerance_label = Yageo_RC_L.tolerance_labels[tolerance]
        packaging_label = Yageo_RC_L.packaging_labels[packaging]
        reel_power_label = Yageo_RC_L.reel_power_labels[reel_power]
        resistance_label = Yageo_RC_L.gen_resistance_str(resistance)
        return f'RC{size}{tolerance_label}{packaging_label}-{reel_power_label}{resistance_label}L'

    def gen_series_str(series_list):
        ret_str = ''
        for series in series_list:
            ret_str += series
            if series is not series_list[-1]:
                ret_str += ', '
        return ret_str
                

    def gen_components():
        component_list = []

        # Using some common parameters across all components for now
        packaging = 'Paper taping reel'
        reel_power = '7 inch dia. Reel & Standard power'

        # Size we are generating for
        size = '0805'

        # Add jumper to list first (not in series maps)
        resistance = 0
        component_list.append(
            component.ChipComponent(
                value=Yageo_RC_L.gen_resistance_str(resistance),
                series='Jumper',
                tolerance='Jumper',
                size=size,
                power_rating='Jumper',
                description=f'{Yageo_RC_L.gen_resistance_str(resistance)} Jumper, {size}',
                comment='=Value',
                manufacturer='Yageo',
                manufacturer_pn=Yageo_RC_L.gen_pn(
                    size=size,
                    tolerance='5.0%', # Used for jumpers according to datasheet
                    packaging=packaging,
                    reel_power=reel_power,
                    resistance=0,
                ),
                symbol_path=common.SYMBOL_PATH,
                symbol_ref='Resistor',
                footprint_path=common.FOOTPRINT_PATH,
                footprint_ref=size,
            ).to_dict()
        )

        # Now generate all resistors
        power_rating = '1/8W'
        values_map = values.ValueSeries.gen_values_map_in_range(min_value=1, max_value=10, accepted_series_list=[values.E24, values.E96])
        tolerances = ['1.0%']
        for tolerance in tolerances:
            for value, series_list in values_map.items():
                component_list.append(
                    component.ChipComponent(
                        value=Yageo_RC_L.gen_resistance_str(value),
                        series=Yageo_RC_L.gen_series_str(series_list),
                        tolerance=tolerance,
                        size=size,
                        power_rating=power_rating,
                        description=f'{Yageo_RC_L.gen_resistance_str(value)} {tolerance} Resistor, {size}, {power_rating}',
                        comment='=Value',
                        manufacturer='Yageo',
                        manufacturer_pn=Yageo_RC_L.gen_pn(
                            size=size,
                            tolerance=tolerance,
                            packaging=packaging,
                            reel_power=reel_power,
                            resistance=value,
                        ),
                        symbol_path=common.SYMBOL_PATH,
                        symbol_ref='Resistor',
                        footprint_path=common.FOOTPRINT_PATH,
                        footprint_ref=size,
                    ).to_dict()
                )


        return component_list
    

comps = Yageo_RC_L.gen_components()
import pandas as pd
df = pd.DataFrame(comps)#.set_index('Manufacturer Part Number')
print(df)
df.to_excel('yageo_RC_L.xlsx')