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



