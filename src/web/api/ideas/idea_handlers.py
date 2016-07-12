from anillo.http import responses

from core.ideas import idea_actions

from tools.adt.converter import to_plain, from_plain


# @login_required
def list_ideas(request):
    return responses.Ok([
        {
            "uuid": "q8h89asdhfb93c8b9",
            "title": "Detector de metano",
            "description": "La idea es simple: Un Arduino conectado a una Raspberri PI que a su vez tenga un detector de gases que consulte a través de fruskis a unos datos de bigdata repository on the cloud with diamonds que nos de una aproximación empírica de cuánto huele a caca en el WC",
            "owner": {
                "user_name": "pepito",
                "email": "pepito@delospalotes.es",
                "full_name": "Pepito el de los Palotes",
                "avatar": {
                    "head": 1,
                    "body": 1,
                    "legs": 1,
                },
            },
            "created_at": "2016-07-11T16:25:13.112432",
            "is_public": True,
            "forked_from": None,
            "comments_count": 3,
            "reactions_counts": {"thumbsup": 3, "dancer": 10},
        },
        {
            "uuid": "9adfsnansyhr234hor283",
            "title": "Gimnasio virtual",
            "description": "CUÁNTAS VECES habeis mentido a vuestra pareja diciendo que ibais al gimnasio cuando en realidad os bajabais al bar a tomaros unos cuba-libres.\n\nSe acabo el inventar excusas!!\n\ncon el revolucionario…",
            "owner": {
                "user_name": "fulanito",
                "email": "fulanito@perez.org",
                "full_name": "Fulanito Pérez",
                "avatar": {
                    "head": 2,
                    "body": 2,
                    "legs": 2,
                },
            },
            "created_at": "2016-07-11T17:30:15.442647",
            "is_public": False,
            "forked_from": None,
            "comments_count": 0,
            "reactions_counts": {},
        },
        {
            "uuid": "32498fjerfhfhr79rr",
            "title": "πweekr",
            "description": "La idea es aglomerar en una aplicacion toda la “vida” de la piweek. Desde que empieza una nueva edicion a la promocion de los proyectos y la gestion del hype previo.\n\nAdemas tambien servira como escaparate a los…",
            "owner": {
                "user_name": "fulanito",
                "email": "fulanito@perez.org",
                "full_name": "Fulanito Pérez",
                "avatar": {
                    "head": 2,
                    "body": 2,
                    "legs": 2,
                },
            },
            "created_at": "2016-07-12T03:45:18.3335556",
            "is_public": True,
            "forked_from": None,
            "comments_count": 10,
            "reactions_counts": {"dancer": 7, "confused": 1},
        },
    ])

