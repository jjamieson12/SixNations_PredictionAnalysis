from string import Template
from PredictionData.Predictions2025 import *
from Scripts.AnalysisScripts import find_best_predictions, final_score_to_string

weeks = [1,2,3,4,5]

finalscores = [{
    ("France","Wales"):(43,0),
    ("Scotland","Italy"):(31,19),
    ("Ireland","England"):(27,22),
},
{
    ("Italy","Wales"):(22,15),
    ("England","France"):(26,25),
    ("Scotland","Ireland"):(18,32),
},
{
    ("Wales","Ireland"):(18,27),
    ("England","Scotland"):(16,15),
    ("Italy","France"):(24,73),
},
{
    ("Ireland","France"):(27,42),
    ("Scotland","Wales"):(35,29),
    ("England","Italy"):(47,24),
},
{
    ("Italy","Ireland"):( 17,22 ),
    ("Wales","England"):( 14,68 ),
    ("France","Scotland"):( 35,16 ),
}
]
predictions = [predictions_wk1,
               predictions_wk2,
               predictions_wk3,
               predictions_wk4,
               predictions_wk5,

]

# Define the input (template) and output file names
game_template_file = "./docs/Templates/template_week_game.html"
ranking_template_file = "./docs/Templates/template_week_ranking.html"

game_output_file = "./docs/weekXXX_game.html"
ranking_output_file = "./docs/weekXXX_ranking.html"


# Read the template files
with open(game_template_file, "r", encoding="utf-8") as gfile:
    gamecontent = gfile.read()
with open(ranking_template_file, "r", encoding="utf-8") as rfile:
    rankingcontent = rfile.read()

# Define the replacement values
repl = {}

for week in weeks:
    gametemplate = Template(gamecontent)
    rankingtemplate = Template(rankingcontent)
    repl["WEEK"] = str(week)
    repl["FINALSCORE1"] = final_score_to_string(finalscores[week-1],1)
    repl["FINALSCORE2"] = final_score_to_string(finalscores[week-1],2)
    repl["FINALSCORE3"] = final_score_to_string(finalscores[week-1],3)

    names, bestpreds = find_best_predictions(finalscores[week-1],predictions[week-1])
    repl["BESTPRED1"] = final_score_to_string(bestpreds,1)
    repl["BESTPRED2"] = final_score_to_string(bestpreds,2)
    repl["BESTPRED3"] = final_score_to_string(bestpreds,3)
    
    repl["WINNER1"] = names[0]
    repl["WINNER2"] = names[1]
    repl["WINNER3"] = names[2]

    game_html = gametemplate.substitute(repl)
    ranking_html = rankingtemplate.substitute(repl)

    # Save the modified content to a new file
    with open(game_output_file.replace("XXX",str(week)), "w", encoding="utf-8") as gfile:
        gfile.write(game_html)
    with open(ranking_output_file.replace("XXX",str(week)), "w", encoding="utf-8") as rfile:
        rfile.write(ranking_html)

    print("Generated files for week {}".format(week))


