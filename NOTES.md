Implement JWT authentication for protected endpoints

- Update SignupPage to create new user with password hashing
- Update LoginPage to validate email and password and generate new bearer token
- Add logic to save and retrieve the bearer token to localStorage, ensuring secure API calls.
- Implement fetching and displaying account data with bearer token authentication
- Implement `GetSelfAccounts` Page to asynchronously fetch account data from `/api/accounts/self_accounts` using a bearer token for authentication.

