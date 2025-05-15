# Environment Configuration

Configure the `.env` file in the root of your project:

```env
# Environment
ENVIRONMENT=dev

# Database
DATABASE_URL=sqlite:///./taskflow.db

# Security
SECRET_KEY="_secret_key_"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:5173
```

> For production, use PostgreSQL and replace the `DATABASE_URL` accordingly.

---

You're now ready to use or contribute to TaskFlow!
