import common

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog='Main Passives Components Database Generator',
        description='Main interface for generating a library of passive components for Altium',
    )
    # parser.add_argument(
    #     'com_port1',
    #     action='store',
    #     help='Define com port for device 1.'
    # )
    args = parser.parse_args()

    # Generate components first as a list of dicts for each series we want in our database
    print("Generating components...")

    comps = []

    import yageo_RC_L
    comps += yageo_RC_L.gen_all_components()

    import yageo_CC
    comps += yageo_CC.gen_all_components()

    print("Restructuring as DataFrame...")
    import pandas as pd
    df = pd.DataFrame(comps).set_index('Manufacturer Part Number')
    print(df)

    print("Pushing to Excel document...")
    df.to_excel(common.OUTPUT_XLSX_PATH)

    print("Done!")