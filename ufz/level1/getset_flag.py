#!/usr/bin/env python
from __future__ import print_function
import numpy as np

__all__ = ['get_flag', 'get_maxflag', 'set_flag']

# --------------------------------------------------------------------

def get_flag(flags, n):
    """
        Get the flags at position n from CHS data flag vector.


        Definition
        ----------
        def get_flag(flags, n):


        Input
        -----
        flags   ND-array of integers
        n       position to extract

        
        Output
        ------
        ND-array of integers with flag at position n of flags
        returns -1 if input integer is less than 10**(n+1)


        Examples
        --------
        >>> flags = np.array([9, 90, 91, 900, 901, 9001, 9201, 912121212])
        >>> print(get_flag(flags, 0))
        [9 9 9 9 9 9 9 9]

        >>> print(get_flag(flags, 1))
        [-1  0  1  0  0  0  2  1]

        >>> print(get_flag(flags, 2))
        [-1 -1 -1  0  1  0  0  2]

        >>> print(get_flag(flags, 3))
        [-1 -1 -1 -1 -1  1  1  1]

        >>> print(get_flag(flags, 4))
        [-1 -1 -1 -1 -1 -1 -1  2]


        License
        -------
        This file is part of the UFZ Python package.

        The UFZ Python package is free software: you can redistribute it and/or modify
        it under the terms of the GNU Lesser General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        The UFZ Python package is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
        GNU Lesser General Public License for more details.

        You should have received a copy of the GNU Lesser General Public License
        along with the UFZ makefile project (cf. gpl.txt and lgpl.txt).
        If not, see <http://www.gnu.org/licenses/>.

        Copyright 2015 Matthias Cuntz


        History
        -------
        Written,  MC, Mar 2015
    """
    out = np.ones(flags.shape, dtype=np.int)*(-1)   # if not enough digits -> -1

    # deal with -9999
    jj = np.where(flags <= 0)
    if jj[0].size>0: out[jj] = -2

    # normal flags starting with 9
    jj = np.where(flags > 0)
    if jj[0].size>0:
        oo = out[jj]
        ilog10 = np.log10(flags[jj]).astype(np.int)         # how many digits
        ii = np.where((ilog10-n) >= 0)               # otherwise extract n-th digit
        if ii[0].size > 0:
            oo[ii] = (flags[jj][ii] // 10**(ilog10[ii]-n)) % 10
        out[jj] = oo

    return out

# --------------------------------------------------------------------

def set_flag(flags, n, iflag, ii=None):
    """
        Set the flags at position n to iflag at indeces ii of CHS data flag vector.


        Definition
        ----------
        def set_flag(flags, n, iflag, ii=None):


        Input
        -----
        flags   CHS data flag vector, ND-array of integers
        n       position in flag to set, missing positions will be cretaed and filled with 0
        iflag   set flag to this value


        Optional Input
        --------------
        ii      indices at which to set flag (default: None, i.e. each entry)

        
        Output
        ------
        ND-array of integers with flag at position n of flags set to iflag


        Examples
        --------
        >>> flags = np.array([9, 90, 901, 9101, 912121212])
        >>> print(set_flag(flags, 1, 2, [0,1,2]))
        [       92        92       921      9101 912121212]

        >>> print(set_flag(flags, 3, 2, [0,1,2,3]))
        [     9002      9002      9012      9102 912121212]

        >>> print(set_flag(flags, 1, 2))
        [       92        92       921      9201 922121212]


        License
        -------
        This file is part of the UFZ Python package.

        The UFZ Python package is free software: you can redistribute it and/or modify
        it under the terms of the GNU Lesser General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        The UFZ Python package is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
        GNU Lesser General Public License for more details.

        You should have received a copy of the GNU Lesser General Public License
        along with the UFZ makefile project (cf. gpl.txt and lgpl.txt).
        If not, see <http://www.gnu.org/licenses/>.

        Copyright 2015 Matthias Cuntz


        History
        -------
        Written,  MC, Mar 2015
    """
    fflags = flags.copy()
    # extend flag vector if needed
    ilog10 = np.log10(fflags).astype(np.int)  # are there enough flag positions (i)
    jj = np.where(ilog10 < n)[0]
    if jj.size > 0:                          # increase number (filled with 0)
        fflags[jj] *= 10**(n-ilog10[jj])
        ilog10 = np.log10(fflags).astype(np.int)
        
    # get entries in flag vector
    isflags = get_flag(fflags, n)

    # set entries in flag vector
    if ii is None:                                  # set all to iflag
        fflags += 10**(ilog10-n) * (iflag-isflags)
    else:
        if np.size(ii) > 0:                         # set ii to iflag
            fflags[ii] += 10**(ilog10[ii]-n) * (iflag-isflags[ii])

    return fflags

# --------------------------------------------------------------------

def get_maxflag(flags):
    """
        Returns the overall flag for each flag from CHS data flag vector.


        Definition
        ----------
        def get_maxflag(flags):


        Input
        -----
        flags   ND-array of integers

        
        Output
        ------
        ND-array of integers with overall flag 
        returns:
            2, if at least one flag is 2
            1, if at least one flag is 1
            0, if all flags are 0 or still -9999


        Examples
        --------
        >>> flags = np.array([9, 90, 91, 900, 901, 9001, 9201, 912121212, -9999])
        >>> print(get_maxflag(flags))
        [-1  0  1  0  1  1  2  2 -2]


        License
        -------
        This file is part of the UFZ Python package.

        The UFZ Python package is free software: you can redistribute it and/or modify
        it under the terms of the GNU Lesser General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        The UFZ Python package is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
        GNU Lesser General Public License for more details.

        You should have received a copy of the GNU Lesser General Public License
        along with the UFZ makefile project (cf. gpl.txt and lgpl.txt).
        If not, see <http://www.gnu.org/licenses/>.

        Copyright 2015 Juliane Mai


        History
        -------
        Written,  JM, Mar 2015
    """

    # Determine number of flags
    n_flags_precip = 18
    
    # Determine overall flag:
    #      cumflag=2,  if at least one flag is 2,     e.g. '9002010'
    #      cumflag=1,  if at least one flag is 1,     e.g. '9000100'
    #      cumflag=0,  if all individual flags are 0, e.g. '9000000'
    #      cumflag=-1, if flag is '9'
    #      cumflag=-2, if flag is '-9999'
    cumflag=np.ones(np.shape(flags), dtype=np.int) * (-2)
    for ii in np.arange(1,n_flags_precip+1):
        cumflag = np.maximum(cumflag,get_flag(flags,ii))
    
    return cumflag

# --------------------------------------------------------------------

if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
