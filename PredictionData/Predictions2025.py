#[Path_to_marker.png, printing_scale]
player_markers = {
    "Fan":["Assets/Fan_marker.png",0.04],
    "Eels":["Assets/Eelliot_marker.png",0.04],
    "JJ":["Assets/JJ_marker.png",0.04],
    "Dylan":["Assets/Dylan_marker.png",0.04],
    "Rory":["Assets/Rory_marker.png",0.04],
    "Dave":["Assets/Dave_marker.png",0.04],
    "Harriet":["Assets/Harriet_marker.png",0.04],
    "Parisa":["Assets/Parisa_marker.png",0.04],
    "Giuseppe":["Assets/Giuseppe_marker.png",0.04],
    "Anna":["Assets/Anna_marker.png",0.04],
    "Katie":["Assets/Katie_marker.png",0.04],
    "Veera":["Assets/Veera_marker.png",0.035],
    "Jay":["Assets/Jay_marker.png",0.04],
    "Paul":["Assets/Paul_marker.png",0.04],
    "Martin":["Assets/Martin_marker.png",0.04],
    "Deepstate":["Assets/Deepstate_marker.png",0.04],
    "Chatgpt":["Assets/Chatgpt_marker.png",0.03],
    "2024":["Assets/2024_marker.png",0.03],
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
    "Fan":{
        ("France","Wales"):( 32,10 ),
        ("Scotland","Italy"):( 24,22 ),
        ("Ireland","England"):( 21,17 ),
    },
    "Eels":{
        ("France","Wales"):( 35,15 ),
        ("Scotland","Italy"):( 25,7 ),
        ("Ireland","England"):( 25,21 ),
    },
    "JJ":{
        ("France","Wales"):( 39,20 ),
        ("Scotland","Italy"):( 27,17 ),
        ("Ireland","England"):( 30,27 ),
    },
    "Dylan":{
        ("France","Wales"):( 43,26 ),
        ("Scotland","Italy"):( 34,10 ),
        ("Ireland","England"):( 31,35 ),
    },
    "Rory":{
        ("France","Wales"):( 28,17 ),
        ("Scotland","Italy"):( 29,7 ),
        ("Ireland","England"):( 26,15 ),
    },
    "Dave":{
        ("France","Wales"):( 35,17 ),
        ("Scotland","Italy"):( 28,10 ),
        ("Ireland","England"):( 38,28 ),
    },
    "Harriet":{
        ("France","Wales"):( 28,13 ),
        ("Scotland","Italy"):( 26,12 ),
        ("Ireland","England"):( 34,27 ),
    },
    "Parisa":{
        ("France","Wales"):( 22,35 ),
        ("Scotland","Italy"):( 17,20 ),
        ("Ireland","England"):( 42,18 ),
    },
    "Giuseppe":{
        ("France","Wales"):( 33,10 ),
        ("Scotland","Italy"):( 27,7 ),
        ("Ireland","England"):( 25,20 ),
    },
    "Anna":{
        ("France","Wales"):( 44,25 ),
        ("Scotland","Italy"):( 33,28 ),
        ("Ireland","England"):( 35,31 ),
    },
    "Katie":{
        ("France","Wales"):( 20,22 ),
        ("Scotland","Italy"):( 32,6 ),
        ("Ireland","England"):( 22,15 ),
    },
    "Veera":{
        ("France","Wales"):( 35,17 ),
        ("Scotland","Italy"):( 45,10 ),
        ("Ireland","England"):( 33,28 ),
    },
    "Jay":{
        ("France","Wales"):( 11,28 ),
        ("Scotland","Italy"):( 59,17 ),
        ("Ireland","England"):( 32,13 ),
    },
    "Paul":{
        ("France","Wales"):( 17,15 ),
        ("Scotland","Italy"):( 30,12 ),
        ("Ireland","England"):( 22,28 ),
    },
    "Martin":{
        ("France","Wales"):( 22,17 ),
        ("Scotland","Italy"):( 28,17 ),
        ("Ireland","England"):( 30,25 ),
    },
    "Deepstate":{
        ("France","Wales"):( 32,18 ),
        ("Scotland","Italy"):( 30,20 ),
        ("Ireland","England"):( 26,16 ),
    },
    "Chatgpt":{
        ("France","Wales"):( 32,15 ),
        ("Scotland","Italy"):( 28,18 ),
        ("Ireland","England"):( 27,16 ),
    },
    "2024":{
        ("France","Wales"):( 45,24 ),
        ("Scotland","Italy"):( 29,31 ),
        ("Ireland","England"):( 22,23 ),
    },
}

predictions_wk2 = {
    "Fan":{
        ("Italy","Wales"):( 32,13 ),
        ("England","France"):( 21,28 ),
        ("Scotland","Ireland"):( 24,24 ),
    },
    "Eels":{
        ("Italy","Wales"):( 17,7 ),
        ("England","France"):( 21,28 ),
        ("Scotland","Ireland"):( 24,24 ),
    },
    "JJ":{
        ("Italy","Wales"):( 25,15 ),
        ("England","France"):( 26,33 ),
        ("Scotland","Ireland"):( 16,38 ),
    },
    "Dylan":{
        ("Italy","Wales"):( 13,5 ),
        ("England","France"):( 28,26 ),
        ("Scotland","Ireland"):( 20,39 ),
    },
    "Rory":{
        ("Italy","Wales"):( 11,14 ),
        ("England","France"):( 32,23 ),
        ("Scotland","Ireland"):( 18,25 ),
    },
    "Dave":{
        ("Italy","Wales"):( 10,24 ),
        ("England","France"):( 25,23 ),
        ("Scotland","Ireland"):( 14,32 ),
    },
    "Harriet":{
        ("Italy","Wales"):( 24,16 ),
        ("England","France"):( 27,31 ),
        ("Scotland","Ireland"):( 24,27 ),
    },
    "Parisa":{
        ("Italy","Wales"):( 12,9 ),
        ("England","France"):( 23,20 ),
        ("Scotland","Ireland"):( 25,30 ),
    },
    "Giuseppe":{
        ("Italy","Wales"):( 23,7 ),
        ("England","France"):( 21,28 ),
        ("Scotland","Ireland"):( 19,17 ),
    },
    "Anna":{
        ("Italy","Wales"):( 17,8 ),
        ("England","France"):( 24,30 ),
        ("Scotland","Ireland"):( 22,35 ),
    },
    "Katie":{
        ("Italy","Wales"):( 3,12 ),
        ("England","France"):( 27,22 ),
        ("Scotland","Ireland"):( 30,32 ),
    },
    "Veera":{
        ("Italy","Wales"):( 13,10 ),
        ("England","France"):( 20,25 ),
        ("Scotland","Ireland"):( 23,35 ),
    },
    "Jay":{
        ("Italy","Wales"):( 14,14 ),
        ("England","France"):( 24,29 ),
        ("Scotland","Ireland"):( 16,41 ),
    },
    "Paul":{
        ("Italy","Wales"):( 19,6 ),
        ("England","France"):( 15,32 ),
        ("Scotland","Ireland"):( 19,38 ),
    },
    "Martin":{
        ("Italy","Wales"):( 14,17 ),
        ("England","France"):( 19,28 ),
        ("Scotland","Ireland"):( 21,24 ),
    },
    "Deepstate":{
        ("Italy","Wales"):( 15,25 ),
        ("England","France"):( 20,24 ),
        ("Scotland","Ireland"):( 18,28 ),
    },
    "Chatgpt":{
        ("Italy","Wales"):( 20,25 ),
        ("England","France"):( 18,24 ),
        ("Scotland","Ireland"):( 22,28 ),
    },
    "2024":{
        ("Italy","Wales"):(24,21 ),
        ("England","France"):( 31,33 ),
        ("Scotland","Ireland"):( 13,17 ),
    },
}


predictions_wk3 = {
    "Fan":{
        ("Wales","Ireland"):( 7,38 ),
        ("England","Scotland"):( 22,24 ),
        ("Italy","France"):( 15,35 ),
    },
    "Eels":{
        ("Wales","Ireland"):( 0,40 ),
        ("England","Scotland"):( 28,21 ),
        ("Italy","France"):( 12,25 ),
    },
    "JJ":{
        ("Wales","Ireland"):( 8,36 ),
        ("England","Scotland"):( 24,26 ),
        ("Italy","France"):( 18,21 ),
    },
    "Dylan":{
        ("Wales","Ireland"):( 5,38 ),
        ("England","Scotland"):( 30,28 ),
        ("Italy","France"):( 7,25 ),
    },
    "Rory":{
        ("Wales","Ireland"):( 6,53 ),
        ("England","Scotland"):( 32,21 ),
        ("Italy","France"):( 5,18 ),
    },
    "Dave":{
        ("Wales","Ireland"):( 10,47 ),
        ("England","Scotland"):( 28,21 ),
        ("Italy","France"):( 14,46 ),
    },
    "Harriet":{
        ("Wales","Ireland"):(7,33 ),
        ("England","Scotland"):( 23,29 ),
        ("Italy","France"):( 10,37 ),
    },
    "Parisa":{
        ("Wales","Ireland"):( 15,28 ),
        ("England","Scotland"):( 12,20 ),
        ("Italy","France"):( 17,30 ),
    },
    "Giuseppe":{
        ("Wales","Ireland"):( 10,45 ),
        ("England","Scotland"):( 22,25 ),
        ("Italy","France"):( 14,25 ),
    },
    "Anna":{
        ("Wales","Ireland"):( 0,38 ),
        ("England","Scotland"):( 30,21 ),
        ("Italy","France"):( 12,28 ),
    },
    "Katie":{
        ("Wales","Ireland"):( 12,9 ),
        ("England","Scotland"):( 20,22 ),
        ("Italy","France"):( 3,39 ),
    },
    "Veera":{
        ("Wales","Ireland"):( 5,36 ),
        ("England","Scotland"):( 26,22 ),
        ("Italy","France"):( 10,38 ),
    },
    "Jay":{
        ("Wales","Ireland"):( 7,39 ),
        ("England","Scotland"):( 34,22 ),
        ("Italy","France"):( 13,31 ),
    },
    "Paul":{
        ("Wales","Ireland"):( 3,38 ),
        ("England","Scotland"):( 15,25 ),
        ("Italy","France"):( 9,30 ),
    },
    "Martin":{
        ("Wales","Ireland"):( 5,34 ),
        ("England","Scotland"):( 27,29 ),
        ("Italy","France"):( 12,31 ),
    },
    "Deepstate":{
        ("Wales","Ireland"):( 16,30 ),
        ("England","Scotland"):( 20,23 ),
        ("Italy","France"):( 12,35 ),
    },
    "Chatgpt":{
        ("Wales","Ireland"):( 10,32 ),
        ("England","Scotland"):( 24,18 ),
        ("Italy","France"):( 15,38 ),
    },
    "2024":{
        ("Wales","Ireland"):( 7,31 ),
        ("England","Scotland"):( 21,30 ),
        ("Italy","France"):( 13,13 ),
    },
}

predictions_wk4 = {
    "Fan":{
        ("Ireland","France"):( 25,28 ),
        ("Scotland","Wales"):( 33,27 ),
        ("England","Italy"):( 31,19 ),
    },
    "Eels":{
        ("Ireland","France"):( 25,21 ),
        ("Scotland","Wales"):( 21,18 ),
        ("England","Italy"):( 30,15 ),
    },
    "JJ":{
        ("Ireland","France"):( 41,26 ),
        ("Scotland","Wales"):( 32,17 ),
        ("England","Italy"):( 30,22 ),
    },
    "Dylan":{
        ("Ireland","France"):( 28,31 ),
        ("Scotland","Wales"):( 24,12 ),
        ("England","Italy"):( 28,15 ),
    },
    "Rory":{
        ("Ireland","France"):( 28,19 ),
        ("Scotland","Wales"):( 32,23 ),
        ("England","Italy"):( 43,17 ),
    },
    "Dave":{
        ("Ireland","France"):( 28,7 ),
        ("Scotland","Wales"):( 28,7 ),
        ("England","Italy"):( 28,7 ),
    },
    "Harriet":{
        ("Ireland","France"):(36,24 ),
        ("Scotland","Wales"):( 25,21 ),
        ("England","Italy"):( 31,18 ),
    },
    "Parisa":{
        ("Ireland","France"):( 26,28 ),
        ("Scotland","Wales"):( 22,18 ),
        ("England","Italy"):( 25,20 ),
    },
    "Giuseppe":{
        ("Ireland","France"):( 21,17 ),
        ("Scotland","Wales"):( 25,12 ),
        ("England","Italy"):( 31,15 ),
    },
    "Anna":{
        ("Ireland","France"):( 27,25 ),
        ("Scotland","Wales"):( 34,28 ),
        ("England","Italy"):( 30,16 ),
    },
    "Katie":{
        ("Ireland","France"):( 22,20 ),
        ("Scotland","Wales"):( 13,17 ),
        ("England","Italy"):( 19,15 ),
    },
    "Jay":{
        ("Ireland","France"):( 32,35 ),
        ("Scotland","Wales"):( 19,20 ),
        ("England","Italy"):( 41,17 ),
    },
    "Paul":{
        ("Ireland","France"):( 30,20 ),
        ("Scotland","Wales"):( 21,5 ),
        ("England","Italy"):( 30,10 ),
    },
    "Martin":{
        ("Ireland","France"):( 27,36 ),
        ("Scotland","Wales"):( 13,13 ),
        ("England","Italy"):( 28,19 ),
    },
    "Deepstate":{
        ("Ireland","France"):( 24,20 ),
        ("Scotland","Wales"):( 28,17 ),
        ("England","Italy"):( 35,10 ),
    },
    "Chatgpt":{
        ("Ireland","France"):( 28,23 ),
        ("Scotland","Wales"):( 35,18 ),
        ("England","Italy"):( 40,21 ),
    },
    "2024":{
        ("Ireland","France"):( 38,17 ),
        ("Scotland","Wales"):( 27,26 ),
        ("England","Italy"):( 27,24 ),
    },
}

predictions_wk5 = {
    "Fan":{
        ("Italy","Ireland"):( 24,41 ),
        ("Wales","England"):( 14,34 ),
        ("France","Scotland"):( 38,28 ),
    },
    "Eels":{
        ("Italy","Ireland"):( 20,42 ),
        ("Wales","England"):( 9,37 ),
        ("France","Scotland"):( 28,32 ),
    },
    "JJ":{
        ("Italy","Ireland"):( 18,32 ),
        ("Wales","England"):( 16,36 ),
        ("France","Scotland"):( 30,18 ),
    },
    "Dylan":{
        ("Italy","Ireland"):( 12,36 ),
        ("Wales","England"):( 12,36 ),
        ("France","Scotland"):( 28,28 ),
    },
    "Rory":{
        ("Italy","Ireland"):( 14,40 ),
        ("Wales","England"):( 18,37 ),
        ("France","Scotland"):( 37,22 ),
    },
    "Dave":{
        ("Italy","Ireland"):( 14,38 ),
        ("Wales","England"):( 14,25 ),
        ("France","Scotland"):( 40,14 ),
    },
    "Harriet":{
        ("Italy","Ireland"):( 5,45 ), #Forgot to predict, as punishment gets worst prediction for each team
        ("Wales","England"):( 21,32 ),
        ("France","Scotland"):( 18,26 ),
    },
    "Parisa":{
        ("Italy","Ireland"):( 12,27 ),
        ("Wales","England"):( 10,20 ),
        ("France","Scotland"):( 24,15 ),
    },
    "Giuseppe":{
        ("Italy","Ireland"):( 10,45 ),
        ("Wales","England"):( 17,34 ),
        ("France","Scotland"):( 21,17 ),
    },
    "Anna":{
        ("Italy","Ireland"):( 22,40 ),
        ("Wales","England"):( 12,37 ),
        ("France","Scotland"):( 30,20 ),
    },
    "Katie":{
        ("Italy","Ireland"):( 9,22 ),
        ("Wales","England"):( 14,12 ),
        ("France","Scotland"):( 28,29 ),
    },
    "Veera":{
        ("Italy","Ireland"):( 15,33 ),
        ("Wales","England"):( 5,24 ),
        ("France","Scotland"):( 38,16 ),
    },
    "Jay":{
        ("Italy","Ireland"):( 20,34 ),
        ("Wales","England"):( 13,34 ),
        ("France","Scotland"):( 29,28 ),
    },
    "Paul":{
        ("Italy","Ireland"):( 5,40 ),
        ("Wales","England"):( 10,30 ),
        ("France","Scotland"):( 30,22 ),
    },
    "Martin":{
        ("Italy","Ireland"):( 13,28 ),
        ("Wales","England"):( 7,26 ),
        ("France","Scotland"):( 33,24 ),
    },
    "Deepstate":{
        ("Italy","Ireland"):( 10,30 ),
        ("Wales","England"):( 16,22 ),
        ("France","Scotland"):( 27,15 ),
    },
    "Chatgpt":{
        ("Italy","Ireland"):( 13,34 ),
        ("Wales","England"):( 18,27 ),
        ("France","Scotland"):( 23,20 ),
    },
    "2024":{
        ("Italy","Ireland"):( 0,36 ),
        ("Wales","England"):( 14,16 ),
        ("France","Scotland"):( 20,16 ),
    },
}

