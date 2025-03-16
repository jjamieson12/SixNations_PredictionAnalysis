#[Path_to_marker.png, printing_scale]
player_markers = {
    "player1":["Assets/MarkerPlayer1.png",0.15],
    "player2":["Assets/MarkerPlayer2.png",0.15],
    "player3":["Assets/MarkerPlayer3.png",0.15],
}

nation_markers = {
    "Scotland":r"🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "England":r"🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Wales":r"🏴󠁧󠁢󠁷󠁬󠁳󠁿",
    "Italy":r"🇮🇹",
    "Ireland":r"🇮🇪",
    "France":r"🇫🇷",
}

#There's almost certainly a better way to input predictions...
#WARNING: do not use player name: "Average"
predictions_wk1 = {
    "player1":{
        ("France","Ireland"):(25,32),
        ("Italy","England"):(21,20),
        ("Wales","Scotland"):(31,10),
    },
    "player2":{
        ("France","Ireland"):(15,40),
        ("Italy","England"):(24,28),
        ("Wales","Scotland"):(14,5),
    },
    "player3":{
        ("France","Ireland"):(25,21),
        ("Italy","England"):(27,22),
        ("Wales","Scotland"):(24,5),
    }
}

predictions_wk2 = {
    "player1":{
        ("Scotland","France"):(24,21),
        ("England","Wales"):(28,17),
        ("Ireland","Italy"):(35,10),
    },
    "player2":{
        ("Scotland","France"):(28,14),
        ("England","Wales"):(22,5),
        ("Ireland","Italy"):(24,5),
    },
    "player3":{
        ("Scotland","France"):(22,17),
        ("England","Wales"):(23,26),
        ("Ireland","Italy"):(27,9),
    }
}