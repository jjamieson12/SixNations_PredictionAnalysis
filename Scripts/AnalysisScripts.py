import numpy as np

#Calculate goodness-of-prediction metric "Try^2" (Lower is better)
#Try^2 = Average_variance * WinSF where winSF is a modifyable parameter to favour picking the correct winner
#optionally normalised over largest individual player variance (ensures values are between 0 and 1)
#Also return up,down,combined,and average variances for each player for each game (needed for ranking plot)
def calc_trysq(games,predictions,FinalScore,win_SF=0.9,do_norm=True) -> dict:
    variances_up = {}
    variances_down = {}
    variances_comb = {}
    variances = {"up":{},"down":{},"combined":{},"average":{}}
    try_sq = {}
    overall_try_sq = {}
    for game_number,game in enumerate(games):
        vartotal_up = []
        vartotal_down = []
        vartotal_comb = []
        try_sq[game] = {}
        for name,prediction in predictions.items():
            if game_number == 0:
                variances_up[name] = {}
                variances_down[name] = {}
                variances_comb[name] = {}
                overall_try_sq[name] = 0
            if game not in prediction.keys(): continue
            vartotal_up.append(prediction[game][0] - FinalScore[game][0])
            vartotal_down.append(prediction[game][1] - FinalScore[game][1])
            vartotal_comb.append(abs(prediction[game][0] - FinalScore[game][0]))
            vartotal_comb.append(abs(prediction[game][1] - FinalScore[game][1]))
        var_up_max = abs(max(vartotal_up,key=abs))
        var_down_max = abs(max(vartotal_down,key=abs))
        avg_var = np.mean(vartotal_comb)
        variances["average"][game] = avg_var
        for name,prediction in predictions.items():
            if game not in prediction.keys(): continue
            var_up = (prediction[game][0] - FinalScore[game][0])
            var_down = (prediction[game][1] - FinalScore[game][1])
            if do_norm:
                var_up = var_up*1.0/var_up_max
                var_down = var_down*1.0/var_down_max
            var_comb = (abs(var_up) + abs(var_down))/2.0
            variances_up[name][game] = var_up
            variances_down[name][game] = var_down
            variances_comb[name][game] = var_comb
            win_pred = prediction[game][0] - prediction[game][1]
            win_true = FinalScore[game][0] - FinalScore[game][1]
            prediction_SF = win_SF if (np.sign(win_pred) == np.sign(win_true)) else 1
            try_sq[game][name] = ((abs(var_up) + abs(var_down))/2.0) * prediction_SF
            #overall_try_sq[name] += (((abs(var_up) + abs(var_down))/2.0) * prediction_SF)/len(games)
            overall_try_sq[name] += (((abs(var_up) + abs(var_down))/2.0) * prediction_SF)/len(prediction.keys())
        try_sq[game] = dict(sorted(try_sq[game].items(), key=lambda item: item[1],reverse=True))
    overall_trySQ = dict(sorted(overall_try_sq.items(), key=lambda item: item[1],reverse=True))
    try_sq["combined"] = overall_trySQ
    variances["up"] = variances_up
    variances["down"] = variances_down
    variances["combined"] = variances_comb
    return try_sq,variances