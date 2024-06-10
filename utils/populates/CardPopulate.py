from utils.DataBaseManager import DB_Manager, Session

from models import Card, Cards_Type

card_type = [
    {
        "slug": 'hero',
        "name": {
            "pt-br": "herói"},
        "description": {
            'pt-br': '''
                Os heróis são representações dos <strong>históricos heróis bíblicos</strong>. Guerreiros lendários como Josué e Davi, Profetas como Elias e Moisés, ou figuras históricas como Adão, Eva ou Maria.
                Essas cartas são destacadas por sua cor, e por terem um símbolo de <strong>espada</strong> do lado esquerdo seguido de um número (este é seu ponto de ataque) e um símbolo de <strong>escudo</strong> do lado direito seguido de um número (este é seu ponto de defesa)
                Usar os Heróis para atacar seu adversário é a forma básica de diminuir seus pontos e <strong>vencer a partida</strong>.
                <strong>Obs.:</strong> Os Heróis entram em jogo diretamente  na zona de preparação, tendo que esperar seu próximo turno para ir a zona de combate. Heróis que atacaram não podem voltar para a zona de preparação neste turno, a não ser que a descrição da carta diga o contrário.
            '''
        }
    },
    {
        "slug": "artifacts",
        "name": {
            'pt-br': 'artefatos',
        },
        "description": {
            'pt-br': '''
                São representações dos lendários <strong>artefatos citados nas histórias bíblicas</strong>, como por exemplo o cajado de Moisés, os 10 mandamentos e a Espada do Espírito, artefatos só podem ser jogados no seu turno.
                No Faith Battle os artefatos são representados pela sua cor Amarela, eles são equipamentos poderosos que potencializam seus heróis, dando mais <strong>força, resistência e habilidades especiais</strong>.
                <strong>Obs.:</strong> Os artefatos só podem ser equipados na zona de preparação, se um herói morre equipado a um artefato, o mesmo será descartado junto ao herói que foi eliminado, se você quiser passar um artefato equipado de um herói a outro, terá que regressar esse herói a zona de preparação, gastando um turno para preparar e voltar ao combate, se você já atacou com este herói nesse turno não poderá voltar para zona de preparação, deverá escolher entre <strong>atacar ou preparar-se</strong>, a não ser que a descrição da carta diga o contrário.
            '''
        }
    },
    {
        'slug': 'miracles',
        'name': {
            'pt-br': 'milagres'
        },
        'description': {
            'pt-br': '''
                São representações dos <strong>milagres relatados na Bíblia</strong>, que no jogo tem a intenção de interagir com os heróis em batalhas. São representados pela cor Verde.
                Quando usados de forma estratégica, os milagres podem mudar completamente o andamento do jogo, potencializando seus ataques com a carta " Força de Sansão", <strong>protegendo</strong> seus heróis com a "Proteção Divina " ou até <strong>cancelando uma jogada</strong> do oponente com "Liberação Celestial ".
                <strong>Obs.:</strong> Os milagres podem ser jogados em qualquer momento do jogo, eles não afetam cartas na zona de preparação, eles só terão como alvo as cartas que já estão na zona de batalha, a não ser que a descrição da carta diga o contrário.
            '''
        },
    },
    {
        "slug": "sins",
        "name": {
            'pt-br': "pecados"
        },
        "description": {
            "pt-br": '''
                        São representações dos pecados citados nas narrativas bíblicas. No Faith Battle os pecados são <strong>"cartas armadilha"</strong> como as cartas utilizadas em distintos cardgames, que produzem efeitos negativos ao oponente. São representados pela cor vermelha.
                        Assim como as cartas de milagre, os pecados em um custo de sabedoria, porém <strong>necessitam uma consigna para serem ativadas</strong>, um ataque do oponente ou uma ação especial, etc. Ao usar um pecado, o jogador perde automaticamente um ponto de fé, e também poderá opitar por pagar seu custo com pontos de fé em vez de sabedoria, além do ponto que ja perdeu.
                        <strong>Obs.:</strong> Assim como os milagres, os pecados só afetam cartas na <strong>zona de batalha</strong>, a não ser que a descrição da carta diga o contrário.
                    '''
        }
    },
    {
        "slug": "legendary",
        'name': {
            'pt-br': 'lendárias'
        },
        'description': {
            'pt-br': '''
                        A mecânica de ativação das cartas lendárias, é semelhante a mecânica de “fusão” que está presente em distintos cardgames.  Para ativar um herói lendário,o jogador precisará descer a versão básica dela em jogo, pagar seu custo de ativação pela segunda vez,e colocar a carta lendária em cima da versão básica, fundindo as duas cartas. Quando essa ativação é concluída, este herói agora terá as novas habilidades descritas na carta lendária, além das outras habilidades que já tinha na sua versão básica.  
                        Os Heróis lendários tem a habilidade de “ativação”, pagando [IMAGEM_ICONE_SABEDORIA] ( que simboliza 1 de sabedoria), a habilidade do herói se ativa, provocando seu efeito permanente ou temporario, de acordo com a descrição da carta.
                        Obsevações: Os pontos de ataque e defesa deste herói serão os que constam na sua versão lendária, e se a versão básica tem uma habilidade que se ativa ao entrar em jogo,essa habilidade se ativará uma segunda vez, ao entrar a carta lendária, exemplo: Quando o herói Moisés entra em jogo, o jogador alvo busca um milagre no baralho ou mar do esquecimento, depois que  Moisés já está em jogo, se o jogador optar por pagar o custo novamente,  fundindo a versão lendária a ele. sua habilidade se reativará, dando a possibilidade de buscar outro milagre.  
                        Está proibido ter a cópia de uma carta lendária em seu baralho. Você poderá optar em armar seu deck de duas formas:  
                        >  Jogar com as cartas lendárias, usando apenas uma versão básica dessa carta no seu  baralho.
                        > Jogar com duas cópias das versões básicas, impossibilitando a ativação da carta lendária.
                    '''
        }
    },
    {
        'slug': 'wisdon',
        "name": {
            'pt-br': 'sabedoria'
        },
        'description': {
            'pt-br': '''
                        Cada carta possui um <strong>custo</strong> para entrar em jogo ou ser ativada, esse custo é representado por um ícone azul no canto superior esquerdo. São as cartas de sabedorias que <strong>possibilitam fazer qualquer jogada</strong>, são elas que definem a quantidade de pontos de sabedoria que o jogador tem para <strong>gastar no seu turno</strong>.
                        Essa mecânica é parecida às <strong>energias</strong> usadas no pokémon, o custo de sacrifício do Yu-gi-oh, ou a <strong>mana</strong> de jogos como Hearthstone, Gwen ou Magic The Gathering.
                        <strong>Obs.:</strong> Para ativar uma carta de sabedoria, o jogador sinaliza a carta e a gira para baixo, com isso se soma 1 ponto de sabedoria para ativar cartas. No começo do seu turno, volte suas cartas para cima, para que possa reutilizá-las, além disso, se acrescenta mais uma carta de sabedoria ao seu campo, somando <strong>10 cartas no total</strong>!
                    '''
        }
    }
]

fake_cards = [
    (1, 'Davi', '_', '_', '_', 1, 1, 1, False, False, False),
    (1, 'Ester', '_', '_', '_', 1, 0, 1, False, False, False),
    (2, 'Arca de Noé', '_', '_', '_', 3, 0, 0, True, False, True),
    (3, 'Sarça Ardente', '_', '_', '_', 2, 0, 0, False, True, False),
    (4, 'Idolatria', '_', '_', '_', 2, 0, 0, False, True, False),
    (2, 'Espada da Justiça', '_', '_', '_', 2, 1, 0, False, True, True)
]

DB = DB_Manager()

# with Session(DB.engine) as session:
    # for types in card_type:
    #     newCardType = Cards_Type(type_name=types['name']['pt-br'], type_description=types['description']['pt-br'])
    #     session.add(newCardType)
    #     session.commit()
    # for card in fake_cards:
    #     newCard = Card(
    #         card_type=card[0],
    #         card_name=card[1],
    #         card_description=card[2],
    #         card_holy_reference=card[3],
    #         card_image=card[4],
    #         card_wisdom_cost=card[5],
    #         card_attack_points=card[6],
    #         card_defense_points=card[7]
    #     )
    #     session.add(newCard)
        # session.commit()
        # print(newCard)
