import random
import string
import requests
import time

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"

def generate_random_code(length=18):
    """Generates a random alphanumeric string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_to_webhook_with_embed(code):
    """Sends an embedded message to the configured Discord webhook, with an @everyone mention."""
    embed = {
        "title": "🎉 Valid Gift Code Found! 🎉",
        "description": f"**Code:** `{code}`\n\nCheck it out before it’s gone! 🚀",
        "color": 0x00ff00,  # Green
        "footer": {
            "text": "Discord Gift Code Checker",
            "icon_url": "https://support.discord.com/hc/article_attachments/28008656909207"
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    payload = {
        "content": "@everyone 🚨 A valid Nitro code was found! 🚨",
        "embeds": [embed]
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print(f"✅ Sent valid code with @everyone ping to webhook: {code}")
        else:
            print(f"❌ Failed to send to webhook (Code: {response.status_code}): {code}")
    except Exception as e:
        print(f"⚠️ Error sending to webhook: {e}")

def check_code(code):
    """Checks the generated code using a GET request."""
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ Valid Code: {code}")
            send_to_webhook_with_embed(code)
        else:
            print(f"❌ Invalid Code: {code}")
    except Exception as e:
        print(f"⚠️ Error checking code: {e}")

def main():
    """Main function to continuously generate and check codes."""
    print("Starting infinite code generator...")
    while True:
        code = generate_random_code()
        check_code(code)
        time.sleep(1)

if __name__ == "__main__":
    main()
