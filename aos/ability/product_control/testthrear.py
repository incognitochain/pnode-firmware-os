# import threading, time
#
# import thread
#
#
# class MyThread(threading.Thread):
#     def run(self):
#         while True:
#             print "ga ..."
#             time.sleep(1)
#
#
# th = MyThread()
# th.daemon = True
# th.start()
#
# time.sleep(5)
# thread.exit()


class A(object):
    def ga(self, x):
        print "ga" + x

a = A()

getattr(a, "ga")("vai dai ")