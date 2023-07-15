import json
import random
import threading
import time

import requests
import schedule as schedule

from workers.lib import html_parser, dataclass_helper
from loguru import logger

from workers.types.interfaces import \
    InterfaceLogin, \
    InterfaceCalendarData, \
    InterfaceReservationData, InterfaceReservationParams


class Donkey:
    urls = {
        "__main__page": "https://consul.mofa.go.kr/",
        "__login__user": "https://consul.mofa.go.kr/cipl/0100/loginProcess.do",
        "__calendar_endpoint": "https://consul.mofa.go.kr/ciph/0800/selectVisitReserveCalendarYes.do",
        "__get_reservation_time_endpoint": "https://consul.mofa.go.kr/ciph/0800/selectVisitReserveTime.do",
        "__reservation_endpoint": "https://consul.mofa.go.kr/ciph/0800/selectVisitReserveTime.do"
    }

    functions = [
        "__checker_auth_pool",
        "login"
    ]

    delay_ms = 3000

    attacking_time = "01:42"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initial box of class
        self.scheduleEvent = None
        self.logoutEvent = None
        self.isAuth = False

        # Some instance of important classes for work
        self.session = requests.Session()

        # Typimg datas for requests
        self.user = InterfaceLogin(loginId="kadyrovshavkatbek030@mailkg.ru")
        self.calendar = InterfaceCalendarData(
            emblCd="GR",
            emblTime="202307",
            visitResveBussGrpCd="GR0001"
        )
        # Logger configuration
        logger.add("static/logs/%s__user_debug__.log" % "kadyrovshavkatbek")

    def run(self):

        """
            Will be start subprocess to check authentication
            and update cookie every dynamical times, else will be login again.
        """

        # Start schedule for run attacking handler when time setten by user
        schedule.every().day.at(self.attacking_time).do(self.__set_attacking_thread)
        logger.info("Schedule has started for attacking time %s " % self.attacking_time)

        # scheduleEvent this code for start new Threading instance for run Schedule pooling
        self.scheduleEvent = self.run_continuously()
        logger.success("Schedule proccess has successfully started... ")

        # logoutEvent this code for start new Threading instance for run Tesing logout handlers every some time
        self.logoutEvent = self.run_logout_continuously()
        logger.success("Test logouting thread has started for every time... ")

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
                logger.info("User authenticated...")

                # Sleep for secure session of block
                time.sleep(self.delay_ms / 1000)

    def __set_attacking_thread(self, interval=1):

        """
            The code defines a function __set_attacking_thread that creates a continuous thread.
            It stops any previously running thread, creates an event to control the thread's execution,
            and defines a subclass of threading.Thread with a custom run() method. The run() method continuously
            calls self.attacking() until the event is set. Finally, an instance of the subclass is created and
            started as the continuous thread.
        """

        try:
            # self.logoutEvent.set()
            self.scheduleEvent.set()
        except Exception or None as e:
            logger.error(e.args)

        cease_continuous_run = threading.Event()

        class TargettingThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    self.attacking()
                    time.sleep(interval)

        continuous_thread = TargettingThread()
        continuous_thread.start()

    @staticmethod
    def run_continuously(interval=1):
        """Continuously run, while executing pending jobs at each
        elapsed time interval.
        @return cease_continuous_run: threading. Event which can
        be set to cease continuous run. Please note that it is
        *intended behavior that run_continuously() does not run
        missed jobs*. For example, if you've registered a job that
        should run every minute and you set a continuous run
        interval of one hour then your job won't be run 60 times
        at each interval but only once.
        """
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    def run_logout_continuously(self, interval=1):
        logout_continuously = threading.Event()

        class ScheduleLogoutThread(threading.Thread):
            @classmethod
            def run(cls):
                while not logout_continuously.is_set():
                    self.logout()
                    time.sleep(random.randint(1, 11))

        continuous_thread = ScheduleLogoutThread()
        continuous_thread.start()
        return logout_continuously

    def login(self):

        """ This function for authentication user to
        mofa without any sub_threads and cycle"""

        try:
            logger.debug("Session posting... [Login]")

            response = self.session.post(
                allow_redirects=True,
                url=self.urls.get("__login__user"),
                data=dataclass_helper.get_dict(self.user)
            )

            self.isAuth = html_parser.isUsrExist(
                html=response.text
            )

        except requests.exceptions.RequestException as e:
            logger.error(e.args)

    def logout(self):
        self.session.get("https://consul.mofa.go.kr/cipl/0100/logout.do")

    def __getter_main_page(self):

        """ Getting main page using http requests
            - Can update cookie
            - Can get username to check exist on main view. If exist then bot has authenticated else not
        """

        try:
            response = self.session.get(
                url=self.urls.get("__main__page")
            )
            self.isAuth = html_parser.isUsrExist(
                html=response.text
            )
            return self.isAuth
        except requests.exceptions.RequestException as e:
            logger.error(e.args)
            return

    def make_reservation(self, obj):
        """ This function for authentication user to
                        mofa without any sub_threads and cycle"""
        logger.info(f"{obj}")
        # try:
        #     logger.debug("Sending reservation complection... [Data]")
        #     payload = InterfaceReservationData(
        #         timeCd="",
        #         visitDe="",
        #         remk="Assalom Aleikum",
        #         resveTimeNm="",
        #         visitResveId="",
        #     )
        #
        #     r = self.session.post(
        #         allow_redirects=True,
        #         url=self.urls.get("__reservation_endpoint"),
        #         data=dataclass_helper.get_dict(payload)
        #     )
        #     response = json.loads(r.content)
        #     for obj in response:
        #         if obj["visitYn"] == "Y" and self.isAuth:
        #             break
        #
        # except requests.exceptions.RequestException as e:
        #     logger.error(e.args)

    def get_reservation_times(self, obj):

        """ This function for authentication user to
            mofa without any sub_threads and cycle"""
        payload = InterfaceReservationParams(
            emblCd=obj["emblCd"],
            visitDe=obj["visitDe"],
            visitResveBussGrpCd=self.calendar.visitResveBussGrpCd
        )
        try:
            logger.debug("Getting reservation data complection... [Data]")
            r = self.session.post(
                allow_redirects=True,
                url=self.urls.get("__get_reservation_time_endpoint"),
                data=dataclass_helper.get_dict(payload)
            )
            response = json.loads(r.content)
            print(response)
            # for obj in response["resveResult"]:
            #     if obj["visitYn"] == "Y":
            #         self.make_reservation(obj)
            #         break

        except requests.exceptions.RequestException as e:
            logger.error(e.args)

    def attacking(self):

        """ This function for authentication user to
                mofa without any sub_threads and cycle"""

        try:
            logger.debug("Getting calendar data... [Data]")

            r = self.session.post(
                allow_redirects=True,
                url=self.urls.get("__calendar_endpoint"),
                data=dataclass_helper.get_dict(self.calendar)
            )
            response = json.loads(r.content)
            for obj in response["visitReserveCalendarYesResult"]:
                if obj["visitYn"] == "Y" and self.isAuth:
                    self.get_reservation_times(obj)
                    break

        except requests.exceptions.RequestException as e:
            logger.error(e.args)


if __name__ == "__main__":
    app = Donkey()
    app.run()
