from langchain.schema import Document

def load_documents_from_database():
    records = [
        {
            "id": 1,
            "title": "O que são Pokémon?",
            "content": (
                "Pokémon são criaturas fictícias criadas pela franquia japonesa Pokémon. "
                "Cada Pokémon possui tipos, habilidades e estatísticas únicas. "
                "Eles podem evoluir, batalhar entre si e são capturados por treinadores usando Pokébolas."
            )
        },
        {
            "id": 2,
            "title": "Tipos de Pokémon",
            "content": (
                "Existem 18 tipos diferentes de Pokémon, como Fogo, Água, Planta, Elétrico, Dragão, Fantasma e outros. "
                "Cada tipo possui forças e fraquezas em relação aos outros. Por exemplo, tipo Água é forte contra Fogo, "
                "mas fraco contra Elétrico e Planta."
            )
        },
        {
            "id": 3,
            "title": "Evoluções",
            "content": (
                "A maioria dos Pokémon pode evoluir para formas mais fortes. Por exemplo, Charmander evolui para Charmeleon e depois para Charizard. "
                "A evolução pode acontecer por nível, por uso de pedras especiais ou por felicidade. Algumas evoluções têm condições específicas, "
                "como estar de dia ou segurar um item."
            )
        },
        {
            "id": 4,
            "title": "Pokémon Lendários",
            "content": (
                "Pokémon lendários são criaturas raras e extremamente poderosas. Alguns exemplos incluem Mewtwo, Lugia, Rayquaza e Arceus. "
                "Normalmente não evoluem e aparecem em momentos importantes da história. São frequentemente tema de filmes e eventos especiais."
            )
        },
        {
            "id": 5,
            "title": "Batalhas Pokémon",
            "content": (
                "Batalhas Pokémon envolvem o uso de estratégias, tipos e movimentos. Cada Pokémon pode aprender até quatro golpes, "
                "e os treinadores devem escolher bem suas ações. O sistema de turnos é baseado em velocidade e fatores como vantagem de tipo, "
                "status e habilidades fazem grande diferença."
            )
        },
        {
            "id": 6,
            "title": "Regiões Pokémon",
            "content": (
                "O mundo Pokémon é dividido em várias regiões como Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola e Galar. "
                "Cada uma possui seus próprios Pokémon nativos, líderes de ginásio e desafios. "
                "As regiões servem como cenário dos jogos principais e expandem a mitologia da franquia."
            )
        }
    ]

    return [
        Document(
            page_content=rec["content"],
            metadata={"title": rec["title"], "id": rec["id"]}
        )
        for rec in records
    ]
