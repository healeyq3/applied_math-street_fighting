from numpy import (ndarray, array, all, abs, zeros)
from numpy.linalg import (eig)
import cvxpy as cp

'''
Functions:
- Determine stability
- simulate LTI
- plots
- determine stability
- Linear Quadratic Control

'''

def is_open_loop_stable(A: ndarray) -> tuple[bool, ndarray]:
    """
    Determines if the *discrete time* LTI system
    x_t+1 = Ax_t + Bu_t
    is asympotically stable for u_t \equiv 0.

    Note that this function is very simple and assumes
    that A can be diagonalized.

    Returns
    -------
    tuple[bool, ndarray]
        bool : whether the system governed by A is asymptotically stable
        ndarray : associated eigenvalues
    """
    eigvals, eigvecs = eig(A)
    if all(abs(eigvals) < 1):
        return True, eigvals
    else:
        return False, eigvals

def simulate(A: ndarray, B: array, epoch, T, x_init, u_t):
    """
    cannot handle feedback

    assumes x_init is (n, 1) ndarray (or doesn't matter)

    give possibility to pass in C?

    """
    
    n = A.shape[0]
    m = B.shape[1]
    x_t = x_init

    num_steps = int(epoch * T)
    state_history = zeros((n, num_steps+1))
    state_history[:, 0] = x_t.flatten()

    for step in range(num_steps):
        x_t = A@x_t + (B @ u_t[:, step]).reshape(n, 1)
        state_history[:, step+1] = x_t.flatten()
    
    return state_history
    
def solve_lqr(A, B, C, T, x_init, y_des):
    """
    Future Features
    ----------------
    - adding additional constraints: refactor into class
    - 
    """

    n = A.shape[0]
    m = B.shape[1]
    
    x0 = cp.Parameter((n, 1), value=x_init)
    
    u = cp.Variable((m, T))
    x = cp.Variable((n, T+1))

    J_output = cp.sum_squares(C@x)
    J_input = cp.sum_squares(u)
    # J_tracking
