import re
import numpy as np
import requests


def _parse_cell(value, mode):
    """Clean a single HTML table cell value.

    mode='int'   — strip thousands separator '.'
    mode='float' — replace decimal comma ',' with '.'
    Returns np.nan for empty cells ('&nbsp;'), 0.0 for dash ('-').
    """
    if value == '&nbsp;':
        return np.nan
    if value == '-':
        return 0.0
    if mode == 'int':
        return value.replace('.', '')
    if mode == 'float':
        return value.replace(',', '.')
    return value


def fetch_profile(university_id, area_id, gruppo_id):
    """Scrape graduate profile statistics from AlmaLaurea.

    Parameters
    ----------
    university_id : str
        AlmaLaurea university ID, or 'tutti' for national aggregate.
    area_id : str
        Discipline area code (e.g. '1', '2', '3', '4', or 'tutti').
    gruppo_id : str
        Discipline group code ('1'–'15', or 'tutti').

    Returns
    -------
    list : [num_laureati, pct_maschi, pct_femmine, voto_laurea,
            anni, ateneo, facolta, area, gruppo,
            eta_meno23, eta_23_24, eta_25_26, eta_27_oltre,
            cs_elevata, cs_media_imp, cs_media_aut, cs_lavoro_es]
        Arrays are numpy arrays over years; metadata strings are None on failure.
        Indices 9-12:  Età alla laurea (%) — <23, 23-24, 25-26, 27+.
        Indices 13-16: Classe sociale (%) — elevata, media imp., media aut., lavoro esec.
    """
    url = (
        "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php"
        f"?anno=tutti&corstipo=tutti&ateneo={university_id}&facolta=tutti"
        f"&gruppo={gruppo_id}&livello=tutti&area4={area_id}&pa={university_id}"
        "&classe=tutti&postcorso=tutti&isstella=0&presiui=tutti"
        "&disaggregazione=&LANG=it&CONFIG=profilo"
    )
    text = requests.get(url).text

    ateneo_m = re.findall(r"Ateneo: (.*)", text)

    if not ateneo_m:
        empty = np.full(19, np.nan)
        return [empty, empty, empty, empty, [], None, None, None, None]

    ateneo  = ateneo_m[0][:-1]
    facolta = re.findall(r"Facoltà/Dipartimento/Scuola: (.*)", text)[0][:-1]
    area    = re.findall(r"area disciplinare: (.*)", text)[0][:-1]
    gruppo  = re.findall(r"gruppo disciplinare: (.*)", text)[0][:-1]

    anni = re.findall(r"<b>anno di laurea......(.*?)'", text)
    anni = list(dict.fromkeys(anni))

    def _extract_bold(pattern):
        t = re.findall(pattern, text)
        vals = re.findall(r"<td class='datobold'>(.*)</td>", t[0])
        return np.array([_parse_cell(v, 'int') for v in vals], float)

    def _extract_normal(pattern):
        t = re.findall(pattern, text)
        vals = re.findall(r"<td class='dato'>(.*)</td>", t[0])
        return np.array([_parse_cell(v, 'float') for v in vals], float)

    num_laureati = _extract_bold(
        r"Numero di laureati([\s\S]*)Hanno compilato il questionario"
    )
    pct_maschi = _extract_normal(r"Uomini([\s\S]*?)Donne")
    pct_femmine = _extract_normal(r"Donne([\s\S]*?)Età alla laurea")
    voto_laurea = _extract_normal(
        r"Voto di laurea([\s\S]*?)Regolarità negli studi"
    )

    # --- Età alla laurea (%) ---
    # Sub-rows: "Meno di 23 anni", "23-24 anni", "25-26 anni", "27 anni e oltre"
    # Section bounded by the "(medie, in anni)" row that immediately follows
    def _sub(section, start, end=None):
        pat = rf"{start}([\s\S]*?){end}" if end else rf"{start}([\s\S]*)"
        m = re.findall(pat, section)
        if not m:
            return np.array([np.nan])
        vals = re.findall(r"<td class='dato'>(.*)</td>", m[0])
        return np.array([_parse_cell(v, 'float') for v in vals], float)

    t_eta = re.findall(
        r"Età alla laurea \(%\)([\s\S]*?)Età alla laurea \(medie", text
    )
    if t_eta:
        eta_meno23   = _sub(t_eta[0], r"Meno di 23",  r"23-24")
        eta_23_24    = _sub(t_eta[0], r"23-24",        r"25-26")
        eta_25_26    = _sub(t_eta[0], r"25-26",        r"27 anni")
        eta_27_oltre = _sub(t_eta[0], r"27 anni",      None)
    else:
        empty = np.array([np.nan])
        eta_meno23 = eta_23_24 = eta_25_26 = eta_27_oltre = empty

    # --- Classe sociale (%) ---
    # Sub-rows: "Classe elevata", "Classe media impiegatizia",
    #           "Classe media autonoma", "Classe del lavoro esecutivo"
    # Section is the last block in table dati3; end anchor is "Diploma (%)"
    # which opens the next HTML table (dati4, secondary education)
    t_cs = re.findall(
        r"Classe sociale \(%\)([\s\S]*?)Diploma \(%\)", text
    )
    if t_cs:
        cs_elevata   = _sub(t_cs[0], r"Classe elevata",            r"Classe media impiegatizia")
        cs_media_imp = _sub(t_cs[0], r"Classe media impiegatizia", r"Classe media autonoma")
        cs_media_aut = _sub(t_cs[0], r"Classe media autonoma",     r"Classe del lavoro")
        cs_lavoro_es = _sub(t_cs[0], r"Classe del lavoro",         None)
    else:
        empty = np.array([np.nan])
        cs_elevata = cs_media_imp = cs_media_aut = cs_lavoro_es = empty

    return [num_laureati, pct_maschi, pct_femmine, voto_laurea,
            anni, ateneo, facolta, area, gruppo,
            eta_meno23, eta_23_24, eta_25_26, eta_27_oltre,
            cs_elevata, cs_media_imp, cs_media_aut, cs_lavoro_es]


def fetch_employment(university_id, survey_year, area_id, gruppo_id,
                     degree_class, years_since_graduation):
    """Scrape employment and salary statistics from AlmaLaurea.

    Parameters
    ----------
    university_id : str
        AlmaLaurea university ID, or 'tutti'.
    survey_year : str
        Year of the survey (e.g. '2023').
    area_id : str
        Discipline area code or 'tutti'.
    gruppo_id : str
        Discipline group code or 'tutti'.
    degree_class : str
        Degree class code, or 'tutti'.
    years_since_graduation : str
        '1', '3', or '5'.

    Returns
    -------
    list : [num_laureati, pct_maschi, pct_femmine, tasso_occupazione,
            tasso_disoccupazione, salary_maschi, salary_femmine, salary_totale,
            ateneo, facolta, area, gruppo]
        Single-element lists for numeric values; metadata strings or None.
    """
    if degree_class == 'tutti':
        url = (
            "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php"
            f"?anno={survey_year}&corstipo=tutti&ateneo={university_id}&facolta=tutti"
            f"&gruppo={gruppo_id}&livello=tutti&area4={area_id}&pa={university_id}"
            f"&classe={degree_class}&postcorso=tutti&isstella=0"
            f"&annolau={years_since_graduation}&condocc=tutti&iscrls=tutti"
            "&disaggregazione=&LANG=it&CONFIG=occupazione"
        )
    else:
        url = (
            "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php"
            f"?anno={survey_year}&corstipo=LS&ateneo={university_id}&facolta=tutti"
            f"&gruppo={gruppo_id}&livello=tutti&area4={area_id}&pa={university_id}"
            f"&classe={degree_class}&postcorso=tutti&isstella=0"
            f"&annolau={years_since_graduation}&condocc=tutti&iscrls=tutti"
            "&disaggregazione=&LANG=it&CONFIG=occupazione"
        )
    text = requests.get(url).text

    ateneo_m = re.findall(r"Ateneo: (.*)", text)

    if not ateneo_m:
        nan = [np.nan]
        return [nan, nan, nan, nan, nan, nan, nan, nan, None, None, None, None]

    ateneo  = ateneo_m[0][:-1]
    facolta = re.findall(r"Facoltà/Dipartimento/Scuola: (.*)", text)[0][:-1]
    area    = re.findall(r"area disciplinare: (.*)", text)[0][:-1]
    gruppo  = re.findall(r"gruppo disciplinare: (.*)", text)[0][:-1]

    # --- Numero di laureati ---
    t = re.findall(r"Numero di laureati([\s\S]*?)Numero di intervistati", text)
    raw = re.findall(r"<td class='datobold'>(.*)</td>", t[0])
    num_laureati = [float(_parse_cell(raw[0], 'int'))]

    # --- Genere ---
    t_genere = re.findall(r"Genere([\s\S]*?)Età alla laurea", text)

    t_m = re.findall(r"Uomini([\s\S]*?)Donne", t_genere[0])
    raw_m = re.findall(r"<td class='dato'>(.*)</td>", t_m[0])
    pct_maschi = [float(_parse_cell(raw_m[0], 'float'))]

    t_f = re.findall(r"Donne([\s\S]*?)Età alla laurea", text)
    raw_f = re.findall(r"<td class='dato'>(.*)</td>", t_f[0])
    pct_femmine = [float(_parse_cell(raw_f[0], 'float'))]

    # --- Tasso di occupazione (pattern differs pre/post 2020) ---
    if int(survey_year) < 2020:
        t_occ = re.findall(
            r"Tasso di occupazione([\s\S]*?)Tasso di disoccupazione", text
        )
    else:
        t_occ = re.findall(
            r"Totale([\s\S]*?)Tasso di disoccupazione", text
        )
    raw_occ = re.findall(r"<td class='datobold'>(.*)</td>", t_occ[0])
    tasso_occupazione = [float(_parse_cell(raw_occ[0], 'float'))]

    # --- Tasso di disoccupazione ---
    t_dis = re.findall(
        r"Tasso di disoccupazione([\s\S]*?)Ingresso nel mercato", text
    )
    raw_dis = re.findall(r"<td class='datobold'>(.*)</td>", t_dis[0])
    tasso_disoccupazione = [float(_parse_cell(raw_dis[0], 'float'))]

    # --- Retribuzione mensile ---
    t_sal = re.findall(r"Retribuzione mensile([\s\S]*?)Utilizzo", text)
    if len(t_sal) > 1:
        t_sal[0] = t_sal[-1]
    raw_sal = re.findall(r"<td class='dato'>(.*)</td>", t_sal[0])
    salary_maschi  = [float(_parse_cell(raw_sal[0], 'int'))]
    salary_femmine = [float(_parse_cell(raw_sal[1], 'int'))]

    raw_sal_bold = re.findall(r"<td class='datobold'>(.*)</td>", t_sal[0])
    cleaned_bold = [
        float(_parse_cell(v, 'int'))
        for v in raw_sal_bold
        if v not in ('&nbsp;', 'nan')
    ]
    salary_totale = [cleaned_bold[0]]

    return [num_laureati, pct_maschi, pct_femmine,
            tasso_occupazione, tasso_disoccupazione,
            salary_maschi, salary_femmine, salary_totale,
            ateneo, facolta, area, gruppo]
