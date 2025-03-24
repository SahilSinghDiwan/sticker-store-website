from typing import Dict, Any, Optional
from datetime import datetime
from bson import ObjectId

class User:
    def __init__(
        self,
        email: str,
        name: str,
        password: bytes,
        role: str = "customer",
        _id: Optional[str] = None,
        active: bool = True
    ):
        self._id = ObjectId(_id) if _id else ObjectId()
        self.email = email
        self.name = name
        self.password = password
        self.role = role
        self.active = active
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.last_login = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            '_id': self._id,
            'email': self.email,
            'name': self.name,
            'password': self.password,
            'role': self.role,
            'active': self.active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_login': self.last_login
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'User':
        return User(
            email=data['email'],
            name=data['name'],
            password=data['password'],
            role=data.get('role', 'customer'),
            _id=str(data['_id']) if data.get('_id') else None,
            active=data.get('active', True)
        ) 