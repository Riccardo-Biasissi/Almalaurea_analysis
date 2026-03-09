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
    plot_eta_laurea,
    plot_classe_sociale,
)

DATA_DIR  = os.path.join(os.path.dirname(__file__), 'data')
PLOTS_DIR = os.path.join(os.path.dirname(__file__), 'plots')


def main():
    plt.rcParams.update({'font.size': 15})
    os.makedirs(PLOTS_DIR, exist_ok=True)

    # # Scrape data from AlmaLaurea and save to CSV files. Comment out if not needed.
    # collect_data()
    # collect_profile_data()

    df = pd.read_csv(os.path.join(DATA_DIR, 'almalaurea.csv'))

    plot_graduate_share(df, PLOTS_DIR)
    plot_salary_by_group(df, PLOTS_DIR)
    plot_pay_gap(df, PLOTS_DIR)
    plot_unemployment(df, PLOTS_DIR)

    df_profilo = pd.read_csv(os.path.join(DATA_DIR, 'almalaurea_profilo.csv'))
    plot_gender_split(df_profilo, PLOTS_DIR)
    plot_eta_laurea(df_profilo, PLOTS_DIR)
    plot_classe_sociale(df_profilo, PLOTS_DIR)


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


def collect_profile_data():
    """Scrape graduate profile data from AlmaLaurea and save to data/almalaurea_profilo.csv."""
    from tqdm import tqdm
    from almalaurea.scraper import fetch_profile

    G = ['tutti'] + [str(i) for i in range(1, 16)]

    data = []
    with tqdm(total=len(G)) as pbar:
        for g in G:
            result = fetch_profile('tutti', 'tutti', g)
            pct_maschi, pct_femmine, anni, gruppo_nome = (
                result[1], result[2], result[4], result[8]
            )
            eta_meno23, eta_23_24, eta_25_26, eta_27_oltre = (
                result[9], result[10], result[11], result[12]
            )
            cs_elevata, cs_media_imp, cs_media_aut, cs_lavoro_es = (
                result[13], result[14], result[15], result[16]
            )
            for i, (anno, m, f) in enumerate(zip(anni, pct_maschi, pct_femmine)):
                data.append([
                    g, int(anno), float(m), float(f), gruppo_nome,
                    float(eta_meno23[i])   if i < len(eta_meno23)   else float('nan'),
                    float(eta_23_24[i])    if i < len(eta_23_24)    else float('nan'),
                    float(eta_25_26[i])    if i < len(eta_25_26)    else float('nan'),
                    float(eta_27_oltre[i]) if i < len(eta_27_oltre) else float('nan'),
                    float(cs_elevata[i])   if i < len(cs_elevata)   else float('nan'),
                    float(cs_media_imp[i]) if i < len(cs_media_imp) else float('nan'),
                    float(cs_media_aut[i]) if i < len(cs_media_aut) else float('nan'),
                    float(cs_lavoro_es[i]) if i < len(cs_lavoro_es) else float('nan'),
                ])
            pbar.update(1)

    columns = [
        'gruppo_id', 'anno', 'percentuale_maschi', 'percentuale_femmine', 'gruppo_nome',
        'eta_meno23', 'eta_23_24', 'eta_25_26', 'eta_27_oltre',
        'cs_classe_elevata', 'cs_media_impiegatizia', 'cs_media_autonoma', 'cs_lavoro_esecutivo',
    ]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(os.path.join(DATA_DIR, 'almalaurea_profilo.csv'), index=False)
    print(df)


if __name__ == '__main__':
    main()
