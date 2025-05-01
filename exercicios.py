# exercicios.py

exercicios_por_grupo = {
    "Peito": {
        "Iniciante": [
            {"nome": "Supino reto", "series": 3, "reps": 12},
            {"nome": "Supino inclinado com halteres", "series": 3, "reps": 12},
            {"nome": "Crucifixo no banco reto", "series": 2, "reps": 15},
            {"nome": "Crossover", "series": 3, "reps": 15},
        ],
        "Intermediário": [
            {"nome": "Supino declinado", "series": 4, "reps": 10},
            {"nome": "Peck deck", "series": 3, "reps": 12},
            {"nome": "Flexão no solo", "series": 3, "reps": 20},
        ],
        "Avançado": [
            {"nome": "Supino com Drop Set", "series": 4, "reps": "10-8-6"},
            {"nome": "Flexão com palmas", "series": 3, "reps": 15},
            {"nome": "Crucifixo inclinado com halteres", "series": 4, "reps": 12},
        ],
    },

    "Costas": {
        "Iniciante": [
            {"nome": "Puxada na frente", "series": 3, "reps": 12},
            {"nome": "Remada curvada", "series": 3, "reps": 12},
            {"nome": "Pulldown", "series": 3, "reps": 12},
            {"nome": "Remada baixa", "series": 3, "reps": 15},
        ],
        "Intermediário": [
            {"nome": "Remada unilateral com halteres", "series": 4, "reps": 10},
            {"nome": "Levantamento terra", "series": 3, "reps": 8},
            {"nome": "Puxada pronada", "series": 3, "reps": 12},
        ],
        "Avançado": [
            {"nome": "Remada cavalinho", "series": 4, "reps": 12},
            {"nome": "Pulldown com Drop Set", "series": 3, "reps": "12-10-8"},
            {"nome": "Levantamento terra com barra hexagonal", "series": 4, "reps": 6},
        ],
    },

    "Perna": {
        "Iniciante": [
            {"nome": "Agachamento livre", "series": 3, "reps": 12},
            {"nome": "Leg press", "series": 3, "reps": 15},
            {"nome": "Cadeira extensora", "series": 3, "reps": 15},
            {"nome": "Mesa flexora", "series": 3, "reps": 15},
        ],
        "Intermediário": [
            {"nome": "Avanço com halteres", "series": 3, "reps": 12},
            {"nome": "Stiff com halteres", "series": 3, "reps": 10},
            {"nome": "Agachamento búlgaro", "series": 3, "reps": 10},
        ],
        "Avançado": [
            {"nome": "Agachamento com Drop Set", "series": 4, "reps": "12-10-8"},
            {"nome": "Afundo no smith", "series": 4, "reps": 10},
            {"nome": "Cadeira extensora unilateral", "series": 4, "reps": 12},
        ],
    },

    "Ombro": {
        "Iniciante": [
            {"nome": "Desenvolvimento com halteres", "series": 3, "reps": 12},
            {"nome": "Elevação lateral", "series": 3, "reps": 15},
            {"nome": "Elevação frontal", "series": 3, "reps": 15},
            {"nome": "Crucifixo inverso", "series": 3, "reps": 12},
        ],
        "Intermediário": [
            {"nome": "Arnold press", "series": 3, "reps": 12},
            {"nome": "Remada alta", "series": 3, "reps": 12},
        ],
        "Avançado": [
            {"nome": "Desenvolvimento militar com barra", "series": 4, "reps": 10},
            {"nome": "Elevação lateral com Drop Set", "series": 3, "reps": "15-12-10"},
        ],
    },

    "Bíceps": {
        "Iniciante": [
            {"nome": "Rosca direta", "series": 3, "reps": 12},
            {"nome": "Rosca alternada", "series": 3, "reps": 12},
            {"nome": "Rosca martelo", "series": 3, "reps": 12},
            {"nome": "Rosca concentrada", "series": 3, "reps": 10},
        ],
        "Intermediário": [
            {"nome": "Rosca Scott", "series": 3, "reps": 12},
            {"nome": "Rosca 21", "series": 3, "reps": "7-7-7"},
        ],
        "Avançado": [
            {"nome": "Rosca direta com Drop Set", "series": 4, "reps": "12-10-8"},
            {"nome": "Rosca inversa", "series": 3, "reps": 12},
        ],
    },

    "Tríceps": {
        "Iniciante": [
            {"nome": "Tríceps corda", "series": 3, "reps": 15},
            {"nome": "Tríceps francês", "series": 3, "reps": 12},
            {"nome": "Tríceps banco", "series": 3, "reps": 15},
            {"nome": "Tríceps testa", "series": 3, "reps": 12},
        ],
        "Intermediário": [
            {"nome": "Tríceps pulley inverso", "series": 3, "reps": 12},
            {"nome": "Tríceps com halteres sentado", "series": 3, "reps": 12},
        ],
        "Avançado": [
            {"nome": "Tríceps corda com Drop Set", "series": 3, "reps": "15-12-10"},
            {"nome": "Mergulho entre bancos", "series": 4, "reps": 12},
        ],
    },

    "Abdômen": {
        "Iniciante": [
            {"nome": "Crunch abdominal", "series": 3, "reps": 20},
            {"nome": "Elevação de pernas", "series": 3, "reps": 15},
            {"nome": "Prancha", "series": 3, "reps": "30s"},
            {"nome": "Abdominal oblíquo no solo", "series": 3, "reps": 20},
        ],
        "Intermediário": [
            {"nome": "Prancha lateral", "series": 3, "reps": "30s"},
            {"nome": "Bicicleta no solo", "series": 3, "reps": 30},
        ],
        "Avançado": [
            {"nome": "Abdominal na polia", "series": 4, "reps": 15},
            {"nome": "Prancha com peso", "series": 4, "reps": "30s"},
        ],
    },

    "Trapézio": {
        "Iniciante": [
            {"nome": "Encolhimento com halteres", "series": 3, "reps": 15},
            {"nome": "Encolhimento com barra", "series": 3, "reps": 15},
            {"nome": "Remada alta com halteres", "series": 3, "reps": 12},
            {"nome": "Encolhimento no smith", "series": 3, "reps": 12},
        ],
        "Intermediário": [
            {"nome": "Encolhimento com barra por trás", "series": 3, "reps": 15},
            {"nome": "Remada alta com barra", "series": 3, "reps": 12},
        ],
        "Avançado": [
            {"nome": "Encolhimento com Drop Set", "series": 4, "reps": "15-12-10"},
            {"nome": "Remada alta com Drop Set", "series": 3, "reps": "12-10-8"},
        ],
    }
}
