# Feature Planning Best Practices

This guide provides detailed best practices for creating effective implementation plans.

## Task Granularity

### Right-Sized Tasks

**Too Large:**
- "Implement user authentication system"
- "Build the entire dashboard"
- "Add social media integration"

**Too Small:**
- "Import the uuid library"
- "Add a single line of code"
- "Create an empty file"

**Just Right:**
- "Create User model with email, password hash, and timestamps"
- "Implement JWT token generation and validation utility"
- "Add login endpoint with rate limiting"
- "Create protected route middleware"

### Task Independence

Each task should be implementable without needing to switch context frequently:

**Good:**
```markdown
#### Task 1: Database Schema
Create the `users` table with proper indexes and constraints.
Dependencies: None

#### Task 2: User Model
Implement the User model class with validation methods.
Dependencies: Task 1

#### Task 3: Auth Service
Create authentication service for login/logout operations.
Dependencies: Task 2
```

**Avoid:**
```markdown
#### Task 1: Part 1 of User Authentication
Add some user fields...

#### Task 2: Part 2 of User Authentication
Finish the user fields from Task 1...
```

## Specificity in Task Descriptions

### Include File Paths

**Vague:**
"Add the authentication logic"

**Specific:**
"Add authentication logic in `src/services/auth.py:45` following the pattern from `src/services/session.py:23-67`"

### Provide Context

**Vague:**
"Update the user handler"

**Specific:**
"Update the user handler in `api/handlers/user.py:120` to validate email format using the existing `validators.email()` utility. Follow the validation pattern from `api/handlers/auth.py:89`"

### Specify Expected Behavior

**Vague:**
"Add error handling"

**Specific:**
"Add try/except block to catch `DatabaseError` and return 500 status with error message. Log the full exception using the existing logger instance. See similar handling in `api/handlers/base.py:34`"

## Architecture Decision Documentation

Always explain **why**, not just **what**:

**Good:**
```markdown
### Architecture Decisions

**Choice: JWT tokens over sessions**
- Rationale: API needs to be stateless for horizontal scaling
- Trade-off: Tokens can't be revoked until expiry (mitigated with 15min expiry)
- Implementation: Use existing `pyjwt` library already in project

**Choice: Bcrypt for password hashing**
- Rationale: Industry standard, already used in related project
- Configuration: Cost factor of 12 (matches security team guidelines)
```

**Avoid:**
```markdown
### Architecture Decisions
- Using JWT
- Using Bcrypt
```

## Dependencies and Ordering

### Explicit Dependencies

```markdown
#### Task 1: Create User Model
Dependencies: None

#### Task 2: Create UserRepository
Dependencies: Task 1 (needs User model definition)

#### Task 3: Implement Registration Endpoint
Dependencies: Task 1, Task 2

#### Task 4: Add Registration Tests
Dependencies: Task 3
```

### Natural Ordering

Follow the natural flow of development:

1. **Foundation first**: Models, schemas, database
2. **Core logic**: Services, utilities, business logic
3. **API layer**: Endpoints, handlers, middleware
4. **Frontend**: UI components, state management
5. **Integration**: Connecting pieces
6. **Testing**: Comprehensive tests
7. **Documentation**: User guides, API docs

## Edge Cases and Error Handling

### Identify Early

For each task, consider:
- What could go wrong?
- What are the edge cases?
- How should errors be handled?
- What validation is needed?

**Example:**
```markdown
#### Task 3: User Registration Endpoint

**Core functionality:**
- Accept email and password
- Validate input
- Create user record
- Return success response

**Edge cases to handle:**
- Email already exists → Return 409 Conflict
- Invalid email format → Return 400 with validation error
- Password too weak → Return 400 with requirements
- Database connection failure → Return 500, log error
- Rate limiting → Return 429 if >5 attempts/minute

**Validation:**
- Email: Valid format, max 255 chars, lowercase
- Password: Min 8 chars, must include number and special char
```

## Testing Strategy

### Test Coverage Planning

For each feature, identify:
- **Unit tests**: Individual functions and methods
- **Integration tests**: API endpoints, database operations
- **Edge case tests**: Error conditions, boundary values
- **Security tests**: Authentication, authorization, input validation

**Example:**
```markdown
### Testing Strategy

**Unit Tests:**
- `test_hash_password()` - Password hashing utility
- `test_validate_email()` - Email validation
- `test_generate_jwt_token()` - Token generation

**Integration Tests:**
- `test_register_user_success()` - Happy path registration
- `test_register_duplicate_email()` - Duplicate prevention
- `test_login_with_valid_credentials()` - Authentication flow
- `test_login_with_invalid_credentials()` - Auth failure

**Security Tests:**
- `test_sql_injection_prevention()` - Input sanitization
- `test_rate_limiting()` - Brute force protection
- `test_password_strength_requirements()` - Password policy
```

## Example: Complete Feature Plan

```markdown
## Feature: User Profile Management

### Overview
Allow users to view and edit their profile information including name, bio, and avatar. Profiles are public but only editable by the owner.

### Architecture Decisions

**Choice: Store avatars in S3**
- Rationale: Existing S3 bucket and upload utilities available
- Location: Follow pattern from `src/utils/s3_upload.py`
- Size limit: 5MB (enforced in backend)

**Choice: Optimistic UI updates**
- Rationale: Better UX, matches existing patterns
- Rollback on error via Redux state management

### Implementation Tasks

#### Task 1: Extend User Model
- **File**: `src/models/user.py:23`
- **Description**: Add profile fields to User model
- **Details**:
  - Add fields: `bio` (text, max 500 chars), `avatar_url` (string, nullable)
  - Create migration for new fields
  - Add validation methods
- **Dependencies**: None
- **Reference**: See model pattern in `src/models/post.py:15-45`

#### Task 2: Create Profile API Endpoints
- **File**: `src/api/routes/profile.py` (new file)
- **Description**: Add GET and PATCH endpoints for profile
- **Details**:
  - `GET /api/users/:id/profile` - Public, anyone can view
  - `PATCH /api/users/:id/profile` - Protected, owner only
  - Authorization: Use existing `@require_auth` decorator
  - Validation: Bio max 500 chars, avatar_url is valid URL
- **Dependencies**: Task 1
- **Reference**: Follow pattern from `src/api/routes/posts.py:67-89`

#### Task 3: Avatar Upload Utility
- **File**: `src/services/avatar_service.py` (new file)
- **Description**: Handle avatar upload to S3 with validation
- **Details**:
  - Accept image files (jpg, png, gif)
  - Validate size (max 5MB)
  - Resize to 400x400px
  - Upload to S3 using existing `S3Upload` class
  - Return public URL
- **Dependencies**: None (can work parallel to Task 1-2)
- **Reference**: Use `src/utils/s3_upload.py` and `src/services/image_processor.py`

#### Task 4: Frontend Profile Component
- **File**: `src/components/Profile/ProfileView.tsx` (new file)
- **Description**: Display user profile information
- **Details**:
  - Show avatar, name, bio
  - Conditional "Edit" button if viewing own profile
  - Responsive layout
  - Loading and error states
- **Dependencies**: Task 2 (needs API)
- **Reference**: Similar layout to `src/components/Post/PostView.tsx`

#### Task 5: Frontend Profile Edit Component
- **File**: `src/components/Profile/ProfileEdit.tsx` (new file)
- **Description**: Edit profile with avatar upload
- **Details**:
  - Form with bio textarea, avatar file upload
  - Character counter for bio (500 max)
  - Image preview before upload
  - Optimistic updates on save
  - Validation and error display
- **Dependencies**: Task 3, Task 4
- **Reference**: Form pattern from `src/components/Post/PostEditor.tsx`

#### Task 6: Integration Tests
- **File**: `tests/integration/test_profile_api.py` (new file)
- **Description**: Test profile endpoints
- **Tests**:
  - View any user's profile (public)
  - Edit own profile (success)
  - Edit other's profile (forbidden)
  - Bio validation (too long)
  - Avatar upload (success and size limit)
- **Dependencies**: Task 1, Task 2, Task 3

#### Task 7: Frontend Tests
- **File**: `tests/components/Profile.test.tsx` (new file)
- **Description**: Test profile components
- **Tests**:
  - ProfileView renders correctly
  - Edit button shown for own profile only
  - ProfileEdit form validation
  - Avatar upload preview
  - Optimistic update behavior
- **Dependencies**: Task 4, Task 5

### Testing Strategy

**Unit Tests:**
- User model validation methods
- Avatar resizing logic
- S3 upload utility

**Integration Tests:**
- API endpoints (all success and error cases)
- Authorization (owner vs non-owner)
- End-to-end profile update flow

**Security:**
- Authorization enforcement (can't edit others' profiles)
- File upload validation (type, size)
- XSS prevention in bio field

### Integration Points

**Existing systems affected:**
- User model (extends with new fields)
- S3 bucket (shares with post images)
- Auth middleware (reuses existing decorators)

**New routes:**
- `GET /api/users/:id/profile`
- `PATCH /api/users/:id/profile`
- `POST /api/users/:id/avatar` (upload)
```

## Anti-Patterns to Avoid

### 1. Over-Planning

**Bad:**
Planning every single line of code, including variable names and exact syntax.

**Good:**
Plan structure, key decisions, and task boundaries. Let implementer handle details.

### 2. Under-Planning

**Bad:**
"Add user profiles" with no further detail.

**Good:**
Break down into tasks with context, files, and acceptance criteria.

### 3. Ignoring Existing Patterns

**Bad:**
Designing from scratch without checking the codebase.

**Good:**
Reference existing code patterns and maintain consistency.

### 4. Skipping Edge Cases

**Bad:**
Only planning the happy path.

**Good:**
Explicitly call out error handling and validation for each task.

### 5. Creating Dependent Chains

**Bad:**
Every task depends on the previous one, forcing strict sequential execution.

**Good:**
Identify tasks that can be parallelized (e.g., backend and frontend utilities).

## Checklist for a Good Plan

Before handing off to plan-implementer, verify:

- [ ] Requirements are clearly understood
- [ ] Architecture decisions are documented with rationale
- [ ] Tasks are right-sized (30min - 2hrs each)
- [ ] Each task has clear acceptance criteria
- [ ] Dependencies are explicitly stated
- [ ] File paths and code references are included
- [ ] Edge cases and error handling are addressed
- [ ] Testing strategy is defined
- [ ] Follows existing project patterns (checked CLAUDE.md)
- [ ] User has reviewed and approved the plan
