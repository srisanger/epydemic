# Gillespie dynamics over a compartmented model
#
# Copyright (C) 2017 Simon Dobson
# 
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

from epydemic import * 

import numpy


class CompartmentedStochasticDynamics(StochasticDynamics):
        
    def __init__( self, m, g = None ):
        '''Create a dynamics over the given process model, optionally
        initialised to run on the given network.
       
        :param m: the compartmented model for the disease process
        :param g: prototype network to run the dynamics over (optional)'''
        super(CompartmentedStochasticDynamics, self).__init__(g)
        self._model = m

    def _drawFrom( self, dist ):
        '''Draw an element from a distribution. Essentially this converts a uniformly
        distributed value (which is easily obtainable) into a number drawn from a
        discrete but arbitrary distribution.

        :param dist: the distribution represented as a list of (value, probability) pairs
        :returns: a value selected at random according to the distribution'''
        r1 = numpy.random.random()
        a = 0.0
        for (s, p) in dist:
            a = a + p
            if r1 <= a:
                return s

    def setUp( self, params ):
        '''Set up the experiment for a run. This performs the default action of
        copying the prototype network and then uses the model to initialise the
        nodes into the various compartments according to the parameters.

        :params params: the experimental parameters'''
        
        # perform the default setup
        super(CompartmentedStochasticDynamics, self).setUp(params)

        # initialise the network from the model
        g = self.network()
        self._model.setUp(g, params)

    def eventRateDistribution( self, t ):
        '''Convert the model's event distribution into the rate-based distribution
        required by Gillespie simulation.

        :param t: the current time
        :returns: the event rate distribution'''
        dist = self._model.eventDistribution(t)
        return map((lambda (l, p, f): (l, p * self._model.sizeOfLocus(l), f)), dist)

    def experimentalResults( self ):
        '''Report the model's experimental results.

        :returns: the results as seen by the model'''
        return self._model.results(self.network())
    