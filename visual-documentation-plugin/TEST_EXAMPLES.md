# Test Examples for Visual Documentation Skills

This document provides test examples for each of the four visual documentation skills.

## 1. Flowchart Creator Test

### Simple Test
```
Create a flowchart showing the user authentication process
```

### Detailed Test
```
Create a flowchart for the following e-commerce checkout process:

1. User adds items to cart
2. User clicks checkout
3. System validates cart (if invalid, show error)
4. User enters shipping information
5. User selects payment method
6. System processes payment
   - If payment fails: show error and return to payment step
   - If payment succeeds: create order
7. System sends confirmation email
8. Display order confirmation page

Please use different colors for different types of steps (user actions, system processes, decisions).
```

### Expected Output
- HTML file with SVG flowchart
- Clear visual flow with arrows
- Decision diamonds for conditional paths
- Different colors/styles for different step types
- Responsive design that works on different screen sizes

---

## 2. Dashboard Creator Test

### Simple Test
```
Create a dashboard showing basic server metrics
```

### Detailed Test
```
Create a metrics dashboard for a web application monitoring system with the following sections:

**System Metrics:**
- CPU Usage: 45%
- Memory Usage: 68%
- Disk Usage: 52%
- Network I/O: 2.3 GB/s

**Application Metrics:**
- Active Users: 1,247
- Requests/sec: 3,421
- Average Response Time: 142ms
- Error Rate: 0.3%

**Database Metrics:**
- Query Performance: 23ms avg
- Active Connections: 45/100
- Cache Hit Rate: 94%

**Recent Alerts:**
- High memory usage warning (5 min ago)
- Slow query detected (12 min ago)

Use color coding (green/yellow/red) based on thresholds and include visual indicators like progress bars and gauges.
```

### Expected Output
- HTML file with organized dashboard layout
- Visual metric cards with icons
- Color-coded status indicators
- Progress bars or gauge charts for percentages
- Clear typography and spacing
- Alert section with timestamps

---

## 3. Timeline Creator Test

### Simple Test
```
Create a timeline for a product launch
```

### Detailed Test
```
Create a project timeline for our SaaS product development from Q4 2024 to Q2 2025:

**Q4 2024:**
- Oct 2024: Project kickoff and requirements gathering
- Nov 2024: Design system and wireframes complete
- Dec 2024: MVP development begins

**Q1 2025:**
- Jan 2025: Core features development
  - User authentication system
  - Dashboard implementation
  - API integration
- Feb 2025: Beta testing phase
  - Internal testing
  - Bug fixes
  - Performance optimization
- Mar 2025: Beta user feedback and iterations

**Q2 2025:**
- Apr 2025: Final testing and polish
- May 2025: Marketing campaign launch
- Jun 2025: Public release v1.0

Please use different visual styles to distinguish between planning, development, testing, and launch phases.
```

### Expected Output
- HTML file with horizontal or vertical timeline
- Clear chronological flow
- Milestone markers with dates
- Grouped events by phase/category
- Visual distinction between different types of events
- Descriptive labels and sub-items

---

## 4. Technical Documentation Creator Test

### Simple Test
```
Create technical documentation for a REST API endpoint
```

### Detailed Test
```
Create technical documentation for the following REST API:

**API: User Management Service**

**Base URL:** `https://api.example.com/v1`

**Authentication:** Bearer token required in Authorization header

**Endpoints:**

1. **GET /users**
   - Description: Retrieve list of users
   - Query Parameters:
     - `page` (integer, optional): Page number (default: 1)
     - `limit` (integer, optional): Items per page (default: 20, max: 100)
     - `role` (string, optional): Filter by role (admin, user, guest)
   - Response: 200 OK
     ```json
     {
       "users": [
         {
           "id": "usr_123",
           "email": "user@example.com",
           "role": "user",
           "created_at": "2024-01-15T10:30:00Z"
         }
       ],
       "pagination": {
         "page": 1,
         "total_pages": 5,
         "total_items": 98
       }
     }
     ```
   - Errors: 401 Unauthorized, 403 Forbidden

2. **POST /users**
   - Description: Create a new user
   - Request Body:
     ```json
     {
       "email": "newuser@example.com",
       "password": "secure_password",
       "role": "user"
     }
     ```
   - Response: 201 Created
     ```json
     {
       "id": "usr_456",
       "email": "newuser@example.com",
       "role": "user",
       "created_at": "2024-10-20T14:30:00Z"
     }
     ```
   - Errors: 400 Bad Request, 409 Conflict (email exists)

3. **GET /users/:id**
   - Description: Get user by ID
   - Path Parameters: `id` (string, required)
   - Response: 200 OK (same user object as above)
   - Errors: 404 Not Found

**Rate Limiting:** 1000 requests per hour per API key

**Error Format:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": ["email field must be a valid email address"]
  }
}
```

Include code examples in JavaScript and Python.
```

### Expected Output
- HTML file with well-structured technical documentation
- Table of contents with navigation
- Color-coded HTTP methods (GET, POST, etc.)
- Syntax-highlighted code examples
- Clear parameter tables
- Response/request examples
- Error documentation
- Clean, readable typography
- Copy-to-clipboard functionality for code blocks

---

## Testing Checklist

For each skill, verify:

- [ ] Skill activates correctly when requested
- [ ] Generates valid HTML file
- [ ] HTML renders properly in browser
- [ ] Styling is modern and professional
- [ ] Content is well-organized and readable
- [ ] SVG graphics render correctly (where applicable)
- [ ] Responsive design works on different screen sizes
- [ ] No broken references to templates/resources
- [ ] Color scheme is consistent and accessible
- [ ] File is saved to appropriate location

## How to Test

1. **Setup:**
   ```bash
   ln -s /Users/map/Documents/Repos/claude-skills-marketplace/visual-documentation-plugin ~/.claude/plugins/user/visual-documentation-skills
   ```

2. **Restart Claude Code**

3. **Run each test example** by copying the test prompts into Claude Code

4. **Verify outputs** using the checklist above

5. **Check browser console** for any errors when viewing HTML files

6. **Test responsiveness** by resizing browser window

## Expected File Locations

Generated HTML files should be saved to:
- Current working directory, OR
- User-specified location, OR
- A logical default like `~/Documents/` or project root
