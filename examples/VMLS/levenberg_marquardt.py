from typing import Callable

from numpy import (array, ndarray, eye, zeros)
from numpy.linalg import (inv, norm)

def solve(x0: ndarray, lm0: float, max_iter: int,
          f: Callable[[ndarray], ndarray], 
          Df: Callable[[ndarray], ndarray],
          eps: float=1e-3, verbose: bool=False):
    
    n = x0.shape[0]

    if verbose:
        soln_traj_x = zeros((n, max_iter+1))
        soln_traj_x[:, 0] = x0.flatten()
        soln_traj_lm = zeros(max_iter)
        soln_traj_lm[0] = lm0
        cost_history = zeros(max_iter+1)
        cost_history[0] = norm(f(x0))**2

    x_k = x0
    lm_k = lm0
    k = 0
    early_termination=False
    
    while k < max_iter:
        k += 1
        
        # Compute tentative iterate
        f_x_k = f(x_k)
        Df_k = Df(x_k)
        H_k = inv(Df_k.T @ Df_k + lm_k*eye(n))
        x_k_potential = x_k - H_k @ Df_k @ f(f_x_k)

        # check stopping criteria
        f_x_k1 = f(x_k_potential)
        norm_fxk1_sq = norm(f_x_k1, 2)**2
        if (norm_fxk1_sq < eps):
            if verbose:
                cost_history[k] = norm_fxk1_sq
                soln_traj_x[:, k] = x_k_potential.flatten()
            x_k = x_k_potential
            early_termination=True
            break
        # potentially include other stopping criteria
        
        # Check tentative iterate
        norm_fxk_sq = norm(f_x_k, 2)**2
        if (norm_fxk1_sq < norm_fxk_sq):
            x_k = x_k_potential
            lm_k = 0.8*lm_k
            if verbose:
                cost_history[k] = norm_fxk1_sq
        else:
            lm_k = 2*lm_k
            if verbose:
                cost_history[k] = norm_fxk_sq

        if verbose:
            soln_traj_x[:, k] = x_k.flatten()
            soln_traj_lm[k] = lm_k
    
    if verbose:
        return (x_k, early_termination, soln_traj_x, soln_traj_lm, cost_history)
    else:
        return (x_k, early_termination)
        
        
