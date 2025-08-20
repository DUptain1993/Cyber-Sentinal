from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, PreCheckoutQueryHandler, MessageHandler, filters
import requests
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

# Function to handle product purchase with Telegram Payments
def handle_purchase(update: Update, context: CallbackContext, product_key: str) -> None:
    user = update.message.from_user
    chat_id = user.id
    product = products.get(product_key)
    
    if product:
        if product_key in inventory and inventory[product_key] > 0:
            # Create invoice for Telegram Payments
            title = f"Purchase: {product['name']}"
            description = product['description']
            payload = f"product_{product_key}_{chat_id}"
            provider_token = os.getenv('PAYMENT_PROVIDER_TOKEN')  # You'll need to set this up
            currency = "USD"
            prices = [LabeledPrice(product['name'], int(product['price'] * 100))]  # Amount in cents
            
            try:
                context.bot.send_invoice(
                    chat_id=chat_id,
                    title=title,
                    description=description,
                    payload=payload,
                    provider_token=provider_token,
                    currency=currency,
                    prices=prices,
                    start_parameter=f"buy_{product_key}",
                    photo_url="https://via.placeholder.com/300x200?text=Product",
                    photo_width=300,
                    photo_height=200,
                    photo_size=300,
                    is_flexible=False,
                    disable_notification=False,
                    protect_content=True
                )
            except Exception as e:
                # Fallback to direct payment method
                context.bot.send_message(
                    chat_id=chat_id, 
                    text=f"Payment setup required. Please contact admin for direct payment to @{os.getenv('ADMIN_USERNAME', 'admin')}"
                )
        else:
            context.bot.send_message(chat_id=chat_id, text="Product out of stock.")
    else:
        context.bot.send_message(chat_id=chat_id, text="Product not found.")

# Handle successful payments
def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    """Confirms the successful payment."""
    query = update.message.successful_payment
    user = update.message.from_user
    
    # Extract product info from payload
    payload_parts = query.invoice_payload.split('_')
    if len(payload_parts) >= 2:
        product_key = payload_parts[1]
        product = products.get(product_key)
        
        if product:
            # Deduct from inventory
            if product_key in inventory:
                inventory[product_key] -= 1
                save_inventory_to_csv(inventory)
            
            # Send confirmation
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Thank you for your purchase! Your {product['name']} will be delivered shortly."
            )
            
            # Send product details via email if available
            if hasattr(user, 'email') and user.email:
                send_product_to_email(user, product)

# Handle pre-checkout queries
def precheckout_callback(update: Update, context: CallbackContext) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # answer the pre-checkout query
    query.answer(ok=True)

# Function to send product to customer's email
def send_product_to_email(user, product):
    sender_email = os.getenv('GOOGLE_EMAIL')
    sender_password = os.getenv('GOOGLE_PASSWORD')
    recipient_email = getattr(user, 'email', None)  # Get email if available

    if not recipient_email:
        return  # No email available

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Your Purchase: {product['name']}"

    body = f"Dear {user.first_name},\n\nThank you for your purchase! Here are the details of your order:\n\nProduct: {product['name']}\nPrice: ${product['price']}\nDescription: {product['description']}\n\nBest regards,\nCyber-Sentinal"

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

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

    # Add payment handlers
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

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
