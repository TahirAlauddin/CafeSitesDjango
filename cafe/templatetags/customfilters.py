from django import template

def startswith(value, arg):
    """Removes all values of arg from the given string"""
    return value.startswith(arg)


def minus(value, arg):
    """Removes all values of arg from the given string"""
    return int(value) - int(arg)


register = template.Library()


register.filter('startswith', startswith)
register.filter('minus', minus)
