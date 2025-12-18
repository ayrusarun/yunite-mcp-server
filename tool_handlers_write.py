"""
Tool call handlers for write operations
Maps tool names to API endpoints for POST, PUT, PATCH, DELETE operations
"""

async def handle_write_tool_call(name: str, arguments: dict, make_api_request):
    """
    Route write tool calls to appropriate API endpoints
    Returns result dict from API
    """
    
    # ==================== POSTS ====================
    if name == "create_post":
        data = {"content": arguments["content"], "title": arguments.get("title")}
        return await make_api_request("POST", "/posts/", data=data)
    
    elif name == "update_post":
        post_id = arguments["post_id"]
        data = {k: v for k, v in arguments.items() if k != "post_id" and v is not None}
        return await make_api_request("PUT", f"/posts/{post_id}", data=data)
    
    elif name == "update_post_metadata":
        post_id = arguments["post_id"]
        return await make_api_request("PATCH", f"/posts/{post_id}/metadata", data=arguments["metadata"])
    
    elif name == "create_post_alert":
        post_id = arguments["post_id"]
        data = {"alert_title": arguments["alert_title"], "alert_message": arguments.get("alert_message")}
        return await make_api_request("POST", f"/posts/{post_id}/alert", data=data)
    
    # ==================== ENGAGEMENT ====================
    elif name == "add_comment":
        post_id = arguments["post_id"]
        data = {"content": arguments["content"]}
        return await make_api_request("POST", f"/posts/{post_id}/comments", data=data)
    
    elif name == "delete_comment":
        post_id = arguments["post_id"]
        comment_id = arguments["comment_id"]
        return await make_api_request("DELETE", f"/posts/{post_id}/comments/{comment_id}")
    
    elif name == "toggle_like":
        post_id = arguments["post_id"]
        return await make_api_request("POST", f"/posts/{post_id}/like")
    
    elif name == "toggle_ignite":
        post_id = arguments["post_id"]
        return await make_api_request("POST", f"/posts/{post_id}/ignite")
    
    # ==================== DEPARTMENTS ====================
    elif name == "create_department":
        data = {
            "name": arguments["name"],
            "code": arguments["code"],
            "description": arguments.get("description"),
            "is_active": arguments.get("is_active", True)
        }
        return await make_api_request("POST", "/departments/", data=data)
    
    elif name == "update_department":
        dept_id = arguments["department_id"]
        data = {k: v for k, v in arguments.items() if k != "department_id" and v is not None}
        return await make_api_request("PUT", f"/departments/{dept_id}", data=data)
    
    elif name == "deactivate_department":
        dept_id = arguments["department_id"]
        return await make_api_request("DELETE", f"/departments/{dept_id}")
    
    elif name == "activate_department":
        dept_id = arguments["department_id"]
        return await make_api_request("POST", f"/departments/{dept_id}/activate")
    
    # ==================== ACADEMIC MANAGEMENT ====================
    elif name == "create_academic_year":
        data = {
            "year_name": arguments["year_name"],
            "start_date": arguments["start_date"],
            "end_date": arguments["end_date"],
            "is_active": arguments.get("is_active", False)
        }
        return await make_api_request("POST", "/academic/years", data=data)
    
    elif name == "update_academic_year":
        year_id = arguments["year_id"]
        data = {k: v for k, v in arguments.items() if k != "year_id" and v is not None}
        return await make_api_request("PUT", f"/academic/years/{year_id}", data=data)
    
    elif name == "activate_academic_year":
        year_id = arguments["year_id"]
        return await make_api_request("POST", f"/academic/years/{year_id}/activate")
    
    elif name == "create_program":
        data = {
            "college_id": arguments["college_id"],
            "department_id": arguments["department_id"],
            "code": arguments["code"],
            "name": arguments["name"],
            "short_name": arguments.get("short_name"),
            "duration_years": arguments["duration_years"],
            "description": arguments.get("description"),
            "is_active": arguments.get("is_active", True)
        }
        return await make_api_request("POST", "/academic/programs", data=data)
    
    elif name == "update_program":
        program_id = arguments["program_id"]
        data = {k: v for k, v in arguments.items() if k != "program_id" and v is not None}
        return await make_api_request("PUT", f"/academic/programs/{program_id}", data=data)
    
    elif name == "create_cohort":
        data = {
            "college_id": arguments["college_id"],
            "program_id": arguments["program_id"],
            "admission_year": arguments["admission_year"],
            "code": arguments["code"],
            "name": arguments["name"],
            "expected_graduation_year": arguments.get("expected_graduation_year"),
            "current_semester": arguments.get("current_semester", 1),
            "is_active": arguments.get("is_active", True)
        }
        return await make_api_request("POST", "/academic/cohorts", data=data)
    
    elif name == "update_cohort":
        cohort_id = arguments["cohort_id"]
        data = {k: v for k, v in arguments.items() if k != "cohort_id" and v is not None}
        return await make_api_request("PUT", f"/academic/cohorts/{cohort_id}", data=data)
    
    elif name == "create_class":
        data = {
            "college_id": arguments["college_id"],
            "cohort_id": arguments["cohort_id"],
            "program_id": arguments["program_id"],
            "section_code": arguments["section_code"],
            "section_name": arguments.get("section_name"),
            "capacity": arguments.get("capacity"),
            "is_active": arguments.get("is_active", True)
        }
        return await make_api_request("POST", "/academic/classes", data=data)
    
    elif name == "update_class":
        class_id = arguments["class_id"]
        data = {k: v for k, v in arguments.items() if k != "class_id" and v is not None}
        return await make_api_request("PUT", f"/academic/classes/{class_id}", data=data)
    
    elif name == "assign_teacher_to_class":
        data = {
            "class_id": arguments["class_id"],
            "teacher_id": arguments["teacher_id"],
            "subject": arguments.get("subject")
        }
        return await make_api_request("POST", "/academic/class-teachers", data=data)
    
    elif name == "remove_teacher_from_class":
        assignment_id = arguments["assignment_id"]
        return await make_api_request("DELETE", f"/academic/class-teachers/{assignment_id}")
    
    # ==================== ADMIN & USER MANAGEMENT ====================
    elif name == "create_student":
        data = {
            "username": arguments["username"],
            "email": arguments["email"],
            "full_name": arguments["full_name"],
            "password": arguments["password"],
            "role": "student",
            "college_id": arguments["college_id"],
            "department_id": arguments["department_id"],
            "program_id": arguments["program_id"],
            "cohort_id": arguments["cohort_id"],
            "class_id": arguments["class_id"],
            "admission_year": arguments["admission_year"]
        }
        return await make_api_request("POST", "/admin/users", data=data)
    
    elif name == "create_staff":
        data = {
            "username": arguments["username"],
            "email": arguments["email"],
            "full_name": arguments["full_name"],
            "password": arguments["password"],
            "role": arguments.get("role", "staff"),
            "college_id": arguments["college_id"],
            "department_id": arguments.get("department_id")
        }
        return await make_api_request("POST", "/admin/users", data=data)
    
    elif name == "update_user_profile":
        user_id = arguments["user_id"]
        data = {k: v for k, v in arguments.items() if k != "user_id" and v is not None}
        return await make_api_request("PUT", f"/users/{user_id}", data=data)
    
    elif name == "update_user_role":
        user_id = arguments["user_id"]
        data = {"role": arguments["role"]}
        return await make_api_request("PUT", f"/admin/users/{user_id}/role", data=data)
    
    elif name == "update_user_status":
        user_id = arguments["user_id"]
        data = {"status": arguments["status"]}
        return await make_api_request("PUT", f"/admin/users/{user_id}/status", data=data)
    
    elif name == "delete_user":
        user_id = arguments["user_id"]
        return await make_api_request("DELETE", f"/admin/users/{user_id}")
    
    elif name == "grant_permission":
        user_id = arguments["user_id"]
        data = {
            "permission_name": arguments["permission_name"],
            "grant": arguments.get("grant", True)
        }
        return await make_api_request("POST", f"/admin/users/{user_id}/permissions", data=data)
    
    elif name == "remove_permission":
        user_id = arguments["user_id"]
        permission_name = arguments["permission_name"]
        return await make_api_request("DELETE", f"/admin/users/{user_id}/permissions/{permission_name}")
    
    # ==================== GROUPS ====================
    elif name == "create_group":
        data = {
            "name": arguments["name"],
            "description": arguments.get("description"),
            "is_public": arguments.get("is_public", True),
            "group_type": arguments.get("group_type")
        }
        return await make_api_request("POST", "/groups/", data=data)
    
    elif name == "update_group":
        group_id = arguments["group_id"]
        data = {k: v for k, v in arguments.items() if k != "group_id" and v is not None}
        return await make_api_request("PUT", f"/groups/{group_id}", data=data)
    
    elif name == "delete_group":
        group_id = arguments["group_id"]
        return await make_api_request("DELETE", f"/groups/{group_id}")
    
    elif name == "join_group":
        group_id = arguments["group_id"]
        return await make_api_request("POST", f"/groups/{group_id}/join")
    
    elif name == "add_group_member":
        group_id = arguments["group_id"]
        data = {
            "user_id": arguments["user_id"],
            "role": arguments.get("role", "member")
        }
        return await make_api_request("POST", f"/groups/{group_id}/members", data=data)
    
    elif name == "update_group_member_role":
        group_id = arguments["group_id"]
        user_id = arguments["user_id"]
        data = {"role": arguments["role"]}
        return await make_api_request("PUT", f"/groups/{group_id}/members/{user_id}", data=data)
    
    elif name == "remove_group_member":
        group_id = arguments["group_id"]
        user_id = arguments["user_id"]
        return await make_api_request("DELETE", f"/groups/{group_id}/members/{user_id}")
    
    # ==================== ALERTS ====================
    elif name == "create_alert":
        data = {
            "title": arguments["title"],
            "message": arguments["message"],
            "alert_type": arguments.get("alert_type"),
            "user_ids": arguments.get("user_ids", [])
        }
        return await make_api_request("POST", "/alerts/", data=data)
    
    elif name == "create_group_alert":
        data = {
            "title": arguments["title"],
            "message": arguments["message"],
            "group_id": arguments["group_id"],
            "alert_type": arguments.get("alert_type")
        }
        return await make_api_request("POST", "/alerts/group-alerts", data=data)
    
    elif name == "update_alert":
        alert_id = arguments["alert_id"]
        data = {k: v for k, v in arguments.items() if k != "alert_id" and v is not None}
        return await make_api_request("PUT", f"/alerts/{alert_id}", data=data)
    
    elif name == "delete_alert":
        alert_id = arguments["alert_id"]
        return await make_api_request("DELETE", f"/alerts/{alert_id}")
    
    elif name == "mark_all_alerts_read":
        return await make_api_request("POST", "/alerts/mark-all-read")
    
    # ==================== AUTHENTICATION ====================
    elif name == "login":
        data = {"username": arguments["username"], "password": arguments["password"]}
        return await make_api_request("POST", "/auth/login", data=data)
    
    elif name == "logout":
        return await make_api_request("POST", "/auth/logout")
    
    elif name == "update_password":
        data = {
            "current_password": arguments["current_password"],
            "new_password": arguments["new_password"]
        }
        return await make_api_request("PUT", "/auth/update-password", data=data)
    
    # ==================== REWARDS ====================
    elif name == "give_reward":
        data = {
            "user_id": arguments["user_id"],
            "points": arguments["points"],
            "reason": arguments.get("reason")
        }
        return await make_api_request("POST", "/rewards/", data=data)
    
    elif name == "credit_pool":
        data = {
            "points": arguments["points"],
            "description": arguments.get("description")
        }
        return await make_api_request("POST", "/pool/credit", data=data)
    
    # ==================== FILES ====================
    elif name == "upload_file":
        data = {
            "file_name": arguments["file_name"],
            "file_data": arguments["file_data"],
            "folder_id": arguments.get("folder_id")
        }
        return await make_api_request("POST", "/files/upload", data=data)
    
    elif name == "create_folder":
        data = {
            "name": arguments["name"],
            "parent_folder_id": arguments.get("parent_folder_id")
        }
        return await make_api_request("POST", "/files/folders/create", data=data)
    
    elif name == "delete_folder":
        data = {"folder_id": arguments["folder_id"]}
        return await make_api_request("DELETE", "/files/folders/delete", data=data)
    
    elif name == "move_folder":
        data = {
            "folder_id": arguments["folder_id"],
            "new_parent_id": arguments["new_parent_id"]
        }
        return await make_api_request("PUT", "/files/folders/move", data=data)
    
    elif name == "update_file":
        file_id = arguments["file_id"]
        data = {k: v for k, v in arguments.items() if k != "file_id" and v is not None}
        return await make_api_request("PUT", f"/files/{file_id}", data=data)
    
    elif name == "delete_file":
        file_id = arguments["file_id"]
        return await make_api_request("DELETE", f"/files/{file_id}")
    
    # ==================== AI TOOLS ====================
    elif name == "ask_ai":
        data = {
            "question": arguments["question"],
            "context": arguments.get("context")
        }
        return await make_api_request("POST", "/ai/ask", data=data)
    
    elif name == "search_knowledge":
        data = {
            "query": arguments["query"],
            "limit": arguments.get("limit", 10)
        }
        return await make_api_request("POST", "/ai/search", data=data)
    
    elif name == "rewrite_content":
        data = {
            "content": arguments["content"],
            "style": arguments.get("style")
        }
        return await make_api_request("POST", "/ai/rewrite", data=data)
    
    # ==================== DEVICE MANAGEMENT ====================
    elif name == "register_device":
        data = {
            "device_token": arguments["device_token"],
            "device_type": arguments["device_type"],
            "device_name": arguments.get("device_name")
        }
        return await make_api_request("POST", "/users/devices", data=data)
    
    elif name == "unregister_device":
        device_id = arguments["device_id"]
        return await make_api_request("DELETE", f"/users/devices/{device_id}")
    
    elif name == "unregister_device_by_token":
        data = {"device_token": arguments["device_token"]}
        return await make_api_request("DELETE", "/users/devices", data=data)
    
    # Tool not found
    else:
        return {
            "error": True,
            "message": f"Unknown write tool: {name}"
        }
