#------------------------------------------------------------------------------
# Pylon Tutorial "Reinforcement Learning"
#
# Author: Richard Lincoln, r.w.lincoln@gmail.com
#------------------------------------------------------------------------------

__author__ = 'Richard Lincoln, r.w.lincoln@gmail.com'

import sys, logging
from pylon import Case, Bus, Generator

from pyreto import \
    MarketExperiment, ParticipantEnvironment, ProfitTask, SmartMarket

from pyreto.renderer import ExperimentRenderer

from pybrain.tools.shortcuts import buildNetwork
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import ENAC

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
    format="%(levelname)s: %(message)s")

""" Create a simple case. """
g1 = Generator(name="G1", p_max=60.0, p_min=0.0)
g2 = Generator(name="G2", p_max=100.0, p_min=0.0)
bus1 = Bus(name="Bus1", generators=[g1, g2], p_demand=80.0, q_demand=0.0)
case = Case(name="1Bus", buses=[bus1])

""" The market will clear submitted offers/bids and return dispatch info. """
mkt = SmartMarket(case)

agents = []
tasks = []
for g in bus1.generators:
    """ Create an environment for each agent with an asset and a market. """
    env = ParticipantEnvironment(g, mkt, n_offbids=2)

    """ Create a task for the agent to achieve. """
    task = ProfitTask(env)

    """ Build an artificial neural network for the agent. """
    net = buildNetwork(task.outdim, task.indim, bias=False,
                       outputbias=False)
#    net._setParameters(array([9]))

    """ Create a learning agent with a learning algorithm. """
    agent = LearningAgent(module=net, learner=ENAC())
    """ Initialize parameters (variance). """
#    agent.setSigma([-1.5])
    """ Set learning options. """
    agent.learner.alpha = 2.0
    # agent.learner.rprop = True
    agent.actaspg = False
#    agent.disableLearning()

    agents.append(agent)
    tasks.append(task)

""" The Experiment will coordintate the interaction of the given agents and
their associated tasks. """
experiment = MarketExperiment(tasks, agents, mkt)
experiment.setRenderer(ExperimentRenderer())

""" Instruct the experiment to coordinate a set number of interactions. """
experiment.doInteractions(3)
