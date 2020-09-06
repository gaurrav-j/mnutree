# -*- coding: utf-8 -*-
"""The step defs fixtures and hooks
This module contains shared fixtures, steps, and hooks.
"""

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """The error definations
    """
    print(f'Step failed: {step}')
