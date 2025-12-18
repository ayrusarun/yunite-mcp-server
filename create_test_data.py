#!/usr/bin/env python3
"""
Create test data for Yunite MCP Server
Creates sample departments, programs, cohorts, sections, and users
"""

import asyncio
import httpx
from dotenv import load_dotenv
import os
import json

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


async def get_headers(token):
    """Get headers with token"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


async def get_user_info(token):
    """Get current user info to extract college_id"""
    async with httpx.AsyncClient() as client:
        headers = await get_headers(token)
        response = await client.get(f"{API_BASE_URL}/users/me", headers=headers)
        response.raise_for_status()
        return response.json()


async def create_test_data():
    """Create comprehensive test data"""
    print("🚀 Starting Test Data Creation")
    print("="*60)
    
    # Get token and user info
    print("\n1️⃣  Getting authentication token...")
    token = await get_token()
    headers = await get_headers(token)
    user_info = await get_user_info(token)
    college_id = user_info.get("college_id")
    print(f"   ✅ Authenticated as: {user_info.get('full_name')} ({user_info.get('username')})")
    print(f"   College ID: {college_id}")
    
    async with httpx.AsyncClient() as client:
        
        # Create Test Department
        print("\n2️⃣  Creating Test Department...")
        dept_data = {
            "name": "Test Department - Data Science",
            "code": "TEST-DS",
            "description": "Test department for data science programs",
            "is_active": True
        }
        try:
            response = await client.post(
                f"{API_BASE_URL}/departments/",
                headers=headers,
                json=dept_data
            )
            if response.status_code in [200, 201]:
                dept = response.json()
                dept_id = dept.get("id")
                print(f"   ✅ Created Department: {dept.get('name')} (ID: {dept_id})")
            else:
                print(f"   ⚠️  Department creation: {response.status_code} - {response.text}")
                # Try to find existing department
                response = await client.get(f"{API_BASE_URL}/departments/", headers=headers)
                depts = response.json()
                test_dept = next((d for d in depts if d.get("code") == "TEST-DS"), None)
                if test_dept:
                    dept_id = test_dept.get("id")
                    print(f"   ℹ️  Using existing department (ID: {dept_id})")
                else:
                    print("   ❌ Cannot proceed without department")
                    return
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Use existing program
        print("\n3️⃣  Getting existing programs...")
        try:
            response = await client.get(
                f"{API_BASE_URL}/academic/programs",
                headers=headers
            )
            programs = response.json() if response.status_code == 200 else []
            
            if not programs:
                print("   ❌ No programs found. Please create a program first.")
                return
            
            # Use the first available program
            program = programs[0]
            program_id = program.get("id")
            dept_id = program.get("department_id")
            print(f"   ✅ Using program: {program.get('name')} (ID: {program_id})")
            print(f"      Department ID: {dept_id}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Use existing cohort
        print("\n4️⃣  Getting existing cohorts...")
        try:
            response = await client.get(
                f"{API_BASE_URL}/academic/cohorts",
                headers=headers
            )
            cohorts = response.json() if response.status_code == 200 else []
            
            if not cohorts:
                print("   ❌ No cohorts found. Please create a cohort first.")
                return
            
            # Use the first available cohort for the program
            cohort = next((c for c in cohorts if c.get("program_id") == program_id), cohorts[0])
            cohort_id = cohort.get("id")
            print(f"   ✅ Using cohort: {cohort.get('name')} (ID: {cohort_id})")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Get existing sections
        print("\n5️⃣  Getting existing sections...")
        try:
            response = await client.get(
                f"{API_BASE_URL}/academic/classes",
                headers=headers
            )
            sections = response.json() if response.status_code == 200 else []
            
            if not sections:
                print("   ❌ No sections found. Please create sections first.")
                return
            
            # Filter sections for this cohort
            cohort_sections = [s for s in sections if s.get("cohort_id") == cohort_id]
            if not cohort_sections:
                print(f"   ⚠️  No sections for cohort {cohort_id}, using any available section")
                cohort_sections = sections[:2]  # Use first 2 sections
            
            sections = cohort_sections
            print(f"   ✅ Found {len(sections)} sections for this cohort")
            for section in sections[:2]:
                print(f"      - {section.get('section_name')} (ID: {section.get('id')})")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Create Test Students
        print("\n6️⃣  Creating Test Students...")
        students_created = 0
        for i in range(1, 4):  # Create 3 test students
            student_data = {
                "username": f"test_student_{i}",
                "email": f"test.student{i}@test.edu",
                "full_name": f"Test Student {i}",
                "password": "test123",
                "college_id": college_id,
                "department_id": dept_id,
                "program_id": program_id,
                "cohort_id": cohort_id,
                "class_id": sections[i % len(sections)].get("id"),
                "admission_year": 2025
            }
            try:
                response = await client.post(
                    f"{API_BASE_URL}/admin/users",
                    headers=headers,
                    json=student_data
                )
                if response.status_code in [200, 201]:
                    student = response.json()
                    print(f"   ✅ Created Student: {student.get('full_name')} ({student.get('username')})")
                    students_created += 1
                else:
                    print(f"   ⚠️  Student {i} creation: {response.status_code} - {response.text[:100]}")
            except Exception as e:
                print(f"   ❌ Error creating student {i}: {e}")
        
        # Create Test Staff
        print("\n7️⃣  Creating Test Staff...")
        staff_data = {
            "username": "test_faculty_1",
            "email": "test.faculty@test.edu",
            "full_name": "Test Faculty Member",
            "password": "test123",
            "college_id": college_id,
            "department_id": dept_id,
            "role": "faculty"
        }
        try:
            response = await client.post(
                f"{API_BASE_URL}/admin/users",
                headers=headers,
                json=staff_data
            )
            if response.status_code in [200, 201]:
                staff = response.json()
                print(f"   ✅ Created Staff: {staff.get('full_name')} ({staff.get('username')})")
            else:
                print(f"   ⚠️  Staff creation: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"   ❌ Error creating staff: {e}")
        
        # Create Test Post
        print("\n8️⃣  Creating Test Post...")
        post_data = {
            "title": "Welcome to Test Department!",
            "content": "This is a test post created by the test data script. Welcome all test students to the Data Science program!"
        }
        try:
            response = await client.post(
                f"{API_BASE_URL}/posts/",
                headers=headers,
                json=post_data
            )
            if response.status_code in [200, 201]:
                post = response.json()
                print(f"   ✅ Created Post: {post.get('title')}")
            else:
                print(f"   ⚠️  Post creation: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error creating post: {e}")
    
    print("\n" + "="*60)
    print("✅ Test Data Creation Complete!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   - Department: Test Department - Data Science (ID: {dept_id})")
    print(f"   - Program: Master of Data Science (ID: {program_id})")
    print(f"   - Cohort: MDS Test Batch 2025 (ID: {cohort_id})")
    print(f"   - Sections: {len(sections)} created")
    print(f"   - Students: {students_created} created")
    print(f"   - Staff: 1 faculty member")
    print(f"   - Posts: 1 announcement")
    print("\n🔐 Test User Credentials:")
    print("   Username: test_student_1, test_student_2, test_student_3")
    print("   Username: test_faculty_1")
    print("   Password: test123")


if __name__ == "__main__":
    asyncio.run(create_test_data())
