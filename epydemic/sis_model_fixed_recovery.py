# SIS with a fixed recovery time
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

class SIS_FixedRecovery(SIS):
    '''The Susceptible-Infected-Susceptible :term:`compartmented model of disease`,
    in the variation where the time spent infected is fixed rather than happening
    with some probability.'''
    
    # the additional model parameter
    T_INFECTED = 'tInfected'           #: Parameter for the time spent infected before becoming susceptible again.

    # node attribute for infection time
    INFECTION_TIME = 'infection_time'  #: Attribute recording when a node became infected
    
    def __init__( self ):
        super(SIS_FixedRecovery, self).__init__()

    def build( self, params ):
        '''Build the variant SIS model. The difference between this and the
        reference :class:`SIS` model is that only infection events happen
        probabilistically, with recovery events happening on a fixed schedule
        depending on the :attr:`T_INFECTED` parameter.

        :param params: the model parameters'''
        pInfected = params[self.P_INFECTED]
        pInfect = params[self.P_INFECT]
        self._tInfected = params[self.T_INFECTED]
        
        self.addCompartment(self.SUSCEPTIBLE, 1 - pInfected)
        self.addCompartment(self.INFECTED, pInfected)

        self.addLocus(self.SUSCEPTIBLE, self.INFECTED, name = self.SI)
        self.addEvent(self.SI, pInfect, lambda t, g, e: self.infect(t, g, e))

    def setUp( self, dyn, g, params ):
        '''After setting up as normal, post recovery events for any nodes that are
        initially infected.

        :param dyn: the dynamics
        :param g: the network
        :param params: the simulation parameters'''
        super(SIS_FixedRecovery, self).setUp(dyn, g, params)

        # traverse the set of initially-infected nodes
        tInfected = params[self.T_INFECTED]
        for n in self.compartment(g, self.INFECTED):
            # record that the node was initially infected
            g.node[n][self.INFECTION_TIME] = 0.0
        
            # post the corresponding removal event
            dyn.postEvent(tInfected, g, n, lambda d, t, g, e: self.removal(d, t, g, e))          

    def infect( self, dyn, t, g, e ):
        '''Perform the normal infection event, and then post an event to recover
        the infected node back to susceptible at the appropriate time.

        :param dyn: the dynamics
        :param t: the simulation time
        :param g: the network
        :param e: the edge transmitting the infection, susceptible-infected'''
        (n, m) = e

        # infect as normal
        super(SIS_FixedRecovery, self).infect(dyn, t, g, e)

        # record the infection time
        g.node[n][self.INFECTION_TIME] = t
        
        # post the removal event for the appropriate time in the future
        dyn.postEvent(t + self._tInfected, g, n, lambda d, t, g, e: self.remove(d, t, g, e))
                
                
                
   
