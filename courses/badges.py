# https://github.com/pinax/pinax-badges/blob/master/pinax/badges/base.py
import datetime
from django.utils import timezone
from courses.models import BadgeAward

def possibly_award_badge(events, user):
    points = user.profile.award_points
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_awards = BadgeAward.objects.filter(user=user, slug=events, awarded_at__gte=last_minute)

    awarded_lvl = 1
    if points > 30000:
        awarded_lvl = 4
    elif points > 10000:
        awarded_lvl = 3
    elif points > 7500:
        awarded_lvl = 2
    elif points > 5000:
        awarded_lvl = 1

    if not similar_awards:
        badge = BadgeAward(
            user=user,
            slug=events,
            level=awarded_lvl
        )
        badge.save()
        return True
    return False
