import re


def get_first_name(email):
    """
    :param email = foo@example.com:
    :return foo:
    """
    regex_str = r'([a-zA-Z]+)'
    match_obj = re.search(regex_str, email)
    if match_obj:
        return match_obj.group(1)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address
