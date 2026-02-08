#!/usr/bin/env python3
"""
Script to verify deployment is working correctly
Run this after deploying to test all endpoints
"""
import requests
import sys
import json
from datetime import date

def test_endpoint(method, url, data=None, description=""):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, timeout=10)
        
        print(f"✓ {description}")
        print(f"  Status: {response.status_code}")
        if response.status_code < 400:
            print(f"  Response: {json.dumps(response.json(), indent=2)[:200]}...")
        else:
            print(f"  Error: {response.text[:200]}")
        print()
        return response
    except Exception as e:
        print(f"✗ {description}")
        print(f"  Error: {str(e)}")
        print()
        return None

def main():
    # Get API URL from command line or use default
    api_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"Testing API at: {api_url}\n")
    print("=" * 60)
    print()
    
    # Test health check
    test_endpoint("GET", f"{api_url}/health", description="Health Check")
    
    # Test root endpoint
    test_endpoint("GET", f"{api_url}/", description="API Info")
    
    # Test getting employees (should be empty initially)
    employees_response = test_endpoint("GET", f"{api_url}/api/employees", description="Get All Employees")
    
    # Test creating an employee
    test_employee = {
        "employee_id": "TEST001",
        "full_name": "Test Employee",
        "email": "test@example.com",
        "department": "Testing"
    }
    create_response = test_endpoint("POST", f"{api_url}/api/employees", data=test_employee, description="Create Employee")
    
    if create_response and create_response.status_code == 201:
        employee_id = create_response.json().get("id")
        
        # Test getting single employee
        test_endpoint("GET", f"{api_url}/api/employees/{employee_id}", description="Get Single Employee")
        
        # Test marking attendance
        attendance_data = {
            "employee_id": employee_id,
            "attendance_date": str(date.today()),
            "status": "Present"
        }
        test_endpoint("POST", f"{api_url}/api/attendance", data=attendance_data, description="Mark Attendance")
        
        # Test getting employees with attendance
        test_endpoint("GET", f"{api_url}/api/attendance/employees-with-attendance?attendance_date={date.today()}", description="Get Employees with Attendance")
        
        # Test getting attendance records
        test_endpoint("GET", f"{api_url}/api/attendance?attendance_date={date.today()}", description="Get Attendance Records")
        
        # Clean up - delete test employee
        test_endpoint("DELETE", f"{api_url}/api/employees/{employee_id}", description="Delete Test Employee")
    
    print("=" * 60)
    print("\nDeployment verification complete!")
    print(f"\nAPI Documentation: {api_url}/docs")

if __name__ == "__main__":
    main()

