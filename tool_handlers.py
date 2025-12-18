"""
Tool call handlers for comprehensive Yunite MCP Server
Maps tool names to API endpoints
"""

async def handle_tool_call(name: str, arguments: dict, make_api_request):
    """
    Route tool calls to appropriate API endpoints
    Returns result dict from API
    """
    
    # ==================== USER & AUTH TOOLS ====================
    if name == "get_my_profile":
        return await make_api_request("GET", "/users/me")
    
    elif name == "list_users":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/users/", params=params)
    
    elif name == "get_user_by_id":
        return await make_api_request("GET", f"/users/{arguments['user_id']}")
    
    # ==================== POSTS & CONTENT TOOLS ====================
    elif name == "list_posts":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/posts/", params=params)
    
    elif name == "get_post_by_id":
        return await make_api_request("GET", f"/posts/{arguments['post_id']}")
    
    elif name == "get_posts_by_type":
        params = {"limit": arguments.get("limit", 20), "offset": arguments.get("offset", 0)}
        return await make_api_request("GET", f"/posts/type/{arguments['post_type']}", params=params)
    
    elif name == "get_post_comments":
        params = {"limit": arguments.get("limit", 50), "offset": arguments.get("offset", 0)}
        return await make_api_request("GET", f"/posts/{arguments['post_id']}/comments", params=params)
    
    elif name == "get_post_likes":
        params = {"page": arguments.get("page", 1), "page_size": arguments.get("page_size", 50)}
        return await make_api_request("GET", f"/posts/{arguments['post_id']}/likes", params=params)
    
    elif name == "get_post_ignites":
        params = {"page": arguments.get("page", 1), "page_size": arguments.get("page_size", 50)}
        return await make_api_request("GET", f"/posts/{arguments['post_id']}/ignites", params=params)
    
    elif name == "check_user_liked_post":
        return await make_api_request("GET", f"/posts/{arguments['post_id']}/is-liked")
    
    # ==================== DEPARTMENTS ====================
    elif name == "list_departments":
        params = {}
        if arguments.get("include_stats"):
            params["include_stats"] = True
        return await make_api_request("GET", "/departments/", params=params)
    
    elif name == "get_departments_with_stats":
        return await make_api_request("GET", "/departments/with-stats")
    
    elif name == "get_department_by_id":
        return await make_api_request("GET", f"/departments/{arguments['department_id']}")
    
    # ==================== PROGRAMS ====================
    elif name == "list_programs":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/academic/programs", params=params)
    
    elif name == "get_program_by_id":
        return await make_api_request("GET", f"/academic/programs/{arguments['program_id']}")
    
    # ==================== COHORTS ====================
    elif name == "list_cohorts":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/academic/cohorts", params=params)
    
    elif name == "get_cohort_by_id":
        return await make_api_request("GET", f"/academic/cohorts/{arguments['cohort_id']}")
    
    # ==================== CLASSES/SECTIONS ====================
    elif name == "list_classes":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/academic/classes", params=params)
    
    elif name == "get_class_by_id":
        return await make_api_request("GET", f"/academic/classes/{arguments['class_id']}")
    
    elif name == "get_class_students":
        return await make_api_request("GET", f"/academic/classes/{arguments['class_id']}/students")
    
    elif name == "get_class_teachers":
        return await make_api_request("GET", f"/academic/classes/{arguments['class_id']}/teachers")
    
    # ==================== ACADEMIC YEARS ====================
    elif name == "list_academic_years":
        return await make_api_request("GET", "/academic/years")
    
    elif name == "get_current_academic_year":
        return await make_api_request("GET", "/academic/years/current")
    
    elif name == "get_academic_year_by_id":
        return await make_api_request("GET", f"/academic/years/{arguments['year_id']}")
    
    # ==================== GROUPS ====================
    elif name == "list_groups":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/groups/", params=params)
    
    elif name == "get_my_groups":
        return await make_api_request("GET", "/groups/my-groups")
    
    elif name == "get_group_by_id":
        return await make_api_request("GET", f"/groups/{arguments['group_id']}")
    
    elif name == "get_group_members":
        return await make_api_request("GET", f"/groups/{arguments['group_id']}/members")
    
    # ==================== EVENTS ====================
    elif name == "list_events":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/events/", params=params)
    
    elif name == "get_my_events":
        return await make_api_request("GET", "/events/my-events")
    
    elif name == "get_my_event_registrations":
        return await make_api_request("GET", "/events/my-registrations")
    
    elif name == "get_event_by_id":
        return await make_api_request("GET", f"/events/{arguments['event_id']}")
    
    elif name == "get_event_attendees":
        return await make_api_request("GET", f"/events/{arguments['event_id']}/attendees")
    
    elif name == "get_event_registrations":
        return await make_api_request("GET", f"/events/{arguments['event_id']}/registrations")
    
    elif name == "get_my_event_registration":
        return await make_api_request("GET", f"/events/{arguments['event_id']}/my-registration")
    
    elif name == "get_event_check_ins":
        return await make_api_request("GET", f"/events/{arguments['event_id']}/check-ins")
    
    elif name == "get_event_custom_fields":
        return await make_api_request("GET", f"/events/{arguments['event_id']}/custom-fields")
    
    elif name == "get_event_feedback_summary":
        return await make_api_request("GET", f"/events/{arguments['event_id']}/feedback/summary")
    
    elif name == "get_event_notifications":
        return await make_api_request("GET", f"/events/{arguments['event_id']}/notifications")
    
    elif name == "get_event_updates":
        return await make_api_request("GET", f"/events/{arguments['event_id']}/updates")
    
    elif name == "get_event_analytics":
        return await make_api_request("GET", f"/events/{arguments['event_id']}/analytics")
    
    # ==================== REWARDS & POINTS ====================
    elif name == "list_rewards":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/rewards/", params=params)
    
    elif name == "get_my_rewards":
        return await make_api_request("GET", "/rewards/me")
    
    elif name == "get_rewards_leaderboard":
        params = {"limit": arguments.get("limit", 50)}
        return await make_api_request("GET", "/rewards/leaderboard", params=params)
    
    elif name == "get_user_reward_points":
        return await make_api_request("GET", f"/rewards/points/{arguments['user_id']}")
    
    elif name == "get_reward_types":
        return await make_api_request("GET", "/rewards/types")
    
    # ==================== STORE & PRODUCTS ====================
    elif name == "list_product_categories":
        return await make_api_request("GET", "/rewards/store/categories")
    
    elif name == "list_products":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/rewards/store/products", params=params)
    
    elif name == "get_product_by_id":
        return await make_api_request("GET", f"/rewards/store/products/{arguments['product_id']}")
    
    elif name == "get_my_cart":
        return await make_api_request("GET", "/rewards/store/cart")
    
    elif name == "get_my_orders":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/rewards/store/orders", params=params)
    
    elif name == "get_order_by_id":
        return await make_api_request("GET", f"/rewards/store/orders/{arguments['order_id']}")
    
    elif name == "get_my_balance":
        return await make_api_request("GET", "/rewards/store/balance")
    
    elif name == "get_balance_history":
        params = {"limit": arguments.get("limit", 50), "offset": arguments.get("offset", 0)}
        return await make_api_request("GET", "/rewards/store/balance/history", params=params)
    
    elif name == "get_my_wishlist":
        return await make_api_request("GET", "/rewards/store/wishlist")
    
    # ==================== POOL ====================
    elif name == "get_pool_balance":
        return await make_api_request("GET", "/pool/balance")
    
    elif name == "get_pool_transactions":
        params = {"limit": arguments.get("limit", 50), "offset": arguments.get("offset", 0)}
        return await make_api_request("GET", "/pool/transactions", params=params)
    
    elif name == "get_pool_analytics":
        return await make_api_request("GET", "/pool/analytics")
    
    # ==================== FILES & FOLDERS ====================
    elif name == "list_files":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/files/", params=params)
    
    elif name == "get_file_by_id":
        return await make_api_request("GET", f"/files/{arguments['file_id']}")
    
    elif name == "browse_folder":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/files/folders/browse", params=params)
    
    elif name == "list_file_departments":
        return await make_api_request("GET", "/files/departments/list")
    
    elif name == "get_file_stats":
        return await make_api_request("GET", "/files/stats/summary")
    
    # ==================== ALERTS ====================
    elif name == "list_my_alerts":
        params = {k: v for k, v in arguments.items() if v is not None}
        return await make_api_request("GET", "/alerts/", params=params)
    
    elif name == "get_alert_by_id":
        return await make_api_request("GET", f"/alerts/{arguments['alert_id']}")
    
    elif name == "get_unread_alert_count":
        return await make_api_request("GET", "/alerts/unread-count")
    
    # ==================== AI & SEARCH ====================
    elif name == "search_knowledge":
        data = {
            "query": arguments["query"],
            "content_type": arguments.get("content_type"),
            "limit": arguments.get("limit", 10)
        }
        return await make_api_request("POST", "/ai/search", data=data)
    
    elif name == "get_ai_stats":
        return await make_api_request("GET", "/ai/stats")
    
    elif name == "get_my_ai_conversations":
        params = {"limit": arguments.get("limit", 20)}
        return await make_api_request("GET", "/ai/conversations", params=params)
    
    # ==================== NEWS ====================
    elif name == "get_tech_headlines":
        params = {"limit": arguments.get("limit", 10)}
        return await make_api_request("GET", "/news/tech-headlines", params=params)
    
    elif name == "get_news_cache_status":
        return await make_api_request("GET", "/news/cache-status")
    
    # ==================== ADMIN ====================
    elif name == "list_all_permissions":
        return await make_api_request("GET", "/admin/permissions")
    
    elif name == "list_all_roles":
        return await make_api_request("GET", "/admin/roles")
    
    elif name == "get_user_permissions":
        return await make_api_request("GET", f"/admin/users/{arguments['user_id']}/permissions")
    
    # If no handler found, return error
    else:
        return {"error": True, "message": f"Unknown tool: {name}"}
