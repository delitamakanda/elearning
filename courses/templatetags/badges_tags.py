from django import template
from courses.models import BadgeAward

register = template.Library()

@register.simple_tag
def badge_count(user):
    return BadgeAward.objects.filter(user=user).count()


@register.simple_tag
def badges_for_user(user):
    return BadgeAward.objects.filter(user=user).order_by('-awarded_at')


@register.filter
def badge_level_user(user):
    try:
        badge = BadgeAward.objects.filter(user=user).order_by('-awarded_at').first()
        levels = [
            "Bronze",
            "Silver",
            "Gold",
            "Platinum",
        ]
        for x in levels:
            lvl_idx = levels.index(x)
            lvl_range = lvl_idx + 1
            if lvl_range == badge.level:
                return levels[lvl_idx]
    except AttributeError:
        return levels[0]
