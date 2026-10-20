# Authentication

    - Verifies the identity of a user or system
    - who are you ?
    - email, password -> login
    - Examples: logging in with username/password, OTP, biometric scan, JWT token validation
    - If authentication fails, the request is rejected outright — the system doesn't even know who's asking

# Authorization

    - Determines what an authenticated user can access or perform
    - what can you do ?
    - Examples: checking if a user has admin role, permission to edit a resource, or access to a specific API endpoint
    - If authorization fails, the system knows who you are but denies the specific action
    User A:
        Youtube - Application
        - login - email, password (Authenticated)
        - Authorization
          - video = upload
          - video = delete
          - video = comments(read)

    User B:
        Youtube = Application
        - login = email, password (Authenticated)
        - Authorization
          - video = watch
          - video = like
          - video = comments
          - subscribe
