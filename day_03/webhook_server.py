from flask import Flask, request, jsonify
import hmac
import hashlib
import os
import json
from datetime import datetime

app = Flask(__name__)
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret-key")

# Store processed webhooks for idempotency
processed_webhooks = set()

def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify webhook signature"""
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected_signature)

def process_webhook_event(event_type: str, data: dict):
    """Process webhook event based on type"""
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Processing event: {event_type}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    # Event handler mapping
    handlers = {
        "task.created": handle_task_created,
        "task.updated": handle_task_updated,
        "task.completed": lambda d: print(f"✅ Task completed: {d.get('task', {}).get('id')}"),
        "user.registered": handle_user_registered,
        "user.updated": lambda d: print(f"👤 User updated: {d.get('user', {}).get('id')}"),
        "payment.completed": handle_payment_completed,
        "payment.failed": lambda d: print(f"❌ Payment failed: {d.get('payment', {}).get('id')}"),
        "order.created": lambda d: print(f"🛒 Order created: {d.get('order', {}).get('id')}"),
        "order.shipped": handle_order_shipped,
        "notification.sent": lambda d: print(f"📧 Notification sent: {d.get('notification', {}).get('type')}"),
    }
    
    handler = handlers.get(event_type)
    if handler:
        try:
            handler(data)
            print(f"✅ Successfully processed {event_type}")
        except Exception as e:
            print(f"❌ Error processing {event_type}: {e}")
            raise
    else:
        print(f"⚠️ Unknown event type: {event_type}")

def handle_task_created(data: dict):
    """Handle task created event"""
    task = data.get('task', {})
    print(f"📝 New task created: {task.get('id')} - {task.get('title')}")
    # Add your business logic here
    # e.g., send notifications, update database, etc.

def handle_task_updated(data: dict):
    """Handle task updated event"""
    task = data.get('task', {})
    print(f"✏️ Task updated: {task.get('id')} - Status: {task.get('status')}")
    # Add your business logic here

def handle_user_registered(data: dict):
    """Handle user registered event"""
    user = data.get('user', {})
    print(f"👤 New user registered: {user.get('id')} - {user.get('email')}")
    # Add your business logic here

def handle_payment_completed(data: dict):
    """Handle payment completed event"""
    payment = data.get('payment', {})
    print(f"💳 Payment completed: {payment.get('id')} - ${payment.get('amount')}")
    # Add your business logic here

def handle_order_shipped(data: dict):
    """Handle order shipped event"""
    order = data.get('order', {})
    print(f"📦 Order shipped: {order.get('id')} - Tracking: {order.get('tracking_number')}")
    # Add your business logic here

@app.route("/webhook", methods=["POST"])
def webhook():
    """Webhook endpoint"""
    try:
        # Get signature from header
        signature = request.headers.get("X-Signature")
        if not signature:
            return jsonify({"error": "Missing signature"}), 401
        
        # Get raw payload
        payload = request.get_data()
        
        # Verify signature
        if not verify_signature(payload, signature):
            return jsonify({"error": "Invalid signature"}), 401
        
        # Parse JSON
        data = request.json
        
        # Check idempotency
        webhook_id = data.get("id")
        if webhook_id and webhook_id in processed_webhooks:
            return jsonify({"status": "already_processed"}), 200
        
        # Process webhook
        event_type = data.get("event")
        if not event_type:
            return jsonify({"error": "Missing event type"}), 400
        
        process_webhook_event(event_type, data)
        
        # Mark as processed
        if webhook_id:
            processed_webhooks.add(webhook_id)
        
        return jsonify({"status": "ok"}), 200
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/webhook/events", methods=["GET"])
def list_events():
    """List supported event types"""
    events = [
        "task.created", "task.updated", "task.completed",
        "user.registered", "user.updated",
        "payment.completed", "payment.failed",
        "order.created", "order.shipped",
        "notification.sent"
    ]
    return jsonify({"supported_events": events}), 200

@app.route("/webhook/test", methods=["POST"])
def test_webhook():
    """Test endpoint for webhook without signature verification"""
    try:
        data = request.json
        event_type = data.get("event")
        if not event_type:
            return jsonify({"error": "Missing event type"}), 400
        
        print("🧪 TEST WEBHOOK (no signature verification)")
        process_webhook_event(event_type, data)
        
        return jsonify({"status": "test_ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    print("🚀 Starting webhook server...")
    print("Endpoints:")
    print("  POST /webhook - Main webhook endpoint (with signature verification)")
    print("  POST /webhook/test - Test endpoint (no signature verification)")
    print("  GET /webhook/events - List supported event types")
    print("  GET /health - Health check")
    port = int(os.getenv("PORT", 5001))
    print(f"Server running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
