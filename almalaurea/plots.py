import os
import numpy as np
import matplotlib.pyplot as plt

from almalaurea.constants import GRUPPO_ID, AREA_NOME, AREA_GRUPPI


def plot_gender_split(df, out_dir):
    """Plot male/female graduate percentages by discipline group.

    Reads from a pre-loaded almalaurea_profilo.csv dataframe. Produces M_VS_F.png.

    Parameters
    ----------
    df : pandas.DataFrame
        Pre-loaded almalaurea_profilo.csv data with columns:
        gruppo_id, anno, percentuale_maschi, percentuale_femmine, gruppo_nome.
    out_dir : str
        Directory where the output PNG will be saved.
    """
    fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(24, 20))

    fig.suptitle(
        'Percentuale di laureati maschi e femmine per i vari gruppi disciplinari'
        ' (e aree disciplinari al 2024 in ordinata, classificazione MUR 2020)',
        y=0.92,
    )
    fig.supxlabel('Anno', y=0.08)
    fig.supylabel('Percentuale sul totale [%]', x=0.07)

    area_nome = ['ALE', 'EGS', 'STEM', 'SAV']

    df_tot = df[df['gruppo_id'] == 'tutti'].sort_values('anno')
    M_tot_last = df_tot['percentuale_maschi'].values[-1]
    F_tot_last = df_tot['percentuale_femmine'].values[-1]

    for z in range(1, 16):
        z_str = str(z)
        df_g = df[df['gruppo_id'] == z_str].sort_values('anno')
        anni = df_g['anno'].tolist()
        M = df_g['percentuale_maschi'].values
        F = df_g['percentuale_femmine'].values
        gruppo_nome = df_g['gruppo_nome'].iloc[0]

        row, col = (z - 1) // 4, (z - 1) % 4
        title = 'Gruppo ' + gruppo_nome
        if len(title) >= 35:
            title = title.replace(' e ', ' e\n')
        ax[row][col].set_title(title)
        ax[row][col].plot(anni, M, color='royalblue', marker='o', lw=1.5, label='Maschi')
        ax[row][col].plot(anni, F, color='deeppink',  marker='o', lw=1.5, label='Femmine')
        ax[row][col].plot([anni[0], anni[-1]], [50, 50], c='black', ls='dashed', lw=1.5)
        ax[row][col].grid()

        if col == 0:
            ax[row][col].set_ylabel(
                f"{area_nome[row]} - M: {round(M_tot_last, 1)}% - F: {round(F_tot_last, 1)}%"
            )

    # Last panel: totals
    anni = df_tot['anno'].tolist()
    M = df_tot['percentuale_maschi'].values
    F = df_tot['percentuale_femmine'].values

    ax[3][3].set_title(f'Totale - M: {round(M[-1], 1)}% - F: {round(F[-1], 1)}%')
    ax[3][3].plot(anni, M, color='royalblue', marker='o', lw=2, label='Maschi')
    ax[3][3].plot(anni, F, color='deeppink',  marker='o', lw=2, label='Femmine')
    ax[3][3].plot([anni[0], anni[-1]], [50, 50], c='black', ls='dashed', lw=1.5)
    ax[3][3].annotate(
        'Source: AlmaLaurea\n\nElaboration by\nBiasissi Riccardo',
        xy=(0.03, 0.03), xytext=(0.03, 0.03), xycoords='axes fraction',
        va='bottom', fontsize=15,
    )
    ax[3][3].legend()
    ax[3][3].grid()

    plt.subplots_adjust(wspace=0.08, hspace=0.24)
    plt.savefig(os.path.join(out_dir, 'M_VS_F.png'), dpi=200, bbox_inches='tight')
    plt.close()


def plot_salary_by_group(df, out_dir):
    """Plot monthly net salary by gender and discipline group.

    Produces retribuzione_gruppi_1.png, _3.png, _5.png.

    Parameters
    ----------
    df : pandas.DataFrame
        Pre-loaded almalaurea.csv data.
    out_dir : str
        Directory where output PNGs will be saved.
    """
    for yrl in ['1', '3', '5']:
        fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(24, 20))

        fig.suptitle(
            f'Retribuzione mensile netta (a {yrl} anni dal titolo) suddivisa per genere'
            ' e gruppo disciplinare (classificazione MUR 2020)',
            y=0.93,
        )
        fig.supxlabel('Anno', y=0.08)
        fig.supylabel('Retribuzione mensile netta [€]', x=0.08)

        for g in [str(i) for i in range(1, 16)]:
            row, col = (int(g) - 1) // 4, (int(g) - 1) % 4
            title = 'Gruppo ' + GRUPPO_ID[g]
            ax[row][col].set_title(title.replace(' e ', ' e\n'))

            df_t = df[(df['gruppo'] == g) & (df['anni_da_conseguimento_titolo'] == int(yrl))]
            M = df_t['retribuzione_mensile_maschi']
            F = df_t['retribuzione_mensile_femmine']
            T = df_t['retribuzione_mensile']

            ax[row][col].plot(df_t['anno'], M, color='royalblue', marker='o', lw=1.5, label='Maschi')
            ax[row][col].plot(df_t['anno'], F, color='deeppink',  marker='o', lw=1.5, label='Femmine')
            ax[row][col].plot(df_t['anno'], T, color='black',     marker='o', lw=1.5, label='Totale')
            ax[row][col].grid()

        # Last panel: totals
        df_t = df[(df['gruppo'] == 'tutti') & (df['anni_da_conseguimento_titolo'] == int(yrl))]
        M = df_t['retribuzione_mensile_maschi']
        F = df_t['retribuzione_mensile_femmine']
        T = df_t['retribuzione_mensile']

        ax[3][3].set_title('Totale')
        ax[3][3].plot(df_t['anno'], M, color='royalblue', marker='o', lw=2, label='Maschi')
        ax[3][3].plot(df_t['anno'], F, color='deeppink',  marker='o', lw=2, label='Femmine')
        ax[3][3].plot(df_t['anno'], T, color='black',     marker='o', lw=2, label='Totale')
        ax[3][3].grid()
        ax[3][3].legend()
        ax[2][3].annotate(
            'Source: AlmaLaurea\n\nElaboration by\nBiasissi Riccardo',
            xy=(0.97, 0.03), xytext=(0.97, 0.03), xycoords='axes fraction',
            va='bottom', ha='right', fontsize=15,
        )

        plt.subplots_adjust(wspace=0.08, hspace=0.24)
        plt.savefig(
            os.path.join(out_dir, f'retribuzione_gruppi_{yrl}.png'),
            dpi=200, bbox_inches='tight',
        )
        plt.close()


def plot_pay_gap(df, out_dir):
    """Plot gender pay gap (%) over time by discipline group.

    Produces divario_retributivo.png.

    Parameters
    ----------
    df : pandas.DataFrame
        Pre-loaded almalaurea.csv data.
    out_dir : str
        Directory where the output PNG will be saved.
    """
    fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(24, 20))

    fig.suptitle(
        'Divario retributivo maschile-femminile (a 1, 3, 5 anni dal titolo)'
        ' per gruppo disciplinare (classificazione MUR 2020)',
        y=0.93,
    )
    fig.supxlabel('Anno', y=0.08)
    fig.supylabel('Divario retributivo [%]', x=0.08)

    groups = [str(i) for i in range(1, 16)] + ['tutti']
    colors = ['royalblue', 'deeppink', 'darkgreen']
    labels = ['1 anno', '3 anni', '5 anni']

    for idx, g in enumerate(groups):
        row, col = idx // 4, idx % 4
        if g != 'tutti':
            title = 'Gruppo ' + GRUPPO_ID[g]
            ax[row][col].set_title(title.replace(' e ', ' e\n'))
        else:
            ax[row][col].set_title('Totale')

        for yrl, color, label in zip(['1', '3', '5'], colors, labels):
            df_t = df[(df['gruppo'] == g) & (df['anni_da_conseguimento_titolo'] == int(yrl))]
            if not df_t.empty:
                M = df_t['retribuzione_mensile_maschi']
                F = df_t['retribuzione_mensile_femmine']
                divario = 100 * (M - F) / M
                ax[row][col].plot(df_t['anno'], divario, marker='o', lw=2, color=color, label=label)

        ax[row][col].grid()
        if idx == 15:
            ax[row][col].legend()
            ax[row][col].annotate(
                'Source: AlmaLaurea\n\nElaboration by\nBiasissi Riccardo',
                xy=(0.03, 0.03), xytext=(0.03, 0.03), xycoords='axes fraction',
                va='bottom', fontsize=15,
            )

    plt.subplots_adjust(wspace=0.08, hspace=0.24)
    plt.savefig(os.path.join(out_dir, 'divario_retributivo.png'), dpi=200, bbox_inches='tight')
    plt.close()


def plot_unemployment(df, out_dir):
    """Plot unemployment rate over time by discipline group.

    Produces disoccupazione_gruppi.png.

    Parameters
    ----------
    df : pandas.DataFrame
        Pre-loaded almalaurea.csv data.
    out_dir : str
        Directory where the output PNG will be saved.
    """
    fig, ax = plt.subplots(4, 4, sharex=True, sharey=True, figsize=(24, 20))

    fig.suptitle(
        'Tasso di disoccupazione totale (a 1, 3, 5 anni dal titolo)'
        ' per gruppo disciplinare (classificazione MUR 2020)',
        y=0.93,
    )
    fig.supxlabel('Anno', y=0.09)
    fig.supylabel('Tasso di disoccupazione [%]', x=0.08)

    groups = [str(i) for i in range(1, 16)] + ['tutti']
    colors = ['royalblue', 'deeppink', 'darkgreen']
    labels = ['1 anno', '3 anni', '5 anni']

    for idx, g in enumerate(groups):
        row, col = idx // 4, idx % 4
        if g != 'tutti':
            title = 'Gruppo ' + GRUPPO_ID[g]
            ax[row][col].set_title(title.replace(' e ', ' e\n'))
        else:
            ax[row][col].set_title('Totale')

        for yrl, color, label in zip(['1', '3', '5'], colors, labels):
            df_t = df[(df['gruppo'] == g) & (df['anni_da_conseguimento_titolo'] == int(yrl))]
            if not df_t.empty:
                ax[row][col].plot(
                    df_t['anno'], df_t['tasso_disoccupazione_totale'],
                    marker='o', lw=2, color=color, label=label,
                )

        ax[row][col].set_ylim(0, 35)
        ax[row][col].grid()

        if idx == 11:
            ax[row][col].annotate(
                'Source: AlmaLaurea\n\nElaboration by\nBiasissi Riccardo',
                xy=(0.03, 0.95), xytext=(0.03, 0.95), xycoords='axes fraction',
                va='top', ha='left', fontsize=15,
            )
        if idx == 15:
            ax[row][col].legend()

    plt.subplots_adjust(wspace=0.06, hspace=0.24)
    plt.savefig(os.path.join(out_dir, 'disoccupazione_gruppi.png'), dpi=200, bbox_inches='tight')
    plt.close()


def plot_graduate_share(df, out_dir):
    """Plot fraction of graduates per discipline group relative to national total.

    Produces numero_laureati_percentuale.png.

    Parameters
    ----------
    df : pandas.DataFrame
        Pre-loaded almalaurea.csv data.
    out_dir : str
        Directory where the output PNG will be saved.
    """
    fig, ax = plt.subplots(4, 4, sharex=True, figsize=(24, 20))

    fig.suptitle(
        'Frazione di laureati sul totale per gruppo disciplinare'
        ' (e aree disciplinari al 2024 in ordinata, classificazione MUR 2020)',
        y=0.93,
    )
    fig.supxlabel('Anno', y=0.08)
    fig.supylabel('Frazione di laureati [%]', x=0.07)

    groups = [str(i) for i in range(1, 16)] + ['tutti']

    for idx, g in enumerate(groups):
        row, col = idx // 4, idx % 4

        if g != 'tutti':
            title = 'Gruppo ' + GRUPPO_ID[g]
            ax[row][col].set_title(title.replace(' e ', ' e\n'))

            df_t = df[(df['gruppo'] == g) & (df['anni_da_conseguimento_titolo'] == 1)]
            anni       = df_t['anno']
            n_laureati = df_t['numero_laureati']
            tot_anno   = df[
                (df['anni_da_conseguimento_titolo'] == 1) & (df['gruppo'] == 'tutti')
            ]['numero_laureati']
            percentuale = 100 * np.array(n_laureati) / np.array(tot_anno)

            ax[row][col].plot(anni, percentuale, marker='o', lw=2, color='black')
            ax[row][col].set_ylim(0, 16)
            if col != 0:
                ax[row][col].set_yticklabels([])
            ax[row][col].grid()

            if col == 0:
                gruppi_area = AREA_GRUPPI.get(row, [])
                tot_2024 = df[
                    (df['anno'] == 2024) & (df['anni_da_conseguimento_titolo'] == 1)
                    & (df['gruppo'] == 'tutti')
                ]['numero_laureati'].sum()
                n_area = df[
                    (df['anno'] == 2024) & (df['gruppo'].isin(gruppi_area))
                    & (df['anni_da_conseguimento_titolo'] == 1)
                ]['numero_laureati'].sum()
                pct_area = 100 * n_area / tot_2024
                ax[row][col].set_ylabel(f"{AREA_NOME[row]} - {pct_area:.1f}%")

        else:
            ax[row][col].set_title('Totale assoluto annuale (in milioni)')
            df_t       = df[(df['gruppo'] == g) & (df['anni_da_conseguimento_titolo'] == 1)]
            n_laureati = df_t['numero_laureati'] / 1e6

            ax[row][col].plot(df_t['anno'], n_laureati, marker='o', lw=2, color='black')
            ax[row][col].grid()
            ax[row][col].yaxis.tick_right()
            ax[row][col].annotate(
                'Source: AlmaLaurea\n\nElaboration by\nBiasissi Riccardo',
                xy=(0.97, 0.03), xytext=(0.97, 0.03), xycoords='axes fraction',
                va='bottom', ha='right', fontsize=15,
            )

    plt.subplots_adjust(wspace=0.06, hspace=0.24)
    plt.savefig(
        os.path.join(out_dir, 'numero_laureati_percentuale.png'),
        dpi=200, bbox_inches='tight',
    )
    plt.close()
