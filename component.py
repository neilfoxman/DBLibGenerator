# Generate base class for component in database to help enforce parameters needed
class ComponentBase:
    def __init__(
        self,
        description,
        comment,
        manufacturer,
        manufacturer_pn,
        symbol_path,
        symbol_ref,
        footprint_path,
        footprint_ref,
        *args,
        **kwargs):

        self.description = description
        self.comment = comment
        self.manufacturer = manufacturer
        self.manufacturer_pn = manufacturer_pn
        self.symbol_path = symbol_path
        self.symbol_ref = symbol_ref
        self.footprint_path = footprint_path
        self.footprint_ref = footprint_ref
        for arg in args:
            print(f"Warning: Unassigned argument: {arg}")
        for key, val in kwargs.items():
            print(f"Warning: Unassigned key-val pair: {key} : {val}")

    def to_dict(self):
        # https://www.altium.com/documentation/altium-designer/creating-defining-database-library
        d = {}
        d['Description'] = self.description
        d['Comment'] = self.comment
        d['Manufacturer'] = self.manufacturer
        d['Manufacturer Part Number'] = self.manufacturer_pn
        d['Library Path'] = self.symbol_path
        d['Library Ref'] = self.symbol_ref
        d['Footprint Path'] = self.footprint_path
        d['Footprint Ref'] = self.footprint_ref
        return d

class ValuedComponent(ComponentBase):
    def __init__(
        self,
        value,
        series,
        tolerance,
        *args,
        **kwargs):

        super().__init__(*args, **kwargs)
        self.value = value
        self.series = series
        self.tolerance = tolerance
    
    def to_dict(self):
        d = super().to_dict()
        d['Value'] = self.value
        d['Series'] = self.series
        d['Tolerance'] = self.tolerance
        return d

class ChipComponent(ValuedComponent):
    def __init__(
        self,
        size,
        power_rating,
        *args,
        **kwargs):

        super().__init__(*args, **kwargs)
        self.size = size
        self.power_rating = power_rating
    
    def to_dict(self):
        d = super().to_dict()
        d['Package / Case'] = self.size
        d['Power Rating'] = self.power_rating
        return d

# R = ValuedComponent(
# R = ChipComponent(
#     value='5R',
#     series='Esomething',
#     tolerance='1%',
#     size='0804',
#     power_rating='1/8W',
#     description='dscrpt',
#     comment='comment',
#     manufacturer='mfg',
#     manufacturer_pn='pn',
#     symbol_path='sympath',
#     symbol_ref='symref',
#     footprint_path='footpath',
#     footprint_ref='footref'
# )
# print(R.to_dict())