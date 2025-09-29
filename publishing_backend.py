"""
Content X AI Studio - Publishing Backend
Complete social media publishing automation system
"""

import asyncio
import json
import logging
import os
import time
import uuid
import hashlib
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiohttp
import httpx

logger = logging.getLogger(__name__)

class PublishingBackend:
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.output_dir = Path("generated_content")
        self.publishing_dir = Path("publishing")
        self.schedules_dir = Path("schedules")
        
        # Create directories
        for dir_path in [self.upload_dir, self.output_dir, self.publishing_dir, self.schedules_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # API Keys (in production, use environment variables)
        self.instagram_token = os.getenv("INSTAGRAM_TOKEN", "demo_token")
        self.facebook_token = os.getenv("FACEBOOK_TOKEN", "demo_token")
        self.linkedin_token = os.getenv("LINKEDIN_TOKEN", "demo_token")
        self.twitter_token = os.getenv("TWITTER_TOKEN", "demo_token")
        
        # Publishing status tracking
        self.publishing_jobs = {}
        self.scheduled_posts = {}
        self.platform_status = {
            "instagram": {"connected": False, "last_check": None},
            "facebook": {"connected": False, "last_check": None},
            "linkedin": {"connected": False, "last_check": None},
            "twitter": {"connected": False, "last_check": None}
        }
        
        # Content optimization rules
        self.platform_optimizations = {
            "instagram": {
                "max_caption_length": 2200,
                "hashtag_limit": 30,
                "image_ratios": ["1:1", "4:5", "9:16"],
                "video_max_duration": 60,
                "supported_formats": ["jpg", "jpeg", "png", "mp4", "mov"]
            },
            "facebook": {
                "max_text_length": 63206,
                "image_ratios": ["1:1", "16:9", "4:5"],
                "video_max_duration": 240,
                "supported_formats": ["jpg", "jpeg", "png", "gif", "mp4", "mov"]
            },
            "linkedin": {
                "max_text_length": 3000,
                "image_ratios": ["1:1", "16:9"],
                "video_max_duration": 600,
                "supported_formats": ["jpg", "jpeg", "png", "mp4", "mov"]
            },
            "twitter": {
                "max_text_length": 280,
                "image_ratios": ["16:9", "1:1"],
                "video_max_duration": 140,
                "supported_formats": ["jpg", "jpeg", "png", "gif", "mp4", "mov"]
            }
        }
    
    async def connect_platform(self, platform: str, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Connect to a social media platform"""
        try:
            # Simulate platform connection
            await asyncio.sleep(random.uniform(1, 3))
            
            # Store credentials (in production, encrypt these)
            self.platform_status[platform]["connected"] = True
            self.platform_status[platform]["last_check"] = datetime.now(timezone.utc).isoformat()
            
            # Simulate API validation
            connection_id = f"{platform}_{int(time.time())}"
            
            logger.info(f"Successfully connected to {platform}")
            
            return {
                "status": "success",
                "platform": platform,
                "connection_id": connection_id,
                "connected_at": datetime.now(timezone.utc).isoformat(),
                "capabilities": self.platform_optimizations[platform]
            }
            
        except Exception as e:
            logger.error(f"Error connecting to {platform}: {e}")
            return {
                "status": "error",
                "platform": platform,
                "error": str(e)
            }
    
    async def schedule_post(self, user_id: str, content: Dict[str, Any], 
                          platforms: List[str], schedule_time: str) -> Dict[str, Any]:
        """Schedule a post across multiple platforms"""
        try:
            post_id = str(uuid.uuid4())
            schedule_datetime = datetime.fromisoformat(schedule_time.replace('Z', '+00:00'))
            
            # Validate content for each platform
            optimized_content = await self._optimize_content_for_platforms(content, platforms)
            
            # Create scheduled post
            scheduled_post = {
                "post_id": post_id,
                "user_id": user_id,
                "content": optimized_content,
                "platforms": platforms,
                "schedule_time": schedule_datetime.isoformat(),
                "status": "scheduled",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "optimizations": {}
            }
            
            # Store scheduled post
            self.scheduled_posts[post_id] = scheduled_post
            
            # Schedule the actual posting
            asyncio.create_task(self._execute_scheduled_post(post_id))
            
            logger.info(f"Scheduled post {post_id} for {len(platforms)} platforms")
            
            return {
                "status": "success",
                "post_id": post_id,
                "schedule_time": schedule_datetime.isoformat(),
                "platforms": platforms,
                "optimized_content": optimized_content
            }
            
        except Exception as e:
            logger.error(f"Error scheduling post: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def publish_immediately(self, user_id: str, content: Dict[str, Any], 
                                platforms: List[str]) -> Dict[str, Any]:
        """Publish content immediately across platforms"""
        try:
            post_id = str(uuid.uuid4())
            
            # Optimize content for each platform
            optimized_content = await self._optimize_content_for_platforms(content, platforms)
            
            # Create publishing job
            self.publishing_jobs[post_id] = {
                "post_id": post_id,
                "user_id": user_id,
                "content": optimized_content,
                "platforms": platforms,
                "status": "publishing",
                "created_at": datetime.now(timezone.utc),
                "results": {}
            }
            
            # Start publishing process
            asyncio.create_task(self._publish_to_platforms(post_id))
            
            return {
                "status": "publishing",
                "post_id": post_id,
                "platforms": platforms,
                "estimated_time": f"{len(platforms) * 2} minutes"
            }
            
        except Exception as e:
            logger.error(f"Error publishing immediately: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _optimize_content_for_platforms(self, content: Dict[str, Any], 
                                            platforms: List[str]) -> Dict[str, Any]:
        """Optimize content for each platform's requirements"""
        optimized = content.copy()
        
        for platform in platforms:
            platform_rules = self.platform_optimizations[platform]
            
            # Optimize text/caption
            if "text" in content:
                text = content["text"]
                max_length = platform_rules.get("max_text_length", 1000)  # Default fallback
                
                if len(text) > max_length:
                    text = text[:max_length-3] + "..."
                
                optimized[f"{platform}_text"] = text
            
            # Optimize hashtags
            if "hashtags" in content:
                hashtags = content["hashtags"]
                hashtag_limit = platform_rules.get("hashtag_limit", 30)
                
                if len(hashtags) > hashtag_limit:
                    hashtags = hashtags[:hashtag_limit]
                
                optimized[f"{platform}_hashtags"] = hashtags
            
            # Add platform-specific optimizations
            optimized[f"{platform}_optimized"] = True
        
        return optimized
    
    async def _execute_scheduled_post(self, post_id: str):
        """Execute a scheduled post when the time comes"""
        try:
            post = self.scheduled_posts[post_id]
            schedule_time = datetime.fromisoformat(post["schedule_time"])
            
            # Wait until scheduled time
            now = datetime.now(timezone.utc)
            if schedule_time > now:
                wait_seconds = (schedule_time - now).total_seconds()
                await asyncio.sleep(wait_seconds)
            
            # Publish to platforms
            await self._publish_to_platforms(post_id)
            
        except Exception as e:
            logger.error(f"Error executing scheduled post {post_id}: {e}")
            if post_id in self.scheduled_posts:
                self.scheduled_posts[post_id]["status"] = "failed"
                self.scheduled_posts[post_id]["error"] = str(e)
    
    async def _publish_to_platforms(self, post_id: str):
        """Publish content to all specified platforms"""
        try:
            job = self.publishing_jobs.get(post_id) or self.scheduled_posts.get(post_id)
            if not job:
                return
            
            platforms = job["platforms"]
            content = job["content"]
            results = {}
            
            for platform in platforms:
                try:
                    # Simulate platform-specific publishing
                    result = await self._publish_to_platform(platform, content, post_id)
                    results[platform] = result
                    
                    # Add delay between platforms
                    await asyncio.sleep(random.uniform(2, 5))
                    
                except Exception as e:
                    logger.error(f"Error publishing to {platform}: {e}")
                    results[platform] = {
                        "status": "failed",
                        "error": str(e)
                    }
            
            # Update job status
            job["status"] = "completed"
            job["results"] = results
            job["completed_at"] = datetime.now(timezone.utc).isoformat()
            
            logger.info(f"Completed publishing job {post_id}")
            
        except Exception as e:
            logger.error(f"Error in publishing process: {e}")
            if post_id in self.publishing_jobs:
                self.publishing_jobs[post_id]["status"] = "failed"
                self.publishing_jobs[post_id]["error"] = str(e)
    
    async def _publish_to_platform(self, platform: str, content: Dict[str, Any], 
                                 post_id: str) -> Dict[str, Any]:
        """Publish content to a specific platform"""
        try:
            # Simulate API call to platform
            await asyncio.sleep(random.uniform(3, 8))
            
            # Generate platform-specific post ID
            platform_post_id = f"{platform}_{post_id}_{int(time.time())}"
            
            # Simulate successful posting
            result = {
                "status": "success",
                "platform": platform,
                "platform_post_id": platform_post_id,
                "published_at": datetime.now(timezone.utc).isoformat(),
                "url": f"https://{platform}.com/posts/{platform_post_id}",
                "metrics": {
                    "likes": random.randint(0, 1000),
                    "shares": random.randint(0, 100),
                    "comments": random.randint(0, 50)
                }
            }
            
            logger.info(f"Successfully published to {platform}: {platform_post_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error publishing to {platform}: {e}")
            return {
                "status": "failed",
                "platform": platform,
                "error": str(e)
            }
    
    def get_publishing_status(self, post_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a publishing job"""
        job = self.publishing_jobs.get(post_id) or self.scheduled_posts.get(post_id)
        if not job:
            return None
        
        # Convert datetime objects to ISO strings
        result = job.copy()
        if 'created_at' in result and hasattr(result['created_at'], 'isoformat'):
            result['created_at'] = result['created_at'].isoformat()
        if 'completed_at' in result and hasattr(result['completed_at'], 'isoformat'):
            result['completed_at'] = result['completed_at'].isoformat()
        
        return result
    
    def get_scheduled_posts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all scheduled posts for a user"""
        user_posts = []
        for post in self.scheduled_posts.values():
            if post["user_id"] == user_id:
                # Convert datetime objects
                result = post.copy()
                if 'created_at' in result and hasattr(result['created_at'], 'isoformat'):
                    result['created_at'] = result['created_at'].isoformat()
                user_posts.append(result)
        
        return sorted(user_posts, key=lambda x: x["schedule_time"], reverse=True)
    
    def get_publishing_analytics(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Get publishing analytics for a user"""
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        total_posts = 0
        successful_posts = 0
        platform_stats = {}
        
        # Analyze publishing jobs
        for job in self.publishing_jobs.values():
            if job["user_id"] == user_id:
                created_at = job.get("created_at")
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                
                if start_date <= created_at <= end_date:
                    total_posts += 1
                    if job.get("status") == "completed":
                        successful_posts += 1
                    
                    # Platform statistics
                    for platform, result in job.get("results", {}).items():
                        if platform not in platform_stats:
                            platform_stats[platform] = {"posts": 0, "successful": 0}
                        
                        platform_stats[platform]["posts"] += 1
                        if result.get("status") == "success":
                            platform_stats[platform]["successful"] += 1
        
        return {
            "period": f"{days} days",
            "total_posts": total_posts,
            "successful_posts": successful_posts,
            "success_rate": round(successful_posts / total_posts * 100, 2) if total_posts > 0 else 0,
            "platform_stats": platform_stats,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    
    def get_platform_status(self) -> Dict[str, Any]:
        """Get status of all connected platforms"""
        return {
            "platforms": self.platform_status,
            "total_connected": sum(1 for p in self.platform_status.values() if p["connected"]),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    
    def cancel_scheduled_post(self, post_id: str) -> Dict[str, Any]:
        """Cancel a scheduled post"""
        if post_id in self.scheduled_posts:
            self.scheduled_posts[post_id]["status"] = "cancelled"
            return {
                "status": "success",
                "message": "Post cancelled successfully"
            }
        else:
            return {
                "status": "error",
                "message": "Post not found"
            }

# Initialize publishing backend
publishing_backend = PublishingBackend()
