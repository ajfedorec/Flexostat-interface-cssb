from numpy import array
import math

class State:
    """ The state variable for the control funcion
    
    This does not need to adhear to any proper interface although a
    readable __str__() method is highly recommended to allow for debugging.
    """
    def __init__(self):
        self.z = 0
    def __str__(self):
        return '%.4f' % self.z

def computeControl(self,od,z,chamber=0,time=0.0):
    """  Controller function
    
    self: self referrs to the main controller object that conains
    all state such as the parameters file.  computeControl should never write
    to any members of self
    od: current od of the camber
    chamber: the chamber number indexed from zero
    time: the current time since start up.
    
    Returns: a tuple (list of dilution values for this chamber, state object)
    
    """
    if z == None:
        z = State()
    #calculate control
    T = [1,1,2,2,4,4,8,8]; #hz
    setpoints = map(lambda T:0.5+0.25*math.sin(T*time/60/60*2*math.pi),T)
    
    err_sig = 1000*(od-setpoints[chamber])
    z.z = z.z+err_sig*float(self.cparams['ki'])
    if z.z<0:
        z.z = 0
    if z.z>float(self.cparams['maxdilution']):
        z.z = float(self.cparams['maxdilution'])
    
    u = z.z+err_sig*float(self.cparams['kp'])
    if u < float(self.cparams['mindilution']):
        u = float(self.cparams['mindilution'])
    if u > float(self.cparams['maxdilution']):
        u = float(self.cparams['maxdilution'])
    u = int(u) # make sure u is an int
    
    return (array([u]),z)