__author__ = 'Richard Lincoln, r.w.lincoln@gmail.com'

""" This script creates the plots published in Learning to Trade Power by
Richard Lincoln. """

import matplotlib
#matplotlib.use('WXAgg')#'TkAgg')

#matplotlib.rc('font', **{'family': 'sans-serif',
#                         'sans-serif': ['Computer Modern Sans serif']})
#matplotlib.rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
#matplotlib.rc('text', usetex=True)

import random

from pylab import \
    figure, plot, xlabel, ylabel, legend, savefig, rcParams, clf, title, \
    xlim, ylim, show, errorbar, subplot, twinx, subplots_adjust

from scipy import arange, sqrt
from scipy.io import mmread

from common import \
    get_winter_hourly, get_summer_hourly, get_spring_autumn_hourly, \
    get_weekly, get_daily

matplotlib.rcParams['lines.linewidth'] = 0.5
matplotlib.rcParams['axes.linewidth'] = 0.7
matplotlib.rcParams['axes.titlesize'] = 10

tex = False

if tex:
    # Set up publication quality graphs.
    matplotlib.rc('font', **{'family': 'serif',
                             'serif': ['Computer Modern Roman']})

    #fig_width_pt = 246.0  # Get this from LaTeX using \showthe\columnwidth
    #inches_per_pt = 1.0 / 72.27               # Convert pt to inch
    golden_mean = (sqrt(5) - 1.0) / 2.0 # Aesthetic ratio
    fig_width = 6.15#fig_width_pt * inches_per_pt  # width in inches
    fig_height = 10.0#fig_width * golden_mean      # height in inches
    fig_size = [fig_width, fig_height]
    params = {'backend': 'ps',
              'axes.labelsize': 10,
              'text.fontsize': 10,
              'legend.fontsize': 8,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              'text.usetex': True,
    #          'markup': 'tex',
    #          'text.latex.unicode': True,
              'figure.figsize': fig_size}
    rcParams.update(params)
else:
    matplotlib.rcParams['figure.figsize'] = (8, 10)


clr = ["black", "0.5", "0.8"]
ls = ["-"]#, ":", "--", "-."]
nc, ns = len(clr), len(ls)


def plot_results(results, ai, ylab, xlab="Time (h)"):
    nplot = len(results)

    for i, (result_mean, result_std, epsilon, lab, y2lab, y2max, y2min) in \
    enumerate(results):

        subplot(nplot, 1, i + 1)

        title(lab)

        x = arange(0.0, result_mean.shape[1], 1.0)
        y = result_mean[ai, :]
        e = result_std[ai, :]
        y2 = epsilon[ai, :]

#        plot(x, result_mean[ai, :],
#             color=clr[ai % nc],
#             linestyle=ls[ai % ns],
#             label=lab)

        errorbar(x, y, yerr=e, fmt='ko', linestyle="None",
                 label="Action/Reward",
                 capsize=0, markersize=3)#, linewidth=0.2)
        ylabel(ylab)

#        l = legend(loc="upper right")
#        l.get_frame().set_linewidth(0.5)

        # Exploration rate plot.
        twinx()
        plot(x, y2, color="black", label=y2lab)
        ylabel(y2lab)
        if y2max is not None:
            ylim(ymax=y2max)
        if y2min is not None:
            ylim(ymin=y2min)

#        l = legend(loc="lower right")
#        l.get_frame().set_linewidth(0.5)

#        subplots_adjust(left=0.09, bottom=0.05, right=None,
#                        wspace=None, hspace=None)

    xlabel(xlab)


def plot5_1():
    re_epsilon = mmread("./out/ex5_1_rotherev_epsilon.mtx")
    q_epsilon = mmread("./out/ex5_1_q_epsilon.mtx")
    reinforce_epsilon = mmread("./out/ex5_1_reinforce_epsilon.mtx")
    enac_epsilon = mmread("./out/ex5_1_enac_epsilon.mtx")

    re_action_mean = mmread("./out/ex5_1_rotherev_action_mean.mtx")
    re_action_std = mmread("./out/ex5_1_rotherev_action_std.mtx")
    q_action_mean = mmread("./out/ex5_1_q_action_mean.mtx")
    q_action_std = mmread("./out/ex5_1_q_action_std.mtx")
    reinforce_action_mean = mmread("./out/ex5_1_reinforce_action_mean.mtx")
    reinforce_action_std = mmread("./out/ex5_1_reinforce_action_std.mtx")
    enac_action_mean = mmread("./out/ex5_1_enac_action_mean.mtx")
    enac_action_std = mmread("./out/ex5_1_enac_action_std.mtx")

    actions = [
        (re_action_mean, re_action_std, re_epsilon,
         "Roth-Erev", "Boltzmann Temperature", None, None),
        (q_action_mean, q_action_std, q_epsilon,
         "Q-Learning", "Epsilon", 1.0, 0.0),
        (reinforce_action_mean, reinforce_action_std, reinforce_epsilon,
         "REINFORCE", "Sigma", None, None),
        (enac_action_mean, enac_action_std, enac_epsilon,
         "ENAC", "Sigma", None, None)
    ]

    for ai in [0, 1]:
        figure(ai)
        plot_results(actions, ai, "Action (\%)")
        if tex:
            savefig('./out/fig5_1_a%d_action.pdf' % ai)
        else:
            savefig('./out/fig5_1_a%d_action.png' % ai)


    re_reward_mean = mmread("./out/ex5_1_rotherev_reward_mean.mtx")
    re_reward_std = mmread("./out/ex5_1_rotherev_reward_std.mtx")
    q_reward_mean = mmread("./out/ex5_1_q_reward_mean.mtx")
    q_reward_std = mmread("./out/ex5_1_q_reward_std.mtx")
    reinforce_reward_mean = mmread("./out/ex5_1_reinforce_reward_mean.mtx")
    reinforce_reward_std = mmread("./out/ex5_1_reinforce_reward_std.mtx")
    enac_reward_mean = mmread("./out/ex5_1_enac_reward_mean.mtx")
    enac_reward_std = mmread("./out/ex5_1_enac_reward_std.mtx")

    rewards = [
        (re_reward_mean, re_reward_std, re_epsilon,
         "Roth-Erev", "Boltzmann Temperature", None, None),
        (q_reward_mean, q_reward_std, q_epsilon,
         "Q-Learning", "Epsilon", 1.0, 0.0),
        (reinforce_reward_mean, reinforce_reward_std, reinforce_epsilon,
         "REINFORCE", "Sigma", None, None),
        (enac_reward_mean, enac_reward_std, enac_epsilon,
         "ENAC", "Sigma", None, None)
    ]

    for ai in [0, 1]:
        figure(ai + 10)
        plot_results(rewards, ai, r"Reward (\verb+$+)")
        if tex:
            savefig('./out/fig5_1_a%d_reward.pdf' % ai)
        else:
            savefig('./out/fig5_1_a%d_reward.png' % ai)

    if not tex:
        show()


def plot_profiles():
    figure()
    clf()
    x = arange(0.0, 52.0, 1.0)
    plot(x, get_weekly(), color="black")
    xlabel("Week of the year, starting January 1st")
    ylabel("Percentage of annual peak load")
    xlim((0.0, 51.0))
    ylim((0.0, 100.0))
#    title("IEEE RTS Weekly Load Profile")
    legend()
    savefig('./out/ieee_rts_weekly.pdf')


    clf()
    x = arange(1.0, 8.0, 1.0)
    plot(x, get_daily(), color="black")
    xlabel("Day of the week, starting Monday")
    ylabel("Percentage of weekly peak load")
    xlim((1.0, 7.0))
    ylim((0.0, 100.0))
#    title("IEEE RTS Daily Load Profile")
    legend()
    savefig('./out/ieee_rts_daily.pdf')


    clf()
    hourly_winter_wkdy, hourly_winter_wknd = get_winter_hourly()
    hourly_summer_wkdy, hourly_summer_wknd = get_summer_hourly()
    hourly_spring_autumn_wkdy, hourly_spring_autumn_wknd = \
        get_spring_autumn_hourly()

    x = arange(0.0, 24.0, 0.5)

    plot(x, hourly_winter_wkdy + hourly_winter_wknd,
         label="Winter (Weeks 1-8 \& 44-52)", color="black")
    plot(x, hourly_summer_wkdy + hourly_summer_wknd,
         label="Summer (Weeks 18-30)", color="0.4")
    plot(x, hourly_spring_autumn_wkdy + hourly_spring_autumn_wknd,
         label="Spring \& Autumn (Weeks 9-17 \& 31-43)", color="0.6")

    xlabel("Hour of the day, starting at midnight")
    ylabel("Percentage of daily peak load")
    xlim((0.0, 23.0))
    ylim((0.0, 100.0))
#    title("IEEE RTS Hourly Load Profiles")
    legend(loc="lower right")

    savefig('./out/ieee_rts_hourly.pdf')


if __name__ == "__main__":
    plot5_1()
#    plot_profiles()