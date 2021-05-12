from datetime import datetime

mappings = {
    'mappings': {
        'event': {
            'properties': {
                'id': {'type': 'text'},
                'name': {'type': 'text', 'analyzer': 'english'},
                'description': {'type': 'text', 'analyzer': 'english'},
                'city': {'type': 'text'},
                'start_date': {'type': 'date'},
                'price': {'type': 'float'}
            }
        }
    }
}

documents = [
    {
        'id': '1',
        'name': 'Heisenberg uncertainity principle',
        'description': """Who in the world would have thought that there is a limitation to what 
            we can find about a microscopic object. Lets dive deep into what Heisenberg uncertainity principle is
            and how it puts a contraint on our ability to predict the momentum and position of an object. Later we will
            also see how everything is of dual nature.""",
        'city': 'Ohio',
        'start_date': datetime(2018, 6, 20),
        'price': 5000.00
    },
    {
        'id': '2',
        'name': 'The melting icebergs: Global warming',
        'description': """Global warming, also referred to as climate change, is the observed 
            century-scale rise in the average temperature of the Earth's 
            climate system and its related effects. Multiple lines of scientific 
            evidence show that the climate system is warming.[2][3][4] Many of the observed changes 
            since the 1950s are unprecedented in the instrumental temperature record, 
            and in paleoclimate proxy records of climate change over thousands to millions of years.[5]""",
        'city': 'Geneva',
        'start_date': datetime(2018, 3, 20),
        'price': 8000.00
    },
]
