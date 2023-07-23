import json
import sys
import threading
import time
import requests
import schedule as schedule
from loguru import logger

# from workers.custom_types import interfaces
# from workers.lib import dataclass_helper, html_parser, error_messages, cookie_helpers


#
from lib import dataclass_helper, html_parser, error_messages, cookie_helpers
from custom_types import interfaces


class Donkey:
    urls = {
        "__main__page": "https://consul.mofa.go.kr/ciph/0800/selectCIPH0801Deng.do",
        "__login__user": "https://consul.mofa.go.kr/cipl/0100/loginProcess.do",
        "__calendar_endpoint": "https://consul.mofa.go.kr/ciph/0800/selectVisitReserveCalendarYes.do",
        "__get_reservation_time_endpoint": "https://consul.mofa.go.kr/ciph/0800/selectVisitReserveTime.do",
        "__reservation_endpoint": "https://consul.mofa.go.kr/ciph/0800/insertResveVisitEng.do",
        "__get_captcha_endpoint": "http://192.168.0.106:8000/api/v1/tasks/get-captcha-solve/"
    }

    delay_ms = 3000
    attacking_time = "12:46"

    attackingEvent = threading.Event()
    scheduleEvent = threading.Event()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initial box of class
        self.captcha_text: str = ""
        self.shorting_url = 26
        self.isAuth = False
        self.session = requests.Session()

        # Logger configuration
        logs_file = sys.argv[1]
        logger.add(f"static/logs/{logs_file}", format="{time} {level} {message}")

        # Import Configurations
        self.username = sys.argv[2]
        manifest = json.load(open("botconfig.json"))

        logger.debug(f"host={manifest.get('host')} port={manifest.get('port')}")

        # Typimg datas for request
        self.user = interfaces.InterfaceLogin(loginId="kadrovamukhab@sarnoz.com")
        self.calendar = interfaces.InterfaceCalendarData(
            emblCd="KY",
            emblTime="202308",
            visitResveBussGrpCd="KY0001"
        )

    def run(self):

        """
            Will be start subprocess to check authentication
            and update cookie every dynamical times, else will be login again.
        """

        # Start schedule for run attacking handler when time setten by user
        schedule.every().day.at(self.attacking_time).do(self.__set_attacking_thread)
        logger.info("Schedule has started for attacking time %s " % self.attacking_time)

        # scheduleEvent this code for start new Threading instance for run Schedule pooling
        self.run_continuously()
        logger.success("Schedule proccess has successfully started... ")

        logger.debug("All processes: %s" % threading.active_count())

        # Core Project
        import time
        while 1:

            # Working every time
            # if function got False then user not authenticated.
            if not self.__getter_main_page():

                logger.warning("Authentication is failed. Trying login again...")
                self.login()
            else:
                # Sleep for secure session of block
                time.sleep(self.delay_ms / 1000)

    def __set_attacking_thread(self):

        """
            The code defines a function __set_attacking_thread that creates a continuous thread.
            It stops any previously running thread, creates an event to control the thread's execution,
            and defines a subclass of threading.Thread with a custom run() method. The run() method continuously
            calls self.attacking() until the event is set. Finally, an instance of the subclass is created and
            started as the continuous thread.
        """

        try:
            self.scheduleEvent.set()
        except Exception or None as e:
            logger.error(e.args)

        class TargettingThread(threading.Thread):
            @classmethod
            def run(cls):
                while not self.attackingEvent.is_set():
                    self.attacking()

        continuous_thread = TargettingThread()
        continuous_thread.start()

    def run_continuously(self, interval=1):
        """Continuously run, while executing pending jobs at each
        elapsed time interval.
        @return cease_continuous_run: threading. Event which can
        be set to cease continuous run. Please note that it is
        *intended behavior that run_continuously() does not run
        missed jobs*. For example, if you've registered a job that
        should run every minute, and you set a continuous run
        interval of one hour then your job won't be run 60 times
        at each interval but only once.
        """

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not self.scheduleEvent.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()

    def login(self):

        """
            The login function handles user authentication for the "mofa" system. It sends an
            HTTP POST request to a specified URL with user data for authentication.
            The response is then processed to determine if the authentication was successful.
        """

        try:
            r = self.session.post(
                allow_redirects=True,
                url=self.urls.get("__login__user"),
                data=dataclass_helper.get_dict(self.user)
            )
            logger.debug(
                f"{r.url}"[self.shorting_url:]
            )
            self.isAuth = html_parser.isUsrExist(
                html=r.text
            )

        except requests.exceptions.RequestException as e:
            logger.error(e.args)

    def __getter_main_page(self):

        """ Getting main page using http request
            - Can update cookie
            - Can get username to check exist on main view. If exist then bot has authenticated else not

            The __getter_main_page function retrieves the main page using an HTTP GET request.
            It checks if the user is authenticated by examining the response from the server and
            sets the isAuth flag accordingly.
        """

        try:
            r = self.session.get(
                url=self.urls.get("__main__page")
            )
            logger.debug(
                f"{r.url}"[self.shorting_url:]
            )
            self.isAuth = html_parser.isUsrExist(
                html=r.text
            )
            return self.isAuth
        except requests.exceptions.RequestException as e:
            logger.error(e.args)
            return

    def make_reservation(self, obj):

        """
            The make_reservation function is used to make a reservation. Here's a short description of its usage:

            Call the make_reservation method on an instance of the class, providing the necessary obj parameter containing reservation details.
            The function sends an HTTP POST request to the reservation endpoint URL with the payload data.
            The server response is parsed as JSON, and specific error conditions are checked.
            Depending on the response, different actions are taken, such as logging errors or setting event flags.
            If no errors occur, event flags are set and a warning message is logged indicating the bot has stopped, possibly due to unknown errors or replacement.
            Exception handling is in place to catch request-related or general exceptions, with appropriate logging.

        :param obj:
        :return:
        """

        try:
            payload = interfaces.InterfaceReservationData(
                timeCd=obj["timeCd"],
                visitDe=obj["visitDe"],
                remk="Assalom Aleikum",
                resveTimeNm=obj["timeNm"][:5],
                visitResveId=obj["visitResveId"],
                captchaTxt=self.captcha_text,
            )
            r = self.session.post(
                allow_redirects=True,
                url=self.urls.get("__reservation_endpoint"),
                data=dataclass_helper.get_dict(payload)
            )
            response = json.loads(r.content)

            if response.get("wsdlErrorNm") == "실패":
                logger.error(error_messages.msg_error.get(
                    response.get("wsdlErrorNm")
                ))
                return

            if response.get("result") == 0:
                logger.error(
                    error_messages.msg_error.get("captcha")
                )
                return

            params: dict = response.get("param")
            if params.get("errMsg") == "E03":
                return

            if params.get("E01") or params.get("E02"):
                logger.error("Unknown error from server. Bot has stopped!")

            self.scheduleEvent.set()
            self.attackingEvent.set()
            logger.warning("Bot has stopped. Perhaps bot taken place or got unknown error")

        except requests.exceptions.RequestException or Exception as e:
            logger.error(e.args)

    def get_reservation_times(self, obj):

        """
        The get_reservation_times function retrieves reservation times for a specific date. Here's a short description of its usage:

        Call the get_reservation_times method on an instance of the class, providing the required obj parameter containing reservation details.
        The function creates a payload using the InterfaceReservationParams class and the provided obj parameters.
        An HTTP POST request is sent to the reservation time endpoint URL specified by self.urls.get("__get_reservation_time_endpoint"), with the payload data included in the request.
        The server response is parsed as JSON, and the function iterates through the resveResult objects in the response.
        If a reservation is available (visitYn is "Y"), the make_reservation method is called, passing the reservation details from the response object.
        Only the first available reservation is processed, and the loop is terminated using break.
        Exception handling is in place to catch request-related or general exceptions, with appropriate logging.

        """
        payload = interfaces.InterfaceReservationParams(
            emblCd=obj["emblCd"],
            visitDe=obj["visitDe"],
            visitResveBussGrpCd=self.calendar.visitResveBussGrpCd
        )
        try:
            r = self.session.post(
                allow_redirects=True,
                url=self.urls.get("__get_reservation_time_endpoint"),
                data=dataclass_helper.get_dict(payload)
            )
            logger.debug(
                f"{r.url}"[self.shorting_url:]
            )
            response = json.loads(r.content)
            for obj in response["resveResult"]:
                if obj["visitYn"] == "Y":
                    self.make_reservation(obj)
                    break

        except requests.exceptions.RequestException or Exception as e:
            logger.error(e.args)

    def attacking(self):

        """ This function for authentication user to
                mofa without any sub_threads and cycle"""

        try:
            r = self.session.post(
                allow_redirects=True,
                url=self.urls.get("__calendar_endpoint"),
                data=dataclass_helper.get_dict(self.calendar)
            )
            logger.debug(
                f"{r.url}"[self.shorting_url:]
            )
            response = json.loads(r.content)
            for obj in response["visitReserveCalendarYesResult"][14:]:
                if obj["visitYn"] == "Y" and self.isAuth:
                    self.get_reservation_times(obj)
                    break

        except requests.exceptions.RequestException or Exception as e:
            logger.error(e.args)

    def get_captcha(self):
        try:
            payload = {
                "Cookie": cookie_helpers.cookie_to_dict(self.session.cookies)
            }
            r = self.session.post(self.urls.get("__get_captcha_endpoint"), data=payload)
            response = json.loads(r.content)
            self.captcha_text = response.get("captcha")
            return True
        except Exception as e:
            logger.error(e.args)
            return False


if __name__ == "__main__":
    app = Donkey()
    app.run()
