# Payment System Setup Guide

## Overview

Your shop bot now has **TWO payment options**:

### Option 1: Telegram Payments (Advanced)
- Uses Telegram's official payment system
- Requires payment provider setup
- More professional but complex

### Option 2: Direct Payments (Recommended)
- Simple and direct
- No third-party payment processors
- Money goes directly to your accounts

## 🎯 **Recommended: Direct Payment System**

This is the simplest setup where customers pay directly to your accounts:

### Environment Variables to Set:

Add these to your `.env` file and Render dashboard:

```env
# Your Telegram username (without @)
ADMIN_USERNAME=your_telegram_username

# Your crypto wallet address
CRYPTO_ADDRESS=your_bitcoin_or_ethereum_address

# Your CashApp username (with $)
CASHAPP_USERNAME=$your_cashapp_username

# Your PayPal email
PAYPAL_EMAIL=your_paypal@email.com
```

### How It Works:

1. **Customer selects product** → `/buy_atm_exploit`
2. **Bot shows payment options** → Crypto, CashApp, PayPal
3. **Customer chooses payment method**
4. **Bot provides your payment details**
5. **Customer sends payment directly to you**
6. **Customer confirms payment** → Bot updates inventory
7. **You manually deliver the product**

## 🔧 **Setup Instructions**

### Step 1: Create Your .env File

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here

# Email (for product delivery)
GOOGLE_EMAIL=your_gmail@gmail.com
GOOGLE_PASSWORD=your_gmail_app_password

# Payment Details
ADMIN_USERNAME=your_telegram_username
CRYPTO_ADDRESS=bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
CASHAPP_USERNAME=$YourCashAppUsername
PAYPAL_EMAIL=your_paypal@email.com

# Flask Dashboard
SECRET_KEY=your_secret_key_here
```

### Step 2: Choose Your Bot Version

**For Direct Payments (Recommended):**
- Use `telegram_bot/bot_simple_payment.py`
- Rename it to `bot.py` or update your deployment

**For Telegram Payments:**
- Use `telegram_bot/bot.py` (updated version)
- Requires payment provider setup

### Step 3: Deploy to Render

1. **Push your code to GitHub**
2. **Go to [render.com](https://render.com)**
3. **Create new Blueprint**
4. **Connect your repository**
5. **Add environment variables** in Render dashboard

## 💰 **Payment Flow Example**

```
Customer: /buy_atm_exploit

Bot: 🛒 Purchase Request
     Product: ATM Exploit Program
     Price: $500.00
     Stock: 10 available
     
     Please select your payment method:
     [💳 Pay with Crypto] [💰 Pay with CashApp] [💸 Pay with PayPal]

Customer: *clicks Crypto*

Bot: 💳 Cryptocurrency Payment
     Product: ATM Exploit Program
     Price: $500.00
     
     Send $500.00 worth of crypto to:
     bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
     
     Instructions:
     1. Send the payment to the address above
     2. Include your Telegram username in the payment note
     3. Contact @your_username with your payment proof
     4. Your product will be delivered within 24 hours
     
     Order ID: 123456789_atm_exploit_crypto
     
     [✅ I've Paid] [❌ Cancel]

Customer: *clicks "I've Paid"*

Bot: ✅ Payment Received!
     Product: ATM Exploit Program
     Payment Method: Crypto
     
     Your order has been confirmed! Please contact @your_username 
     with your payment proof to receive your product.
     
     Order ID: 123456789_atm_exploit_crypto
```

## 🔒 **Security Features**

- **Order IDs** for tracking
- **Inventory management** (automatic deduction)
- **Payment confirmation** system
- **Admin verification** required
- **No sensitive data** stored

## 📊 **Benefits**

✅ **No payment processor fees**
✅ **Direct to your accounts**
✅ **Simple setup**
✅ **Full control**
✅ **Works immediately**
✅ **No KYC requirements**

## 🚀 **Deployment**

Your `render.yaml` is already configured for both services:

- **Flask Dashboard**: File upload interface
- **Telegram Bot**: Payment processing

Both will deploy automatically when you push to GitHub!

## 📝 **Next Steps**

1. **Set up your payment accounts** (Crypto, CashApp, PayPal)
2. **Create your .env file** with all variables
3. **Deploy to Render** using the Blueprint
4. **Test the payment flow**
5. **Start selling!**

## 🆘 **Support**

If you need help:
1. Check the logs in Render dashboard
2. Verify all environment variables are set
3. Test locally first with `python bot_simple_payment.py`
