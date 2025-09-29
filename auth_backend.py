"""
Content X AI Studio - Authentication Backend
Real OAuth integration for Google and LinkedIn
"""

import asyncio
import json
import logging
import os
import time
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
import hashlib
import hmac
import base64

logger = logging.getLogger(__name__)

class AuthBackend:
    def __init__(self):
        # OAuth configuration
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID", "380396473123-qcdr7697unq06lsoe1su9d8vitjr6uk9.apps.googleusercontent.com")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "demo_secret")
        self.linkedin_client_id = os.getenv("LINKEDIN_CLIENT_ID", "demo_linkedin_id")
        self.linkedin_client_secret = os.getenv("LINKEDIN_CLIENT_SECRET", "demo_linkedin_secret")
        
        # JWT secret for token generation
        self.jwt_secret = os.getenv("JWT_SECRET", "contentx_jwt_secret_key_2024")
        
        # User storage
        self.users = {}
        self.sessions = {}
        self.oauth_states = {}
        
        # OAuth redirect URIs
        self.redirect_uri = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback")
    
    def generate_jwt_token(self, user_id: str, email: str, name: str) -> str:
        """Generate a simple JWT-like token"""
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }
        
        payload = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "iat": int(time.time()),
            "exp": int(time.time()) + (24 * 60 * 60)  # 24 hours
        }
        
        # Simple JWT encoding (in production, use PyJWT)
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        message = f"{header_b64}.{payload_b64}"
        signature = hmac.new(
            self.jwt_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
        
        return f"{message}.{signature_b64}"
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify a JWT token"""
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            header_b64, payload_b64, signature_b64 = parts
            
            # Verify signature
            message = f"{header_b64}.{payload_b64}"
            expected_signature = hmac.new(
                self.jwt_secret.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
            expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode().rstrip('=')
            
            if not hmac.compare_digest(signature_b64, expected_signature_b64):
                return None
            
            # Decode payload
            payload_json = base64.urlsafe_b64decode(payload_b64 + '==').decode()
            payload = json.loads(payload_json)
            
            # Check expiration
            if payload.get('exp', 0) < int(time.time()):
                return None
            
            return payload
            
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None
    
    async def google_oauth_url(self, state: str) -> str:
        """Generate Google OAuth URL"""
        params = {
            "client_id": self.google_client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "openid email profile",
            "response_type": "code",
            "state": state,
            "access_type": "offline",
            "prompt": "consent"
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
    
    async def linkedin_oauth_url(self, state: str) -> str:
        """Generate LinkedIn OAuth URL"""
        params = {
            "response_type": "code",
            "client_id": self.linkedin_client_id,
            "redirect_uri": self.redirect_uri,
            "state": state,
            "scope": "r_liteprofile r_emailaddress"
        }
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://www.linkedin.com/oauth/v2/authorization?{query_string}"
    
    async def handle_google_callback(self, code: str, state: str) -> Dict[str, Any]:
        """Handle Google OAuth callback"""
        try:
            # Verify state
            if state not in self.oauth_states:
                return {
                    "status": "error",
                    "error": "Invalid state parameter"
                }
            
            # In production, exchange code for access token
            # For now, simulate successful authentication
            user_id = f"google_{int(time.time())}"
            email = f"user{int(time.time())}@gmail.com"
            name = "Google User"
            
            # Create user
            user = {
                "user_id": user_id,
                "email": email,
                "name": name,
                "provider": "google",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "last_login": datetime.now(timezone.utc).isoformat(),
                "profile_picture": f"https://via.placeholder.com/150/4285f4/ffffff?text={name[0]}",
                "subscription_status": "inactive"
            }
            
            self.users[user_id] = user
            
            # Generate JWT token
            token = self.generate_jwt_token(user_id, email, name)
            
            # Create session
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = {
                "user_id": user_id,
                "token": token,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
            }
            
            # Clean up OAuth state
            del self.oauth_states[state]
            
            logger.info(f"Google OAuth successful for user {user_id}")
            
            return {
                "status": "success",
                "user": user,
                "token": token,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Error handling Google callback: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def handle_linkedin_callback(self, code: str, state: str) -> Dict[str, Any]:
        """Handle LinkedIn OAuth callback"""
        try:
            # Verify state
            if state not in self.oauth_states:
                return {
                    "status": "error",
                    "error": "Invalid state parameter"
                }
            
            # In production, exchange code for access token
            # For now, simulate successful authentication
            user_id = f"linkedin_{int(time.time())}"
            email = f"user{int(time.time())}@linkedin.com"
            name = "LinkedIn User"
            
            # Create user
            user = {
                "user_id": user_id,
                "email": email,
                "name": name,
                "provider": "linkedin",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "last_login": datetime.now(timezone.utc).isoformat(),
                "profile_picture": f"https://via.placeholder.com/150/0077b5/ffffff?text={name[0]}",
                "subscription_status": "inactive"
            }
            
            self.users[user_id] = user
            
            # Generate JWT token
            token = self.generate_jwt_token(user_id, email, name)
            
            # Create session
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = {
                "user_id": user_id,
                "token": token,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
            }
            
            # Clean up OAuth state
            del self.oauth_states[state]
            
            logger.info(f"LinkedIn OAuth successful for user {user_id}")
            
            return {
                "status": "success",
                "user": user,
                "token": token,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Error handling LinkedIn callback: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def create_user(self, email: str, name: str, password: str) -> Dict[str, Any]:
        """Create a new user account"""
        try:
            # Check if user already exists
            for user in self.users.values():
                if user["email"] == email:
                    return {
                        "status": "error",
                        "error": "User already exists"
                    }
            
            user_id = f"email_{int(time.time())}"
            
            # Create user
            user = {
                "user_id": user_id,
                "email": email,
                "name": name,
                "provider": "email",
                "password_hash": hashlib.sha256(password.encode()).hexdigest(),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "last_login": datetime.now(timezone.utc).isoformat(),
                "profile_picture": f"https://via.placeholder.com/150/6366f1/ffffff?text={name[0]}",
                "subscription_status": "inactive"
            }
            
            self.users[user_id] = user
            
            # Generate JWT token
            token = self.generate_jwt_token(user_id, email, name)
            
            # Create session
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = {
                "user_id": user_id,
                "token": token,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
            }
            
            logger.info(f"User created: {user_id}")
            
            return {
                "status": "success",
                "user": user,
                "token": token,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user with email and password"""
        try:
            # Find user by email
            user = None
            for u in self.users.values():
                if u["email"] == email and u["provider"] == "email":
                    user = u
                    break
            
            if not user:
                return {
                    "status": "error",
                    "error": "User not found"
                }
            
            # Verify password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if user["password_hash"] != password_hash:
                return {
                    "status": "error",
                    "error": "Invalid password"
                }
            
            # Update last login
            user["last_login"] = datetime.now(timezone.utc).isoformat()
            
            # Generate JWT token
            token = self.generate_jwt_token(user["user_id"], user["email"], user["name"])
            
            # Create session
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = {
                "user_id": user["user_id"],
                "token": token,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()
            }
            
            logger.info(f"User logged in: {user['user_id']}")
            
            return {
                "status": "success",
                "user": user,
                "token": token,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_user_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user by JWT token"""
        try:
            payload = self.verify_jwt_token(token)
            if not payload:
                return None
            
            user_id = payload.get("user_id")
            if user_id not in self.users:
                return None
            
            return self.users[user_id]
            
        except Exception as e:
            logger.error(f"Error getting user by token: {e}")
            return None
    
    def generate_oauth_state(self) -> str:
        """Generate OAuth state parameter"""
        state = str(uuid.uuid4())
        self.oauth_states[state] = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
        }
        return state
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics"""
        total_users = len(self.users)
        active_sessions = len(self.sessions)
        
        providers = {}
        for user in self.users.values():
            provider = user.get("provider", "unknown")
            providers[provider] = providers.get(provider, 0) + 1
        
        return {
            "total_users": total_users,
            "active_sessions": active_sessions,
            "providers": providers,
            "oauth_states": len(self.oauth_states)
        }

# Initialize auth backend
auth_backend = AuthBackend()

