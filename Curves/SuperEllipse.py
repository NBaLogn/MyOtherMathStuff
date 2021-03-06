import matplotlib.pyplot as plt
import numpy as np

# https://web.archive.org/web/20171208231427/http://ftp.lyx.de/Lectures/SuperformulaU.pdf


def superellipse(a=1,b=1,m1=2,m2=None,n=1001,draw=True):
    
    if m2 == None:
        m2 = m1
    
    th = np.linspace(0,2*np.pi,n)
    
    sin_vals = np.sin(th)
    cos_vals = np.cos(th)
    
    
    x = a*np.abs(sin_vals)**(2/m1)*np.sign(sin_vals)
    y = b*np.abs(cos_vals)**(2/m2)*np.sign(cos_vals)
    
    if draw == True:
        
        fig = plt.figure()
        fig.set_size_inches(12,12)
        ax = plt.axes()
        ax.set_aspect("equal","datalim")
        ax.axis('off')
        ax.set_xticks([])
        ax.set_yticks([])
        
        plt.plot(x,y)
    
    return x,y


def superformula(a=1, b=1, m1=0, m2=0, n1=1, n2=1, n3=1, turns=1, n=1001, draw=True):
    
    th = np.linspace(0,2*turns*np.pi,n)
    
    cos_vals = np.cos((m1*th)/4)
    sin_vals = np.sin((m2*th)/4)
    
    aux1 = np.absolute(cos_vals/a)**n2
    aux2 = np.absolute(sin_vals/b)**n3
    raux = (aux1+aux2)**(-1/n1)
    x = raux*np.cos(th)
    y = raux*np.sin(th)
    
    if draw == True:
        
        fig = plt.figure()
        fig.set_size_inches(12,12)
        ax = plt.axes()
        ax.set_aspect("equal","datalim")
        ax.axis('off')
        ax.set_xticks([])
        ax.set_yticks([])
        
        plt.plot(x,y)
    
    return x,y





if __name__ == '__main__':
        
#    
#    x,y = superformula(a=1,b=1,n2=1,n3=6,n1=-20,m1=88,m2=64,n=4001)
#    x,y = superformula(a=1,b=1,n2=1,n3=1,n1=2,m1=8,m2=3,turns=2,n=4001)
#    x,y = superformula(m1=2,m2=2,n1=.5,n2=.5,n3=.5)
    x,y = superellipse(7,5,3)
    x,y = superellipse(7,5,.5,6)
#    x,y = superellipse()