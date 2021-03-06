#import numpy as np
from Utils.Math import sort_by_nth, prod

def median(L):
    L = sorted(L)
    parity = len(L)%2
    half_range = len(L)//2
    
    if parity == 1:
        return L[half_range]
    else:
        return (L[half_range-1]+L[half_range])/2


# Crude weighted median
# Weighted median should be equivalent of having extra entries corresponding to
# the weights
# Should return the lower median on an even set
def weighted_median(L,W):
    LW = [(l,w) for l,w in zip(L,W)]
    LW = sort_by_nth(LW,0)
    
    s = sum(W)
    
    t = 0
    ctr = 0
    while t <= s/2:
        t += LW[ctr][1]
        ctr += 1
    
    return LW[ctr-1][0]
    

def arithmetic_mean(L):
    return sum(L)/len(L)


# Arithmetic mean with quartiles beyond t and 1-t removed
#def truncated_mean(L,t=.05):


def weighted_mean(L,W=[]):
    if len(W) == 0:
        W = [1]*len(L)
    T = [l*w for l,w in zip(L,W)]
    return sum(T)/sum(W)


def geometric_mean(L):
    P = prod(L)
    return P**(1/len(L))


def harmonic_mean(L):
    S = sum([1/l for l in L])
    return len(L)/S





if __name__ == '__main__':
    
    # Make some graphics showing different measures
    
    import Utils.Drawing as draw
    import numpy as np
    from Utils.PointManip import push_from_center, midpoint



    def weighted_mean_example():
        canvas, plot = draw.make_blank_canvas([-10,10],box=True)
        draw.title("The Weighted Mean is the Point of Balance",size=25)
        
        X = [x for x in range(-8,9)]
        W = np.random.randint(0,5,17)**2
        W[0] = 50
        W[1] = 40
        
        for i in range(len(X)-1):
            draw.draw_rect_xy(X[i]+.05,0,X[i+1]-.05,W[i]/10)
        
        draw.connect_p([-8,0],[8,0],color="black",linewidth=3)
        draw.draw_dots_xy([weighted_mean(X,W)],[-.2],color="red",marker="^",s=200)



    def median_mean_example():
        canvas, plot = draw.make_blank_canvas(size=[16,8])
        draw.canvas_title("The Median is the Point of Typicality\nThe Mean is the Point of Balance",size=25,y=1.05)
        
        n = 20
        X = np.random.uniform(-8,8,n//2)
        X = np.append(X,np.random.uniform(5,8,n//2))
        
        draw.make_blank_subplot(1,2,1,[-10,10])
        draw.draw_circles_xy(X,[.2]*n,[.2]*n)
        draw.connect_p([-8,-.01],[8,-.01],color="black")
        draw.draw_dots_xy([arithmetic_mean(X)],[-.35],color="black",marker="^",s=200)
        draw.draw_dots_xy([median(X)],[-.35],color="lightgray",marker="^",s=200)
        draw.title("Mean",size=25)
        
        draw.make_blank_subplot(1,2,2,[-10,10])        
        draw.draw_circles_xy(X,[.2]*n,[.2]*n)
        draw.connect_p([-8,-.01],[8,-.01],color="black")
        draw.draw_dots_xy([median(X)],[-.35],color="black",marker="^",s=200)
        draw.draw_dots_xy([arithmetic_mean(X)],[-.35],color="lightgray",marker="^",s=200)
        draw.title("Median",size=25)


 
    def harmonic_mean_example():
        canvas, plot = draw.make_blank_canvas([-1.5,1.5],[-1.5,1.5],[10,10])
        draw.canvas_title("The Harmonic Mean is Relevant to Rates\nWhat Is the Average Speed Around The Track Below?\nEach Distance is Equal",size=25,y=1.05)
        
        th = np.linspace(0,2*np.pi,8)
        X = np.sin(th)[:-1]
        Y = np.cos(th)[:-1]
        
        P = [(x,y) for x,y in zip(X,Y)]
        # Hard to read change this
        M = [midpoint(a,b) for a,b in zip(P[1:]+[P[-1]],P[:-1]+[P[0]])]
        M = [push_from_center(m,[0,0],.2) for m in M]
        
        draw.draw_dots_xy(X,Y)
        draw.draw_closed_curve_xy(X,Y,linewidth=.5,color="black")

        S = np.random.randint(1,9,7)
        for speed,p in zip(S,M):
            draw.text(p[0],p[1],f"{speed} mph",ha='center',size=12)
            
        draw.text(0,0,f"Average Speed: {harmonic_mean(S):.2f} mph",ha='center',size=20)
        print(sum([1/s for s in S]))
            

    weighted_mean_example()
#    median_mean_example()
#    harmonic_mean_example()