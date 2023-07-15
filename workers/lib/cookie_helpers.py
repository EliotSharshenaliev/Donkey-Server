from requests.cookies import RequestsCookieJar


def cookie_to_dict(cookie: RequestsCookieJar):

    """
        USING: cookie instance RequestsCookieJar()
        will become and parse to str
    :param cookie:
    :return:
    """


    cookie_str = ""
    for key, value in cookie.items():
        cookie_str += "%s=%s;" % (key, value)

    return cookie_str
