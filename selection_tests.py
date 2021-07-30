import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats as stats
import scipy.linalg as linalg
import matplotlib.pyplot as plt

from scipy.optimize import minimize
from scipy.stats import norm

# stats
import statsmodels.api as sm
from statsmodels.base.model import GenericLikelihoodModel

#organization
from shi_test import *


def potential_bidders(df, date_name='Bid Open Date', bidder_name='Bidder Name'):

    df_edit = df.copy()
    df_edit['month_year'] = pd.to_datetime(
        df_edit[date_name]).dt.to_period('M').astype(str)
    new_dict = df_edit.groupby('month_year').apply(
        lambda x: x[bidder_name].unique().tolist()).to_dict()

    delete = ['2013-05', 'NaT']
    # for d in delete:
    #    del new_dict[d]
    # print(len(new_dict))
    print(dict(sorted(new_dict.items())))


def create_panel(df, time_col, cross_col, time_attr, cross_attr):
    """ time_col = name of time column
    cross_col = name of cross-sectional unit column
    attribute_names = x variable data """

    time_units = df[time_col].unique()
    cross_units = df[cross_col].unique()
    # TODO: Modify this so that cross sectional unit has both auction, and bidder

    # create a multi-index with all the units
    panel_index = pd.MultiIndex.from_product(
        [time_units, cross_units], names=[time_col, cross_col])

    # most numerical attributes
    panel = pd.DataFrame(index=panel_index)

    attr_array = df[[time_col, cross_col] + cross_attr].copy()

    # create count and attr / creating a group_by by time units, cross-section units
    attr_array = attr_array.groupby([time_col, cross_col]).mean()
    panel = panel.join(attr_array, how='left')

    # TODO: may need to do 2 merges, first by auction, then by bidder?
    #attr_array = attr_array.groupby([time_col,cross_col]).mean()
    attr_array = attr_array.groupby([time_col, cross_col]).mean()

    #panel = panel.join(attr_array,how='left')

    # Each bid in the auction needs the auction characteristics

    return panel


# TODO 2: Get Tobit working..

class Tobit(GenericLikelihoodModel):

    def __init__(self, *args, ols=False, cc=False, **kwargs):
        super(Tobit, self).__init__(*args, **kwargs)
        self._set_extra_params_names(['var'])
        self.cutoff = stats.mode(self.endog)[0][0]
        #start with OLS as a guess
        init_model = sm.OLS(self.endog[self.endog> self.cutoff] ,self.exog[self.endog > self.cutoff,:]).fit()
        sigma = np.sum(init_model.resid**2)/init_model.resid.shape[0]
        self.start_params = np.concatenate( (init_model.params,[sigma]) )
 
        self.cc = cc
        self.ols = ols
        
    def resid(self, params):
        y = self.endog
        x = self.exog
        m = 1*(self.endog <= self.cutoff) #missingness

        beta = params[0:-1]
        sigma2 = max(params[-1],1e-10)
        
        mu_y = np.matmul(x,beta) #not sure if this is right?
        
        return  (1-m)*(y - mu_y )
        
        
    def loglikeobs(self, params):
        y = self.endog
        x = self.exog
        m = 1*(self.endog <= self.cutoff) #missingness

        beta = params[0:-1]
        sigma2 = max(params[-1],1e-10)
        
        mu_y = np.matmul(x,beta) #not sure if this is right?
    
        pr_y = stats.norm.logpdf( y , loc =  (mu_y), scale=np.sqrt(sigma2))
        #print('pr',y.shape,pr_y.shape)# 
        #print(x.shape)
        #print(y.shape,np.isnan(y).argmax())
        #print(y[np.isnan(pr_y)])

        #if complete case, assign pr missing to all observations...
        pr_m = np.log(max(m.mean(),1e-4))

        if not self.cc:
            pr_m = stats.norm.logcdf( y , loc =  (mu_y) , scale=np.sqrt(sigma2))
        
        #we're done if ols
        if self.ols:
            return pr_y
        else:
            ll = (1-m)*pr_y + m*pr_m
            #print( 'obs: %s, missing: %s'%( (1-m).sum(), m.sum() ) ) 
            #print(('missing ll:%.1f, ols ll: %.1f, seen ll:%.1f')%( (m*pr_m).sum() , ((1-m)*pr_y).sum() , ((1-m)*pr_y + m*pr_m).sum()) )
            return ll
        

# TODO 3: Get LLR test classic version working


def setup_test(yn, xn):
    model1 = Tobit(yn, (xn),cc=True)
    model1_fit = model1.fit(disp=False)
    ll1 = model1.loglikeobs(model1_fit.params)
    grad1 = model1.score_obs(model1_fit.params)
    hess1 = model1.hessian(model1_fit.params)
    params1 = model1_fit.params

    # fit logistic values
    model2 = Tobit(yn, (xn))
    model2_fit = model2.fit(disp=False)
    ll2 = model2.loglikeobs(model2_fit.params)
    grad2 = model2.score_obs(model2_fit.params)
    hess2 = model2.hessian(model2_fit.params)
    params2 = model2_fit.params

    return  ll1, grad1, hess1, params1, ll2, grad2, hess2, params2


def regular_test(yn, xn, setup_test):
    ll1, grad1, hess1, params1, ll2, grad2, hess2, params2 = setup_test(yn, xn)
    nobs = ll1.shape[0]
    llr = (ll1 - ll2).sum()
    omega = np.sqrt((ll1 - ll2).var())
    test_stat = llr/(omega*np.sqrt(nobs))
    print('regular: test, llr, omega ----')
    print(test_stat, llr, omega)
    print('---- ')
    return 1*(test_stat >= 1.96) + 2*(test_stat <= -1.96),test_stat


# helper functions for bootstrap

def compute_eigen2(ll1,grad1,hess1,params1,ll2,grad2,hess2,params2):
    """required for computing bias adjustement for the test"""
    n = ll1.shape[0]
    hess1 = hess1/n
    hess2 = hess2/n

    k1 = params1.shape[0]
    k2 = params2.shape[0]
    k = k1 + k2
    
    #A_hat:
    A_hat1 = np.concatenate([hess1,np.zeros((k2,k1))])
    A_hat2 = np.concatenate([np.zeros((k1,k2)),-1*hess2])
    A_hat = np.concatenate([A_hat1,A_hat2],axis=1)

    #B_hat, covariance of the score...
    B_hat =  np.concatenate([grad1,-grad2],axis=1) #might be a mistake here..
    B_hat = np.cov(B_hat.transpose())

    #compute eigenvalues for weighted chisq
    sqrt_B_hat= linalg.sqrtm(B_hat)
    W_hat = np.matmul(sqrt_B_hat,linalg.inv(A_hat))
    W_hat = np.matmul(W_hat,sqrt_B_hat)
    V,W = np.linalg.eig(W_hat)

    return V


def bootstrap_distr(ll1,grad1,hess1,params1,ll2,grad2,hess2,params2,c=0,trials=500):
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


    #final product, bootstrap
    V =  compute_eigen2(ll1,grad1,hess1,params1,ll2,grad2,hess2,params2)
    test_stats = np.array(test_stats+ V.sum()/(2))
    variance_stats = np.sqrt(np.array(variance_stats)*nobs + c*(V*V).sum())

    #set up test stat   
    omega = np.sqrt((ll1 - ll2).var()*nobs + c*(V*V).sum())
    llr = (ll1 - ll2).sum() +V.sum()/(2)
    print('V ----')
    print(V.sum()/2)
    print('----')
    return test_stats,variance_stats,llr,omega

# TODO 4: Get Bootstrap test working

def bootstrap_test(yn,xn,setup_test,c=0,trials=500):
    ll1,grad1,hess1,params1,ll2,grad2,hess2,params2 = setup_test(yn,xn)

    #set up bootstrap distr
    test_stats,variance_stats,llr,omega  = bootstrap_distr(ll1,grad1,hess1,params1,ll2,grad2,hess2,params2,c=c,trials=trials)
    test_stats = test_stats/variance_stats
    
    #set up confidence intervals
    cv_lower = np.percentile(test_stats, 2.5, axis=0)
    cv_upper = np.percentile(test_stats, 97.5, axis=0)
    print('---- bootstrap: llr, omega ----')
    print(llr,omega)
    print('----')

    return  2*(0 >= cv_upper) + 1*(0 <= cv_lower), cv_lower, cv_upper


def test_table(yn,xn,setup_test, trials=100):
    result_boot, cv_lower, cv_upper = bootstrap_test(yn,xn,setup_test, trials=trials)
    result_class, test_stat = regular_test(yn,xn,setup_test)
    result_shi, stat_shi, cv_shi= ndVuong(yn,xn,setup_test)
    print('\\begin{center}\n\\begin{tabular}{ccc}\n\\toprule')
    print('\\textbf{Version} & \\textbf{Result} & \\textbf{95 \\% CI} \\\\ \\midrule' )
    print('Bootstrap & H%s & [%.3f, %.3f] \\\\'%(result_boot,cv_lower,cv_upper))
    print('Shi (2015) & H%s & [%.3f, %.3f] \\\\'%(result_shi, stat_shi- cv_shi,stat_shi+ cv_shi))
    print('Classical & H%s & [%.3f, %.3f] \\\\'%(result_class,test_stat- 1.959,test_stat+ 1.959))
    print('\\bottomrule\n\\end{tabular}\n\\end{center}')