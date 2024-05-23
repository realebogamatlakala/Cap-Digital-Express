# from flask import Flask, request, jsonify
# import vonage

# app = Flask(__name__)

# # Initialize Nexmo client
# client = vonage.Client(key='$omhl@b%rzw@98', secret='to send messages to a user after registering')
# sms = vonage.Sms(client)

# @app.route('/send-sms', methods=['POST'])
# def send_sms():
#     data = request.get_json()
#     recipient_number = data.get('to')
#     message_text = data.get('message')

#     if not recipient_number or not message_text:
#         return jsonify({'error': 'Invalid input'}), 400

#     response = sms.send_message({
#         "from": "banking-app",
#         "to": recipient_number,
#         "text": message_text
#     })

#     if response["messages"][0]["status"] == "0":
#         return jsonify({'success': 'Message sent successfully.'}), 200
#     else:
#         return jsonify({'error': response['messages'][0]['error-text']}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
from twilio.rest import Client
import os

# Setting environment variables (should be done securely in a real application)
os.environ['TWILIO_ACCOUNT_SID'] = 'ACc3b436ef8f8bc5c225777d33f96f4fed'
os.environ['TWILIO_AUTH_TOKEN'] = 'b7097a4483a84ca2dc1cab2b33ae52f'
os.environ['TWILIO_PHONE_NUMBER'] = '+17069673093'

app = Flask(__name__)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    recipient_number = data.get('to')
    message_text = data.get('message')

    if not recipient_number or not message_text:
        return jsonify({'error': 'Recipient number and message text are required'}), 400

    try:
        message = client.messages.create(
            body=message_text,
            from_=TWILIO_PHONE_NUMBER,
            to=recipient_number
        )
        return jsonify({'status': 'Message sent', 'sid': message.sid}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

