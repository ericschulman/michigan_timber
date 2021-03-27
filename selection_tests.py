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


def potential_bidders(df,date_name='Bid Open Date',bidder_name='Bidder Name' ):

    df_edit = df.copy()
    df_edit['month_year'] = pd.to_datetime(
        df_edit[date_name]).dt.to_period('M').astype(str)
    new_dict = df_edit.groupby('month_year').apply(
        lambda x: x[bidder_name].unique().tolist()).to_dict()

    delete = ['2013-05', 'NaT']
    #for d in delete:
    #    del new_dict[d]
    #print(len(new_dict))
    print(dict(sorted(new_dict.items())))

    
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
    
    def __init__(self, *args,ols=False, **kwargs):
        super(Tobit,self).__init__(*args,**kwargs)
        self._set_extra_params_names(['var'])
        self.start_params = np.array([1]*(self.exog.shape[1]+1))
        self.ols = ols
        #2 sets of params for z, 1 for x, 2 variances...
    
    def loglikeobs(self, params):
        y = self.endog
        x = self.exog
        m = 1*(self.endog == 0) #missingness
        
        beta = params[0:-1]
        sigma2 = max(params[-1],1e-3)
        
        mu_y = np.matmul(x,beta)
        
        pr_y = stats.norm.logpdf( y, loc = mu_y, scale=np.sqrt(sigma2))
        pr_m = stats.norm.logcdf( y, loc = mu_y, scale=np.sqrt(sigma2))
        
        #we're done if ols
        if self.ols:
            return pr_y
        else:
            ll = (1-m)*pr_y + m*pr_m
            return ll

# TODO 3: Get LLR test classic version working

def setup_test(yn,xn):
    model1 = Tobit(yn,sm.add_constant(xn))
    model1_fit = model1.fit(disp=False)
    ll1 = model1.loglikeobs(model1_fit.params)
    grad1 =  model1.score_obs(model1_fit.params)    
    hess1 = model1.hessian(model1_fit.params)
    params1 = model1_fit.params
    
    #fit logistic values
    model2 = Tobit(yn,sm.add_constant(xn),ols=True)
    model2_fit = model2.fit(disp=False)
    ll2 = model2.loglikeobs(model2_fit.params)
    grad2 =  model2.score_obs(model2_fit.params)    
    hess2 = model2.hessian(model2_fit.params)
    params2 = model2_fit.params
    
    return ll1,grad1,hess1,ll2,params1, grad2,hess2,params2


def regular_test(yn,xn,setup_test):
    ll1,grad1,hess1,ll2,params1, grad2,hess2,params2 = setup_test(yn,xn)
    nobs = ll1.shape[0]
    llr = (ll1 - ll2).sum()
    omega = np.sqrt( (ll1 -ll2).var())
    test_stat = llr/(omega*np.sqrt(nobs))
    return 1*(test_stat >= 1.96) + 2*( test_stat <= -1.96)


# TODO 4: Get Bootstrap test working

def bootstrap_test(yn,xn,setup_test):
    ll1,grad1,hess1,ll2,params1, grad2,hess2,params2 = setup_test(yn,xn)
    nobs = ll1.shape[0]
    test_stats = []
    variance_stats = []
    llr = ll1-ll2
     
    for i in range(trials):
        np.random.seed()
        sample  = np.random.choice(np.arange(0,nobs),nobs,replace=True)
        llrs = llr[sample]
        test_stats.append( llrs.sum() )
        variance_stats.append( llrs.var() )
    
    #final product
    test_stats = np.array(test_stats)
    variance_stats = np.sqrt(variance_stats)*np.sqrt(nobs)
    
    cv_lower = 2*test_stat - np.percentile(test_stats/variance_stats, 97.5, axis=0)
    cv_upper = 2*test_stat -  np.percentile(test_stats/variance_stats, 2.5, axis=0)
    return  2*(0 >= cv_upper) + 1*(0 <= cv_lower)