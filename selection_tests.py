import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats as stats
import scipy.linalg as linalg
import matplotlib.pyplot as plt

from scipy.optimize import minimize
from scipy.stats import norm

#stats
import statsmodels.api as sm
from statsmodels.base.model import GenericLikelihoodModel



def create_panel(df,time_col,cross_col,time_attr,cross_attr):
    """ time_col = name of time column
    cross_col = name of cross-sectional unit column
    attribute_names = x variable data """

    time_units = df[time_col].unique()
    cross_units = df[cross_col].unique()
    #TODO: Modify this so that cross sectional unit has both auction, and bidder

    #create a multi-index with all the units
    panel_index = pd.MultiIndex.from_product([time_units, cross_units], names=[time_col, cross_col])

    #most numerical attributes
    panel = pd.DataFrame(index=panel_index)
    
    attr_array = df[[time_col,cross_col] + cross_attr].copy()

    #create count and attr / creating a group_by by time units, cross-section units
    attr_array = attr_array.groupby([time_col,cross_col]).mean()
    panel = panel.join(attr_array,how='left')

    #TODO: may need to do 2 merges, first by auction, then by bidder? 
    #attr_array = attr_array.groupby([time_col,cross_col]).mean()
    attr_array = attr_array.groupby([time_col,cross_col]).mean()

    #panel = panel.join(attr_array,how='left')

    # Each bid in the auction needs the auction characteristics
    
    return panel


# TODO 2: Get Tobit working..

class Tobit(GenericLikelihoodModel):
    
    def __init__(self, *args, error_distr=stats.norm, **kwargs):
        self.error_distr = error_distr
        super(Tobit,self).__init__(*args,**kwargs)
        self._set_extra_params_names(['var'])
        self.start_params = np.array([1]*(self.exog.shape[1]+1))
    
    def loglikeobs(self, params):
        y = self.endog
        x = self.exog
        m = 1*(self.endog == 0) #missingness
        
        beta = params[0:-1]
        sigma2 = max(params[-1],1e-3)
        
        mu_y = np.matmul(x,beta)
        
        pr_y = self.error_distr.logpdf( y, loc = mu_y, scale=np.sqrt(sigma2))
        pr_m = self.error_distr.logcdf( y, loc = mu_y, scale=np.sqrt(sigma2))
        ll =  (1-m)*pr_y + m*pr_m
        return ll
    
    #if needed can add in score function...

# TODO 3: Get LLR test classic version working

def compute_llr(yn,xn):
    #fit normal values
    model1 = Tobit(yn,sm.add_constant(xn))
    model1_fit = model1.fit(disp=False)
    ll1 = model1.loglikeobs(model1_fit.params)
    
    #fit logistic values
    model2 = Tobit(yn,sm.add_constant(xn),error_distr=stats.logistic)
    model2_fit = model2.fit(disp=False)
    ll2 = model2.loglikeobs(model2_fit.params)
    
    llr = ll1.sum() - ll2.sum()
    omega2 = (ll1- ll2).var()
    return llr,np.sqrt(omega2)


def regular_test(yn,xn,nobs,compute_llr,hist=False):
    llr, omega = compute_llr(yn,xn)
    test_stat = llr/(omega*np.sqrt(nobs))
    if hist:
        x = np.linspace(-2.5, 2.5, 100)
        plt.plot(x, stats.norm.pdf(x, 0, 1),label="Normal")
    
    return 1*(test_stat >= 1.96) + 2*( test_stat <= -1.96)


# TODO 4: Get Bootstrap test working

def bootstrap_test(yn,xn,nobs,compute_llr,hist=False):
    test_stats = []
    trials = 100
    for i in range(trials):
        subn = 1000
        np.random.seed()
        sample  = np.random.choice(np.arange(0,nobs),subn,replace=True)
        ys,xs = yn[sample],xn[sample]
        llr, omega = compute_llr(ys,xs)
        test_stat = llr/(omega*np.sqrt(subn))
        test_stats.append(test_stat)
        
    llr, omega = compute_llr(yn,xn)
    test_stat = llr/(omega*np.sqrt(nobs))
    
    #plot
    if hist:
        plt.hist( 2*test_stat - test_stats, density=True,bins=10, label="Bootstrap")
    
    cv_lower = 2*test_stat - np.percentile(test_stats, 97.5, axis=0)
    cv_upper = 2*test_stat -  np.percentile(test_stats, 2.5, axis=0)
    return  2*(0 >= cv_upper) + 1*(0 <= cv_lower)