from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Define your products
products = {
    'atm_exploit': {'name': 'ATM Exploit Program', 'price': 500.00, 'description': 'AI ATM Exploiters: Unlock the potential of our AI-driven ATM exploiters, which identify vulnerabilities and exploit them to dispense cash with unparalleled accuracy.'},
    'info_stealer': {'name': 'Abysss Info-Stealer', 'price': 250.00, 'description': 'Browser Data Exfiltrator – a powerful and stealthy tool designed to extract and exfiltrate sensitive data from popular web browsers.'},
    'daily_fullz_x10': {'name': 'DAILY FULLZ X10', 'price': 5.00, 'description': 'Get access to the latest fullz data for your needs.'},
    'daily_fullz_bulk': {'name': 'DAILY FULLZ BULK', 'price': 50.00, 'description': 'Bulk buy option for DAILY FULLZ.'},
    'credit_cards_x5': {'name': 'CREDIT CARDS X5', 'price': 15.00, 'description': '80% VALIDITY USA 08/05/25'},
    'credit_cards_x50': {'name': 'CREDIT CARDS X50', 'price': 75.00, 'description': '80% VALIDITY USA 08/05/25'}
}

# Load inventory from CSV
def load_inventory_from_csv(file_path):
    inventory = {}
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                product_key = row['product_key']
                quantity = int(row['quantity'])
                inventory[product_key] = quantity
    return inventory

inventory = load_inventory_from_csv('uploads/inventory.csv')

# Function to handle product purchase with direct payment
def handle_purchase(update: Update, context: CallbackContext, product_key: str) -> None:
    user = update.message.from_user
    chat_id = user.id
    product = products.get(product_key)
    
    if product:
        if product_key in inventory and inventory[product_key] > 0:
            # Create payment options
            keyboard = [
                [InlineKeyboardButton("💳 Pay with Crypto", callback_data=f"pay_crypto_{product_key}")],
                [InlineKeyboardButton("💰 Pay with CashApp", callback_data=f"pay_cashapp_{product_key}")],
                [InlineKeyboardButton("💸 Pay with PayPal", callback_data=f"pay_paypal_{product_key}")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            message_text = f"""
🛒 **Purchase Request**

**Product:** {product['name']}
**Price:** ${product['price']}
**Description:** {product['description']}
**Stock:** {inventory[product_key]} available

Please select your payment method:
            """
            
            context.bot.send_message(
                chat_id=chat_id,
                text=message_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            context.bot.send_message(chat_id=chat_id, text="❌ Product out of stock.")
    else:
        context.bot.send_message(chat_id=chat_id, text="❌ Product not found.")

# Handle payment method selection
def handle_payment_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == "cancel":
        query.edit_message_text("❌ Purchase cancelled.")
        return
    
    # Extract payment method and product
    parts = query.data.split('_')
    if len(parts) >= 3:
        payment_method = parts[1]
        product_key = parts[2]
        product = products.get(product_key)
        
        if product:
            # Get admin username from environment
            admin_username = os.getenv('ADMIN_USERNAME', 'admin')
            
            payment_info = {
                'crypto': {
                    'name': 'Cryptocurrency',
                    'address': os.getenv('CRYPTO_ADDRESS', 'your_crypto_address'),
                    'message': f"Send ${product['price']} worth of crypto to:"
                },
                'cashapp': {
                    'name': 'CashApp',
                    'address': os.getenv('CASHAPP_USERNAME', '$your_cashapp_username'),
                    'message': f"Send ${product['price']} via CashApp to:"
                },
                'paypal': {
                    'name': 'PayPal',
                    'address': os.getenv('PAYPAL_EMAIL', 'your_paypal@email.com'),
                    'message': f"Send ${product['price']} via PayPal to:"
                }
            }
            
            if payment_method in payment_info:
                payment = payment_info[payment_method]
                
                message_text = f"""
💳 **{payment['name']} Payment**

**Product:** {product['name']}
**Price:** ${product['price']}

{payment['message']}
`{payment['address']}`

**Instructions:**
1. Send the payment to the address above
2. Include your Telegram username in the payment note
3. Contact @{admin_username} with your payment proof
4. Your product will be delivered within 24 hours

**Order ID:** `{chat_id}_{product_key}_{payment_method}`
                """
                
                keyboard = [
                    [InlineKeyboardButton("✅ I've Paid", callback_data=f"paid_{product_key}_{payment_method}")],
                    [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                query.edit_message_text(
                    text=message_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )

# Handle payment confirmation
def handle_payment_confirmation(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data.startswith("paid_"):
        parts = query.data.split('_')
        if len(parts) >= 3:
            product_key = parts[1]
            payment_method = parts[2]
            product = products.get(product_key)
            
            if product:
                admin_username = os.getenv('ADMIN_USERNAME', 'admin')
                
                # Deduct from inventory
                if product_key in inventory:
                    inventory[product_key] -= 1
                    save_inventory_to_csv(inventory)
                
                message_text = f"""
✅ **Payment Received!**

**Product:** {product['name']}
**Payment Method:** {payment_method.title()}

Your order has been confirmed! Please contact @{admin_username} with your payment proof to receive your product.

**Order ID:** `{query.from_user.id}_{product_key}_{payment_method}`
                """
                
                query.edit_message_text(
                    text=message_text,
                    parse_mode='Markdown'
                )

# Function to save inventory to CSV
def save_inventory_to_csv(inventory):
    with open('uploads/inventory.csv', mode='w', newline='') as file:
        fieldnames = ['product_key', 'quantity']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product_key, quantity in inventory.items():
            writer.writerow({'product_key': product_key, 'quantity': quantity})

# Define command handlers for each product
def buy_atm(update: Update, context: CallbackContext) -> None:
    handle_purchase(update, context, 'atm_exploit')

def buy_info_stealer(update: Update, context: CallbackContext) -> None:
    handle_purchase(update, context, 'info_stealer')

def buy_daily_fullz_x10(update: Update, context: CallbackContext) -> None:
    handle_purchase(update, context, 'daily_fullz_x10')

def buy_daily_fullz_bulk(update: Update, context: CallbackContext) -> None:
    handle_purchase(update, context, 'daily_fullz_bulk')

def buy_credit_cards_x5(update: Update, context: CallbackContext) -> None:
    handle_purchase(update, context, 'credit_cards_x5')

def buy_credit_cards_x50(update: Update, context: CallbackContext) -> None:
    handle_purchase(update, context, 'credit_cards_x50')

# Main function to set up the bot
def main() -> None:
    global inventory
    inventory = load_inventory_from_csv('uploads/inventory.csv')
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add callback handlers
    application.add_handler(CallbackQueryHandler(handle_payment_callback, pattern="^pay_"))
    application.add_handler(CallbackQueryHandler(handle_payment_confirmation, pattern="^paid_"))
    application.add_handler(CallbackQueryHandler(handle_payment_callback, pattern="^cancel$"))

    # Add product handlers
    application.add_handler(CommandHandler('buy_atm', buy_atm))
    application.add_handler(CommandHandler('buy_info_stealer', buy_info_stealer))
    application.add_handler(CommandHandler('buy_daily_fullz_x10', buy_daily_fullz_x10))
    application.add_handler(CommandHandler('buy_daily_fullz_bulk', buy_daily_fullz_bulk))
    application.add_handler(CommandHandler('buy_credit_cards_x5', buy_credit_cards_x5))
    application.add_handler(CommandHandler('buy_credit_cards_x50', buy_credit_cards_x50))

    application.run_polling()

if __name__ == '__main__':
    main()
