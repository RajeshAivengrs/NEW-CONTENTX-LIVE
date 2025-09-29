#!/usr/bin/env python3
"""
Razorpay Payment Backend for Content X AI Studio
Optimized for Indian market with INR pricing
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uuid

# Mock Razorpay client for testing (replace with real import in production)
class MockCustomerAPI:
    def create(self, data):
        return {
            "id": f"cust_{uuid.uuid4().hex[:14]}",
            **data,
            "created_at": datetime.now().timestamp()
        }

class MockOrderAPI:
    def create(self, data):
        return {
            "id": f"order_{uuid.uuid4().hex[:14]}",
            **data,
            "status": "created"
        }

class MockUtilityAPI:
    def verify_payment_signature(self, params):
        # Mock verification - always returns True
        return True

class MockPaymentAPI:
    def refund(self, payment_id, data):
        return {
            "id": f"rfnd_{uuid.uuid4().hex[:14]}",
            "payment_id": payment_id,
            **data,
            "status": "processed"
        }

class MockRazorpayClient:
    def __init__(self, auth):
        self.key_id, self.key_secret = auth
        self.customer = MockCustomerAPI()
        self.order = MockOrderAPI()
        self.utility = MockUtilityAPI()
        self.payment = MockPaymentAPI()

# Try to import real Razorpay, fallback to mock
try:
    import razorpay
    RazorpayClient = razorpay.Client
except ImportError:
    RazorpayClient = MockRazorpayClient

# Configure logging
logger = logging.getLogger(__name__)

class RazorpayBackend:
    def __init__(self):
        """Initialize Razorpay backend"""
        self.razorpay_key_id = os.getenv("RAZORPAY_KEY_ID", "rzp_test_123456789")
        self.razorpay_key_secret = os.getenv("RAZORPAY_KEY_SECRET", "test_secret_123456789")
        
        try:
            self.client = RazorpayClient(auth=(self.razorpay_key_id, self.razorpay_key_secret))
            if isinstance(self.client, MockRazorpayClient):
                logger.info("Razorpay backend initialized in demo mode!")
            else:
                logger.info("Razorpay backend initialized successfully!")
        except Exception as e:
            logger.error(f"Failed to initialize Razorpay: {e}")
            self.client = None
        
        # In-memory storage for demo (replace with database in production)
        self.customers = {}
        self.subscriptions = {}
        self.payments = {}
        
        # Indian pricing plans in INR
        self.plans = {
            "script-starter": {
                "name": "Script Starter",
                "amount": 1200,  # ₹1200
                "currency": "INR",
                "interval": "monthly",
                "description": "100 AI-generated scripts per month"
            },
            "script-professional": {
                "name": "Script Professional", 
                "amount": 3500,  # ₹3500
                "currency": "INR",
                "interval": "monthly",
                "description": "500 AI-generated scripts per month"
            },
            "script-enterprise": {
                "name": "Script Enterprise",
                "amount": 7500,  # ₹7500
                "currency": "INR", 
                "interval": "monthly",
                "description": "Unlimited AI-generated scripts"
            },
            "content-creator": {
                "name": "Content Creator",
                "amount": 2500,  # ₹2500
                "currency": "INR",
                "interval": "monthly", 
                "description": "Scripts + Video creation (50 videos/month)"
            },
            "content-professional": {
                "name": "Content Professional",
                "amount": 5000,  # ₹5000
                "currency": "INR",
                "interval": "monthly",
                "description": "Scripts + Video creation (200 videos/month)"
            },
            "content-enterprise": {
                "name": "Content Enterprise", 
                "amount": 10000,  # ₹10000
                "currency": "INR",
                "interval": "monthly",
                "description": "Scripts + Video creation (unlimited)"
            },
            "publishing-basic": {
                "name": "Publishing Basic",
                "amount": 800,  # ₹800
                "currency": "INR",
                "interval": "monthly",
                "description": "Basic publishing automation"
            },
            "publishing-pro": {
                "name": "Publishing Pro",
                "amount": 2000,  # ₹2000
                "currency": "INR", 
                "interval": "monthly",
                "description": "Advanced publishing with analytics"
            },
            "full-stack": {
                "name": "Full Stack",
                "amount": 15000,  # ₹15000
                "currency": "INR",
                "interval": "monthly",
                "description": "Everything: Scripts + Videos + Publishing"
            }
        }

    def create_customer(self, email: str, name: str, phone: str = None) -> Dict[str, Any]:
        """Create a new customer in Razorpay"""
        try:
            customer_data = {
                "name": name,
                "email": email,
                "contact": phone,
                "notes": {
                    "platform": "Content X AI Studio",
                    "created_at": datetime.now().isoformat()
                }
            }
            
            if self.client:
                customer = self.client.customer.create(customer_data)
                customer_id = customer["id"]
            else:
                # Demo mode
                customer_id = f"cust_{uuid.uuid4().hex[:14]}"
                customer = {"id": customer_id, **customer_data}
            
            self.customers[customer_id] = customer
            
            return {
                "success": True,
                "customer_id": customer_id,
                "customer": customer
            }
            
        except Exception as e:
            logger.error(f"Error creating customer: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def create_payment_intent(self, customer_id: str, plan_id: str, quantity: int = 1) -> Dict[str, Any]:
        """Create a payment intent for subscription"""
        try:
            if plan_id not in self.plans:
                return {
                    "success": False,
                    "error": "Invalid plan ID"
                }
            
            plan = self.plans[plan_id]
            amount = plan["amount"] * quantity * 100  # Convert to paise
            
            payment_data = {
                "amount": amount,
                "currency": plan["currency"],
                "receipt": f"receipt_{uuid.uuid4().hex[:12]}",
                "notes": {
                    "plan_id": plan_id,
                    "customer_id": customer_id,
                    "quantity": quantity,
                    "plan_name": plan["name"]
                }
            }
            
            if self.client:
                order = self.client.order.create(payment_data)
                order_id = order["id"]
            else:
                # Demo mode
                order_id = f"order_{uuid.uuid4().hex[:14]}"
                order = {
                    "id": order_id,
                    "amount": amount,
                    "currency": plan["currency"],
                    "receipt": payment_data["receipt"],
                    "status": "created"
                }
            
            self.payments[order_id] = {
                "order": order,
                "customer_id": customer_id,
                "plan_id": plan_id,
                "quantity": quantity,
                "created_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "order_id": order_id,
                "amount": amount,
                "currency": plan["currency"],
                "key_id": self.razorpay_key_id,
                "order": order
            }
            
        except Exception as e:
            logger.error(f"Error creating payment intent: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def verify_payment(self, order_id: str, payment_id: str, signature: str) -> Dict[str, Any]:
        """Verify payment signature"""
        try:
            if self.client:
                params = {
                    'razorpay_order_id': order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
                
                # Verify the payment signature
                self.client.utility.verify_payment_signature(params)
            
            # Update payment status
            if order_id in self.payments:
                self.payments[order_id]["payment_id"] = payment_id
                self.payments[order_id]["status"] = "paid"
                self.payments[order_id]["paid_at"] = datetime.now().isoformat()
                
                # Create subscription
                subscription_id = self.create_subscription(order_id)
                
                return {
                    "success": True,
                    "payment_verified": True,
                    "subscription_id": subscription_id,
                    "message": "Payment verified successfully"
                }
            
            return {
                "success": False,
                "error": "Order not found"
            }
            
        except Exception as e:
            logger.error(f"Payment verification failed: {e}")
            return {
                "success": False,
                "error": "Payment verification failed",
                "details": str(e)
            }

    def create_subscription(self, order_id: str) -> str:
        """Create subscription after successful payment"""
        if order_id not in self.payments:
            return None
        
        payment_info = self.payments[order_id]
        subscription_id = f"sub_{uuid.uuid4().hex[:14]}"
        
        subscription = {
            "id": subscription_id,
            "customer_id": payment_info["customer_id"],
            "plan_id": payment_info["plan_id"],
            "quantity": payment_info["quantity"],
            "status": "active",
            "start_date": datetime.now().isoformat(),
            "next_billing_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "order_id": order_id
        }
        
        self.subscriptions[subscription_id] = subscription
        
        return subscription_id

    def get_subscription_status(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription status"""
        if subscription_id in self.subscriptions:
            subscription = self.subscriptions[subscription_id]
            plan = self.plans.get(subscription["plan_id"], {})
            
            return {
                "success": True,
                "subscription": subscription,
                "plan": plan
            }
        
        return {
            "success": False,
            "error": "Subscription not found"
        }

    def get_pricing_plans(self) -> Dict[str, Any]:
        """Get all available pricing plans"""
        return {
            "success": True,
            "plans": self.plans,
            "currency": "INR",
            "country": "India"
        }

    def create_refund(self, payment_id: str, amount: int = None) -> Dict[str, Any]:
        """Create refund for payment"""
        try:
            if self.client:
                refund_data = {"payment_id": payment_id}
                if amount:
                    refund_data["amount"] = amount
                
                refund = self.client.payment.refund(payment_id, refund_data)
                refund_id = refund["id"]
            else:
                # Demo mode
                refund_id = f"rfnd_{uuid.uuid4().hex[:14]}"
                refund = {
                    "id": refund_id,
                    "payment_id": payment_id,
                    "amount": amount,
                    "status": "processed"
                }
            
            return {
                "success": True,
                "refund_id": refund_id,
                "refund": refund
            }
            
        except Exception as e:
            logger.error(f"Error creating refund: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_payment_history(self, customer_id: str) -> Dict[str, Any]:
        """Get payment history for customer"""
        customer_payments = [
            payment for payment in self.payments.values()
            if payment["customer_id"] == customer_id
        ]
        
        return {
            "success": True,
            "payments": customer_payments
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get payment backend statistics"""
        total_customers = len(self.customers)
        total_subscriptions = len(self.subscriptions)
        active_subscriptions = len([
            sub for sub in self.subscriptions.values()
            if sub["status"] == "active"
        ])
        
        total_revenue = sum([
            self.plans[payment["plan_id"]]["amount"] * payment["quantity"]
            for payment in self.payments.values()
            if payment.get("status") == "paid"
        ])
        
        return {
            "total_customers": total_customers,
            "total_subscriptions": total_subscriptions,
            "active_subscriptions": active_subscriptions,
            "total_revenue_inr": total_revenue,
            "currency": "INR",
            "backend": "Razorpay"
        }

# Initialize global instance
razorpay_backend = RazorpayBackend()
