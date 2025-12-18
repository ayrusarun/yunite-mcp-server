# Yunite MCP Server - Comprehensive Tools Reference

## 📚 Complete Tool List (70+ Tools)

This MCP server provides comprehensive read access to the Yunite API with 70+ tools organized by category.

---

## 👥 USER & AUTH TOOLS (3)

### `get_my_profile`
Get the current authenticated user's detailed profile including academic info, permissions, and college details.

### `list_users`
List all users in the system with pagination and filtering.
- **Filters**: `limit`, `offset`, `role`, `department_id`, `is_active`

### `get_user_by_id`
Get detailed information about a specific user by ID.
- **Required**: `user_id`

---

## 📝 POSTS & CONTENT TOOLS (9)

### `list_posts`
List posts/announcements with pagination, filtering by type, group, and more.
- **Filters**: `limit`, `offset`, `post_type`, `group_id`, `include_engagement`

### `get_post_by_id`
Get detailed information about a specific post including content, metadata, and engagement.
- **Required**: `post_id`

### `get_posts_by_type`
Get all posts filtered by post type (ANNOUNCEMENT, INFO, IMPORTANT, EVENTS, GENERAL).
- **Required**: `post_type`
- **Filters**: `limit`, `offset`

### `get_post_comments`
Get all comments for a specific post.
- **Required**: `post_id`
- **Filters**: `limit`, `offset`

### `get_post_likes`
Get all users who liked a specific post.
- **Required**: `post_id`
- **Filters**: `page`, `page_size`

### `get_post_ignites`
Get all ignites (special likes) for a specific post.
- **Required**: `post_id`
- **Filters**: `page`, `page_size`

### `check_user_liked_post`
Check if the current user has liked a specific post.
- **Required**: `post_id`

---

## 🏢 DEPARTMENTS (3)

### `list_departments`
List all departments with optional statistics.
- **Filters**: `include_stats`

### `get_departments_with_stats`
Get all departments with detailed statistics (student count, program count, etc.).

### `get_department_by_id`
Get detailed information about a specific department.
- **Required**: `department_id`

---

## 🎓 PROGRAMS (2)

### `list_programs`
List academic programs with filtering and statistics.
- **Filters**: `department_id`, `include_stats`, `is_active`

### `get_program_by_id`
Get detailed information about a specific program.
- **Required**: `program_id`

---

## 👨‍🎓 COHORTS/BATCHES (2)

### `list_cohorts`
List cohorts/batches with filtering by program, year, etc.
- **Filters**: `program_id`, `admission_year`, `include_stats`, `is_active`

### `get_cohort_by_id`
Get detailed information about a specific cohort.
- **Required**: `cohort_id`

---

## 🏫 CLASSES/SECTIONS (4)

### `list_classes`
List classes/sections with filtering.
- **Filters**: `cohort_id`, `program_id`, `include_stats`

### `get_class_by_id`
Get detailed information about a specific class/section.
- **Required**: `class_id`

### `get_class_students`
Get all students in a specific class.
- **Required**: `class_id`

### `get_class_teachers`
Get all teachers assigned to a specific class.
- **Required**: `class_id`

---

## 📅 ACADEMIC YEARS (3)

### `list_academic_years`
List all academic years.

### `get_current_academic_year`
Get the currently active academic year.

### `get_academic_year_by_id`
Get details of a specific academic year.
- **Required**: `year_id`

---

## 👥 GROUPS (4)

### `list_groups`
List all groups (clubs, academic groups, events, custom).
- **Filters**: `group_type`, `limit`, `offset`

### `get_my_groups`
Get all groups the current user is a member of.

### `get_group_by_id`
Get detailed information about a specific group.
- **Required**: `group_id`

### `get_group_members`
Get all members of a specific group with their roles.
- **Required**: `group_id`

---

## 🎉 EVENTS (13)

### `list_events`
List all events with comprehensive filtering.
- **Filters**: `status`, `mode`, `group_id`, `start_date`, `end_date`, `limit`, `offset`

### `get_my_events`
Get all events created by the current user.

### `get_my_event_registrations`
Get all events the current user has registered for.

### `get_event_by_id`
Get detailed information about a specific event.
- **Required**: `event_id`

### `get_event_attendees`
Get all attendees/registrations for an event.
- **Required**: `event_id`

### `get_event_registrations`
Get all registrations for an event with status details.
- **Required**: `event_id`

### `get_my_event_registration`
Get the current user's registration for a specific event.
- **Required**: `event_id`

### `get_event_check_ins`
Get all check-ins for an event.
- **Required**: `event_id`

### `get_event_custom_fields`
Get custom registration fields for an event.
- **Required**: `event_id`

### `get_event_feedback_summary`
Get aggregated feedback/ratings for an event.
- **Required**: `event_id`

### `get_event_notifications`
Get all notifications sent for an event.
- **Required**: `event_id`

### `get_event_updates`
Get all updates posted for an event.
- **Required**: `event_id`

### `get_event_analytics`
Get comprehensive analytics for an event (registrations, attendance, demographics).
- **Required**: `event_id`

---

## 🏆 REWARDS & POINTS (5)

### `list_rewards`
List all rewards given/received with filtering.
- **Filters**: `user_id`, `reward_type`, `limit`, `offset`

### `get_my_rewards`
Get reward summary for the current user (total points, given/received counts, recent rewards).

### `get_rewards_leaderboard`
Get the rewards leaderboard showing top users by points.
- **Filters**: `limit`

### `get_user_reward_points`
Get detailed reward points information for a specific user.
- **Required**: `user_id`

### `get_reward_types`
Get all available reward types and their descriptions.

---

## 🛒 STORE & PRODUCTS (9)

### `list_product_categories`
Get all product categories in the rewards store.

### `list_products`
List products in the rewards store with extensive filtering.
- **Filters**: `category`, `status`, `min_points`, `max_points`, `in_stock`, `page`, `page_size`

### `get_product_by_id`
Get detailed information about a specific product.
- **Required**: `product_id`

### `get_my_cart`
Get the current user's shopping cart.

### `get_my_orders`
Get all orders placed by the current user.
- **Filters**: `status`, `page`, `page_size`

### `get_order_by_id`
Get detailed information about a specific order.
- **Required**: `order_id`

### `get_my_balance`
Get the current user's point balance and account info.

### `get_balance_history`
Get transaction history for the current user's point balance.
- **Filters**: `limit`, `offset`

### `get_my_wishlist`
Get the current user's wishlist of products.

---

## 💰 POOL (College Points Pool) (3)

### `get_pool_balance`
Get the college's point pool balance and status.

### `get_pool_transactions`
Get transaction history for the college point pool.
- **Filters**: `limit`, `offset`

### `get_pool_analytics`
Get comprehensive analytics for the college point pool.

---

## 📁 FILES & FOLDERS (5)

### `list_files`
List files uploaded to the system with filtering.
- **Filters**: `department_id`, `file_type`, `folder_path`, `limit`, `offset`

### `get_file_by_id`
Get detailed information about a specific file.
- **Required**: `file_id`

### `browse_folder`
Browse contents of a folder (files and subfolders).
- **Filters**: `path`, `department_id`

### `list_file_departments`
Get list of departments with file counts.

### `get_file_stats`
Get file storage statistics summary.

---

## 🔔 ALERTS & NOTIFICATIONS (3)

### `list_my_alerts`
Get all alerts for the current user.
- **Filters**: `unread_only`, `limit`, `offset`

### `get_alert_by_id`
Get detailed information about a specific alert.
- **Required**: `alert_id`

### `get_unread_alert_count`
Get count of unread alerts for the current user.

---

## 🤖 AI & SEARCH (3)

### `search_knowledge`
Search through indexed content using AI semantic search.
- **Required**: `query`
- **Filters**: `content_type`, `limit`

### `get_ai_stats`
Get AI system statistics (index status, query counts, etc.).

### `get_my_ai_conversations`
Get the current user's AI conversation history.
- **Filters**: `limit`

---

## 📰 NEWS (2)

### `get_tech_headlines`
Get latest technology news headlines.
- **Filters**: `limit`

### `get_news_cache_status`
Get status of the news cache (last update, next refresh, etc.).

---

## 🔐 ADMIN (3)

### `list_all_permissions`
Get list of all available permissions in the system.

### `list_all_roles`
Get list of all available roles in the system.

### `get_user_permissions`
Get all permissions for a specific user.
- **Required**: `user_id`

---

## 🎯 Usage Examples

```
# Get your profile
"Show me my profile"

# List departments with stats
"List all departments with statistics"

# Search for events
"Show me all upcoming events in hybrid mode"

# Get event analytics
"Give me the analytics for event ID 5"

# Check reward points
"What's my current reward points balance?"

# Browse files
"Show me all files in the CS department"

# Search with AI
"Search for posts about exam schedules"

# Get leaderboard
"Show me the top 10 users on the rewards leaderboard"

# List products
"What products are available in the store under 500 points?"

# Get event registrations
"How many people registered for event 10?"
```

---

## 📊 Tool Categories Summary

| Category | Tool Count |
|----------|-----------|
| Users & Auth | 3 |
| Posts & Content | 9 |
| Departments | 3 |
| Programs | 2 |
| Cohorts | 2 |
| Classes | 4 |
| Academic Years | 3 |
| Groups | 4 |
| Events | 13 |
| Rewards | 5 |
| Store & Products | 9 |
| Pool | 3 |
| Files & Folders | 5 |
| Alerts | 3 |
| AI & Search | 3 |
| News | 2 |
| Admin | 3 |
| **TOTAL** | **70+** |

---

## 🔧 Technical Details

- **Transport**: stdio (Docker exec)
- **Authentication**: Bearer token from admin credentials
- **Base URL**: Configurable via `.env`
- **Response Format**: JSON

All tools return structured JSON responses from the API with proper error handling.
