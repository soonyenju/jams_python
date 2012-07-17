#!/usr/bin/env python
import numpy as np

def heaviside(x, value=1., unitstep=False, zero=False):
    """
        Heaviside (or unit step) operator
            H =  0  for x <  0
            H = 1/2 for x =  0
            H =  1  for x >  0
          if unitstep
            H =  0  for x <  0
            H =  1  for x >= 0
          if zero
            H =  0  for x =< 0
            H =  1  for x >  0

        Definition
        ----------
        def heaviside(x, value=1., unitstep=False, zero=False):


        Input
        -----
        x            value or array of values


        Optional Input
        --------------
        value        output is heaviside *= value
	unitstep     If True, H(0)=1 instead of 1/2
	zero         If True, H(0)=0 instead of 1/2


        Output
        ------
        Heaviside function 0, 1/2, and 1


        Restrictions
        ------------
        Returns False if error.


        Examples
        --------
        >>> print heaviside([-1,0.,1.])
        [ 0.   0.5  1. ]

        >>> print heaviside([-1,0.,1.], zero=True)
        [ 0.  0.  1.]

        >>> print heaviside([-1,0.,1.], unitstep=True)
        [ 0.  1.  1.]

        >>> print heaviside([-1,0.,1.], value=2)
        [ 0.  1.  2.]


        License
        -------
        This file is part of the UFZ Python library.

        The UFZ Python library is free software: you can redistribute it and/or modify
        it under the terms of the GNU Lesser General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        The UFZ Python library is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
        GNU Lesser General Public License for more details.

        You should have received a copy of the GNU Lesser General Public License
        along with The UFZ Python library.  If not, see <http://www.gnu.org/licenses/>.

        Copyright 2012 Matthias Cuntz

        
        History
        -------
        Written, MC, Jan 2012
    """
    if zero and unitstep:
        raise ValueError('unitstep and zero mutually exclusive.')

    if zero:
        out = np.where(np.ma.array(x) > 0., 1., 0.)
    elif unitstep:
        out = np.where(np.ma.array(x) >= 0., 1., 0.)
    else:
        out = (np.where(np.ma.array(x) > 0., 1., 0.) - np.where(np.ma.array(x) < 0., 1., 0.) + 1.) * 0.5
    out *= value
    return out

 
if __name__ == '__main__':
    import doctest
    doctest.testmod()
