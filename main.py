#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt

from almalaurea.plots import (
    plot_graduate_share,
    plot_salary_by_group,
    plot_pay_gap,
    plot_unemployment,
    plot_gender_split,
)

DATA_DIR  = os.path.join(os.path.dirname(__file__), 'data')
PLOTS_DIR = os.path.join(os.path.dirname(__file__), 'plots')


def main():
    plt.rcParams.update({'font.size': 15})
    os.makedirs(PLOTS_DIR, exist_ok=True)

    df = pd.read_csv(os.path.join(DATA_DIR, 'almalaurea.csv'))

    plot_graduate_share(df, PLOTS_DIR)
    plot_salary_by_group(df, PLOTS_DIR)
    plot_pay_gap(df, PLOTS_DIR)
    plot_unemployment(df, PLOTS_DIR)

    # Requires live HTTP access to AlmaLaurea — uncomment to regenerate:
    # plot_gender_split(PLOTS_DIR)


def collect_data():
    """Re-scrape employment data from AlmaLaurea and save to data/almalaurea.csv."""
    import numpy as np
    from tqdm import tqdm
    from almalaurea.scraper import fetch_employment

    ID  = 'tutti'
    A   = 'tutti'
    C   = 'tutti'
    G   = ['tutti'] + [str(i) for i in range(1, 16)]
    YRL = [1, 3, 5]
    Y   = list(range(2008, 2025))

    data = []
    with tqdm(total=len(G) * len(YRL) * len(Y)) as pbar:
        for g in G:
            for yrl in YRL:
                for y in Y:
                    temp = fetch_employment(ID, str(y), A, g, C, str(yrl))
                    data.append([
                        y, yrl, 1, g, ID,
                        temp[0][0], temp[1][0], temp[2][0],
                        temp[3][0], temp[4][0],
                        temp[5][0], temp[6][0], temp[7][0],
                    ])
                    pbar.update(1)

    columns = [
        'anno', 'anni_da_conseguimento_titolo', 'area', 'gruppo', 'ateneo',
        'numero_laureati', 'percentuale_maschi', 'percentuale_femmine',
        'tasso_occupazione_totale', 'tasso_disoccupazione_totale',
        'retribuzione_mensile_maschi', 'retribuzione_mensile_femmine',
        'retribuzione_mensile',
    ]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(os.path.join(DATA_DIR, 'almalaurea.csv'), index=False)
    print(df)


if __name__ == '__main__':
    main()
