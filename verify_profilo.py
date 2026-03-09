#!/usr/bin/env python3
"""Verify the new regex patterns for 'Età alla laurea (%)' and 'Classe sociale (%)'
against the AlmaLaurea example URL.

Run with:
    python verify_profilo.py
"""
import re
import requests
import numpy as np

URL = (
    "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php"
    "?anno=2024&corstipo=tutti&ateneo=tutti&facolta=tutti&gruppo=tutti"
    "&livello=tutti&area4=tutti&classe=tutti&postcorso=tutti&isstella=0"
    "&regione=tutti&dimensione=tutti&presiui=tutti&cs_univ=tutti"
    "&cs_facoa=tutti&cs_corsb=tutti&disaggregazione=&LANG=it&CONFIG=profilo"
)


def _parse_cell(value, mode):
    if value == '&nbsp;':
        return np.nan
    if value == '-':
        return 0.0
    if mode == 'int':
        return value.replace('.', '')
    if mode == 'float':
        return value.replace(',', '.')
    return value


def _sub(section, start, end=None):
    pat = rf"{start}([\s\S]*?){end}" if end else rf"{start}([\s\S]*)"
    m = re.findall(pat, section)
    if not m:
        return None
    vals = re.findall(r"<td class='dato'>(.*)</td>", m[0])
    return [_parse_cell(v, 'float') for v in vals]


def main():
    print(f"Fetching: {URL}\n")
    text = requests.get(URL, timeout=15).text

    html_path = "profilo_raw.txt"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Raw HTML saved to: {html_path}\n")

    # ------------------------------------------------------------------ #
    # Età alla laurea (%)                                                  #
    # ------------------------------------------------------------------ #
    print("=" * 60)
    print("ETA' ALLA LAUREA (%)")
    print("=" * 60)
    t_eta = re.findall(r"Età alla laurea([\s\S]*?)Voto di laurea", text)
    if not t_eta:
        print("  [ERROR] Section 'Età alla laurea' not found — check anchor.")
    else:
        for label, start, end in [
            ("Entro 23 anni", r"Entro 23",  r"24-26"),
            ("24-26 anni",    r"24-26",     r"27-30"),
            ("27-30 anni",    r"27-30",     r"31 "),
            ("31 anni e oltre", r"31 ",     None),
        ]:
            vals = _sub(t_eta[0], start, end)
            if vals is None:
                print(f"  {label:25s}  [ERROR] sub-pattern '{start}' not found")
            else:
                print(f"  {label:25s}  {vals}")

    # ------------------------------------------------------------------ #
    # Classe sociale (%)                                                   #
    # ------------------------------------------------------------------ #
    print()
    print("=" * 60)
    print("CLASSE SOCIALE (%)")
    print("=" * 60)
    t_cs = re.findall(r"Classe sociale([\s\S]*?)Titolo di studio", text)
    if not t_cs:
        print("  [ERROR] Section 'Classe sociale' not found — check anchor.")
        # Print nearby HTML to help diagnose:
        nearby = re.findall(r"Classe sociale([\s\S]{0,500})", text)
        if nearby:
            print("\n  --- HTML context after 'Classe sociale' ---")
            print(nearby[0])
    else:
        for label, start, end in [
            ("Borghesia",              r"Borghesia",    r"Classe media"),
            ("Classe media impieg.",   r"Classe media", r"Piccola"),
            ("Piccola borghesia",      r"Piccola",      r"Classe operaia"),
            ("Classe operaia",         r"Classe operaia", None),
        ]:
            vals = _sub(t_cs[0], start, end)
            if vals is None:
                print(f"  {label:25s}  [ERROR] sub-pattern '{start}' not found")
            else:
                print(f"  {label:25s}  {vals}")

    # ------------------------------------------------------------------ #
    # Quick sanity check on existing patterns (gender)                    #
    # ------------------------------------------------------------------ #
    print()
    print("=" * 60)
    print("SANITY CHECK — existing pattern (Uomini %)")
    print("=" * 60)
    t_m = re.findall(r"Uomini([\s\S]*?)Donne", text)
    if t_m:
        vals = re.findall(r"<td class='dato'>(.*)</td>", t_m[0])
        print(f"  Uomini: {vals}")
    else:
        print("  [ERROR] 'Uomini' pattern not found")


if __name__ == '__main__':
    main()
