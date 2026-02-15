from .models import UserProfile


def user_profile(request):
    """Expose user_profile for navbar (profile picture) in all templates."""
    user_profile_obj = None
    if request.user.is_authenticated:
        try:
            user_profile_obj = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass
    return {'user_profile': user_profile_obj}
