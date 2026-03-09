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


def _sub_bold(section, start, end=None):
    pat = rf"{start}([\s\S]*?){end}" if end else rf"{start}([\s\S]*)"
    m = re.findall(pat, section)
    if not m:
        return None
    vals = re.findall(r"<td class='datobold'>(.*)</td>", m[0])
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
    # Bands: Meno di 23 anni / 23-24 anni / 25-26 anni / 27 anni e oltre  #
    # ------------------------------------------------------------------ #
    print("=" * 60)
    print("ETA' ALLA LAUREA (%)")
    print("=" * 60)
    t_eta = re.findall(
        r"Età alla laurea \(%\)([\s\S]*?)Età alla laurea \(medie", text
    )
    if not t_eta:
        print("  [ERROR] Section not found — check outer anchors.")
    else:
        for label, start, end in [
            ("Meno di 23 anni", r"Meno di 23",  r"23-24"),
            ("23-24 anni",      r"23-24",        r"25-26"),
            ("25-26 anni",      r"25-26",        r"27 anni"),
            ("27 anni e oltre", r"27 anni",      None),
        ]:
            vals = _sub(t_eta[0], start, end)
            if vals is None:
                print(f"  {label:20s}  [ERROR] sub-pattern '{start}' not found")
            else:
                print(f"  {label:20s}  {vals}")

    # ------------------------------------------------------------------ #
    # Classe sociale (%)                                                   #
    # Bands: Classe elevata / Classe media impiegatizia /                  #
    #        Classe media autonoma / Classe del lavoro esecutivo           #
    # ------------------------------------------------------------------ #
    print()
    print("=" * 60)
    print("CLASSE SOCIALE (%)")
    print("=" * 60)
    t_cs = re.findall(
        r"Classe sociale \(%\)([\s\S]*?)Diploma \(%\)", text
    )
    if not t_cs:
        print("  [ERROR] Section not found — check outer anchors.")
        nearby = re.findall(r"Classe sociale([\s\S]{0,500})", text)
        if nearby:
            print("\n  --- HTML context after 'Classe sociale' ---")
            print(nearby[0])
    else:
        for label, start, end in [
            ("Classe elevata",           r"Classe elevata",            r"Classe media impiegatizia"),
            ("Classe media impieg.",     r"Classe media impiegatizia", r"Classe media autonoma"),
            ("Classe media autonoma",    r"Classe media autonoma",     r"Classe del lavoro"),
            ("Classe del lavoro esec.",  r"Classe del lavoro",         None),
        ]:
            vals = _sub(t_cs[0], start, end)
            if vals is None:
                print(f"  {label:26s}  [ERROR] sub-pattern '{start}' not found")
            else:
                print(f"  {label:26s}  {vals}")

    # ------------------------------------------------------------------ #
    # Diploma (%)                                                          #
    # ------------------------------------------------------------------ #
    print()
    print("=" * 60)
    print("DIPLOMA (%)")
    print("=" * 60)
    t_dip = re.findall(r"Diploma \(%\)([\s\S]*?)Voto di diploma", text)
    if not t_dip:
        print("  [ERROR] Section not found")
    else:
        for label, fn, start, end in [
            ("Liceale",          _sub_bold, r"Liceale",              r"Liceo classico"),
            ("Liceo classico",   _sub,      r"Liceo classico",        r"Liceo linguistico"),
            ("Liceo linguistico",_sub,      r"Liceo linguistico",     r"Liceo scientifico"),
            ("Liceo scientifico",_sub,      r"Liceo scientifico",     r"Liceo delle scienze"),
            ("Sc. umane",        _sub,      r"Liceo delle scienze",   r"Liceo artistico"),
            ("Artistico",        _sub,      r"Liceo artistico",       r"Tecnico"),
            ("Tecnico",          _sub_bold, r"Tecnico",               r"Tecnico economico"),
            ("Tecnico economico",_sub,      r"Tecnico economico",     r"Tecnico tecnologico"),
            ("Tecnico tecnol.",  _sub,      r"Tecnico tecnologico",   r"Professionale"),
            ("Professionale",    _sub_bold, r"Professionale",         r"Titolo estero"),
            ("Titolo estero",    _sub_bold, r"Titolo estero",         None),
        ]:
            vals = fn(t_dip[0], start, end)
            if vals is None:
                print(f"  {label:22s}  [ERROR] not found")
            else:
                print(f"  {label:22s}  {vals}")

    # ------------------------------------------------------------------ #
    # Sanity check — existing patterns                                     #
    # ------------------------------------------------------------------ #
    print()
    print("=" * 60)
    print("SANITY CHECK — existing patterns")
    print("=" * 60)
    t_m = re.findall(r"Uomini([\s\S]*?)Donne", text)
    if t_m:
        vals = re.findall(r"<td class='dato'>(.*)</td>", t_m[0])
        print(f"  Uomini %: {vals}")
    else:
        print("  [ERROR] 'Uomini' pattern not found")


if __name__ == '__main__':
    main()
