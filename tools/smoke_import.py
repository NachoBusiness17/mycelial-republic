import importlib
m = importlib.import_module('dashboard.rest')
print('ROUTES=', len(getattr(m, 'ROUTES', [])))
