# name, wisdom cost, attack, defense, type
STANDARD_CARDS_RAW_DATA = {
    'abraao': ('Abraão', 2, 1, 2, 'hero'),
    'adao': ('Adão', 1, 1, 1, 'hero'),
    'daniel': ('Daniel', 2, 1, 2, 'hero'),
    'davi': ('Davi', 3, 3, 2, 'hero'),
    'elias': ('Elias', 4, 3, 1, 'hero'),
    'ester': ('Ester', 1, 0, 2, 'hero'),
    'eva': ('Eva', 1, 1, 1, 'hero'),
    'jaco': ('Jaco', 2, 2, 2, 'hero'),
    'jose-do-egito': ('José do Egito', 2, 2, 1, 'hero'),
    'josue': ('Josué', 3, 3, 1, 'hero'),
    'maria': ('Maria', 2, 1, 2, 'hero'),
    'moises': ('Moisés', 3, 2, 2, 'hero'),
    'noe': ('Noé', 1, 2, 1, 'hero'),
    'salomao': ('Salomão', 4, 2, 2, 'hero'),
    'sansao': ('Sansão', 6, 5, 5, 'hero'),
    'davi-lendario': ('Davi', 3, 4, 5, 'legendary'),
    'josue-lendario': ('Josué', 3, 3, 2, 'legendary'),
    'moises-lendario': ('Moisés', 3, 2, 3, 'legendary'),
    'arca-da-alianca': ('Arca da Aliança', 5, 0, 0, 'artifact'),
    'arca-de-noe': ('Arca de Noé', 5, 0, 0, 'artifact'),
    'botas-do-evangelho': ('Botas do Evangelho', 2, 0, 0, 'artifact'),
    'cajado-de-moises': ('Cajado de Moisés', 2, 0, 0, 'artifact'),
    'capacete-da-salvacao': ('Capacete da Salvação', 1, 0, 0, 'artifact'),
    'cinturao-da-verdade': ('Cinturão da Verdade', 4, 0, 0, 'artifact'),
    'couraca-da-justica': ('Couraça da Justiça', 3, 0, 0, 'artifact'),
    'escudo-da-fe': ('Escudo da Fé', 1, 0, 0, 'artifact'),
    'espada-do-espirito': ('Espada do Espírito', 3, 0, 0, 'artifact'),
    'os-10-mandamentos': ('Os 10 Mandamentos', 6, 0, 0, 'artifact'),
    'fruto-proibido': ('Fruto Proibido', 3, 0, 0, 'sin'),
    'idolatria': ('Idolatria', 2, 0, 0, 'sin'),
    'traicao': ('Traição', 2, 0, 0, 'sin'),
    'cordeiro-de-deus': ('Cordeiro de Deus', 4, 0, 0, 'miracle'),
    'diluvio': ('Dilúvio', 6, 0, 0, 'miracle'),
    'fogo-do-ceu': ('Fogo do Céu', 3, 0, 0, 'miracle'),
    'forca-de-sansao': ('Força de Sansão', 2, 0, 0, 'miracle'),
    'liberacao-celestial': ('Liberação Celestial', 2, 0, 0, 'miracle'),
    'no-ceu-tem-pao': ('No Céu tem Pão', 3, 0, 0, 'miracle'),
    'passagem-segura': ('Passagem Segura', 4, 0, 0, 'miracle'),
    'protecao-divina': ('Proteção de  Divina', 1, 0, 0, 'miracle'),
    'ressurreicao': ('Ressurreição', 3, 0, 0, 'miracle'),
    'restauracao-de-fe': ('Restauração de Fé', 2, 0, 0, 'miracle'),
    'sabedoria-de-salomao': ('Sabedoria de Salomão', 1, 0, 0, 'miracle'),
    'sarca-ardente': ('Sarça Ardente', 2, 0, 0, 'miracle'),
}

STANDARD_CARDS_HEROS = [
    'abraao',
    'adao',
    'daniel',
    'davi',
    'elias',
    'ester',
    'eva',
    'jaco',
    'jose-do-egito',
    'josue',
    'maria',
    'moises',
    'noe',
    'salomao',
    'sansao',
]

STANDARD_CARDS_LEGENDARY_HEROS = [
    # 'davi-ssj',
    # 'josue-ssj',
    # 'moises-ssj',
]

STANDARD_CARDS_MIRACLES = [
    # 'cordeiro-de-deus',
    'diluvio',
    'fogo-do-ceu',
    'forca-de-sansao',
    # 'liberacao-celestial',
    'no-ceu-tem-pao',
    # 'passagem-segura',
    # 'protecao-divina',
    'ressurreicao',
    'restauracao-de-fe',
    'sabedoria-de-salomao',
    'sarca-ardente',
]

STANDARD_CARDS_ARTIFACTS = [
    'arca-da-alianca',
    'arca-de-noe',
    'botas-do-evangelho',
    'cajado-de-moises',
    'capacete-da-salvacao',
    'cinturao-da-verdade',
    'couraca-da-justica',
    'escudo-da-fe',
    'espada-do-espirito',
    'os-10-mandamentos',
]

STANDARD_CARDS_SINS = [
    # 'fruto-proibido',
    # 'idolatria',
    # 'traicao',
]

STANDARD_CARDS = [
    *STANDARD_CARDS_HEROS,
    *STANDARD_CARDS_MIRACLES,
    *STANDARD_CARDS_ARTIFACTS,
    *STANDARD_CARDS_SINS,
    *STANDARD_CARDS_LEGENDARY_HEROS,
]
