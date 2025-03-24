from typing import Optional, Dict, Any
import re, decimal
from decimal import Decimal

def validate_product(data: Dict[str, Any]) -> Optional[str]:
    """Validate product data"""
    required_fields = ['name', 'price', 'description', 'category_id']
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
            
    # Validate price
    try:
        price = Decimal(str(data['price']))
        if price <= 0:
            return "Price must be greater than 0"
        if price > 999999.99:  # Maximum price limit
            return "Price exceeds maximum limit"
        # Ensure only 2 decimal places
        if abs(price.as_tuple().exponent) > 2:
            return "Price can only have up to 2 decimal places"
    except (ValueError, decimal.InvalidOperation):
        return "Invalid price format"
        
    # Validate name
    if not 3 <= len(data['name']) <= 100:
        return "Name must be between 3 and 100 characters"
    if not re.match(r'^[\w\s\-\']+$', data['name']):
        return "Name contains invalid characters"
        
    # Validate description
    if not 10 <= len(data['description']) <= 1000:
        return "Description must be between 10 and 1000 characters"
        
    # Validate category_id format (assuming MongoDB ObjectId)
    if not re.match(r'^[0-9a-fA-F]{24}$', data['category_id']):
        return "Invalid category ID format"
        
    # Validate optional fields
    if 'stock' in data:
        try:
            stock = int(data['stock'])
            if stock < 0:
                return "Stock cannot be negative"
            if stock > 999999:
                return "Stock exceeds maximum limit"
        except ValueError:
            return "Invalid stock format"
            
    if 'tags' in data:
        if not isinstance(data['tags'], list):
            return "Tags must be a list"
        if len(data['tags']) > 10:
            return "Maximum 10 tags allowed"
        for tag in data['tags']:
            if not isinstance(tag, str) or len(tag) > 20:
                return "Invalid tag format"
                
    return None

def validate_order_status(status: str) -> bool:
    """Validate order shipping status"""
    valid_statuses = [
        'pending',
        'processing',
        'shipped',
        'delivered',
        'cancelled',
        'refunded',
        'on_hold'
    ]
    return status.lower() in valid_statuses

def validate_user(data: Dict[str, Any]) -> Optional[str]:
    """Validate user data"""
    required_fields = ['email', 'password', 'firstName', 'lastName']
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
            
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, data['email']):
        return "Invalid email format"
        
    # Validate password strength
    if len(data['password']) < 8:
        return "Password must be at least 8 characters long"
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', data['password']):
        return "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"
        
    # Validate name fields
    name_pattern = r'^[a-zA-Z\s\-\']+$'
    if not 2 <= len(data['firstName']) <= 50:
        return "First name must be between 2 and 50 characters"
    if not re.match(name_pattern, data['firstName']):
        return "First name contains invalid characters"
        
    if not 2 <= len(data['lastName']) <= 50:
        return "Last name must be between 2 and 50 characters"
    if not re.match(name_pattern, data['lastName']):
        return "Last name contains invalid characters"
        
    # Validate optional fields
    if 'phoneNumber' in data:
        phone_pattern = r'^\+?1?\d{9,15}$'
        if not re.match(phone_pattern, data['phoneNumber']):
            return "Invalid phone number format"
            
    if 'address' in data:
        if not isinstance(data['address'], dict):
            return "Address must be an object"
        required_address_fields = ['street', 'city', 'state', 'zipCode', 'country']
        for field in required_address_fields:
            if field not in data['address']:
                return f"Missing required address field: {field}"
                
    return None

def validate_payment(data: Dict[str, Any]) -> Optional[str]:
    """Validate payment data"""
    required_fields = ['amount', 'currency', 'payment_method']
    
    for field in required_fields:
        if field not in data:
            return f"Missing required field: {field}"
            
    try:
        amount = Decimal(str(data['amount']))
        if amount <= 0:
            return "Amount must be greater than 0"
        if amount > 999999.99:
            return "Amount exceeds maximum limit"
    except (ValueError, decimal.InvalidOperation):
        return "Invalid amount format"
        
    if data['currency'] not in ['USD', 'EUR', 'GBP']:
        return "Unsupported currency"
        
    if data['payment_method'] not in ['card', 'paypal', 'bank_transfer']:
        return "Unsupported payment method"
        
    return None 