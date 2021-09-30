import pymysql
import requests
import time
import threading
import pyzatt.misc as misc
import pyzatt.pyzatt as pyzatt
import pyzatt.zkmodules.defs as DEFS



myDB = pymysql.connect(
            host = 'localhost',
            user = 'root',
            database = 'zkteco_attendance'
        )

cur = myDB.cursor()


def device254():

    ip_address = '192.168.0.108' # set the ip address of the device to test
    machine_port = 4370
    z = pyzatt.ZKSS()
    z.connect_net(ip_address, machine_port)

    z.disable_device()
    z.read_all_user_id()
    z.enable_device()


    z.enable_realtime()

    try:
        while True:
            # wait for event
            z.recv_event()
            ev = z.get_last_event()

            # process the event
            # print("\n" + "#" * 50)
            # print("Received event")
            # z.recv_event()
            # ev = z.get_last_event()

            #time.sleep(5)
            
            if ev == DEFS.EF_ATTLOG:
                print("EF_ATTLOG: New attendance entry")
                print("User id: %s, verify type %i, date: %s" %
                tuple(z.parse_event_attlog()))
                data = tuple(z.parse_event_attlog())
                val = (data[0], data[2])
                squery = "INSERT INTO zkteco_attendance.attendances (office_id, punch_time) values ("+data[0]+", '{}'  )".format(data[2])
                cur.execute(squery)
                myDB.commit()

                if data[0] == "428":
                    url = "http://clients.muthofun.com:8901/esmsgw/sendsms.jsp?user=abdullah1404&password=abcd&mobiles=+8801400332371&sms=Shakil&unicode=1"
                elif data[0] == "1":
                    url = "http://clients.muthofun.com:8901/esmsgw/sendsms.jsp?user=abdullah1404&password=abcd&mobiles=+8801400332371&sms=Abdullah&unicode=1"
                else:
                    url = ""

                payload={}
                headers = {}
                response = requests.request("GET", url, headers=headers, data=payload)
                    
                print(squery)
                print("record inserted.")
            elif ev == DEFS.EF_FINGER:
                print("EF_FINGER: Finger placed on reader")
                print("User id: %s, verify type %i, date: %s" %
                tuple(z.parse_event_attlog()))
                data = tuple(z.parse_event_attlog())
                val = (data[0], data[2])
                squery = "INSERT INTO zkteco_attendance.attendances (office_id, punch_time) values ("+data[0]+", '{}'  )".format(data[2])
                cur.execute(squery)
                myDB.commit()
                print(squery)

                if data[0] == 428:
                    url = "http://clients.muthofun.com:8901/esmsgw/sendsms.jsp?user=abdullah1404&password=helloman&mobiles=+8801400332371&sms=Shakil&unicode=1"
                elif data[0] == 1:
                    url = "http://clients.muthofun.com:8901/esmsgw/sendsms.jsp?user=abdullah1404&password=helloman&mobiles=+8801400332371&sms=Shakil&unicode=1"
                else:
                    url = ""
                    
                payload={}
                headers = {}
                response = requests.request("GET", url, headers=headers, data=payload)

                print("record inserted.")



    except KeyboardInterrupt:
        misc.print_info("\nExiting...")

    z.disconnect()

device254()