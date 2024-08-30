import scipy.stats as stats
import matplotlib.pyplot as plt

# Data
A = [123, 116, 110, 119, 112, 127, 118, 105, 120, 130]
B = [97, 118, 105, 122, 89, 108, 113, 124, 101, 110]

# QQ plot to check normality
stats.probplot(A, dist="norm", plot=plt)
plt.show()
stats.probplot(B, dist="norm", plot=plt)
plt.show()

# Perform Welch's t-test (two-sample t-test with unequal variances)
t, p = stats.ttest_ind(A, B, equal_var=False, alternative='greater')

# Output the results
print(f"T-statistic: {t:.4f}")
print(f"P-value: {p:.4f}")
