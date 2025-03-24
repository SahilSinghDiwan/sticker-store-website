```
flask-auth-app/
├── app.py
├── models.py
├── routes.py
├── auth.py
├── db.py
├── utils.py
├── config.py
└── requirements.txt
```

## ✅ **Testing the API**

You can test using **Postman** or **curl**:

### 1. **Signup**

```bash
curl -X POST http://localhost:5000/signup \
-H "Content-Type: application/json" \
-d '{"username": "user1", "email": "user1@example.com", "password": "password123"}'
```

### 2. **Login**

```bash
curl -X POST http://localhost:5000/login \
-H "Content-Type: application/json" \
-d '{"email": "user1@example.com", "password": "password123"}'
```

_Response will contain the JWT token._

### 3. **Access Protected Route**

```bash
curl -X GET http://localhost:5000/protected \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## ✅ **Next Steps**

- Implement Logout (optional) by using JWT blacklisting.
- Add error handling using `Flask-RESTful`.
- Add logging for better monitoring.

Would you like me to implement JWT blacklisting for the logout feature next?
