"""
Comprehensive Write Tools for Yunite MCP Server
Generated from OpenAPI schema - 92 write operations
"""

from mcp.types import Tool

def get_write_tools():
    """Returns list of all write operation tools (POST, PUT, PATCH, DELETE)"""
    
    return [
        # ==================== POSTS ====================
        Tool(
            name="create_post",
            description="Create a new post/announcement",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Post content"},
                    "title": {"type": "string", "description": "Post title (optional)"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="update_post",
            description="Update an existing post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID to update"},
                    "content": {"type": "string", "description": "Updated content"},
                    "title": {"type": "string", "description": "Updated title (optional)"}
                },
                "required": ["post_id"]
            }
        ),
        Tool(
            name="update_post_metadata",
            description="Update post metadata (views, shares, etc)",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID"},
                    "metadata": {"type": "object", "description": "Metadata to update"}
                },
                "required": ["post_id", "metadata"]
            }
        ),
        Tool(
            name="create_post_alert",
            description="Create an alert for a post to notify users",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID"},
                    "alert_title": {"type": "string", "description": "Alert title"},
                    "alert_message": {"type": "string", "description": "Alert message"}
                },
                "required": ["post_id", "alert_title"]
            }
        ),
        
        # ==================== ENGAGEMENT ====================
        Tool(
            name="add_comment",
            description="Add a comment to a post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID"},
                    "content": {"type": "string", "description": "Comment content"}
                },
                "required": ["post_id", "content"]
            }
        ),
        Tool(
            name="delete_comment",
            description="Delete a comment from a post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID"},
                    "comment_id": {"type": "integer", "description": "Comment ID to delete"}
                },
                "required": ["post_id", "comment_id"]
            }
        ),
        Tool(
            name="toggle_like",
            description="Like or unlike a post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID to like/unlike"}
                },
                "required": ["post_id"]
            }
        ),
        Tool(
            name="toggle_ignite",
            description="Ignite or un-ignite a post (super like)",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID to ignite/un-ignite"}
                },
                "required": ["post_id"]
            }
        ),
        
        # ==================== DEPARTMENTS ====================
        Tool(
            name="create_department",
            description="Create a new department in the college",
            inputSchema={
                "type": "object",
                "properties": {
                    "college_id": {"type": "integer", "description": "College ID"},
                    "name": {"type": "string", "description": "Department name"},
                    "code": {"type": "string", "description": "Department code (e.g., CS, EE, ME)"},
                    "description": {"type": "string", "description": "Department description (optional)"},
                    "is_active": {"type": "boolean", "description": "Whether the department is active", "default": True}
                },
                "required": ["college_id", "name", "code"]
            }
        ),
        Tool(
            name="update_department",
            description="Update department information",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_id": {"type": "integer", "description": "Department ID"},
                    "name": {"type": "string", "description": "Department name"},
                    "code": {"type": "string", "description": "Department code"},
                    "description": {"type": "string", "description": "Department description"},
                    "is_active": {"type": "boolean", "description": "Active status"}
                },
                "required": ["department_id"]
            }
        ),
        Tool(
            name="deactivate_department",
            description="Deactivate a department",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_id": {"type": "integer", "description": "Department ID to deactivate"}
                },
                "required": ["department_id"]
            }
        ),
        Tool(
            name="activate_department",
            description="Activate a department",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_id": {"type": "integer", "description": "Department ID to activate"}
                },
                "required": ["department_id"]
            }
        ),
        
        # ==================== ACADEMIC MANAGEMENT ====================
        Tool(
            name="create_academic_year",
            description="Create a new academic year",
            inputSchema={
                "type": "object",
                "properties": {
                    "year_name": {"type": "string", "description": "Year name (e.g., 2024-2025)"},
                    "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                    "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
                    "is_active": {"type": "boolean", "description": "Active status", "default": False}
                },
                "required": ["year_name", "start_date", "end_date"]
            }
        ),
        Tool(
            name="update_academic_year",
            description="Update academic year information",
            inputSchema={
                "type": "object",
                "properties": {
                    "year_id": {"type": "integer", "description": "Academic year ID"},
                    "year_name": {"type": "string", "description": "Year name"},
                    "start_date": {"type": "string", "description": "Start date"},
                    "end_date": {"type": "string", "description": "End date"},
                    "is_active": {"type": "boolean", "description": "Active status"}
                },
                "required": ["year_id"]
            }
        ),
        Tool(
            name="activate_academic_year",
            description="Activate an academic year (deactivates others)",
            inputSchema={
                "type": "object",
                "properties": {
                    "year_id": {"type": "integer", "description": "Academic year ID to activate"}
                },
                "required": ["year_id"]
            }
        ),
        Tool(
            name="create_program",
            description="Create an academic program under a department",
            inputSchema={
                "type": "object",
                "properties": {
                    "college_id": {"type": "integer", "description": "College ID"},
                    "department_id": {"type": "integer", "description": "Department ID"},
                    "code": {"type": "string", "description": "Program code (e.g., BTECH-CS, MBA)"},
                    "name": {"type": "string", "description": "Program name"},
                    "short_name": {"type": "string", "description": "Short name (optional)"},
                    "duration_years": {"type": "integer", "description": "Duration in years"},
                    "description": {"type": "string", "description": "Program description (optional)"},
                    "is_active": {"type": "boolean", "description": "Active status", "default": True}
                },
                "required": ["college_id", "department_id", "code", "name", "duration_years"]
            }
        ),
        Tool(
            name="update_program",
            description="Update program information",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_id": {"type": "integer", "description": "Program ID"},
                    "name": {"type": "string", "description": "Program name"},
                    "code": {"type": "string", "description": "Program code"},
                    "short_name": {"type": "string", "description": "Short name"},
                    "duration_years": {"type": "integer", "description": "Duration in years"},
                    "description": {"type": "string", "description": "Description"},
                    "is_active": {"type": "boolean", "description": "Active status"}
                },
                "required": ["program_id"]
            }
        ),
        Tool(
            name="create_cohort",
            description="Create a cohort (batch/year group) for a program",
            inputSchema={
                "type": "object",
                "properties": {
                    "college_id": {"type": "integer", "description": "College ID"},
                    "program_id": {"type": "integer", "description": "Program ID"},
                    "admission_year": {"type": "integer", "description": "Admission year (e.g., 2024)"},
                    "code": {"type": "string", "description": "Cohort code (e.g., BTECH-CS-2024)"},
                    "name": {"type": "string", "description": "Cohort name"},
                    "expected_graduation_year": {"type": "integer", "description": "Expected graduation year (optional)"},
                    "current_semester": {"type": "integer", "description": "Current semester", "default": 1},
                    "is_active": {"type": "boolean", "description": "Active status", "default": True}
                },
                "required": ["college_id", "program_id", "admission_year", "code", "name"]
            }
        ),
        Tool(
            name="update_cohort",
            description="Update cohort information",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {"type": "integer", "description": "Cohort ID"},
                    "name": {"type": "string", "description": "Cohort name"},
                    "code": {"type": "string", "description": "Cohort code"},
                    "current_semester": {"type": "integer", "description": "Current semester"},
                    "expected_graduation_year": {"type": "integer", "description": "Expected graduation year"},
                    "is_active": {"type": "boolean", "description": "Active status"}
                },
                "required": ["cohort_id"]
            }
        ),
        Tool(
            name="create_class",
            description="Create a section/class for a cohort",
            inputSchema={
                "type": "object",
                "properties": {
                    "college_id": {"type": "integer", "description": "College ID"},
                    "cohort_id": {"type": "integer", "description": "Cohort ID"},
                    "program_id": {"type": "integer", "description": "Program ID"},
                    "section_code": {"type": "string", "description": "Section code (e.g., A, B, C)"},
                    "section_name": {"type": "string", "description": "Section name (optional)"},
                    "capacity": {"type": "integer", "description": "Maximum capacity (optional)"},
                    "is_active": {"type": "boolean", "description": "Active status", "default": True}
                },
                "required": ["college_id", "cohort_id", "program_id", "section_code"]
            }
        ),
        Tool(
            name="update_class",
            description="Update class/section information",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_id": {"type": "integer", "description": "Class ID"},
                    "section_code": {"type": "string", "description": "Section code"},
                    "section_name": {"type": "string", "description": "Section name"},
                    "capacity": {"type": "integer", "description": "Maximum capacity"},
                    "is_active": {"type": "boolean", "description": "Active status"}
                },
                "required": ["class_id"]
            }
        ),
        Tool(
            name="assign_teacher_to_class",
            description="Assign a teacher to a class/section",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_id": {"type": "integer", "description": "Class ID"},
                    "teacher_id": {"type": "integer", "description": "Teacher user ID"},
                    "subject": {"type": "string", "description": "Subject being taught (optional)"}
                },
                "required": ["class_id", "teacher_id"]
            }
        ),
        Tool(
            name="remove_teacher_from_class",
            description="Remove a teacher assignment from a class",
            inputSchema={
                "type": "object",
                "properties": {
                    "assignment_id": {"type": "integer", "description": "Teacher assignment ID to remove"}
                },
                "required": ["assignment_id"]
            }
        ),
        
        # ==================== ADMIN & USER MANAGEMENT ====================
        Tool(
            name="create_student",
            description="Create a new student user",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Student username"},
                    "email": {"type": "string", "description": "Student email"},
                    "full_name": {"type": "string", "description": "Student full name"},
                    "password": {"type": "string", "description": "Student password"},
                    "college_id": {"type": "integer", "description": "College ID"},
                    "department_id": {"type": "integer", "description": "Department ID"},
                    "program_id": {"type": "integer", "description": "Program ID"},
                    "cohort_id": {"type": "integer", "description": "Cohort ID"},
                    "class_id": {"type": "integer", "description": "Section/Class ID"},
                    "admission_year": {"type": "integer", "description": "Admission year"}
                },
                "required": ["username", "email", "full_name", "password", "college_id", "department_id", "program_id", "cohort_id", "class_id", "admission_year"]
            }
        ),
        Tool(
            name="create_staff",
            description="Create a new staff/faculty user",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Staff username"},
                    "email": {"type": "string", "description": "Staff email"},
                    "full_name": {"type": "string", "description": "Staff full name"},
                    "password": {"type": "string", "description": "Staff password"},
                    "college_id": {"type": "integer", "description": "College ID"},
                    "department_id": {"type": "integer", "description": "Department ID (optional)"},
                    "role": {"type": "string", "description": "Staff role (e.g., faculty, staff, admin)", "default": "staff"}
                },
                "required": ["username", "email", "full_name", "password", "college_id", "role"]
            }
        ),
        Tool(
            name="update_user_profile",
            description="Update a user's profile information",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID to update"},
                    "full_name": {"type": "string", "description": "Full name (optional)"},
                    "email": {"type": "string", "description": "Email (optional)"},
                    "bio": {"type": "string", "description": "Bio (optional)"},
                    "profile_picture": {"type": "string", "description": "Profile picture URL (optional)"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="update_user_role",
            description="Update a user's role",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"},
                    "role": {"type": "string", "description": "New role (student, faculty, admin, staff)"}
                },
                "required": ["user_id", "role"]
            }
        ),
        Tool(
            name="update_user_status",
            description="Update a user's status (active/inactive/suspended)",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"},
                    "status": {"type": "string", "description": "New status (active, inactive, suspended)"}
                },
                "required": ["user_id", "status"]
            }
        ),
        Tool(
            name="delete_user",
            description="Delete a user from the system",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID to delete"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="grant_permission",
            description="Grant or revoke a permission for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"},
                    "permission_name": {"type": "string", "description": "Permission name"},
                    "grant": {"type": "boolean", "description": "True to grant, False to revoke", "default": True}
                },
                "required": ["user_id", "permission_name"]
            }
        ),
        Tool(
            name="remove_permission",
            description="Remove a custom permission from a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"},
                    "permission_name": {"type": "string", "description": "Permission name to remove"}
                },
                "required": ["user_id", "permission_name"]
            }
        ),
        
        # ==================== GROUPS ====================
        Tool(
            name="create_group",
            description="Create a new group/community",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Group name"},
                    "description": {"type": "string", "description": "Group description"},
                    "is_public": {"type": "boolean", "description": "Public visibility", "default": True},
                    "group_type": {"type": "string", "description": "Group type (optional)"}
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="update_group",
            description="Update group information",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "integer", "description": "Group ID"},
                    "name": {"type": "string", "description": "Group name"},
                    "description": {"type": "string", "description": "Group description"},
                    "is_public": {"type": "boolean", "description": "Public visibility"}
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="delete_group",
            description="Delete a group",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "integer", "description": "Group ID to delete"}
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="join_group",
            description="Join a public group or request to join private group",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "integer", "description": "Group ID to join"}
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="add_group_member",
            description="Add a member to a group (admin action)",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "integer", "description": "Group ID"},
                    "user_id": {"type": "integer", "description": "User ID to add"},
                    "role": {"type": "string", "description": "Member role (member, moderator, admin)", "default": "member"}
                },
                "required": ["group_id", "user_id"]
            }
        ),
        Tool(
            name="update_group_member_role",
            description="Update a group member's role",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "integer", "description": "Group ID"},
                    "user_id": {"type": "integer", "description": "User ID"},
                    "role": {"type": "string", "description": "New role (member, moderator, admin)"}
                },
                "required": ["group_id", "user_id", "role"]
            }
        ),
        Tool(
            name="remove_group_member",
            description="Remove a member from a group",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "integer", "description": "Group ID"},
                    "user_id": {"type": "integer", "description": "User ID to remove"}
                },
                "required": ["group_id", "user_id"]
            }
        ),
        
        # ==================== ALERTS ====================
        Tool(
            name="create_alert",
            description="Create an alert for specific users",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Alert title"},
                    "message": {"type": "string", "description": "Alert message"},
                    "alert_type": {"type": "string", "description": "Alert type (info, warning, success, error)"},
                    "user_ids": {"type": "array", "items": {"type": "integer"}, "description": "List of user IDs to alert"}
                },
                "required": ["title", "message"]
            }
        ),
        Tool(
            name="create_group_alert",
            description="Create an alert for all members of a group",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Alert title"},
                    "message": {"type": "string", "description": "Alert message"},
                    "group_id": {"type": "integer", "description": "Group ID to alert"},
                    "alert_type": {"type": "string", "description": "Alert type"}
                },
                "required": ["title", "message", "group_id"]
            }
        ),
        Tool(
            name="update_alert",
            description="Update an existing alert",
            inputSchema={
                "type": "object",
                "properties": {
                    "alert_id": {"type": "integer", "description": "Alert ID"},
                    "title": {"type": "string", "description": "Alert title"},
                    "message": {"type": "string", "description": "Alert message"},
                    "is_read": {"type": "boolean", "description": "Read status"}
                },
                "required": ["alert_id"]
            }
        ),
        Tool(
            name="delete_alert",
            description="Delete an alert",
            inputSchema={
                "type": "object",
                "properties": {
                    "alert_id": {"type": "integer", "description": "Alert ID to delete"}
                },
                "required": ["alert_id"]
            }
        ),
        Tool(
            name="mark_all_alerts_read",
            description="Mark all alerts as read for the current user",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # ==================== AUTHENTICATION ====================
        Tool(
            name="login",
            description="Login to get authentication token",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Username or email"},
                    "password": {"type": "string", "description": "Password"}
                },
                "required": ["username", "password"]
            }
        ),
        Tool(
            name="logout",
            description="Logout and invalidate current session",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="update_password",
            description="Update user password",
            inputSchema={
                "type": "object",
                "properties": {
                    "current_password": {"type": "string", "description": "Current password"},
                    "new_password": {"type": "string", "description": "New password"}
                },
                "required": ["current_password", "new_password"]
            }
        ),
        
        # ==================== REWARDS ====================
        Tool(
            name="give_reward",
            description="Give reward points to a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID to reward"},
                    "points": {"type": "integer", "description": "Points to award"},
                    "reason": {"type": "string", "description": "Reason for reward"}
                },
                "required": ["user_id", "points"]
            }
        ),
        Tool(
            name="credit_pool",
            description="Credit points to reward pool",
            inputSchema={
                "type": "object",
                "properties": {
                    "points": {"type": "integer", "description": "Points to credit"},
                    "description": {"type": "string", "description": "Description"}
                },
                "required": ["points"]
            }
        ),
        
        # ==================== FILES ====================
        Tool(
            name="upload_file",
            description="Upload a file to the system",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_name": {"type": "string", "description": "File name"},
                    "file_data": {"type": "string", "description": "Base64 encoded file data"},
                    "folder_id": {"type": "integer", "description": "Folder ID (optional)"}
                },
                "required": ["file_name", "file_data"]
            }
        ),
        Tool(
            name="create_folder",
            description="Create a new folder",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Folder name"},
                    "parent_folder_id": {"type": "integer", "description": "Parent folder ID (optional)"}
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="delete_folder",
            description="Delete a folder",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder_id": {"type": "integer", "description": "Folder ID to delete"}
                },
                "required": ["folder_id"]
            }
        ),
        Tool(
            name="move_folder",
            description="Move a folder to a new parent",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder_id": {"type": "integer", "description": "Folder ID to move"},
                    "new_parent_id": {"type": "integer", "description": "New parent folder ID"}
                },
                "required": ["folder_id", "new_parent_id"]
            }
        ),
        Tool(
            name="update_file",
            description="Update file metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_id": {"type": "integer", "description": "File ID"},
                    "name": {"type": "string", "description": "New file name"},
                    "description": {"type": "string", "description": "File description"}
                },
                "required": ["file_id"]
            }
        ),
        Tool(
            name="delete_file",
            description="Delete a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_id": {"type": "integer", "description": "File ID to delete"}
                },
                "required": ["file_id"]
            }
        ),
        
        # ==================== AI TOOLS ====================
        Tool(
            name="ask_ai",
            description="Ask AI a question about the college/content",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Question to ask"},
                    "context": {"type": "string", "description": "Additional context (optional)"}
                },
                "required": ["question"]
            }
        ),
        Tool(
            name="search_knowledge",
            description="Search the AI knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "description": "Max results", "default": 10}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="rewrite_content",
            description="Use AI to rewrite/improve content",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Content to rewrite"},
                    "style": {"type": "string", "description": "Writing style (formal, casual, academic)"}
                },
                "required": ["content"]
            }
        ),
        
        # ==================== DEVICE MANAGEMENT ====================
        Tool(
            name="register_device",
            description="Register a device for push notifications",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_token": {"type": "string", "description": "Device FCM token"},
                    "device_type": {"type": "string", "description": "Device type (ios, android, web)"},
                    "device_name": {"type": "string", "description": "Device name (optional)"}
                },
                "required": ["device_token", "device_type"]
            }
        ),
        Tool(
            name="unregister_device",
            description="Unregister a device by device ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_id": {"type": "integer", "description": "Device ID to unregister"}
                },
                "required": ["device_id"]
            }
        ),
        Tool(
            name="unregister_device_by_token",
            description="Unregister a device by token",
            inputSchema={
                "type": "object",
                "properties": {
                    "device_token": {"type": "string", "description": "Device token to unregister"}
                },
                "required": ["device_token"]
            }
        ),
    ]
