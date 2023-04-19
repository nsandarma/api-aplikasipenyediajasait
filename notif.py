import firebase_admin
from firebase_admin import credentials,messaging
cred = credentials.Certificate('service.json')
firebase_admin.initialize_app(cred)

token = cred.get_access_token().access_token
tokens =['dHJUiH56QSWA8U3Hfc-hJ5:APA91bFXP_nCWuibDr0ezXqX3KiGnYfh0nYBLc13MebCffRbYDSoUzO-XAtOxei9LsTwA4jXg4HQZpt6JaoBuc48T8YoXKSBW9mxt_-mXHOZLVStr4tl3vgqpzf3YRFbRk6NVjWMLLLU']

def send_push(title,msg,token):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=None,
        tokens=token,
    )
    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    
send_push(title='aaa',msg='aaa',token=tokens)

