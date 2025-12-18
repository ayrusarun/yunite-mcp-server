"""
Comprehensive tool definitions for Yunite MCP Server
Based on OpenAPI specification endpoints
"""

from mcp.types import Tool

def get_comprehensive_tools():
    """Return all comprehensive tools for reading data from the API"""
    return [
        # ==================== USER & AUTH TOOLS ====================
        Tool(
            name="get_my_profile",
            description="Get the current authenticated user's detailed profile including academic info, permissions, and college details",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_users",
            description="List all users in the system with pagination and filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of users per page", "default": 50},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0},
                    "role": {"type": "string", "description": "Filter by role (admin, faculty, student, staff)"},
                    "department_id": {"type": "integer", "description": "Filter by department ID"},
                    "is_active": {"type": "boolean", "description": "Filter by active status"}
                }
            }
        ),
        Tool(
            name="get_user_by_id",
            description="Get detailed information about a specific user by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"}
                },
                "required": ["user_id"]
            }
        ),
        
        # ==================== POSTS & CONTENT TOOLS ====================
        Tool(
            name="list_posts",
            description="List posts/announcements with pagination, filtering by type, group, and more",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of posts", "default": 20},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0},
                    "post_type": {"type": "string", "description": "Filter by type: ANNOUNCEMENT, INFO, IMPORTANT, EVENTS, GENERAL"},
                    "group_id": {"type": "integer", "description": "Filter by group ID"},
                    "include_engagement": {"type": "boolean", "description": "Include like/comment counts", "default": true}
                }
            }
        ),
        Tool(
            name="get_post_by_id",
            description="Get detailed information about a specific post including content, metadata, and engagement",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID"}
                },
                "required": ["post_id"]
            }
        ),
        Tool(
            name="get_posts_by_type",
            description="Get all posts filtered by post type",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_type": {
                        "type": "string", 
                        "description": "Post type to filter",
                        "enum": ["ANNOUNCEMENT", "INFO", "IMPORTANT", "EVENTS", "GENERAL"]
                    },
                    "limit": {"type": "integer", "description": "Number of posts", "default": 20},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                },
                "required": ["post_type"]
            }
        ),
        Tool(
            name="get_post_comments",
            description="Get all comments for a specific post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID"},
                    "limit": {"type": "integer", "description": "Number of comments", "default": 50},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                },
                "required": ["post_id"]
            }
        ),
        Tool(
            name="get_post_likes",
            description="Get all users who liked a specific post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID"},
                    "page": {"type": "integer", "description": "Page number", "default": 1},
                    "page_size": {"type": "integer", "description": "Items per page", "default": 50}
                },
                "required": ["post_id"]
            }
        ),
        Tool(
            name="get_post_ignites",
            description="Get all ignites (special likes) for a specific post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID"},
                    "page": {"type": "integer", "description": "Page number", "default": 1},
                    "page_size": {"type": "integer", "description": "Items per page", "default": 50}
                },
                "required": ["post_id"]
            }
        ),
        Tool(
            name="check_user_liked_post",
            description="Check if the current user has liked a specific post",
            inputSchema={
                "type": "object",
                "properties": {
                    "post_id": {"type": "integer", "description": "Post ID"}
                },
                "required": ["post_id"]
            }
        ),
        
        # ==================== DEPARTMENTS & ACADEMIC STRUCTURE ====================
        Tool(
            name="list_departments",
            description="List all departments with optional statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_stats": {"type": "boolean", "description": "Include student/program counts", "default": false}
                }
            }
        ),
        Tool(
            name="get_departments_with_stats",
            description="Get all departments with detailed statistics (student count, program count, etc.)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_department_by_id",
            description="Get detailed information about a specific department",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_id": {"type": "integer", "description": "Department ID"}
                },
                "required": ["department_id"]
            }
        ),
        
        # ==================== PROGRAMS ====================
        Tool(
            name="list_programs",
            description="List academic programs with filtering and statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_id": {"type": "integer", "description": "Filter by department"},
                    "include_stats": {"type": "boolean", "description": "Include cohort/student counts", "default": false},
                    "is_active": {"type": "boolean", "description": "Filter by active status"}
                }
            }
        ),
        Tool(
            name="get_program_by_id",
            description="Get detailed information about a specific program",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_id": {"type": "integer", "description": "Program ID"}
                },
                "required": ["program_id"]
            }
        ),
        
        # ==================== COHORTS (BATCHES) ====================
        Tool(
            name="list_cohorts",
            description="List cohorts/batches with filtering by program, year, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "program_id": {"type": "integer", "description": "Filter by program"},
                    "admission_year": {"type": "integer", "description": "Filter by admission year"},
                    "include_stats": {"type": "boolean", "description": "Include student counts", "default": false},
                    "is_active": {"type": "boolean", "description": "Filter by active status"}
                }
            }
        ),
        Tool(
            name="get_cohort_by_id",
            description="Get detailed information about a specific cohort",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {"type": "integer", "description": "Cohort ID"}
                },
                "required": ["cohort_id"]
            }
        ),
        
        # ==================== CLASSES/SECTIONS ====================
        Tool(
            name="list_classes",
            description="List classes/sections with filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "cohort_id": {"type": "integer", "description": "Filter by cohort"},
                    "program_id": {"type": "integer", "description": "Filter by program"},
                    "include_stats": {"type": "boolean", "description": "Include student counts", "default": false}
                }
            }
        ),
        Tool(
            name="get_class_by_id",
            description="Get detailed information about a specific class/section",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_id": {"type": "integer", "description": "Class ID"}
                },
                "required": ["class_id"]
            }
        ),
        Tool(
            name="get_class_students",
            description="Get all students in a specific class",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_id": {"type": "integer", "description": "Class ID"}
                },
                "required": ["class_id"]
            }
        ),
        Tool(
            name="get_class_teachers",
            description="Get all teachers assigned to a specific class",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_id": {"type": "integer", "description": "Class ID"}
                },
                "required": ["class_id"]
            }
        ),
        
        # ==================== ACADEMIC YEARS ====================
        Tool(
            name="list_academic_years",
            description="List all academic years",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_current_academic_year",
            description="Get the currently active academic year",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_academic_year_by_id",
            description="Get details of a specific academic year",
            inputSchema={
                "type": "object",
                "properties": {
                    "year_id": {"type": "integer", "description": "Academic Year ID"}
                },
                "required": ["year_id"]
            }
        ),
        
        # ==================== GROUPS ====================
        Tool(
            name="list_groups",
            description="List all groups (clubs, academic groups, events, custom)",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_type": {"type": "string", "description": "Filter by type: ACADEMIC, CLUB, EVENT, CUSTOM"},
                    "limit": {"type": "integer", "description": "Number of groups", "default": 50},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                }
            }
        ),
        Tool(
            name="get_my_groups",
            description="Get all groups the current user is a member of",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_group_by_id",
            description="Get detailed information about a specific group",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "integer", "description": "Group ID"}
                },
                "required": ["group_id"]
            }
        ),
        Tool(
            name="get_group_members",
            description="Get all members of a specific group with their roles",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "integer", "description": "Group ID"}
                },
                "required": ["group_id"]
            }
        ),
        
        # ==================== EVENTS ====================
        Tool(
            name="list_events",
            description="List all events with filtering by status, mode, date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Filter by status: DRAFT, PUBLISHED, CANCELLED, COMPLETED"},
                    "mode": {"type": "string", "description": "Filter by mode: ONLINE, OFFLINE, HYBRID"},
                    "group_id": {"type": "integer", "description": "Filter by group"},
                    "start_date": {"type": "string", "description": "Filter events starting after this date (ISO format)"},
                    "end_date": {"type": "string", "description": "Filter events ending before this date (ISO format)"},
                    "limit": {"type": "integer", "description": "Number of events", "default": 50},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                }
            }
        ),
        Tool(
            name="get_my_events",
            description="Get all events created by the current user",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_my_event_registrations",
            description="Get all events the current user has registered for",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_event_by_id",
            description="Get detailed information about a specific event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "Event ID"}
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="get_event_attendees",
            description="Get all attendees/registrations for an event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "Event ID"}
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="get_event_registrations",
            description="Get all registrations for an event with status details",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "Event ID"}
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="get_my_event_registration",
            description="Get the current user's registration for a specific event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "Event ID"}
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="get_event_check_ins",
            description="Get all check-ins for an event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "Event ID"}
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="get_event_custom_fields",
            description="Get custom registration fields for an event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "Event ID"}
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="get_event_feedback_summary",
            description="Get aggregated feedback/ratings for an event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "Event ID"}
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="get_event_notifications",
            description="Get all notifications sent for an event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "Event ID"}
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="get_event_updates",
            description="Get all updates posted for an event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "Event ID"}
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="get_event_analytics",
            description="Get comprehensive analytics for an event (registrations, attendance, demographics)",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "Event ID"}
                },
                "required": ["event_id"]
            }
        ),
        
        # ==================== REWARDS & POINTS ====================
        Tool(
            name="list_rewards",
            description="List all rewards given/received with filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "Filter by user ID"},
                    "reward_type": {"type": "string", "description": "Filter by type: HELPFUL_POST, ACADEMIC_EXCELLENCE, etc."},
                    "limit": {"type": "integer", "description": "Number of rewards", "default": 50},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                }
            }
        ),
        Tool(
            name="get_my_rewards",
            description="Get reward summary for the current user (total points, given/received counts, recent rewards)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_rewards_leaderboard",
            description="Get the rewards leaderboard showing top users by points",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of top users", "default": 50}
                }
            }
        ),
        Tool(
            name="get_user_reward_points",
            description="Get detailed reward points information for a specific user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="get_reward_types",
            description="Get all available reward types and their descriptions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # ==================== STORE & PRODUCTS ====================
        Tool(
            name="list_product_categories",
            description="Get all product categories in the rewards store",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_products",
            description="List products in the rewards store with filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Filter by category"},
                    "status": {"type": "string", "description": "Filter by status: ACTIVE, INACTIVE, OUT_OF_STOCK"},
                    "min_points": {"type": "integer", "description": "Minimum points required"},
                    "max_points": {"type": "integer", "description": "Maximum points required"},
                    "in_stock": {"type": "boolean", "description": "Only show in-stock items"},
                    "page": {"type": "integer", "description": "Page number", "default": 1},
                    "page_size": {"type": "integer", "description": "Items per page", "default": 20}
                }
            }
        ),
        Tool(
            name="get_product_by_id",
            description="Get detailed information about a specific product",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer", "description": "Product ID"}
                },
                "required": ["product_id"]
            }
        ),
        Tool(
            name="get_my_cart",
            description="Get the current user's shopping cart",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_my_orders",
            description="Get all orders placed by the current user",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "Filter by order status"},
                    "page": {"type": "integer", "description": "Page number", "default": 1},
                    "page_size": {"type": "integer", "description": "Items per page", "default": 20}
                }
            }
        ),
        Tool(
            name="get_order_by_id",
            description="Get detailed information about a specific order",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "description": "Order ID"}
                },
                "required": ["order_id"]
            }
        ),
        Tool(
            name="get_my_balance",
            description="Get the current user's point balance and account info",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_balance_history",
            description="Get transaction history for the current user's point balance",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of transactions", "default": 50},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                }
            }
        ),
        Tool(
            name="get_my_wishlist",
            description="Get the current user's wishlist of products",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # ==================== POOL (COLLEGE POINTS POOL) ====================
        Tool(
            name="get_pool_balance",
            description="Get the college's point pool balance and status",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_pool_transactions",
            description="Get transaction history for the college point pool",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of transactions", "default": 50},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                }
            }
        ),
        Tool(
            name="get_pool_analytics",
            description="Get comprehensive analytics for the college point pool",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # ==================== FILES & FOLDERS ====================
        Tool(
            name="list_files",
            description="List files uploaded to the system with filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "department_id": {"type": "integer", "description": "Filter by department"},
                    "file_type": {"type": "string", "description": "Filter by file type: DOCUMENT, IMAGE, VIDEO, etc."},
                    "folder_path": {"type": "string", "description": "Filter by folder path", "default": "/"},
                    "limit": {"type": "integer", "description": "Number of files", "default": 50},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                }
            }
        ),
        Tool(
            name="get_file_by_id",
            description="Get detailed information about a specific file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_id": {"type": "integer", "description": "File ID"}
                },
                "required": ["file_id"]
            }
        ),
        Tool(
            name="browse_folder",
            description="Browse contents of a folder (files and subfolders)",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Folder path to browse", "default": "/"},
                    "department_id": {"type": "integer", "description": "Filter by department (optional)"}
                }
            }
        ),
        Tool(
            name="list_file_departments",
            description="Get list of departments with file counts",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_file_stats",
            description="Get file storage statistics summary",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # ==================== ALERTS & NOTIFICATIONS ====================
        Tool(
            name="list_my_alerts",
            description="Get all alerts for the current user",
            inputSchema={
                "type": "object",
                "properties": {
                    "unread_only": {"type": "boolean", "description": "Only show unread alerts", "default": false},
                    "limit": {"type": "integer", "description": "Number of alerts", "default": 50},
                    "offset": {"type": "integer", "description": "Offset for pagination", "default": 0}
                }
            }
        ),
        Tool(
            name="get_alert_by_id",
            description="Get detailed information about a specific alert",
            inputSchema={
                "type": "object",
                "properties": {
                    "alert_id": {"type": "integer", "description": "Alert ID"}
                },
                "required": ["alert_id"]
            }
        ),
        Tool(
            name="get_unread_alert_count",
            description="Get count of unread alerts for the current user",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # ==================== AI & SEARCH ====================
        Tool(
            name="search_knowledge",
            description="Search through indexed content using AI semantic search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "content_type": {"type": "string", "description": "Filter by content type: post, file, user, etc."},
                    "limit": {"type": "integer", "description": "Number of results", "default": 10}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_ai_stats",
            description="Get AI system statistics (index status, query counts, etc.)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_my_ai_conversations",
            description="Get the current user's AI conversation history",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of conversations", "default": 20}
                }
            }
        ),
        
        # ==================== NEWS ====================
        Tool(
            name="get_tech_headlines",
            description="Get latest technology news headlines",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "description": "Number of headlines", "default": 10}
                }
            }
        ),
        Tool(
            name="get_news_cache_status",
            description="Get status of the news cache (last update, next refresh, etc.)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # ==================== ADMIN TOOLS ====================
        Tool(
            name="list_all_permissions",
            description="Get list of all available permissions in the system",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_all_roles",
            description="Get list of all available roles in the system",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_user_permissions",
            description="Get all permissions for a specific user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "User ID"}
                },
                "required": ["user_id"]
            }
        ),
    ]
