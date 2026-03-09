AREA = {
    'tutti': 'tutti',
    'ALE': '1',
    'EGS': '2',
    'SAV': '3',
    'STEM': '4',
}

GRUPPO = {
    'tutti': 'tutti',
    'Educazione e formazione': '1',
    'Arte e design': '2',
    'Letterario umanistico': '3',
    'Linguistico': '4',
    'Politico-sociale e comunicazione': '5',
    'Psicologico': '6',
    'Economico': '7',
    'Giuridico': '8',
    'Scientifico': '9',
    'Informatica e tecnologie ICT': '10',
    'Architettura e Ing civile': '11',
    "Ing industriale e dell'informazione": '12',
    'Agrario-forestale e veterinario': '13',
    'Medico-sanitario e farmaceutico': '14',
    'Scienze motorie e sportive': '15',
}

GRUPPO_ID = {v: k for k, v in GRUPPO.items()}

PALETTE = ['royalblue', 'deeppink', 'forestgreen', 'crimson', 'purple']

AREA_NOME = ['ALE', 'EGS', 'STEM', 'SAV']

# Maps subplot row index to the discipline group IDs belonging to that area
AREA_GRUPPI = {
    0: ['1', '2', '3', '4'],
    1: ['5', '6', '7', '8'],
    2: ['9', '10', '11', '12'],
    3: ['13', '14', '15'],
}
