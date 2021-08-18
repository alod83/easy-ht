"""
Help on package easy_ht

NAME
    easy_ht

DESCRIPTION
    Python package for easy Hypothesis Tests

PACKAGE CONTENT
    HypothesisTest (class)
"""

from scipy.stats import shapiro
from scipy.stats import normaltest
from scipy.stats import ttest_1samp
from statsmodels.stats.weightstats import ztest
from statsmodels.sandbox.stats.runs import runstest_1samp 
from scipy.stats import kstest
from scipy.stats import chisquare
from scipy.stats import wilcoxon
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import ttest_rel
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu

class HypothesisTest:
    """
    A class used to calculate Hypothesis Tests, including both one sample and two sample tests.

    ...
    Methods
    -------
    check_normality(self,alpha = 0.05)
        Check if samples are follow a normal distribution, using the Shapiro test.
    check_correlation(self, alpha = 0.05)
        Check if samples are correlated. It can be used only in two samples tests.
    check_randomness(self, alpha = 0.05, cutoff='mean')
        Check if the sample has been built in a random way.
    compare_means(self, value = None, alpha = 0.05, n = 50)
        In one sample test, compare the sample to an expected value. In two samples test, compare the mean of the two samples.
    compare_distributions(self, alpha = 0.05, cdf = None, args=(), freq = False)
        In one sample test, compare the sample to a distribution. In two samples tests, compare the distributions of the two samples.
    """

    def __init__(self,x, y = None, verbose = False, alpha = 0.05):
        """
        Parameters
        ----------
        x : array_like
            the (first) sample to be analysed
        y : array_like, optional
            the second sample to be analysed
        verbose : bool, optional, default = False
            enable debug messages
        alpha : float, optional, default = 0.05
            the significance level
        """
        
        self.is_normal = None
        self.verbose = verbose
        self.x = x
        self.y = y
        
        self.is_normal = self.check_normality(alpha = alpha)
        
    
    def _verbose(self,text):
        """
        Print a text passed as argument

        Parameters
        ----------
        text : str
            the text to be printed 
        """
        if self.verbose:
            print(text)
    
    def _result(self, p, alpha):
        """
        Check if p < alpha

        Parameters
        ----------
        p : float
            p value
        alpha : float
            the significance level

        Returns
        -------
        bool
            False, if reject H0, True, if fail to reject H0
        """

        if p < alpha:
            self._verbose('reject H0')
            return False
        else:
            self._verbose('Fail to reject H0')
            return True
    
    def check_normality(self,alpha = 0.05):
        """
        Check if samples follow a normal distribution, according to the Shapiro test. 
        In case of two samples, check if both the samples follow a normal distribution.

        Parameters
        ----------
        alpha : float, optional, default = 0.05
            the significance level

        Returns
        -------
        bool
            True, if the sample of both the samples follow a normal distribution. False, otherwise.
        """

        stat1, p = shapiro(self.x)
            
        if self.y is not None:
            stat2, p2 = shapiro(self.y)
        
        if p < alpha:
            if self.y is not None:
                if p2 < alpha:
                    self._verbose('x and y do not look Gaussian (reject H0)')
                    return False
                else:
                    self._verbose('x does not look Gaussian, but y looks Gaussian (fail to reject H0)')
                    return True
            else:
                self._verbose('Sample does not look Gaussian (reject H0)')
                return False

        else:
            if self.y is not None:
                if p2 < alpha:
                    self._verbose('x looks Gaussian, but y does not look Gaussian (fail to reject H0)')
                    return False
                else:
                    self._verbose('x and y look Gaussian (fail to reject H0)')
                    return True
            else:
                self._verbose('Sample looks Gaussian (fail to reject H0)')
                return True

    def check_correlation(self, alpha = 0.05):
        """
        Check if samples are correlated. If samples follow a normal distribution, the Pearson Correlation Coefficient is used, otherwise the Spearman Rank Correlation is used. 
        This is a simple test, which does not return the statistics. Correlation is calculated only on the basis of p-value.

        Parameters
        ----------
        alpha : float, optional, default = 0.05
            the significance level

        Returns
        ------
        bool or None
            True, if samples are correlated, False otherwise. 
            None is returned in the case that the second sample has not been set.
        """

        if self.y is None:
            return None
        if len(self.x) != len(self.y):
            return None

        if self.is_normal:
            stat, p = pearsonr(self.x, self.y)
        else:
            stat, p = spearmanr(self.x, self.y)
        
        return self._result(p,alpha)

    def check_randomness(self, alpha = 0.05, cutoff='mean'):
        """
        Check if the sample has been generated in a random way.
    
        Parameters
        ----------
        alpha : float, optional, default = 0.05
            the significance level
        cutoff : {'mean', 'median'} or number, optional, default = 'mean'
            the cutoff to split the data into large and small values.

        Returns
        -------
        bool
            True, if the sample has been generated in a random way. False, otherwise.
        """
        
        stat, p = runstest_1samp(self.x, cutoff=cutoff)
        return self._result(p,alpha)

    def compare_means(self, value = None, alpha = 0.05, n = 50):
        """
        Compare the sample mean to a theoretical value, or compare samples means. 
        If samples follow a normal distribution, the t-test is used if the number of samples is less than n.
        The z-test, otherwise. If the samples are not normal, the Wilcoxon test is used.
        
        Parameters
        ----------
        value : float, optional
            the theoretical value to be compared, in case of one sample
        alpha : float, optional, default = 0.05
            the significance level
        n : int, optional, default = 50
            a number used to discriminate if a sample is small or big. 
            if sample size <= n, t-test is used, otherwise z-test is used.  
        
        Returns
        -------
        bool
            True, if the sample means is similar to the theoretical value or the two samples means are similar. 
            False, otherwise.
        """

        p = None
        if self.y is None:
            # one sample test
            if self.is_normal:
                if len(self.x) <= n:
                    stat, p = ttest_1samp(self.x, value)
                else:
                    stat, p = ztest(self.x, value = value)
            else:
                stat, p = wilcoxon(self.x - value)
        else:
            if self.is_normal:
                if len(self.x) <= n:
                    if paired:
                        stat, p = ttest_rel(self.x, self.y)
                    else:
                        stat, p = ttest_ind(self.x, self.y)
                else:
                    stat, p = ztest(self.x, self.y)
            else:
                if paired:
                    stat, p = wilcoxon(self.x, self.y)
                else:
                    stat, p = mannwhitneyu(self.x, self.y)

        return self._result(p,alpha)

    def compare_distributions(self, alpha = 0.05, cdf = None, args=(), freq = False):
        """
        Compare the sample distribution to a given cdf (cumulative distribution function), if one sample is provided.
        The Kolmogorov-Smirnov Test is used.
        Compare the samples distribution, if two samples are provided. 
        In this case, the Chi Square test is used.

        Parameters
        ----------
        alpha : float, optional, default = 0.05
            the significance level
        cdf : str, array_like or callable
            if array_like, it is an array of observations of random variables, and the two-sample test is performed. 
            If a callable, that callable is used to calculate the cdf. 
            If a string, it should be the name of a distribution in scipy.stats, which will be used as the cdf function. 
        args : tuple, sequence, optional
            distribution parameters, used cdf is string or callables.
        freq : bool, optional, default = False
            specify if the sample is an array of frequencies. 
            This is used to discriminate if using the Chi Square Test or Kolmogorov-Smirnov Test.
        
        Returns
        -------
        bool or None
            True, if the sample follows the specified distribution or the two samples follow the same distribution. 
            False, otherwise. If error, return None.
        """

        if freq:
            if self.y is not None:
                stat, p = chisquare(self.x, f_exp = self.y)
            else:
                return None
        else:
            if cdf is not None:
                stat, p = kstest(self.x, cdf = cdf, args=args)
            else:
                if self.y is not None:
                    stat, p = kstest(self.x, cdf = self.y)
                else:
                    return None

        return self._result(p,alpha)

    


    