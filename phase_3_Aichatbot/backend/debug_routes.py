import sys
sys.path.insert(0, '.')

try:
    from main import app
    print('App loaded successfully')
    
    # Check routes
    print(f'Total routes: {len(app.routes)}')
    
    # Look for auth-related routes
    auth_routes = []
    for route in app.routes:
        if hasattr(route, 'path'):
            path = route.path
            if 'auth' in path.lower() or 'login' in path.lower() or 'register' in path.lower():
                auth_routes.append((path, getattr(route, 'methods', 'N/A')))
    
    print(f'Found {len(auth_routes)} auth-related routes:')
    for path, methods in auth_routes:
        print(f'  {path} - {methods}')
        
    # Check for specific login route
    login_route = None
    for route in app.routes:
        if hasattr(route, 'path') and route.path == '/api/login':
            login_route = route
            break
    
    if login_route:
        print(f'Login route found: {login_route.path}')
    else:
        print('Login route NOT found!')
        
except Exception as e:
    print(f'Error loading app: {e}')
    import traceback
    traceback.print_exc()