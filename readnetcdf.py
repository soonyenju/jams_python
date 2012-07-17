#!/usr/bin/env python
import netCDF4 as nc
import numpy as np

def readnetcdf(file, var='', code=-1, reform=False, squeeze=False,
               variables=False, codes=False, units=False, longnames=False,
               attributes=False, sort=False):
    """
        Gets variables or prints information of netcdf file.

        
        Definition
        ----------
        def readnetcdf(file, var='', code=-1, reform=False, squeeze=False,
                       variables=False, codes=False, units=False, 
                       longnames=False, attributes=False, sort=False):
                     

        Input
        -----
        file         netcdf file name
        

        Optional Input Parameters
        -------------------------
        var          name of variable in netcdf file
        code         code number in attribute code
                       

        Options
        -------
        reform       if output is array then squeeze(array)
                     if codes then remove all codes==-1
                     if units or longnames then remove =''
        squeeze      same as reform
        variables    get list of variables in netcdf file
        codes        get list of codes attribute code
        units        get list of units of variables from attribute units
        longnames    get list of long names of variables from
                     attribute long_name
        attributes   get dictionary of all attributes of specific variable
        sort         sort variable names. Codes, units and longnames will be
                     sorted accoringly so that indeces still match.
                            

        Output
        ------
        Either float array of variable/code or information lists
        such as list of all variables in netcdf file.


        Restrictions
        ------------
        If codes, units or longnames are reformed/squeezed,
          they do not match the variable list anymore.
        Attributes can not be sorted nor reformed/squeezed.
                

        Examples
        --------
        >>> readnetcdf('readnetcdf_test.nc',var='is1')
        array([[ 1.,  1.,  1.,  1.],
               [ 1.,  1.,  1.,  1.]])
        >>> readnetcdf('readnetcdf_test.nc',code=129)
        array([[ 2.,  2.,  2.,  2.],
               [ 2.,  2.,  2.,  2.]])
        >>> [unicode(i) for i in readnetcdf('readnetcdf_test.nc',variables=True)]
        [u'x', u'y', u'is1', u'is2']
        >>> [unicode(i) for i in readnetcdf('readnetcdf_test.nc',variables=True,sort=True)]
        [u'is1', u'is2', u'x', u'y']
        >>> [unicode(i) for i in readnetcdf('readnetcdf_test.nc',units=True)]
        [u'xx', u'yy', u'arbitrary', u'arbitrary']
        >>> [unicode(i) for i in readnetcdf('readnetcdf_test.nc',units=True,sort=True)]
        [u'arbitrary', u'arbitrary', u'xx', u'yy']
        >>> [unicode(i) for i in readnetcdf('readnetcdf_test.nc',longnames=True)]
        [u'x-axis', u'y-axis', u'all ones', u'all twos']
        >>> [unicode(i) for i in readnetcdf('readnetcdf_test.nc',longnames=True,sort=True)]
        [u'all ones', u'all twos', u'x-axis', u'y-axis']

        # old: {'units': 'arbitrary', 'long_name': 'all ones', 'code': 128}
        # new: {u'units': u'arbitrary', u'long_name': u'all ones', u'code': 128}
        >>> t1 = readnetcdf('readnetcdf_test.nc',var='is1',attributes=True)
        >>> d = dict()
        >>> for k, v in t1.iteritems():
        ...     if type(k) == type('s'):
        ...         if type(v) == type('s'):
        ...             d[unicode(k)] = unicode(v)
        ...         else:
        ...             d[unicode(k)] = v
        ...     else:
        ...         if type(v) == type('s'):
        ...             d[k] = unicode(v)
        ...         else:
        ...             d[k] = v
        >>> d
        {u'units': u'arbitrary', u'long_name': u'all ones', u'code': 128}
        >>> readnetcdf('readnetcdf_test.nc',codes=True)
        array([  -1.,   -1.,  128.,  129.])
        >>> readnetcdf('readnetcdf_test.nc',codes=True,reform=True)
        array([ 128.,  129.])
        >>> readnetcdf('readnetcdf_test.nc',codes=True,sort=True)
        [128.0, 129.0, -1.0, -1.0]


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

        Copyright 2009-2012 Matthias Cuntz


        History
        -------
        Written,  MC, Jul 2009
        Modified, MC, Jun 2012 - removed quiet
        """
    # Open netcdf file
    try:
        f = nc.Dataset(file, 'r')
    except IOError:
        raise IOError('Cannot open file for reading.'+file)
    # Variables
    vars = f.variables.keys()
    nvars = len(vars)
    # Sort and get sort indices
    if sort:
        svars = sorted(vars)
        ivars = list()
        for v in svars:
            ivars.append(vars.index(v))
    if variables:
        f.close()
        if sort:
            return svars
        else:
            return vars
    # Codes
    cods = np.empty(nvars)
    i=0
    for v in vars:
        attr = f.variables[v].ncattrs()
        if 'code' in attr:
            cods[i] = getattr(f.variables[v],'code')
        else:
            cods[i] = -1
        i += 1
    if codes:
        if sort:
            scods = [cods[i] for i in ivars]
        else:
            scods = cods
        if reform or squeeze:
            scods = np.compress(scods!=-1, scods)
        f.close()
        return scods
    # Get units
    if units:
        unis = list()
        for v in vars:
            attr = f.variables[v].ncattrs()
            if 'units' in attr:
                unis.append(getattr(f.variables[v],'units'))
            else:
                unis.append('')
        if sort:
            sunis = [unis[i] for i in ivars]
        else:
            sunis = unis
        if reform or squeeze:
            nn = sunis.count('')
            if nn > 0:
                for i in range(nn):
                    sunis.remove('')
        f.close()
        return sunis
    # Get long_name
    if longnames:
        longs = list()
        for v in vars:
            attr = f.variables[v].ncattrs()
            if 'long_name' in attr:
                longs.append(getattr(f.variables[v],'long_name'))
            else:
                longs.append('')
        if sort:
            slongs = [longs[i] for i in ivars]
        else:
            slongs = longs
        if reform or squeeze:
            nn = slongs.count('')
            if nn > 0:
                for i in range(nn):
                    slongs.remove('')
        f.close()
        return slongs
    # Get attributes
    if attributes:
        if var not in vars:
            f.close()
            raise ValueError('Variable '+var+' not in file '+file)
        attrs = dict()
        attr = f.variables[var].ncattrs()
        for a in attr:
            attrs[a] = getattr(f.variables[var],a)
        f.close()
        return attrs
    # Get variable
    if var == '' and code==-1:
        f.close()
        raise ValueError('Variable name or code has to be given')
    if var != '':
        if var not in vars:
            f.close()
            raise ValueError('Variable '+var+' not in file '+file)
        arr = f.variables[var][:]
        if reform or squeeze:
            f.close()
            return arr.squeeze()
        else:
            f.close()
            return arr
    if code != -1:
        if code not in cods:
            f.close()
            raise ValueError('Code '+str(code)+' not in file '+file)
        arr = f.variables[np.compress(cods==code, vars)[0]][:]
        if reform or squeeze:
            f.close()
            return arr.squeeze()
        else:
            f.close()
            return arr

if __name__ == '__main__':
    import doctest
    doctest.testmod()
