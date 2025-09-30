# 🚀 Content X AI Studio - Render Deployment Guide

## Complete Enterprise AI Content Generation Platform

### **Deployment Steps:**

#### **1. Create Render Account**
- Go to: https://render.com
- Sign up with GitHub

#### **2. Connect GitHub Repository**
- Click "New +" → "Web Service"
- Connect to GitHub: `RajeshAivengrs/Skryptr-ai-script-generator`
- Or create new repo: `content-x-ai-studio`

#### **3. Configure Service**
- **Name**: `content-x-ai-studio`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python simple_main.py`
- **Plan**: `Starter` (Free) or `Standard` (Paid)

#### **4. Environment Variables**
Set these in Render dashboard:
```
GOOGLE_CLIENT_ID=380396473123-qcdr7697unq06lsoe1su9d8vitjr6uk9.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_secret
RAZORPAY_KEY_ID=rzp_live_your_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
JWT_SECRET=contentx_production_jwt_secret_key_2024
```

#### **5. Deploy**
- Click "Create Web Service"
- Wait for build (5-10 minutes)
- Get live URL: `https://content-x-ai-studio.onrender.com`

### **Features Included:**
✅ **Complete UI/UX** - Premium aqua-themed design
✅ **Real OAuth** - Google & LinkedIn authentication
✅ **Payment Integration** - Razorpay for Indian market
✅ **AI Content Generation** - Scripts, videos, voice
✅ **Voice Cloning** - ElevenLabs integration
✅ **Video Creation** - 3D avatars, reels, automation
✅ **Publishing Automation** - Social media posting
✅ **Enterprise Dashboard** - Analytics, management
✅ **ICP Builder** - Customer profile creation
✅ **Dynamic Pricing** - INR-based cost analysis

### **Live URLs After Deployment:**
- **Homepage**: `https://your-app.onrender.com/`
- **Features**: `https://your-app.onrender.com/features`
- **Pricing**: `https://your-app.onrender.com/pricing`
- **Dashboard**: `https://your-app.onrender.com/dashboard`
- **ICP Builder**: `https://your-app.onrender.com/icp-builder`
- **Google Auth**: `https://your-app.onrender.com/auth/google`

### **API Endpoints:**
- **Health**: `https://your-app.onrender.com/health`
- **Content Generation**: `https://your-app.onrender.com/api/content/generate`
- **Payment**: `https://your-app.onrender.com/api/payment/create`
- **Voice**: `https://your-app.onrender.com/api/voice/generate`

### **Troubleshooting:**
- **Build Fails**: Check Python version (3.11.0)
- **Dependencies**: All included in requirements.txt
- **Memory**: Use Standard plan for heavy AI features
- **Timeout**: Render free tier has 15min sleep

### **Production Ready:**
This deployment includes ALL Content X AI Studio features:
- Complete microservices architecture
- Real authentication & payments
- AI content generation pipeline
- Social media automation
- Enterprise-grade UI/UX
- Cost optimization & analytics

**Ready for commercial launch! 🚀**
