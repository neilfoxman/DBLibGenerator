# Generate list of all possible significands and mappings to specific component value series
# https://eepower.com/resistor-guide/resistor-standards-and-codes/resistor-values/

def val_to_scinot(value):
        scinot_str = f"{value:e}"
        scinot_split_str = scinot_str.split('e')
        scinot_split_str[1] = scinot_split_str[1].replace('+','') # Replace plus sign added to positive exponents (if present)
        return (float(scinot_split_str[0]), int(scinot_split_str[1]))

# First start with three digit representations of all values in each series
class ValueSeries:
    def __init__(self, name, significand3s=[]):
        self.name = name
        self.significand3s = significand3s

    def __repr__(self):
        return f"{self.name}={self.significand3s}"

    def from_str(name, series_str):
        significand3s = []
        for significand3_str in series_str.split():
            significand3s.append(int(significand3_str.ljust(3, '0')))
        return ValueSeries(name, significand3s)

    def merge_series_map(series_list):
        ret_dict = {}
        for series in series_list:
            for significand3 in series.significand3s:
                if significand3 not in ret_dict:
                    ret_dict[significand3] = []
                ret_dict[significand3].append(series.name)
        return ret_dict

    def gen_values_map_in_range(min_value, max_value, accepted_series_list):
        # Get scientific notation representation of min and max
        min_significand, min_expononent = val_to_scinot(min_value)
        max_significand, max_expononent = val_to_scinot(max_value)

        # Convert significand to 3 digit integer for easier comparison to series values (avoid comparing calculated floats for equality)
        min_significand3 = round(min_significand*100)
        max_significand3 = round(max_significand*100)

        merged_series_map = ValueSeries.merge_series_map(accepted_series_list)

        ret_map = {}

        # For each exponent within min and max range
        for exponent in range(min_expononent, max_expononent+1):
            # Inspect each 3-digit significand of an acceptable component value series
            for significand3, series_list in merged_series_map.items():
                # If we are on the lowest or highest possible exponent, compare min and max significands too
                # If looking at an exponent between max and min exponent, then it automatically qualifies as a valid value
                if (exponent == min_expononent and significand3 >= min_significand3) or \
                (exponent == max_expononent and significand3 <= max_significand3) or \
                (exponent > min_expononent and exponent < max_expononent):
                    ret_map[significand3/100.0 * pow(10,exponent)] = series_list
        return dict(sorted(ret_map.items()))
        

E6 = ValueSeries.from_str('E6',
    """
    10	15	22	33	47	68
    """
)

E12 = ValueSeries.from_str('E12',
    """
    10	12	15	18	22	27
    33	39	47	56	68	82
    """
)

E24 = ValueSeries.from_str('E24',
    """
    10	11	12	13	15	16
    18	20	22	24	27	30
    33	36	39	43	47	51
    56	62	68	75	82	91
    """
)

E48 = ValueSeries.from_str('E48',
    """
    100	105	110	115	121	127
    133	140	147	154	162	169
    178	187	196	205	215	226
    237	249	261	274	287	301
    316	332	348	365	383	402
    422	442	464	487	511	536
    562	590	619	649	681	715
    750	787	825	866	909	953
    """
)

E96 = ValueSeries.from_str('E96',
    """
    100	102	105	107	110	113
    115	118	121	124	127	130
    133	137	140	143	147	150
    154	158	162	165	169	174
    178	182	187	191	196	200
    205	210	215	221	226	232
    237	243	249	255	261	267
    274	280	287	294	301	309
    316	324	332	340	348	357
    365	374	383	392	402	412
    422	432	442	453	464	475
    487	499	511	523	536	549
    562	576	590	604	619	634
    649	665	681	698	715	732
    750	768	787	806	825	845
    866	887	909	931	953	976
    """
)

E192 = ValueSeries.from_str('E192',
    """
    100	101	102	104	105	106	107	109	110	111	113	114
    115	117	118	120	121	123	124	126	127	129	130	132
    133	135	137	138	140	142	143	145	147	149	150	152
    154	156	158	160	162	164	165	167	169	172	174	176
    178	180	182	184	187	189	191	193	196	198	200	203
    205	208	210	213	215	218	221	223	226	229	232	234
    237	240	243	246	249	252	255	258	261	264	267	271
    274	277	280	284	287	291	294	298	301	305	309	312
    316	320	324	328	332	336	340	344	348	352	357	361
    365	370	374	379	383	388	392	397	402	407	412	417
    422	427	432	437	442	448	453	459	464	470	475	481
    487	493	499	505	511	517	523	530	536	542	549	556
    562	569	576	583	590	597	604	612	619	626	634	642
    649	657	665	673	681	690	698	706	715	723	732	741
    750	759	768	777	787	796	806	816	825	835	845	856
    866	876	887	898	909	920	931	942	953	965	976	988
    """
)

# print(ValueSeries.gen_values_map_in_range(1, 50, accepted_series_list=[E6, E12, E48]))
# print(ValueSeries.gen_values_map_in_range(1, 10, accepted_series_list=[E24, E96]))