#!/usr/bin/env python3
"""
Test script to verify admin routes are properly registered
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.main import app

def test_admin_routes():
    """Test if admin routes are properly registered"""
    print("Checking all routes in the application:")

    admin_routes_found = []
    all_routes = []

    for route in app.routes:
        if hasattr(route, 'path'):
            path = route.path
            all_routes.append(path)
            print(f"  {path}")

            if 'admin' in path.lower():
                admin_routes_found.append(path)

    print(f"\nTotal routes found: {len(all_routes)}")
    print(f"Admin routes found: {len(admin_routes_found)}")

    if admin_routes_found:
        print("Admin routes:")
        for route in admin_routes_found:
            print(f"  - {route}")
    else:
        print("NO ADMIN ROUTES FOUND!")

        # Let's also check what routers were included
        print("\nChecking the admin router specifically...")
        from backend.src.api.admin import router as admin_router
        print(f"Admin router prefix: {getattr(admin_router, 'prefix', 'No prefix attribute')}")

        for route in admin_router.routes:
            if hasattr(route, 'path'):
                print(f"  Admin router has: {route.path}")

if __name__ == "__main__":
    test_admin_routes()