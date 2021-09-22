from django.core.mail import send_mail


def send_email(msg, to, from_email, subject):
    try:
        # pass
        send_mail(
            subject=subject,
            message=msg,
            from_email=from_email,
            recipient_list=[
                to,
            ],
            fail_silently=True,
        )
    except Exception as e:
        print("Error sending email ", e.args)
