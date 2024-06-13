
"""
Auto-generated by CVXPYgen on June 12, 2024 at 14:41:56.
Content: Custom solve method for CVXPY interface.
"""

import time
import warnings
import numpy as np
from cvxpy.reductions import Solution
from cvxpy.problems.problem import SolverStats
from mpc_controller import cpg_module


standard_settings_names = {"max_iters": "maxit"}


def cpg_solve(prob, updated_params=None, **kwargs):

    # set flags for updated parameters
    upd = cpg_module.cpg_updated()
    if updated_params is None:
        updated_params = ["param9284", "param9283"]
    for p in updated_params:
        try:
            setattr(upd, p, True)
        except AttributeError:
            raise AttributeError(f"{p} is not a parameter.")

    # set solver settings
    cpg_module.set_solver_default_settings()
    for key, value in kwargs.items():
        try:
            eval(f'cpg_module.set_solver_{standard_settings_names.get(key, key)}(value)')
        except AttributeError:
            raise AttributeError(f'Solver setting "{key}" not available.')

    # set parameter values
    par = cpg_module.cpg_params()
    param_dict = prob.param_dict
    par.param9284 = list(param_dict["param9284"].value.flatten(order="F"))
    par.param9283 = list(param_dict["param9283"].value.flatten(order="F"))

    # solve
    t0 = time.time()
    res = cpg_module.solve(upd, par)
    t1 = time.time()

    # store solution in problem object
    prob._clear_solution()
    prob.var_dict['var9281'].save_value(np.array(res.cpg_prim.var9281).reshape((3, 13), order='F'))
    prob.var_dict['var9282'].save_value(np.array(res.cpg_prim.var9282).reshape((1, 12), order='F'))
    prob.constraints[0].save_dual_value(np.array(res.cpg_dual.d0).reshape(3))
    prob.constraints[1].save_dual_value(np.array(res.cpg_dual.d1).reshape(3))
    prob.constraints[2].save_dual_value(np.array(res.cpg_dual.d2))
    prob.constraints[3].save_dual_value(np.array(res.cpg_dual.d3).reshape(3))
    prob.constraints[4].save_dual_value(np.array(res.cpg_dual.d4))
    prob.constraints[5].save_dual_value(np.array(res.cpg_dual.d5).reshape(3))
    prob.constraints[6].save_dual_value(np.array(res.cpg_dual.d6))
    prob.constraints[7].save_dual_value(np.array(res.cpg_dual.d7).reshape(3))
    prob.constraints[8].save_dual_value(np.array(res.cpg_dual.d8))
    prob.constraints[9].save_dual_value(np.array(res.cpg_dual.d9).reshape(3))
    prob.constraints[10].save_dual_value(np.array(res.cpg_dual.d10))
    prob.constraints[11].save_dual_value(np.array(res.cpg_dual.d11).reshape(3))
    prob.constraints[12].save_dual_value(np.array(res.cpg_dual.d12))
    prob.constraints[13].save_dual_value(np.array(res.cpg_dual.d13).reshape(3))
    prob.constraints[14].save_dual_value(np.array(res.cpg_dual.d14))
    prob.constraints[15].save_dual_value(np.array(res.cpg_dual.d15).reshape(3))
    prob.constraints[16].save_dual_value(np.array(res.cpg_dual.d16))
    prob.constraints[17].save_dual_value(np.array(res.cpg_dual.d17).reshape(3))
    prob.constraints[18].save_dual_value(np.array(res.cpg_dual.d18))
    prob.constraints[19].save_dual_value(np.array(res.cpg_dual.d19).reshape(3))
    prob.constraints[20].save_dual_value(np.array(res.cpg_dual.d20))
    prob.constraints[21].save_dual_value(np.array(res.cpg_dual.d21).reshape(3))
    prob.constraints[22].save_dual_value(np.array(res.cpg_dual.d22))
    prob.constraints[23].save_dual_value(np.array(res.cpg_dual.d23).reshape(3))
    prob.constraints[24].save_dual_value(np.array(res.cpg_dual.d24))

    # store additional solver information in problem object
    prob._status = "%d (for description visit https://github.com/embotech/ecos/wiki/Usage-from-C)" % res.cpg_info.status
    if abs(res.cpg_info.obj_val) == 1e30:
        prob._value = np.sign(res.cpg_info.obj_val) * np.inf
    else:
        prob._value = res.cpg_info.obj_val
    primal_vars = {var.id: var.value for var in prob.variables()}
    dual_vars = {c.id: c.dual_value for c in prob.constraints}
    solver_specific_stats = {'obj_val': res.cpg_info.obj_val,
                             'status': prob._status,
                             'iter': res.cpg_info.iter,
                             'pri_res': res.cpg_info.pri_res,
                             'dua_res': res.cpg_info.dua_res,
                             'time': res.cpg_info.time}
    attr = {'solve_time': t1 - t0, 'solver_specific_stats': solver_specific_stats, 'num_iters': res.cpg_info.iter}
    prob._solution = Solution(prob.status, prob.value, primal_vars, dual_vars, attr)
    results_dict = {'solver_specific_stats': solver_specific_stats,
                    'num_iters': res.cpg_info.iter,
                    'solve_time': t1 - t0}
    prob._solver_stats = SolverStats(results_dict, 'ECOS')

    return prob.value
