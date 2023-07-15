from bs4 import BeautifulSoup


def isUsrExist(html: str):
    """
    Will parser username from html and return string username or empty string
    :param html:
    :return Boolean - (isUsername is exist?):
    """
    try:
        b4 = BeautifulSoup(html, "html.parser")
        username = b4.find('span', class_='username').get_text()
    except Exception as e:
        username = ""
        pass

    return not not username.encode('utf-8').decode('utf-8')
