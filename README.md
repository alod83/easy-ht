
# Easy Hypothesis Test

A Python package for easy Hypothesis Tests
## Authors

- [@alod83](https://www.github.com/alod83)

  
## Installation

Install my-project with npm

```bash
  pip install easy-ht
```

## Requirements

* scipy
* statsmodels
* jupyter-lab (optional)
    
## Usage/Examples

For examples, check the folder examples, containing some Jupyter Notebooks to get started.

  
## Documentation

The easy_ht package contains a basic class, called `HypothesisTest`.

### HypothesisTest

A class used to calculate Hypothesis Tests, including both one sample and two sample tests.


**Methods**

* **check_normality(self,alpha = 0.05)** Check if samples follow a normal distribution, using the Shapiro test.
* **check_correlation(self, alpha = 0.05)**
        Check if samples are correlated. It can be used only in two samples tests.
* **check_randomness(self, alpha = 0.05, cutoff='mean')**
        Check if the sample has been built in a random way.
* **compare_means(self, value = None, alpha = 0.05, n = 50)**
        In one sample test, compare the sample to an expected value. In two samples test, compare the mean of the two samples.
* **compare_distributions(self, alpha = 0.05, cdf = None, args=(), freq = False)**
        In one sample test, compare the sample to a distribution. In two samples tests, compare the distributions of the two samples.

#### __init__(self,x, y = None, verbose = False, alpha = 0.05):
**Parameters**
* **x : array_like**
the (first) sample to be analysed
       
*  **y : array_like, optional**
the second sample to be analysed

* **verbose : bool, optional, default = False**
enable debug messages

* **alpha : float, optional, default = 0.05****
the significance level

#### check_normality(self,alpha = 0.05)
Check if samples follow a normal distribution, according to the Shapiro test. 
In case of two samples, check if both the samples follow a normal distribution.

**Parameters**

* **alpha : float, optional, default = 0.05**
the significance level

**Returns**

* bool

True, if the sample of both the samples follow a normal distribution. False, otherwise.

### check_correlation(self, alpha = 0.05)
Check if samples are correlated. If samples follow a normal distribution, the Pearson Correlation Coefficient is used, otherwise the Spearman Rank Correlation is used. 
This is a simple test, which does not return the statistics. Correlation is calculated only on the basis of p-value.

**Parameters**

* **alpha : float, optional, default = 0.05**
the significance level

**Returns**
* bool or None

True, if samples are correlated, False otherwise. 
None is returned in the case that the second sample has not been set.

### check_randomness(self, alpha = 0.05, cutoff='mean'):
Check if the sample has been generated in a random way.
    
**Parameters**

* **alpha : float, optional, default = 0.05**
the significance level

* **cutoff : {'mean', 'median'} or number, optional, default = 'mean'**
the cutoff to split the data into large and small values.

**Returns**
* bool

True, if the sample has been generated in a random way. False, otherwise.

### compare_means(self, value = None, alpha = 0.05, n = 50)
Compare the sample mean to a theoretical value, or compare samples means. 
If samples follow a normal distribution, the t-test is used if the number of samples is less than n.
The z-test, otherwise. If the samples are not normal, the Wilcoxon test is used.
        
**Parameters**

* **value : float, optional**
the theoretical value to be compared, in case of one sample

* **alpha : float, optional, default = 0.05**
the significance level
* **n : int, optional, default = 50**
a number used to discriminate if a sample is small or big. 
if sample size <= n, t-test is used, otherwise z-test is used.  

**Returns**
* bool
True, if the sample means is similar to the theoretical value or the two samples means are similar. 
False, otherwise.
  
### compare_distributions(self, alpha = 0.05, cdf = None, args=(), freq = False):
Compare the sample distribution to a given cdf (cumulative distribution function), if one sample is provided.
The Kolmogorov-Smirnov Test is used.
Compare the samples distribution, if two samples are provided. 
In this case, the Chi Square test is used.

**Parameters**
* **alpha : float, optional, default = 0.05**
the significance level

* **cdf : str, array_like or callable**
if array_like, it is an array of observations of random variables, and the two-sample test is performed. 
If a callable, that callable is used to calculate the cdf. 
If a string, it should be the name of a distribution in scipy.stats, which will be used as the cdf function. 
        
* **args : tuple, sequence, optional**
distribution parameters, used cdf is string or callables.

* **freq : bool, optional, default = False**
specify if the sample is an array of frequencies. 
This is used to discriminate if using the Chi Square Test or Kolmogorov-Smirnov Test.
        
**Returns**

* bool or None
True, if the sample follows the specified distribution or the two samples follow the same distribution. 
False, otherwise. If error, return None.
