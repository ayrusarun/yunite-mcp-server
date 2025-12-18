#!/usr/bin/env python3
"""
Quick test script for Yunite MCP Server
"""

import asyncio
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")


async def get_token():
    """Get API token"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        response.raise_for_status()
        return response.json()["access_token"]


async def test_endpoints():
    """Test all API endpoints"""
    print(f"🔑 Getting token for {ADMIN_USERNAME}...")
    token = await get_token()
    print(f"   ✅ Token obtained\n")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing API Endpoints\n")
        
        # Test 1: User profile
        print("1. Testing /users/me...")
        try:
            response = await client.get(f"{API_BASE_URL}/users/me", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ User: {data.get('username')} ({data.get('full_name')})")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 2: Departments
        print("\n2. Testing /departments/...")
        try:
            response = await client.get(f"{API_BASE_URL}/departments/", headers=headers)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else data.get('count', 0)
                print(f"   ✅ Found {count} departments")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 3: Programs
        print("\n3. Testing /academic/programs...")
        try:
            response = await client.get(f"{API_BASE_URL}/academic/programs", headers=headers)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else data.get('count', 0)
                print(f"   ✅ Found {count} programs")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 4: Cohorts
        print("\n4. Testing /academic/cohorts...")
        try:
            response = await client.get(f"{API_BASE_URL}/academic/cohorts", headers=headers)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else data.get('count', 0)
                print(f"   ✅ Found {count} cohorts")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 5: Posts
        print("\n5. Testing /posts/...")
        try:
            response = await client.get(f"{API_BASE_URL}/posts/?limit=5", headers=headers)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else data.get('count', 0)
                print(f"   ✅ Found {count} posts")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 6: Sections/Classes
        print("\n6. Testing /academic/classes...")
        try:
            response = await client.get(f"{API_BASE_URL}/academic/classes", headers=headers)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else data.get('count', 0)
                print(f"   ✅ Found {count} sections")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 7: User Groups
        print("\n7. Testing /user-groups/my-groups...")
        try:
            response = await client.get(f"{API_BASE_URL}/user-groups/my-groups", headers=headers)
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else data.get('count', 0)
                print(f"   ✅ Found {count} user groups")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("\n" + "="*50)
        print("✅ All view/list endpoint tests completed!")
        print("="*50)
        
        # Test Create Operations (Optional - commented out to avoid creating test data)
        print("\n📝 Note: Create/Update tools are available but not tested here to avoid")
        print("   creating test data. Available create tools:")
        print("   - create_department")
        print("   - create_program")
        print("   - create_cohort")
        print("   - create_section")
        print("   - create_student")
        print("   - create_staff")
        print("   - create_post")
        print("   - update_user_profile")
        print("\n   Test these via MCP client after server is running.")


if __name__ == "__main__":
    asyncio.run(test_endpoints())
