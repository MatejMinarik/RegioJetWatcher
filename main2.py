from flaskr.Lib.RegioJetWatcherLib import *
import time

sesion_var = Session()

sesion_var.find_route("Brno", 'Praha', '21.10.2018')

sesion_var.read_routes()

tmp = sesion_var.get_free_routes()

print("empty routs")
print(tmp)

tmp = sesion_var.get_full_routes()

print("full rutes")
print(tmp)

time.sleep(5)

sesion_var.reload_side()
sesion_var.read_routes()

tmp = sesion_var.get_free_routes()

print("empty routs")
print(tmp)

tmp = sesion_var.get_full_routes()

print("full rutes")
print(tmp)


# class myThread (threading.Thread):
#    def __init__(self, threadID, name, from_place, to_place, from_date, to_date="", from_time="", to_time=""):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.from_place = from_place
#         self.to_place = to_place
#         self.from_date = from_date
#         self.to_date = to_date
#         self.from_time = from_time
#         self.to_time = to_time
#    def run(self):
#         print("Starting " + self.name)
#         thread_function_send_email_when_route_free(self.from_place, self.to_place, self.from_date, self.to_date, self.from_time, self.to_time)
#         print("Exiting " + self.name)
#
# thread1 = myThread(1, "Thread-1", "Brno", "Praha", "21.10.2018")
# thread2 = myThread(2, "Thread-2", "Viedeň", "Košice", "12.11.2018", from_time="15:00")
#
#
# #thread1.start()
# thread2.start()
#
# print("Exiting Main Thread")
