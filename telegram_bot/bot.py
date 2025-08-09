from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
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

# Function to handle product purchase
def handle_purchase(update: Update, context: CallbackContext, product_key: str) -> None:
    user = update.message.from_user
    chat_id = user.id
    product = products.get(product_key)
    if product:
        if product_key in inventory and inventory[product_key] > 0:
            context.bot.send_message(chat_id=chat_id, text=f"Processing payment for {product['name']} - ${product['price']}.")
            # Generate a payment link using Telegram Wallet
            payment_link = generate_payment_link(product['price'], chat_id, product_key)
            context.bot.send_message(chat_id=chat_id, text=f"Please complete your payment using this link: {payment_link}")
            # Deduct from inventory
            inventory[product_key] -= 1
            save_inventory_to_csv(inventory)
        else:
            context.bot.send_message(chat_id=chat_id, text="Product out of stock.")
    else:
        context.bot.send_message(chat_id=chat_id, text="Product not found.")

# Function to generate a payment link using Telegram Wallet
def generate_payment_link(amount: float, chat_id: int, product_key: str) -> str:
    # Replace with the actual endpoint and parameters for generating a payment link
    response = requests.post(
        f'https://api.telegram.org/bot/{os.getenv("TELEGRAM_BOT_TOKEN")}/pay',
        json={
            'chat_id': chat_id,
            'amount': int(amount * 100),  # Amount in cents
            'currency': 'USD',
            'description': f"Payment for {product_key}",
            'payload': product_key
        }
    )
    if response.status_code == 200:
        return response.json().get('payment_link')
    else:
        raise Exception("Failed to generate payment link")

# Function to send product to customer's email
def send_product_to_email(user, product):
    sender_email = os.getenv('GOOGLE_EMAIL')
    sender_password = os.getenv('GOOGLE_PASSWORD')
    recipient_email = user.email  # Retrieve the user's email from your database

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
    updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('buy_atm', buy_atm))
    dispatcher.add_handler(CommandHandler('buy_info_stealer', buy_info_stealer))
    dispatcher.add_handler(CommandHandler('buy_daily_fullz_x10', buy_daily_fullz_x10))
    dispatcher.add_handler(CommandHandler('buy_daily_fullz_bulk', buy_daily_fullz_bulk))
    dispatcher.add_handler(CommandHandler('buy_credit_cards_x5', buy_credit_cards_x5))
    dispatcher.add_handler(CommandHandler('buy_credit_cards_x50', buy_credit_cards_x50))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
