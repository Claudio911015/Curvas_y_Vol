import numpy as np
import pandas as pd


df_curvesdiff = df_curves.diff()[1:]
df_curvesdiff = df_curves

corr_matrix_array = np.corrcoef(df_curvesdiff.T)
cov_matrix_array = np.cov(df_curvesdiff.T)
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix_array)
eigenvalues = np.real(eigenvalues)
eigenvectors = np.real(eigenvectors)

# Put data into a DataFrame
df_eigval = pd.DataFrame({"Eigenvalues":eigenvalues})

# Work out explained proportion 
df_eigval["Explained proportion"] = df_eigval["Eigenvalues"] / np.sum(df_eigval["Eigenvalues"])
#Format as percentage
df_eigval.style.format({"Explained proportion": "{:.2%}"})

pd.DataFrame(eigenvectors[:,:3],columns=['PCA1','PCA2','PCA3']).plot()