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


#Calculate average Try^2 and variances over several predictions with correct normalisation and errors
#do_norm -> Normalise variances and Try^2 seperately
#do_var_err -> Use both (abs) up and down variances for error calculation rather than Try^2 values (double statistics)
def calc_trysq_avg(predictions,FinalScore,win_SF,do_norm,do_var_err):
    variances_up = {}
    variances_down = {}
    try_sq = {}
    variances = {"try_sq":{},"var_up":{},"var_down":{},"error":{}}

    #First get all of the individual variances and Try^2 (Now normalise Try^2 seperately from variance)
    for name,prediction in predictions.items():
        variances_up[name] = []
        variances_down[name] = []
        try_sq[name] = []
        for game, pred in prediction.items():
            var_up = abs(pred[0] - FinalScore[game][0]) #Have to use absolute when averaging or we will get cancellations
            var_down = abs(pred[1] - FinalScore[game][1])
            variances_up[name].append(var_up)
            variances_down[name].append(var_down)
            win_pred = pred[0] - pred[1]
            win_true = FinalScore[game][0] - FinalScore[game][1]
            prediction_SF = win_SF if (np.sign(win_pred) == np.sign(win_true)) else 1
            try_sq[name].append(((var_up+var_down)/2.0) * prediction_SF)

    vartotal_up = [] #To calculate max
    vartotal_down = []
    try_sq_total = []
    for name,pred in variances_up.items():
        mean_absolute_variance_up = np.mean(np.array(pred))
        mean_absolute_variance_down = np.mean(np.array(variances_down[name]))
        mean_try_sq = np.mean(np.array(try_sq[name]))
        variances["var_up"][name] = mean_absolute_variance_up
        vartotal_up.append(mean_absolute_variance_up)
        variances["var_down"][name] = mean_absolute_variance_down
        vartotal_down.append(mean_absolute_variance_down)
        variances["try_sq"][name] = mean_try_sq
        try_sq_total.append(mean_try_sq)

        #Lastly get errors
        #If do_var_err = True, use absolute variances and do standard error on mean
        #If do_var_err = False, use Try^2 values instead  
        combined_vars = try_sq[name]
        if do_var_err:
            combined_vars = pred + variances_up[name]

        std_dev = np.std(np.array(combined_vars), ddof=1)  # Sample standard deviation
        variances["error"][name] = std_dev / np.sqrt(len(combined_vars))

    #Normalise everything if required
    if do_norm:
        var_up_max = max(vartotal_up,key=abs)
        var_down_max = max(vartotal_down,key=abs)
        try_sq_max = max(try_sq_total,key=abs)
        for name in variances["var_up"].keys():
            variances["var_up"][name] *= 1.0/var_up_max
            variances["var_down"][name] *= 1.0/var_down_max
            variances["try_sq"][name] *= 1.0/try_sq_max
            variances["error"][name] *= 1.0/try_sq_max

    #Do ordering by largest Try^2        
    variances["try_sq"] = dict(sorted(variances["try_sq"].items(), key=lambda item: item[1],reverse=True))
    variances["var_up"] = dict(sorted(variances["var_up"].items(), key=lambda t2: variances["try_sq"][t2[0]],reverse=True))
    variances["var_down"] = dict(sorted(variances["var_down"].items(), key=lambda t2: variances["try_sq"][t2[0]],reverse=True))
    variances["error"] = dict(sorted(variances["error"].items(), key=lambda t2: variances["try_sq"][t2[0]],reverse=True))

    return variances


#Calculate goodness-of-prediction metric "Try^2" for each week and combined for the tournament (Lower is better)
#Try^2 = Average_variance * WinSF where winSF is a modifyable parameter to favour picking the correct winner
#Variance_up = Mean absolute variance in home-team predictions
#Variance_down = Mean absolute variance in away-team predictions 
#optionally normalised over largest individual player variance (or Try^2) for each week (ensures values are between 0 and 1)
#Also calculates standard error on the mean for each player's distribution of (normalised) weekly predictions
#Returns variances dictionary containing averaged: Try^2, up variance, down variance, and error for each player
def calc_trysq_weekly(game_info,win_SF=0.9,do_norm=True,do_var_err=True) -> dict:

    variances = {}
    for week,info in game_info.items():
        predictions = info[1]
        FinalScore = info[2]
        variances[week] = calc_trysq_avg(predictions,FinalScore,win_SF,do_norm,do_var_err)

    #Sort the weeks, with "All" last
    variances = dict(sorted(variances.items(), key=lambda wk:wk[0][-1]))
    return variances

def calculate_average_prediction(predictions):
    average_predictions = {}
    is_first = True #Need to get the games first
    for player,preds in predictions.items():
        for game,pred in preds.items():
            if is_first:
                average_predictions[game] = np.array(pred)
            else:
                average_predictions[game] = np.vstack([average_predictions[game],pred])
        is_first = False
    
    predictions["Average"] = {}
    for game,pred in average_predictions.items():
        predictions["Average"][game] = np.mean(pred,axis=0)

def find_best_predictions(finalscores,predictions):
    winners = ["?","?","?"]
    bestpreds = {}
    i = 0
    for game,finalscore in finalscores.items():
        frontrunner = 999
        max_var_front = 999
        for player,prediction in predictions.items():
            var_up = abs(prediction[game][0] - finalscore[0])
            var_down = abs(prediction[game][1] - finalscore[1])
            var = (var_up + var_down)/2.0
            if var < frontrunner:
                winners[i] = player
                bestpreds[game] = prediction[game]
                frontrunner = var
                max_var_front = max(var_up,var_down)
            elif var == frontrunner:
                #For equal scores pick the one with the smallest larger variance
                max_var = max(var_up,var_down)
                if max_var < max_var_front:
                    winners[i] = player
                    bestpreds[game] = prediction[game]
                    frontrunner = var
                    max_var_front = max_var
        i+=1
    return winners,bestpreds

def final_score_to_string(finalscores,game_number):

    x = game_number-1
    scorestring = "{} {} -- {} {}".format(list(finalscores.keys())[x][0],
                                          list(finalscores.values())[x][0],
                                          list(finalscores.values())[x][1],
                                          list(finalscores.keys())[x][1])
    return scorestring

def GetWinDrawLosses(nation,games,predictions,mode="weekly"):
    n_win = []
    n_draw = []
    n_loss = []
    nation_games = [] #Assume input is all games and pick out only those the given nation plays in
    for game in games:
        if nation in game:
            nation_games.append(game)
    for x,week_game in enumerate(nation_games):
        if x == 0:
            n_win.append(0)
            n_draw.append(0)
            n_loss.append(0)
        else:
            if mode=="cumulative":
                n_win.append(n_win[x-1])
                n_draw.append(n_draw[x-1])
                n_loss.append(n_loss[x-1])
            else:
                n_win.append(0)
                n_draw.append(0)
                n_loss.append(0)
        index = week_game.index(nation)
        for player, prediction in predictions.items():
            if player == "Average":
                continue
            if week_game not in prediction.keys():
                continue
            if prediction[week_game][index] > prediction[week_game][1-index]:
                n_win[x] += 1
            elif prediction[week_game][index] == prediction[week_game][1-index]:
                n_draw[x] += 1
            else:
                n_loss[x] += 1
    #if total requested just return single values for number of wins,draw, and losses over whole tournament                 
    if mode=="Total":
        n_win = np.sum(n_win)
        n_draw = np.sum(n_draw)
        n_loss = np.sum(n_loss)

    return n_win, n_draw, n_loss


def GetCumulativeBias(nations,games,predictions,FinalScores,metric="skew",predictwin_SF=1.2):
    #For each team calculate relative bias and under/overestimation for each player cumulatively as predictions come in
    #For metric = variance: 
    #   bias = cumulative difference in score predictions vs the average prediction for given nation, n: (predicted_n - average_n)
    #   overunder = cumulative difference in score predictions vs the true results for given nation, n: (predicted_n - true_n)
    #for metric = skew 
    #   bias = cumulative value of: (predicted_n - average_n)  - (predicted_o - average_o) * (N_preddiff/N_predsame) * predictwin_SF
    #   overunder = cumulative value of: (prediction_n/(prediction_n+prediction_o))*100.0 - (true_n/(true_n+true_o))*100.0, 
    #   where _n indicates the score for the given nation, and _o indicates the score for their opponent in each match

    cumulative_bias = {}
    cumulative_overunder = {}
    total_bias = {}
    total_overunder = {}

    for n in nations:
        cumulative_bias[n] = {}
        cumulative_overunder[n] = {}
        total_bias[n] = {}
        total_overunder[n] = {}
        n_win = []
        n_draw = []
        n_loss = []
        nation_games = []
        for game in games:
            if n in game:
                nation_games.append(game)
        #If we are doing the skew metric then calculate how many draws, wins and losses total
        if metric == "skew":
            n_win, n_draw, n_loss = GetWinDrawLosses(n,games,predictions,mode="cumulative")

        for x,week_game in enumerate(nation_games):
            index = week_game.index(n)
            FinalScore = FinalScores[week_game][index]
            Average = predictions["Average"][week_game][index]
            FinalScore_oth = FinalScores[week_game][1-index]
            Average_oth = predictions["Average"][week_game][1-index]
            percent_finalscore = (FinalScore/(FinalScore+FinalScore_oth))*100.0

            for player, prediction in predictions.items():
                if player == "Average":
                    continue
                if player not in total_bias[n].keys():
                    total_bias[n][player] = []
                    total_overunder[n][player] = []
                    cumulative_bias[n][player] = []
                    cumulative_overunder[n][player] = []
                if week_game not in prediction.keys():
                    continue #If player hasn't made prediction for game just skip and cumulative bias will reflect this
                bias = prediction[week_game][index] - Average
                overunder = prediction[week_game][index] - FinalScore
                #Skew metric is more complex
                if metric == "skew":
                    diffoversame = 1.0
                    predictwin = 1.0
                    if prediction[week_game][index] > prediction[week_game][1-index]:
                        diffoversame = (n_draw[x]+n_loss[x])/float(n_win[x])
                        predictwin = predictwin_SF
                    elif prediction[week_game][index] == prediction[week_game][1-index]:
                        #Draw predictions are rare so shouldn't be penalised too heavily but should increse skew for going against the grain
                        if min(n_win[x],n_loss[x]) == 0:
                            diffoversame = 1.0
                        else:
                            diffoversame = (max(n_win[x],n_loss[x]) + n_draw[x])/float(min(n_win[x],n_loss[x]))
                            predictwin = predictwin_SF*-1.0
                    else:
                        diffoversame = (n_draw[x]+n_win[x])/float(n_loss[x])
                    if diffoversame == 0:
                        diffoversame = 0.5 #If everyone predicts in the same direction limit the skew
                    bias = (bias - (prediction[week_game][1-index] - Average_oth)) * diffoversame * predictwin
                    overunder = (prediction[week_game][index]/(prediction[week_game][index]+prediction[week_game][1-index]))*100.0 - percent_finalscore
                    #overunder = (overunder - (prediction[week_game][1-index] - FinalScore_oth)) #Alternative simpler overunder but I think percentage is better

                #Keep track of the total bias as we add weeks to get the cumulative results
                total_bias[n][player].append(bias) 
                total_overunder[n][player].append(overunder)
            
            for player,bias in total_bias[n].items():
                if len(total_bias[n][player]) == 0:
                    cumulative_bias[n][player].append(0)
                    cumulative_overunder[n][player].append(0)
                else:
                    cumulative_bias[n][player].append(np.mean(total_bias[n][player]))
                    cumulative_overunder[n][player].append(np.mean(total_overunder[n][player]))

    return cumulative_bias, cumulative_overunder

def GetNorm_cumulative_bias(biases,overunders):
    norm_bias = []
    norm_overunder = []
    n_weeks = 0
    for player, bias_set in biases.items():
        n_weeks = len(bias_set)
        break #a bit clunky but works

    for cumul in range(n_weeks):
        all_bias = []
        all_overunder = []
        for player, bias_set in biases.items():
            all_bias.append(abs(bias_set[cumul]))
            all_overunder.append(abs(overunders[player][cumul]))
        norm_bias.append(np.max(all_bias))
        norm_overunder.append(np.max(all_overunder))

    return norm_bias, norm_overunder

