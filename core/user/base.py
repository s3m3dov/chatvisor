from entities.models import CustomerSubscription


def get_full_name(first_name: str, last_name: str = None) -> str:
    full_name = first_name
    if last_name:
        full_name += " " + last_name
    return full_name


def is_user_subscribed(user_id: int) -> bool:
    subscription_model = (
        CustomerSubscription.with_joined(CustomerSubscription.user)
        .where(CustomerSubscription.user_id == user_id)
        .first()
    )
    if not subscription_model:
        return False

    return True
