from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import datetime
import re
from flaskr.Lib.MailLib import EmailServer
import threading

REGIO_BASE_URL = "https://www.regiojet.sk"

DEFAULT_NUMBER_OF_RETRIES = 20


class Session:
    def __init__(self):
        options = Options()
        # options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=options)

        self.driver.implicitly_wait(60)
        self.from_place = ""
        self.to_place = ""
        self.from_date = ""
        self.routes_free = []
        self.routes_full = []
        self.ready = False

    def __del__(self):
        pass
        self.driver.close()

    # @retry(stop_max_attempt_number=DEFAULT_NUMBER_OF_RETRIES)
    def find_route(self, from_place, to_place, from_date):
        self.from_place = from_place
        self.to_place = to_place
        self.from_date = from_date

        self.driver.get("https://www.regiojet.sk")

        elem_from = self.driver.find_element_by_id("destination_from")
        elem_from.clear()
        elem_from.send_keys(self.from_place)

        elem_to = self.driver.find_element_by_id("destination_to")
        elem_to.clear()
        elem_to.send_keys(self.to_place)

        self.driver.find_element_by_class_name("ybus-form-submit").click()

        self.set_date()
        self.driver.find_element_by_class_name("ybus-form-submit").click()

        print("found all routes")

    # @retry(stop_max_attempt_number=DEFAULT_NUMBER_OF_RETRIES)
    def reload_side(self):
        self.driver.refresh()

    # @retry(stop_max_attempt_number=DEFAULT_NUMBER_OF_RETRIES)
    def read_routes(self):
        print("reading routes")

        # reset date if was changed somehow
        elem_left_colum = self.driver.find_element_by_xpath('//div[@class="left_column"]')
        elem_h2 = elem_left_colum.find_element_by_xpath(".//h2").find_element_by_xpath('.//span[last ()]')
        if self.from_date not in elem_h2.text:
            self.set_date()
            self.driver.find_element_by_class_name("ybus-form-submit").click()

        html = self.driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

        soup_ticket_list = soup.find('div', {"id": "ticket_lists"})
        soup_ticke_list_left = soup_ticket_list.find('div', {'class': 'left_column'}, recursive=True)
        date_tag = soup_ticke_list_left.find('h2', {"class": "overflow_hl"}, recursive=True)

        if self.from_date not in date_tag.text:
            return

        # find all routes
        self.routes_free.clear()
        self.routes_full.clear()
        for div_element_route in date_tag.find_next_siblings():
            # find all free routes
            if div_element_route.name == "div" and "free" in div_element_route['class']:
                self.routes_free.append((div_element_route.find_all('div')[1].text,  # start time
                                         div_element_route.find_all('div')[2].text,  # end time
                                         div_element_route.find_all('div')[4].text.strip()  # num free seats
                                         ))

            # find all full routes
            if div_element_route.name == "div" and "full" in div_element_route['class']:
                self.routes_full.append((div_element_route.find_all('div')[1].text,  # start time
                                         div_element_route.find_all('div')[2].text,  # end time
                                         div_element_route.find_all('div')[4].text.strip()  # num free seats
                                         ))

            if div_element_route.name == "h2" and self.from_date not in div_element_route.text:
                print(div_element_route.text)
                break

    def set_date(self):
        match = re.search("(\d+).(\d+).(\d+)", self.from_date)
        date = match.group(1)
        month = match.group(2)
        year = match.group(3)

        # set month
        self.driver.find_element_by_class_name("open-datepicker").click()
        set_month = 0
        while int(month) != set_month:
            elem_date_picker = self.driver.find_element_by_class_name("ui-datepicker-calendar")
            elem_table = elem_date_picker.find_element_by_tag_name("tbody")
            year_element = self.driver.find_element_by_class_name("ui-datepicker-year")
            if int(year_element.text) < int(year):
                self.driver.find_element_by_class_name("ui-datepicker-next").click()
            else:
                for td_element in elem_table.find_elements_by_tag_name("td"):
                    if td_element.get_attribute('data-month') is not None:
                        set_month = int(td_element.get_attribute('data-month')) + 1
                        if set_month > int(month):
                            self.driver.find_element_by_class_name("ui-datepicker-prev").click()
                        if set_month < int(month):
                            self.driver.find_element_by_class_name("ui-datepicker-next").click()
                        break

        # find date
        elem_date_picker = self.driver.find_element_by_class_name("ui-datepicker-calendar")
        elem_table = elem_date_picker.find_element_by_tag_name("tbody")
        elem_table.find_element_by_xpath(".//*[text()='" + date + "']").click()

    def is_ready(self):
        return self.ready

    def get_free_routes(self):
        return self.routes_free

    def get_full_routes(self):
        return self.routes_full


def str_2_hour(string_name):
    return datetime.datetime.strptime(string_name, "%H:%M")


def get_route_from_time(routes, from_time):
    ret = []
    for route_info in routes:
        if str_2_hour(route_info[0]) >= str_2_hour(from_time):
            ret.append(route_info)
    return ret


def get_route_to_time(routes, to_time):
    ret = []
    for route_info in routes:
        if str_2_hour(route_info[0]) <= str_2_hour(to_time):
            ret.append(route_info)
    return ret


def filter_routes(routes, from_time, to_time):
    ret = routes
    if from_time != "":
        ret = get_route_from_time(ret, from_time)
    if to_time != "":
        ret = get_route_to_time(ret, to_time)
    return ret


def is_route_free(free_routes, from_time, to_time):
    if from_time == "" and to_time == "":
        if free_routes:
            return True
        else:
            return False

    filtered_routes = filter_routes(free_routes, from_time, to_time)

    if filtered_routes:
        return True
    else:
        return False


def thread_function_send_email_when_route_free(session, email_server, from_place, to_place, from_date, to_date="", from_time="", to_time=""):
    session.find_route(from_place, to_place, from_date)
    session.read_routes()

    full_routes = filter_routes(session.get_full_routes(), from_time, to_time)
    free_routes = filter_routes(session.get_free_routes(), from_time, to_time)

    print("free " + from_place, free_routes)

    while not is_route_free(free_routes, from_time, to_time):
        # check if there is at least one route that except time criteria
        if not filter_routes(full_routes + free_routes, from_time, to_time):
            email_server.send_error_email()
            print(from_date + " error")
            # probably return and send sorry email
            return

        now_time = datetime.datetime.now()
        now_time += datetime.timedelta(hours=1)    # end 1 hour before from_time
        compare_to_time = "23:59"
        if to_time != "":
            compare_to_time = to_time
        from_date_time = datetime.datetime.strptime(from_date + " " + compare_to_time, "%d.%m.%Y %H:%M")
        if now_time > from_date_time:
            email_server.send_time_out_email()
            print(from_date + " time out")
            # cannot search for date older then this day
            return

        # time.sleep(5 * 60 + random.randint(0, 60))  # 5 minutes + random time of minute

        time.sleep(2)
        full_routes = filter_routes(session.get_full_routes(), from_time, to_time)
        free_routes = filter_routes(session.get_free_routes(), from_time, to_time)

        print("free routes", free_routes)
        print("full routes", full_routes)

        session.reload_side()
        session.read_routes()

    # send email with result
    email_server.send_availability_email()
    print(from_date + " availible")
    # TODO case of not existing date


class WatchThread (threading.Thread):
    def __init__(self, thread_id, name, from_place, to_place, from_date, to_date="", from_time="", to_time=""):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.from_place = from_place
        self.to_place = to_place
        self.from_date = from_date
        self.to_date = to_date
        self.from_time = from_time
        self.to_time = to_time
        self.session = Session()
        self.email_server = EmailServer()
        self.email_server.set_email_to("pavolleopold@gmail.com")

    def run(self):
        print("Starting " + self.name)
        thread_function_send_email_when_route_free(self.session, self.email_server, self.from_place, self.to_place,
                                                   self.from_date, self.to_date, self.from_time, self.to_time)
        print("Exiting " + self.name)
