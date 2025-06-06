from matplotlib import pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Circle, Rectangle, Patch
from matplotlib.lines import Line2D
from matplotlib.transforms import Bbox
import matplotlib.ticker as mticker
from .AnalysisScripts import calc_trysq, GetNorm_cumulative_bias
from math import sqrt, atan, degrees
from imojify import imojify


#Replace marker with scaled png (from: https://stackoverflow.com/a/22570069)
def imscatter(x, y, image, ax=None, zoom=1, opacity=1,drawemoji=False):
    if ax is None:
        ax = plt.gca()
    try:
        if drawemoji:
            image = plt.imread(imojify.get_img_path(image))
        else:
            image = plt.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = OffsetImage(image, zoom=zoom, alpha=opacity)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists

#Draw 1,2,3 sigma expected limits as circle matplotlib patches 
def makepatches(score):
    threepoint_confidence = Circle(score,3,
                                   facecolor=(30/255.0,190/255.0,255/255.0),alpha=0.95,
                                   edgecolor=("black"),linewidth=1, linestyle=(0,(5,6))
                                  )
    try_confidence =        Circle(score,7,
                                   facecolor=(30/255.0,255/255.0,4/255.0),alpha=1,
                                   edgecolor=("black"),linewidth=1, linestyle=(0,(5,6))
                                  )
    twotry_confidence =     Circle(score,14,
                                   facecolor=(254/255.0,240/255.0,0.0),alpha=1,
                                   edgecolor=("black"),linewidth=1, linestyle=(0,(5,6))                               
                                  )
    return ([threepoint_confidence,try_confidence,twotry_confidence],["$\pm$ 3-point expected","$\pm$ 1-try expected","$\pm$ 2-try expected"])

#Masively overcomplicated way to get coordinates for printing text around skewed line (works 90% of the time, every time)
def get_text_coords(y_wins,start_p,x_ext,y_ext,x_skew):
    text_x = {}
    text_y = {}
    if y_wins:
        text_x["Correct"] = start_p+(0.1*x_ext) # No skew just plot coords
        text_y["Correct"] = text_x["Correct"]+(0.03*y_ext*x_skew) # Add a bit more above/below the line if highly skewed
        text_x["Incorrect"] = start_p+(0.13*x_ext) # No skew just plot coords
        text_y["Incorrect"] = text_x["Incorrect"]-(0.03*y_ext*x_skew) # Add a bit more above/below the line if highly skewed
    else:
        text_x["Correct"] = start_p+(0.12*x_ext) # No skew just plot coords
        text_y["Correct"] = text_x["Correct"]-(0.03*y_ext*x_skew)
        text_x["Incorrect"] = start_p+(0.085*x_ext) # No skew just plot coords
        text_y["Incorrect"] = text_x["Incorrect"]+(0.03*y_ext*x_skew)
    return text_x, text_y

#Determine bboxes to crop individual figures out of subplots
#bottom,top,left,right,wspace are default subplot params from: https://matplotlib.org/stable/users/explain/customizing.html#matplotlibrc-sample:~:text=show()%20is%20called.-,%23%23,-The%20figure%20subplot
#Currently no treatment of multi-row subplots
def get_fig_crops(n_figs,fig_x,fig_y,x_label=True,y_label=False,x_pad=0.015,y_pad=0.035,bottom=0.11,top=0.88,left=0.125,right=0.9,wspace=0.2,axis_pad=0.05):

    LRpadding = x_pad*fig_x
    UDpadding = y_pad*fig_y
    wspace_abs = (((fig_x*right) - (fig_x*left) - 2*axis_pad*fig_x)/n_figs)*wspace
    one_fig_width = ((fig_x*right) - (fig_x*left) - ((n_figs-1)*wspace_abs))/n_figs
    x_label_extra = 0
    y_label_extra = 0
    if x_label:
        y_label_extra = fig_y*0.035
    if y_label:
        x_label_extra = fig_x*0.015


    custom_crops = []
    for i in range(n_figs):
        custom_crop = Bbox(np.array([[fig_x*left+(i*(one_fig_width+wspace_abs))-LRpadding-x_label_extra, fig_y*bottom-UDpadding-y_label_extra],
                                     [fig_x*left+((i+1)*one_fig_width)+(i*wspace_abs)+LRpadding, fig_y*top+UDpadding]])) 
        custom_crops.append(custom_crop)

    return custom_crops

#Lambda for matplotlib.ticker, replace negative tick labels with blank spaces
def remove_negative_tick_labels(x, pos):
    if x < 0:
        return ''
    else:
        return x

#Draw lines indicating where correct/incorrect winner+loser predictions lie in score plot
#Angle for line text is complicated as both the x,y ranges and canvas height,width are asymmetric
#This was my best attempt to make it work most of the time
def draw_winloss_line(ax,y_wins,is_draw):
    start_p = max([ax.get_xlim()[0],ax.get_ylim()[0]]) #Max of lower left points
    end_p = min([ax.get_xlim()[1],ax.get_ylim()[1]]) #Min of upper right points
    cols = ['green','red']
    if y_wins:
        cols = ['red','green']
    if is_draw:
        cols = ['black','black']
    ax.axline((start_p,start_p-0.15),(end_p,end_p-0.15), linestyle='-', linewidth=3, color=cols[0], alpha=1)
    ax.axline((start_p,start_p+0.15),(end_p,end_p+0.15), linestyle='-', linewidth=3, color=cols[1], alpha=1)
    x_ext = ax.get_xlim()[1] - ax.get_xlim()[0]
    y_ext = ax.get_ylim()[1] - ax.get_ylim()[0]
    ax_ratio = x_ext/y_ext
    x_skew = max(ax_ratio,1) #Skew is calculated relative to the smaller axis range
    y_skew = max(1/ax_ratio,1)
    grad_skew = max(y_skew,x_skew)/min(y_skew,x_skew)

    angle = 45+(degrees(atan(grad_skew-1))/2.0)
    if y_wins:
        angle = 45-(degrees(atan(1-(1/grad_skew)))/2.0)
        angle *= 1.09 #Fudge as the canvas is not a perfect square

    text_x,text_y = get_text_coords(y_wins,start_p,x_ext,y_ext,x_skew)
    if not is_draw:
        ax.text(text_x["Correct"],text_y["Correct"],"Correct winner",rotation=angle,size=15, color='green',horizontalalignment='center',verticalalignment='center')
        ax.text(text_x["Incorrect"],text_y["Incorrect"],"Incorrect winner",rotation=angle,size=15, color='red',horizontalalignment='center',verticalalignment='center')



#Make 2D score prediction plot for each game
#Options:
#axs -> N suplots, one for each match
#games -> List of tuples for the teams in each game: ("home_team","away_team")
#predictions -> Dictionary mapping player_name to {game:prediction}
#markers -> Dictionary mapping player_name to marker image
#FinalScore -> Final scores for each match (Optional)
#Nexpected -> How many expected limit areas to plot [default=3]
def plot_matches(axs,games,predictions,markers,FinalScore=None,Nexpected=3,show_average=True,show_winloss=True, axis_lims=[-1,-1,-1,-1],offsets=[5,5,5,10]):
    for game_number,ax in enumerate(axs):
        all_x = []
        all_y = []
        game = games[game_number]
        avg_pred = None #instantiating average prediction marker in case its needed
        for name,prediction in predictions.items():
            if name == "Average":
                if show_average:
                    all_x.append(prediction[game][0])
                    all_y.append(prediction[game][1])
                    avg_pred = [prediction[game][0],prediction[game][1]] #Don't draw yet to ensure ordering is correct
            else:
                all_x.append(prediction[game][0])
                all_y.append(prediction[game][1])
                ax.scatter(prediction[game][0],prediction[game][1], 0)
                imscatter(prediction[game][0], prediction[game][1], markers[name][0], zoom=markers[name][1], ax=ax, opacity=1)
        if FinalScore:
            all_x.append(FinalScore[game][0]+14)
            all_x.append(FinalScore[game][0]-14)
            all_y.append(FinalScore[game][1]+14)
            all_y.append(FinalScore[game][1]-14)
        all_pos = all_x + all_y
        if not axis_lims == [-1,-1,-1,-1]:
            ax.set_xlim(axis_lims[0],axis_lims[1])
            ax.set_ylim(axis_lims[2],axis_lims[3])
        else:
            ax.set_xlim([max(0,min(all_x)-offsets[0]),max(all_x)+offsets[1]])
            ax.set_ylim([max(0,min(all_y)-offsets[2]),max(all_y)+offsets[3]])
        ax.tick_params(axis='both', which='major', labelsize=15)
        ax.set_xlabel(game[0]+" (rugbypoints)",size=18,labelpad=15)
        ax.set_ylabel(game[1]+" (rugbypoints)",size=18,labelpad=15)

        if FinalScore:
            patches,labs = makepatches(FinalScore[game])
            for p in reversed(range(Nexpected)): #plot patches in reverse for correct ordering
                ax.add_patch(patches[p])
            fs = ax.scatter(FinalScore[game][0],FinalScore[game][1],500,"red",edgecolors='black',marker="*",zorder=4)
            handles=[fs]
            labels=["Final score"]
            if show_average and not avg_pred == None:
                poc = ax.scatter(avg_pred[0],avg_pred[1],500,"gray",edgecolors='black',marker="*",zorder=3)
                handles.append(poc)
                labels.append("Average prediction")
            for p in range(Nexpected):
                handles.append(patches[p])
                labels.append(labs[p])
            ax.legend(handles=handles,labels=labels,fontsize=16)
            if (show_winloss): #Put line between sigma patches and score markers
                y_wins = FinalScore[game][1] > FinalScore[game][0]
                is_draw = FinalScore[game][1] == FinalScore[game][0]
                draw_winloss_line(ax,y_wins,is_draw)

        elif show_average and not avg_pred == None:
            poc = ax.scatter(avg_pred[0],avg_pred[1],500,"blue",marker="*",zorder=2)
            handles=[poc]
            labels=["Average prediction"]
            ax.legend(handles=handles,labels=labels,fontsize=16)


#Make Try^2 Ranking plot for each game
#Options:
#axs -> N suplots, one for each match
#games -> List of tuples for the teams in each game: ("home_team","away_team")
#predictions -> Dictionary mapping player_name to {game:prediction}
#markers -> Dictionary mapping player_name to marker image
#FinalScore -> Final scores for each match (Optional)
#win_SF -> Float for the extra scale-factor applied to Try^2 if prediction corectly picks winner, 1 if not [default = 0.9]
#week -> Week number for plot title [default = 1]
#draw_markers -> Whether to draw markers for each prediction [default = True]
def plot_ranking(axs,games,predictions,markers,FinalScore,win_SF=0.9,week=1,draw_markers=True,show_average=True,do_norm=True):
    
    try_sq, variances = calc_trysq(games,predictions,FinalScore,win_SF=win_SF,do_norm=do_norm)

    for game_number,ax in enumerate(axs):
        game = games[game_number]

        #Correctly size x-axis if data is not normalised
        max_x = 1.0
        if not do_norm:
            #Find the x limits
            all_x = []
            for name,trySQ in try_sq[game].items():
                if name == "Average" and not show_average:
                    continue
                all_x.append(abs(variances["up"][name][game]))
                all_x.append(abs(variances["down"][name][game]))
                all_x.append(trySQ)
            max_x = max(all_x)
        x_lim = max_x*2

        iter=1
        for name,trySQ in try_sq[game].items():
            if name == "Average" and not show_average:
                continue
            ax.barh(iter+0.05,variances["up"][name][game],height=0.45,color='xkcd:cobalt blue')
            ax.barh(iter-0.05,variances["down"][name][game],height=0.45,color='goldenrod')
            ax.errorbar(trySQ, iter, xerr=1.0/variances["average"][game], fmt="o",color='xkcd:red',ecolor='black',ms=10,lw=4)
            ax.text(max_x*1.2,iter,"Try${}^{2}$ = "+str(round(trySQ,2)),size=15)
            ax.text(max_x*-1.5,iter,str(name),size=15,verticalalignment='center')
            if draw_markers:
                if name == "Average":
                    ax.scatter(max_x*-1.8,iter,1500,"gray",edgecolors='black',marker="*")
                else:
                    imscatter(max_x*-1.8, iter, markers[name][0], zoom=markers[name][1]*0.9, ax=ax, opacity=1)
            iter+=1

        ax.set_xlim(-x_lim,x_lim)
        if do_norm:
            ax.set_xlabel("P-T/max(P-T)",size=15,labelpad=10)
        else:
            ax.set_xlabel("P-T",size=15,labelpad=10)
        ax.tick_params(axis='x', which='major', labelsize=15)
        ax.axvline(0, linestyle='--', color='black', alpha=1)
        ax.axes.get_yaxis().set_visible(False)
        ax.axes.spines[['top','right','left']].set_visible(False)
        ax.set_title("Week {}: {} v {}".format(week,game[0],game[1]),size=22,pad=15)
    print("Combined try^2: ")
    print(try_sq["combined"])

#Reproduce ranking plot but for individual weeks/entire tournament
#Variances are now absolute, mean away team prediction goes to the left, home to the right
def plot_tournament_ranking(axs,weekly_rankings,markers,draw_markers=True,show_average=True,do_norm=False):

    ax_num=0
    for week,rankings in weekly_rankings.items():
        ax = axs[ax_num]
        var_up = rankings["var_up"]
        var_down = rankings["var_down"]
        try_sq = rankings["try_sq"]
        error = rankings["error"]

        #Correctly size x-axis if data is not normalised
        max_x = 1.0
        if not do_norm:
            #Find the x limits
            all_x = []
            for name,trySQ in try_sq.items():
                if name == "Average" and not show_average:
                    continue
                all_x.append(var_up[name])
                all_x.append(var_down[name])
                all_x.append(trySQ)
            max_x = max(all_x)
        x_lim = max_x*2

        iter=1
        for name,trySQ in try_sq.items():
            if name == "Average" and not show_average:
                continue
            ax.barh(iter,var_up[name],height=0.45,color='xkcd:cobalt blue')
            ax.barh(iter,-1*var_down[name],height=0.45,color='goldenrod') #It's an abs value now, make sure it points left
            ax.errorbar(trySQ, iter, xerr=error[name], fmt="o",color='xkcd:red',ecolor='black',ms=15,lw=4)
            ax.text(max_x*1.2,iter,"Mean Try${}^{2}$ = "+str(round(trySQ,2)),size=15)
            ax.text(max_x*-1.5,iter,str(name),size=15,verticalalignment='center')
            if draw_markers:
                if name == "Average":
                    ax.scatter(max_x*-1.8,iter,1500,"gray",edgecolors='black',marker="*")
                else:
                    imscatter(max_x*-1.8, iter, markers[name][0], zoom=markers[name][1]*0.9, ax=ax, opacity=1)
            iter+=1

        ax.set_xlim(-x_lim,x_lim)
        if do_norm:
            ax.set_xlabel(r"Away $\longleftarrow$            |P-T|/max(|P-T|)           $\longrightarrow$ Home",size=15,labelpad=10)
        else:
            ax.set_xlabel(r"Away $\longleftarrow$            |P-T|           $\longrightarrow$ Home",size=15,labelpad=10)
        ax.tick_params(axis='x', which='major', labelsize=15)
        ax.axvline(0, linestyle='--', color='black', alpha=1)
        ax.axes.get_yaxis().set_visible(False)
        ax.axes.spines[['top','right','left']].set_visible(False)
        if week == "All":
            ax.set_title("All games",size=22,pad=15)
        else:
            ax.set_title("Week {}".format(week[-1]),size=22,pad=15)

        ax_num+=1


#Make statistical significance plot for each week and the full tournament
#Options:
#axs -> N suplots, one for each match
#n_toys -> Number of toys thrown to get correct error on average prediction
#game_info -> #game information for all weeks, Shape is: game_info["WeekX"]: [ [list_of_games_as_string_tuple],{predictions_dict},{final_score_dict} ]
#try_sq -> Try^2 values calculated per week, shape is: try_sq["WeekX"]:{'player1': Try^2, 'player2': Try^2,...}
#mean_random -> Dictionary containing mean of all toy Try^2 values for each week
#sigmas -> List of sigma bands calculated from toys
#markers -> Dictionary mapping player_name to marker image
#bottom_pad -> How much space should be below the bottom marker in y-coord space (distance between markers = 1)
#top_pad -> How much extra space should be above the top marker in y-coord space (distance between markers = 1)
#title_pad -> Multiplicative padding factor for title to deal with different numbers of players, totl padding = title_pad*n_players)
def plot_significance(axs,n_toys,game_info,try_sqs,errors,mean_random,sigmas,markers,draw_markers=True,show_average=True,do_norm=True,bottom_pad=0.5,top_pad=0.25,title_pad=2.5):
    ax_num=0
    for week,try_sq in try_sqs.items():
        ax = axs[ax_num]
        avg = mean_random[week]
        oneS = sigmas[0][week]
        twoS = sigmas[1][week]
        threeS = sigmas[2][week]
        
        names_unsorted = game_info[week][1].keys()
        diffs = {}
        for name in names_unsorted:
            diffs[name] = avg-try_sq[name]
        names = sorted(diffs, key=diffs.get)

        max_x = 1.0
        if not do_norm:
            max_x = max(list(try_sq.values())+threeS)
        x_lim = max_x*1.5
        
        n_points = 1
        for name in names:
            if name == "Average" and not show_average: continue
            n_points+=1

        iter=1
        err = (sqrt(n_toys))/n_toys
        rect_1sigma = Rectangle((oneS, 0), 2*(avg-oneS), n_points-1+top_pad, linewidth=0, alpha=0.9, edgecolor='y', facecolor=(254/255.0,240/255.0,0.0))
        rect_2sigma = Rectangle((twoS, 0), 2*(avg-twoS), n_points-1+top_pad, linewidth=0, alpha=0.9, edgecolor='g', facecolor=(30/255.0,255/255.0,4/255.0))
        rect_3sigma = Rectangle((threeS, 0), 2*(avg-threeS), n_points-1+top_pad, linewidth=0, alpha=0.9, edgecolor='b', facecolor=(30/255.0,190/255.0,255/255.0))
        ax.add_patch(rect_3sigma)
        ax.add_patch(rect_2sigma)
        ax.add_patch(rect_1sigma)
        for name in names:
            if name == "Average" and not show_average: continue
            ax.errorbar(try_sq[name], iter, xerr=errors[week][name], fmt="o", color='xkcd:black',ecolor='black',ms=15,lw=4)
            ax.text(max_x*-0.7,iter,str(name),size=15,verticalalignment='center')
            if draw_markers:
                if name == "Average":
                    ax.scatter(max_x*-1.0,iter,1500,"gray",edgecolors='black',marker="*")
                else:
                    imscatter(max_x*-1.0, iter, markers[name][0], zoom=markers[name][1]*0.9, ax=ax, opacity=1)
            iter+=1


        ax.set_xlim(-x_lim,x_lim)
        ax.set_ylim(bottom_pad,n_points)
        if do_norm:
            ax.set_xlabel(r"Try${}^{2}$/max(Try${}^{2}$)",size=15,labelpad=10)
        else:
            ax.set_xlabel(r"Try${}^{2}$",size=15,labelpad=10)
        ax.tick_params(axis='x', which='major', labelsize=15)
        rect_toy_error = Rectangle((avg-err, 0), (2*err), n_points-1+top_pad, linewidth=0, alpha=0.9, edgecolor='grey', fill=False, hatch='/')
        ax.add_patch(rect_toy_error)
        ax.vlines(avg, ymin=0, ymax=n_points-1+top_pad, linestyle='--', lw=1.5, color='black', alpha=1)
        ax.axes.get_yaxis().set_visible(False)
        ax.axes.spines[['top','right','left']].set_visible(False)
        ax.set_title("{}: Significance".format(str(week)),size=22,pad=title_pad*n_points)

        legend_elements = [Line2D([0], [0], color='black', linestyle='--', lw=1.5, label='Avg random'),
                           Patch(facecolor=(254/255.0,240/255.0,0.0), edgecolor='y', linewidth=0, alpha=0.9, label=r'$\pm 1 \sigma$'),
                           Patch(facecolor=(30/255.0,255/255.0,4/255.0), edgecolor='g', linewidth=0, alpha=0.9, label=r'$\pm 2 \sigma$'),
                           Patch(facecolor=(30/255.0,190/255.0,255/255.0), edgecolor='b', linewidth=0, alpha=0.9, label=r'$\pm 3 \sigma$'),
                          ]

        ax.legend(handles=legend_elements, loc=(0.45+(threeS/x_lim),(n_points-1+top_pad)/(n_points)), fontsize=22)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(remove_negative_tick_labels))
        ax_num+=1


#Make plot of total bias and over/underestimation for each player for each team and combine on single plot
#Options:
#axs -> Single suplot, one for each all 6 nations
#cumulative_bias -> Dictionary with cumulative bias calculations for each player for each team (output of GetCumulativeBias)
#cumulative_overunder -> Dictionary with cumulative over/underestimation percentage calculations for each player for each team (output of GetCumulativeBias)
#markers -> Dictionary mapping player_name to marker image
#nation_markers -> Dictionary mapping country name to relevent flag emoji
#bias_metric -> Option for which metric was used for bias calculation (changes the axis labels), options are: "skew" or "variance"
#draw_markers -> Bool to turn on/off custom player markers
#draw_emoji -> Bool to turn on/off flag emoji to label each country's plot, off just prints the name
#plot_settings -> Dictionary of modifiable plot parameters
    # plot_seperation -> Additional Y spacing beytween plot blocks (1 country = 1 block)
    # plot_shift -> Y spacing for the bias and over/under lines from the central plot location
    # axis_shift -> Y spacing for the internal axes objects from central plot location
    # endcap_pad -> Extra X extension beyond max value to place endcaps of bias and over/under lines
    # endcap_size -> Length of endcaps
    # emoji_size -> Size of flag emoji used to label plots
    # marker_size -> Additional scale factor for custom player markers
    # label_pad -> Y padding between axis and tick labels on internal axes
    # label_text_size -> Font size for internal axes tick labels
    # text_pad -> X padding between endcaps and bias labels (SF multiplied by max x-value to get consistent factor for all plots)
    # plot_text_size -> Fontsize for bias and country labels
    # tick_length -> Y height of individual ticks in internal axes
    # n_ticks -> Number of ticks to use (odd numbers are best)
    # w_padding -> Padding to add additional width to sides of full plot (SF multiplied by max x-value to get consistent factor for all plots)
    # h_padding -> Padding to add additional height to full plot (absolute value)

def plot_total_bias(axs,cumulative_bias,cumulative_overunder,markers,nation_markers,bias_metric="skew",draw_markers=True,draw_emoji=True,do_norm=True,
                    plot_settings={
                        "plot_seperation":0.5,"plot_shift":0.4,"axis_shift":0.19,
                        "endcap_pad":1.2,"endcap_size":0.2,
                        "emoji_size":0.18,"marker_size":0.5,
                        "label_pad":0.03,"label_text_size":8,
                        "text_pad":0.02, "plot_text_size":9,
                        "tick_length":0.09, "n_ticks":5,
                        "w_padding":1.75,"h_padding":0.5}):
    
    settings={"plot_seperation":0.5,"plot_shift":0.4,"axis_shift":0.19,"endcap_pad":1.2,"endcap_size":0.2,"w_padding":1.75,"h_padding":0.5,"emoji_size":0.18,"marker_size":0.5,
              "label_pad":0.03,"label_text_size":8,"text_pad":0.02, "plot_text_size":9,"tick_length":0.06, "n_ticks":5}
    

    for key,val in plot_settings.items():
        if key in settings.keys():
            settings[key] = val
        else:
            print(str(key)+"is not a valid setting")

    ax = axs
    if isinstance(axs, np.ndarray):
        print("WARNING: Expected single axis, got multiple, only plotting on first subplot")
        ax = axs[0]
    nations = cumulative_bias.keys()
    all_max_bias = []
    all_endcaps = []
    for n_plot,n in enumerate(cumulative_bias.keys()):
        biases = cumulative_bias[n]
        overunders = cumulative_overunder[n]
        y_loc = n_plot + n_plot*settings["plot_seperation"]

        #First we need the normalisation factors for each cumulation
        norm_bias,norm_overunder = GetNorm_cumulative_bias(biases,overunders)

        #Base axis position off of bias and scale numbers for overunder-estimation to fit
        x_lim = norm_bias[-1]
        if do_norm:
            x_lim = 1.0

        endcap = x_lim*settings["endcap_pad"]
        tick_x = np.linspace(-x_lim,x_lim,settings["n_ticks"])
        
        all_max_bias.append(x_lim)
        all_endcaps.append(endcap)

        #For each nation we need 2 sets of plots each with their own custom axis to fit into a single y value 
        #center lines
        ax.hlines([y_loc-settings["plot_shift"],y_loc+settings["plot_shift"]], xmin=[-endcap], xmax=[endcap], linestyle='-', color='xkcd:red', alpha=1)
        ax.vlines([-endcap,endcap], ymin=[y_loc-settings["plot_shift"]-(settings["endcap_size"]/2.0)], ymax=[y_loc-settings["plot_shift"]+(settings["endcap_size"]/2.0)], linestyle='-', color='black', alpha=1)
        ax.vlines([-endcap,endcap], ymin=[y_loc+settings["plot_shift"]-(settings["endcap_size"]/2.0)], ymax=[y_loc+settings["plot_shift"]+(settings["endcap_size"]/2.0)], linestyle='-', color='black', alpha=1)

        #Nation emoji (requires emojify package)
        if draw_emoji:
            imscatter(0, y_loc, nation_markers[n], zoom=settings["emoji_size"], ax=ax, opacity=1,drawemoji=True)
            ax.text(0.1*x_lim, y_loc, str(n), horizontalalignment='left',verticalalignment='center', fontsize=settings["plot_text_size"])
        else:
            ax.text(0, y_loc, str(n), horizontalalignment='center',verticalalignment='center', fontsize=settings["plot_text_size"])

        #internal axes
        ax.hlines([y_loc-settings["axis_shift"],y_loc+settings["axis_shift"]], xmin=[-x_lim], xmax=[x_lim], linestyle='-', color='black', alpha=1)
        ax.vlines([tick_x], ymin=[y_loc+settings["axis_shift"]], ymax=[y_loc+settings["axis_shift"]+settings["tick_length"]], linestyle='-', color='black', alpha=1)
        ax.vlines([tick_x], ymin=[y_loc-settings["axis_shift"]-settings["tick_length"]], ymax=[y_loc-settings["axis_shift"]], linestyle='-', color='black', alpha=1)

        #Axis point values (upper is bias, lower is estimation)
        for x in tick_x:
            ax.text(x,y_loc+settings["axis_shift"]-settings["label_pad"],str(round(x,2)),horizontalalignment='center',verticalalignment='top',fontsize=settings["label_text_size"])
            scaled_x = (x/norm_bias[-1])*norm_overunder[-1]
            if bias_metric != "skew": #If not skew then do normalisation and show as arbitrary metric
                if do_norm: 
                    ax.text(x,y_loc-settings["axis_shift"]+settings["label_pad"],str(round(x,1)),horizontalalignment='center',fontsize=settings["label_text_size"])
                else:
                    ax.text(x,y_loc-settings["axis_shift"]+settings["label_pad"],str(round(scaled_x,1)),horizontalalignment='center',fontsize=settings["label_text_size"])
            else: #If skew don't normalise and show as percentage
                if do_norm:
                    scaled_x = x*norm_overunder[-1]
                ax.text(x,y_loc-settings["axis_shift"]+settings["label_pad"],str(round(scaled_x,1))+"%",horizontalalignment='center',fontsize=settings["label_text_size"])


        for player, bias_set in biases.items():
            bias = bias_set[-1]
            est = (overunders[player][-1]/norm_overunder[-1])*norm_bias[-1] #If not normalised need to re-scale to fit into bias-based plot
            if do_norm:
                bias /= norm_bias[-1]
                est = (overunders[player][-1]/norm_overunder[-1])

            ax.errorbar(bias, y_loc+settings["plot_shift"], xerr=None, fmt="o",color='xkcd:red',ecolor='black',ms=15,lw=4)
            ax.errorbar(est, y_loc-settings["plot_shift"], xerr=None, fmt="o",color='xkcd:blue',ecolor='black',ms=15,lw=4)

            if draw_markers:
                imscatter(bias, y_loc+settings["plot_shift"], markers[player][0], zoom=markers[player][1]*settings["marker_size"], ax=ax, opacity=1)
                imscatter(est, y_loc-settings["plot_shift"], markers[player][0], zoom=markers[player][1]*settings["marker_size"], ax=ax, opacity=1)


    n_plots = len(nations)
    max_central_y = n_plots-1+(n_plots-1)*settings["plot_seperation"]
    y_mins_bias = np.linspace(0+settings["axis_shift"],max_central_y+settings["axis_shift"],n_plots)
    y_maxs_bias = np.linspace(0+settings["plot_shift"]+settings["axis_shift"],max_central_y+settings["plot_shift"]+settings["axis_shift"],n_plots)
    y_mins_est = np.linspace(0-settings["plot_shift"]-settings["axis_shift"],max_central_y-settings["plot_shift"]-settings["axis_shift"],n_plots)
    y_maxs_est = np.linspace(0-settings["axis_shift"],max_central_y-settings["axis_shift"],n_plots)

    ax.vlines([0]*n_plots, ymin=[y_mins_bias], ymax=[y_maxs_bias], linestyle='--', color='black', alpha=1)
    ax.vlines([0]*n_plots, ymin=[y_mins_est], ymax=[y_maxs_est], linestyle='--', color='black', alpha=1)

    #Plot label text
    norm_text_pad = max(all_endcaps)*settings["text_pad"]
    y_text_bias = np.linspace(0+settings["plot_shift"],max_central_y+settings["plot_shift"],n_plots)
    y_text_est = np.linspace(0-settings["plot_shift"],max_central_y-settings["plot_shift"],n_plots)
    y_central = np.linspace(0,max_central_y,n_plots)


    for i,endcap in enumerate(all_endcaps):
        ax.text(-endcap-norm_text_pad, y_text_bias[i], "Negative\nBias",horizontalalignment='right',verticalalignment='center',fontsize=settings["plot_text_size"])
        ax.text(endcap+norm_text_pad, y_text_bias[i], "Positive\nBias",horizontalalignment='left',verticalalignment='center',fontsize=settings["plot_text_size"])

        ax.text(-endcap-norm_text_pad, y_text_est[i], "Performance\nUnderestimation",horizontalalignment='right',verticalalignment='center',fontsize=settings["plot_text_size"])
        ax.text(endcap+norm_text_pad, y_text_est[i], "Performance\nOverestimation",horizontalalignment='left',verticalalignment='center',fontsize=settings["plot_text_size"])


    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.spines[['bottom','top','right','left']].set_visible(False)

    ax.set_xbound(-1.0*settings["w_padding"]*max(all_max_bias),settings["w_padding"]*max(all_max_bias))
    ax.set_ybound(-1.0*settings["h_padding"],y_loc+settings["h_padding"]) #use final y_loc

