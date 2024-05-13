from models.user import UserModel

def send_match_email(to, subject, body):
    # send email
    return None

def send_match_notification_to_users(user1: UserModel, user2: UserModel):
    send_match_email(user1.email, 'Its a match', f'you are matched with {user2.profile.first_name} {user2.profile.last_name}')
    send_match_email(user2.email, 'Its a match', f'you are matched with {user1.profile.first_name} {user1.profile.last_name}')


