import urllib.parse
import requests


def send_sms_without_save(phone_no, body):
    requests.get(
        "http://www.smsjust.com/blank/sms/user/urlsms.php?username=whstlr&pass=nsts@123&response=Y&msgtype=UNI&senderid=WHSTLR&dest_mobileno=" + str(
            phone_no) + "&message=" + urllib.parse.quote(str(body)))
