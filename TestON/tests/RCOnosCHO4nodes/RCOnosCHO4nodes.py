
class RCOnosCHO4nodes :

    def __init__(self) :
        self.default = ''

#**********************************************************************************************************************************************************************************************
#Test startup
#Tests the startup of Zookeeper1, RamCloud1, and ONOS1 to be certain that all started up successfully
    def CASE1(self,main) :  #Check to be sure ZK, Cass, and ONOS are up, then get ONOS version
        import time
        main.ONOS1.handle.sendline("cp ~/onos.properties.proactive ~/ONOS/conf/onos.properties")
        main.ONOS2.handle.sendline("cp ~/onos.properties.proactive ~/ONOS/conf/onos.properties")
        main.ONOS3.handle.sendline("cp ~/onos.properties.proactive ~/ONOS/conf/onos.properties")
        main.ONOS4.handle.sendline("cp ~/onos.properties.proactive ~/ONOS/conf/onos.properties")

        main.Zookeeper1.start()
        main.Zookeeper2.start()
        main.Zookeeper3.start()
        main.Zookeeper4.start()
        main.RamCloud1.stop_coor()
        main.RamCloud1.stop_serv()
        main.RamCloud2.stop_serv()
        main.RamCloud3.stop_serv()
        main.RamCloud4.stop_serv()
        time.sleep(10)
        main.RamCloud1.del_db()
        main.RamCloud2.del_db()
        main.RamCloud3.del_db()
        main.RamCloud4.del_db()
        time.sleep(10)
        main.log.report("Pulling latest code from github to all nodes")
        for i in range(2):
            uptodate = main.ONOS1.git_pull()
            main.ONOS2.git_pull()
            main.ONOS3.git_pull()
            main.ONOS4.git_pull()
            ver1 = main.ONOS1.get_version()
            ver2 = main.ONOS4.get_version()
            if ver1==ver2:
                break
            elif i==1:
                main.ONOS2.git_pull("ONOS1 master")
                main.ONOS3.git_pull("ONOS1 master")
                main.ONOS4.git_pull("ONOS1 master")
       #if uptodate==0
        if 1:
            main.ONOS1.git_compile()
            main.ONOS2.git_compile()
            main.ONOS3.git_compile()
            main.ONOS4.git_compile()
        main.ONOS1.print_version()
       # main.RamCloud1.git_pull()
       # main.RamCloud2.git_pull()
       # main.RamCloud3.git_pull()
       # main.RamCloud4.git_pull()
       # main.ONOS1.get_version()
       # main.ONOS2.get_version()
       # main.ONOS3.get_version()
       # main.ONOS4.get_version()
        main.RamCloud1.start_coor()
        time.sleep(1)
        main.RamCloud1.start_serv()
        main.RamCloud2.start_serv()
        main.RamCloud3.start_serv()
        main.RamCloud4.start_serv()
        main.ONOS1.start()
        time.sleep(5)
        main.ONOS2.start()
        main.ONOS3.start()
        main.ONOS4.start()
        main.ONOS1.start_rest()
        time.sleep(10)
        test= main.ONOS1.rest_status()
        if test == main.FALSE:
            main.ONOS1.start_rest()
        main.ONOS1.get_version()
        main.log.report("Startup check Zookeeper1, RamCloud1, and ONOS1 connections")
        main.case("Checking if the startup was clean...")
        main.step("Testing startup Zookeeper")
        data =  main.Zookeeper1.isup()
        utilities.assert_equals(expect=main.TRUE,actual=data,onpass="Zookeeper is up!",onfail="Zookeeper is down...")
        main.step("Testing startup RamCloud")
        data =  main.RamCloud1.status_serv()
        if data == main.FALSE:
            main.RamCloud1.stop_coor()
            main.RamCloud1.stop_serv()
            main.RamCloud2.stop_serv()
            main.RamCloud3.stop_serv()
            main.RamCloud4.stop_serv()

            time.sleep(5)
            main.RamCloud1.start_coor()
            main.RamCloud1.start_serv()
            main.RamCloud2.start_serv()
            main.RamCloud3.start_serv()
            main.RamCloud4.start_serv()
        utilities.assert_equals(expect=main.TRUE,actual=data,onpass="RamCloud is up!",onfail="RamCloud is down...")
        main.step("Testing startup ONOS")
        data = main.ONOS1.isup()
        for i in range(3):
            if data == main.FALSE:
                #main.log.report("Something is funny... restarting ONOS")
                #main.ONOS1.stop()
                time.sleep(3)
                #main.ONOS1.start()
                #time.sleep(5)
                data = main.ONOS1.isup()
            else:
                break
        utilities.assert_equals(expect=main.TRUE,actual=data,onpass="ONOS is up and running!",onfail="ONOS didn't start...")
        time.sleep(20)

          
#**********************************************************************************************************************************************************************************************
#Assign Controllers
#This test first checks the ip of a mininet host, to be certain that the mininet exists(Host is defined in Params as <CASE1><destination>).
#Then the program assignes each ONOS instance a single controller to a switch(To be the initial master), then assigns all controllers.
#NOTE: The reason why all four controllers are assigned although one was already assigned as the master is due to the 'ovs-vsctl set-controller' command erases all present controllers if
#      the controllers already assigned to the switch are not specified.

    def CASE2(self,main) :    #Make sure mininet exists, then assign controllers to switches
        import time
        main.log.report("Check if mininet started properly, then assign controllers ONOS 1,2,3 and 4")
        main.case("Checking if one MN host exists")
        main.step("Host IP Checking using checkIP")
        result = main.Mininet1.checkIP(main.params['CASE1']['destination'])
        main.step("Verifying the result")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Host IP address configured",onfail="Host IP address not configured")
        main.step("assigning ONOS controllers to switches")
        for i in range(25): 
            if i < 3:
                j=i+1
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'])
                time.sleep(1)
                main.Mininet1.assign_sw_controller(sw=str(j),count=4,ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'],ip2=main.params['CTRL']['ip2'],port2=main.params['CTRL']['port2'],ip3=main.params['CTRL']['ip3'],port3=main.params['CTRL']['port3'],ip4=main.params['CTRL']['ip4'],port4=main.params['CTRL']['port4'])
            elif i >= 3 and i < 5:
                j=i+1
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip2'],port1=main.params['CTRL']['port2'])
                time.sleep(1)
                main.Mininet1.assign_sw_controller(sw=str(j),count=4,ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'],ip2=main.params['CTRL']['ip2'],port2=main.params['CTRL']['port2'],ip3=main.params['CTRL']['ip3'],port3=main.params['CTRL']['port3'],ip4=main.params['CTRL']['ip4'],port4=main.params['CTRL']['port4'])
            elif i >= 5 and i < 15:
                j=i+1
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip3'],port1=main.params['CTRL']['port3'])
                time.sleep(1)
                main.Mininet1.assign_sw_controller(sw=str(j),count=4,ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'],ip2=main.params['CTRL']['ip2'],port2=main.params['CTRL']['port2'],ip3=main.params['CTRL']['ip3'],port3=main.params['CTRL']['port3'],ip4=main.params['CTRL']['ip4'],port4=main.params['CTRL']['port4'])
            else:
                j=i+16
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=main.params['CTRL']['ip4'],port1=main.params['CTRL']['port4'])
                time.sleep(1)
                main.Mininet1.assign_sw_controller(sw=str(j),count=4,ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'],ip2=main.params['CTRL']['ip2'],port2=main.params['CTRL']['port2'],ip3=main.params['CTRL']['ip3'],port3=main.params['CTRL']['port3'],ip4=main.params['CTRL']['ip4'],port4=main.params['CTRL']['port4'])
        result =  main.Mininet1.get_sw_controller("s1")
        if result:
            result = main.TRUE
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="S1 assigned to controller",onfail="S1 not assigned to controller")

        for i in range(9):
            if result == main.FALSE:
                time.sleep(3)
                result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
            else:
                break 
 
# **********************************************************************************************************************************************************************************************
#Add Flows
#Deletes any remnant flows from any previous test, add flows from the file labeled <FLOWDEF>, then runs the check flow test
#NOTE: THE FLOWDEF FILE MUST BE PRESENT ON TESTON VM!!! TestON will copy the file from its home machine into /tmp/flowtmp on the machine the ONOS instance is present on

    def CASE3(self,main) :    #Delete any remnant flows, then add flows, and time how long it takes flow tables to update
        main.log.report("Delete any flows from previous tests, then add flows using intents and wait for switch flow tables to update")
        import time

        result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
        for counter in range(9):
            if result == main.FALSE:
                time.sleep(3)
                result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
            else:
                break
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Topology check pass",onfail="Topology check FAIL")

        main.case("Taking care of these flows!") 
        main.step("Cleaning out any leftover flows...")
        #main.ONOS1.delete_flow("all")
        main.ONOS1.rm_intents()
        time.sleep(5)
        main.ONOS1.purge_intents()
        strtTime = time.time()
        main.ONOS1.add_intents()
        main.case("Checking flows with pings")
        
        pingAttempts = main.params['pingAttempts']
        pingSleep = main.params['pingSleep']

        count = 1
        i = 6
        while i < 16 :
            main.log.info("\n\t\t\t\th"+str(i)+" IS PINGING h"+str(i+25) )
            ping = main.Mininet1.pingHost(src="h"+str(i),target="h"+str(i+25))
            if ping == main.FALSE and count < int(pingAttempts):
                count = count + 1
               # i = 6
                main.log.report("Ping failed, making attempt number "+str(count)+" in "+str(pingSleep)+"  seconds")
                time.sleep(int(pingSleep))
            elif ping == main.FALSE and count == int(pingAttempts):
                main.log.error("Ping test failed")
                i = 17
                result2 = main.FALSE
            elif ping == main.TRUE:
                i = i + 1
                result2 = main.TRUE
        endTime = time.time()
        result = result and result2
        if result == main.TRUE:
             main.log.report("\n\t\t\t\tTime from pushing intents to successful ping test: "+str(round(endTime-strtTime,2))+" seconds")
        else:
            main.log.report("\tFlows failed check")

        main.step("Verifying the result")
        utilities.assert_equals(expect=main.TRUE,actual=result2,onpass="NO PACKET LOSS, HOST IS REACHABLE",onfail="PACKET LOST, HOST IS NOT REACHABLE")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Testcase passed",onfail="Testcase failed")

#**********************************************************************************************************************************************************************************************
#This test case removes Controllers 2,3, and 4 then performs a ping test.
#The assign controller is used because the ovs-vsctl module deletes all current controllers when a new controller is assigned.
#The ping test performs single pings on hosts from opposite sides of the topology. If one ping fails, the test waits 5 seconds before trying again.
#If the ping test fails 6 times, then the test case will return false

    def CASE4(self,main) :
        main.log.report("Assign all switches to just one ONOS instance then ping until all hosts are reachable or fail after 6 attempts")
        import time
        import random

        random.seed(None)

        num = random.randint(1,4)
        if num == 1:
            ip = main.params['CTRL']['ip1']
            port = main.params['CTRL']['port1']
        elif num == 2:
            ip = main.params['CTRL']['ip2']
            port = main.params['CTRL']['port2']
        elif num == 3:
            ip = main.params['CTRL']['ip3']
            port = main.params['CTRL']['port3']
        else:
            ip = main.params['CTRL']['ip4']
            port = main.params['CTRL']['port4']

        main.log.report("ONOS"+str(num)+" will be the sole controller")
        for i in range(25):
            if i < 15:
                j=i+1
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=ip,port1=port)  #Assigning a single controller removes all other controllers
            else:
                j=i+16
                main.Mininet1.assign_sw_controller(sw=str(j),ip1=ip,port1=port)
      
        strtTime = time.time() 
        result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
        for counter in range(9):
            if result == main.FALSE:
                time.sleep(3)
                result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
            else:
                break
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Topology check pass",onfail="Topology check FAIL")

        pingAttempts = main.params['pingAttempts']
        pingSleep = main.params['pingSleep']

        count = 1
        i = 6
        while i < 16 :
            main.log.info("\n\t\t\t\th"+str(i)+" IS PINGING h"+str(i+25) )
            ping = main.Mininet1.pingHost(src="h"+str(i),target="h"+str(i+25))
            if ping == main.FALSE and count < int(pingAttempts):
                count = count + 1
               # i = 6
                main.log.report("Ping failed, making attempt number "+str(count)+" in "+str(pingSleep)+" seconds")
                time.sleep(int(pingSleep))
            elif ping == main.FALSE and count == int(pingAttempts):
                main.log.error("Ping test failed")
                i = 17
                result2 = main.FALSE
            elif ping == main.TRUE:
                i = i + 1
                result2 = main.TRUE
        endTime = time.time() 
        result = result and result2
        if result == main.TRUE:
            main.log.report("\tTime to complete ping test: "+str(round(endTime-strtTime,2))+" seconds")
        else:
            main.log.report("\tPING TEST FAIL")
        utilities.assert_equals(expect=main.TRUE,actual=result2,onpass="NO PACKET LOSS, HOST IS REACHABLE",onfail="PACKET LOST, HOST IS NOT REACHABLE")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Testcase passed",onfail="Testcase failed")

# **********************************************************************************************************************************************************************************************
#This test case restores the controllers removed by Case 4 then performs a ping test.

    def CASE5(self,main) :
        main.log.report("Restore switch assignments to all 4 ONOS instances then ping until all hosts are reachable or fail after 6 attempts")
        import time
        for i in range(25):
            if i < 15:
                j=i+1
                main.Mininet1.assign_sw_controller(sw=str(j),count=4,ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'],ip2=main.params['CTRL']['ip2'],port2=main.params['CTRL']['port2'],ip3=main.params['CTRL']['ip3'],port3=main.params['CTRL']['port3'],ip4=main.params['CTRL']['ip4'],port4=main.params['CTRL']['port4'])
            else:
                j=i+16
                main.Mininet1.assign_sw_controller(sw=str(j),count=4,ip1=main.params['CTRL']['ip1'],port1=main.params['CTRL']['port1'],ip2=main.params['CTRL']['ip2'],port2=main.params['CTRL']['port2'],ip3=main.params['CTRL']['ip3'],port3=main.params['CTRL']['port3'],ip4=main.params['CTRL']['ip4'],port4=main.params['CTRL']['port4'])
      
        strtTime = time.time() 
        result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
        for counter in range(9):
            if result == main.FALSE:
                time.sleep(3)
                result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
            else:
                break
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Topology check pass",onfail="Topology check FAIL")

        pingAttempts = main.params['pingAttempts']
        pingSleep = main.params['pingSleep']

        count = 1
        i = 6
        while i < 16 :
            main.log.info("\n\t\t\t\th"+str(i)+" IS PINGING h"+str(i+25) )
            ping = main.Mininet1.pingHost(src="h"+str(i),target="h"+str(i+25))
            if ping == main.FALSE and count < int(pingAttempts):
                count = count + 1
               # i = 6
                main.log.report("Ping failed, making attempt number "+str(count)+" in "+str(pingSleep)+" seconds")
                time.sleep(int(pingSleep))
            elif ping == main.FALSE and count == int(pingAttempts):
                main.log.error("Ping test failed")
                i = 17
                result2 = main.FALSE
            elif ping == main.TRUE:
                i = i + 1
                result2 = main.TRUE
        endTime = time.time()
        result = result and result2
        if result == main.TRUE:
            main.log.report("\tTime to complete ping test: "+str(round(endTime-strtTime,2))+" seconds")
        else:
            main.log.report("\tPING TEST FAILED")
        utilities.assert_equals(expect=main.TRUE,actual=result2,onpass="NO PACKET LOSS, HOST IS REACHABLE",onfail="PACKET LOST, HOST IS NOT REACHABLE")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Testcase passed",onfail="Testcase failed")

# **********************************************************************************************************************************************************************************************
#Brings a link that all flows pass through in the mininet down, then runs a ping test to view reroute time

    def CASE6(self,main) :
        main.log.report("Bring Link between s1 and s2 down, then ping until all hosts are reachable or fail after 10 attempts")
        import time

        #add a wait as a work around for a known bug where topology changes after a switch mastership change cuses intents to not reroute
        time.sleep(30)

        main.case("Bringing Link down... ")
        result = main.Mininet1.link(END1=main.params['LINK']['begin'],END2=main.params['LINK']['end'],OPTION="down")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Link DOWN!",onfail="Link not brought down...")

        #add a wait as a work around for a known bug where topology changes after a switch mastership change cuses intents to not reroute
        time.sleep(30)

       
        strtTime = time.time() 
        result1 = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],str(int(main.params['NR_Links'])-2))
        for counter in range(9):
            if result1 == main.FALSE:
                time.sleep(3)
                result1 = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],str(int(main.params['NR_Links'])-2))
            else:
                break
        utilities.assert_equals(expect=main.TRUE,actual=result1,onpass="Topology check pass",onfail="Topology check FAIL")

        pingAttempts = main.params['pingAttempts']
        pingSleep = main.params['pingSleep']

        count = 1
        i = 6
        while i < 16 :
            main.log.info("\n\t\t\t\th"+str(i)+" IS PINGING h"+str(i+25) )
            ping = main.Mininet1.pingHost(src="h"+str(i),target="h"+str(i+25))
            if ping == main.FALSE and count < int(pingAttempts):
                count = count + 1
                main.log.report("Ping failed, making attempt number "+str(count)+" in "+str(pingSleep)+" seconds")
                #i = 6
                time.sleep(int(pingSleep))
            elif ping == main.FALSE and count == int(pingAttempts):
                main.log.error("Ping test failed")
                i = 17
                result2 = main.FALSE
            elif ping == main.TRUE:
                i = i + 1
                result2 = main.TRUE
        endTime = time.time()
        result = result and result2 and result1
        if result == main.TRUE:
            main.log.report("\tTime to complete ping test: "+str(round(endTime-strtTime,2))+" seconds")
        else:
            main.log.report("\tPING TEST FAILED")
        utilities.assert_equals(expect=main.TRUE,actual=result2,onpass="NO PACKET LOSS, HOST IS REACHABLE",onfail="PACKET LOST, HOST IS NOT REACHABLE")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Testcase passed",onfail="Testcase failed")

# **********************************************************************************************************************************************************************************************
#Brings the link that Case 6 took down  back up, then runs a ping test to view reroute time

    def CASE7(self,main) :
        main.log.report("Bring Link between s1 and s2 up, then ping until all hosts are reachable or fail after 10 attempts")
        import time
        main.case("Bringing Link up... ")

        #add a wait as a work around for a known bug where topology changes after a switch mastership change cuses intents to not reroute
        time.sleep(30)

        result = main.Mininet1.link(END1=main.params['LINK']['begin'],END2=main.params['LINK']['end'],OPTION="up")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Link UP!",onfail="Link not brought up...")
      
        strtTime = time.time() 
        result1 = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
        for counter in range(9):
            if result1 == main.FALSE:
                time.sleep(3)
                result1 = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
            else:
                break
        utilities.assert_equals(expect=main.TRUE,actual=result1,onpass="Topology check pass",onfail="Topology check FAIL")

        pingAttempts = main.params['pingAttempts']
        pingSleep = main.params['pingSleep']

        strtTime = time.time()
        count = 1
        i = 6
        while i < 16 :
            main.log.info("\n\t\t\t\th"+str(i)+" IS PINGING h"+str(i+25) )
            ping = main.Mininet1.pingHost(src="h"+str(i),target="h"+str(i+25))
            if ping == main.FALSE and count < int(pingAttempts):
                count = count + 1
                main.log.report("Ping failed, making attempt number "+str(count)+" in " +str(pingSleep)+" seconds")
                #i = 6
                time.sleep(int(pingSleep))
            elif ping == main.FALSE and count == int(pingAttempts):
                main.log.error("Ping test failed")
                i = 17
                result2 = main.FALSE
            elif ping == main.TRUE:
                i = i + 1
                result2 = main.TRUE
        endTime = time.time()
        result = result and result2 and result1
        if result == main.TRUE:
            main.log.report("\tTime to complete ping test: "+str(round(endTime-strtTime,2))+" seconds")
        else:
            main.log.report("\tPING TESTS FAILED")
        
        main.ONOS1.check_exceptions()
        main.ONOS2.check_exceptions()
        main.ONOS3.check_exceptions()
        main.ONOS4.check_exceptions()

        utilities.assert_equals(expect=main.TRUE,actual=result2,onpass="NO PACKET LOSS, HOST IS REACHABLE",onfail="PACKET LOST, HOST IS NOT REACHABLE")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Testcase passed",onfail="Testcase failed")

        #add a wait as a work around for a known bug where topology changes after a switch mastership change cuses intents to not reroute
        time.sleep(30)



# **********************************************************************************************************************************************************************************************
# Runs reactive ping test
    def CASE8(self,main) :
        main.log.report("Reactive flow ping test:ping until the routes are active or fail after 10 attempts")
        import time
      
        strtTime = time.time() 
        result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
        for counter in range(9):
            if result == main.FALSE:
                time.sleep(3)
                result = main.ONOS1.check_status_report(main.params['RestIP'],main.params['NR_Switches'],main.params['NR_Links'])
            else:
                break
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Topology check pass",onfail="Topology check FAIL")

        pingAttempts = main.params['pingAttempts']
        pingSleep = main.params['pingSleep']

        strtTime = time.time()
        count = 1
        i = 6
        while i < 16 :
            main.log.info("\n\t\t\t\th"+str(i)+" IS PINGING h"+str(46-i) )
            ping = main.Mininet1.pingHost(src="h"+str(i),target="h"+str(46-i))
            if ping == main.FALSE and count < int(pingAttempts):
                count = count + 1
                main.log.report("Ping failed, making attempt number "+str(count)+" in " +str(pingSleep)+" seconds")
                #i = 6
                time.sleep(int(pingSleep))
            elif ping == main.FALSE and count == int(pingAttempts):
                main.log.error("Ping test failed")
                i = 17
                result2 = main.FALSE
            elif ping == main.TRUE:
                i = i + 1
                result2 = main.TRUE
        endTime = time.time()
        result = result and result2
        if result == main.TRUE:
            main.log.report("\tTime to complete ping test: "+str(round(endTime-strtTime,2))+" seconds")
        else:
            main.log.report("\tPING TESTS FAILED")
        
        main.ONOS1.check_exceptions()
        main.ONOS2.check_exceptions()
        main.ONOS3.check_exceptions()
        main.ONOS4.check_exceptions()

        utilities.assert_equals(expect=main.TRUE,actual=result2,onpass="NO PACKET LOSS, HOST IS REACHABLE",onfail="PACKET LOST, HOST IS NOT REACHABLE")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Testcase passed",onfail="Testcase failed")


# ******************************************************************************************************************************************************************
# Test Device Discovery function by yanking s6:s6-eth0 interface and re-plug it into a switch

    def CASE9(self,main) :
        main.case("Checking component status")
        result = main.TRUE

        main.step("Checking Zookeeper status")
        result1 = main.Zookeeper1.status()
        if not result1:
            main.log.report("Zookeeper1 encountered a tragic death!")
        result2 = main.Zookeeper2.status()
        if not result2:
            main.log.report("Zookeeper2 encountered a tragic death!")
        result3 = main.Zookeeper3.status()
        if not result3:
            main.log.report("Zookeeper3 encountered a tragic death!")
        result4 = main.Zookeeper4.status()
        if not result4:
            main.log.report("Zookeeper4 encountered a tragic death!")
        result = result and result1 and result2 and result3 and result4

        main.step("Checking RamCloud status")
        result5 = main.RamCloud1.status_coor()
        if not result5:
            main.log.report("RamCloud Coordinator1 encountered a tragic death!")
        result6 = main.RamCloud1.status_serv()
        if not result6:
            main.log.report("RamCloud Server1 encountered a tragic death!")
        result7 = main.RamCloud2.status_serv()
        if not result7:
            main.log.report("RamCloud Server2 encountered a tragic death!")
        result8 = main.RamCloud3.status_serv()
        if not result8:
            main.log.report("RamCloud Server3 encountered a tragic death!")
        result9 = main.RamCloud4.status_serv()
        if not result9:
            main.log.report("RamCloud Server4 encountered a tragic death!")
        result = result and result5 and result6 and result7 and result8 and result9


        main.step("Checking ONOS status")
        result10 = main.ONOS1.status()
        if not result10:
            main.log.report("ONOS1 core encountered a tragic death!")
        result11 = main.ONOS2.status()
        if not result11:
            main.log.report("ONOS2 core encountered a tragic death!")
        result12 = main.ONOS3.status()
        if not result12:
            main.log.report("ONOS3 core encountered a tragic death!")
        result13 = main.ONOS4.status()
        if not result13:
            main.log.report("ONOS4 core encountered a tragic death!")
        result = result and result10 and result11 and result12 and result13



        rest_result =  main.ONOS1.rest_status()
        if not rest_result:
            main.log.report("Simple Rest GUI server is not running on ONOS1")


        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="All Components are running",onfail="One or more components failed")

# ******************************************************************************************************************************************************************
# Test Device Discovery function by yanking s6:s6-eth0 interface and re-plug it into a switch

    def CASE21(self,main) :
        import json
        from drivers.common.api.onosrestapidriver import *
        main.log.report("Test device discovery function, by attach/detach/move host h1 from s1->s6->s1.")
        main.log.report("Check initially hostMAC exist on the mininet...")
        host = main.params['YANK']['hostname']
        mac = main.params['YANK']['hostmac']
        RestIP1 = main.params['RESTCALL']['restIP1']
        RestIP2 = main.params['RESTCALL']['restIP2']
        RestPort = main.params['RESTCALL']['restPort']
        url = main.params['RESTCALL']['restURL']
        #print "host=" + host + ";  RestIP=" + RestIP1 + ";  RestPort=" + str(RestPort)
        
        main.log.info("\n\t\t\t\t ping issue one ping from" + str(host) + "to generate arp to switch. Ping result is not important" )
        ping = main.Mininet1.pingHost(src = str(host),target = "10.0.0.254")
        restcall = OnosRestApiDriver()
        Reststatus, Hoststatus = restcall.find_host(RestIP1,RestPort,url,mac)
        try:
            attachedSW = Hoststatus[0]['attachmentPoint'][0]['switchDPID']
            ip_found = Hoststatus[0]['ipv4'][0]
        except:
            Reststatus = 0

        if Reststatus == 1:
            main.log.report("\tFound host " + host + " attached to switchDPID = " + attachedSW)
            if ip_found != None:
                main.log.report("\t IP discovered is ip_found ( " + ip_found + " ).")
                result = main.TRUE
            else:
                main.log.report("\t Found host attached to switch, but no IP address discovered.")
                result = main.FALSE
        else:
            main.log.report("\t Host " + host + " with MAC:" + str(mac) + " does not exist. FAILED")
            result = main.FALSE

        ##### Step to yank out "s1-eth1" from s1, which is on autoONOS1 #####

        main.log.report("Yank out s1-eth1")
        main.case("Yankout s6-eth1 (link to h1) from s1")
        result = main.Mininet1.yank(SW=main.params['YANK']['sw1'],INTF=main.params['YANK']['intf'])
        time.sleep(3)
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Yank command suceeded",onfail="Yank command failed...")
        ping = main.Mininet1.pingHost(src = str(host),target = "10.0.0.254")
        Reststatus, Hoststatus = restcall.find_host(RestIP1,RestPort,url,mac)
        try:
            attachedSW = Hoststatus[0]['attachmentPoint'][0]['switchDPID']
        except:
            Reststatus = 0
        if Reststatus == 0:
            main.log.report("Attempt to yank out s1-eth1 from s1 sucessfully")
            result = main.TRUE
        else:
            main.log.report("Attempt to yank out s1-eht1 from s1 failed.")
            result = main.FALSE
        
        ##### Step to plug "s1-eth1" to s6, which is on autoONOS3  ######
        main.log.report("Plug s1-eth1 into s6")
        main.case("Plug s1-eth1 to s6")
        result = main.Mininet1.plug(SW=main.params['PLUG']['sw6'],INTF=main.params['PLUG']['intf'])
        time.sleep(3)
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Plug command suceeded",onfail="Plug command failed...")
        ping = main.Mininet1.pingHost(src = str(host),target = "10.0.0.254")
        Reststatus, Hoststatus = restcall.find_host(RestIP2,RestPort,url,mac)
        try:
            attachedSW = Hoststatus[0]['attachmentPoint'][0]['switchDPID']
            ip_found = Hoststatus[0]['ipv4'][0]
        except:
            Reststatus = 0
        if Reststatus == 0:
            main.log.report("Attempt to plug s1-eth1 to s6 FAILED")
            result = main.FALSE
        elif attachedSW == "00:00:00:00:00:00:00:06":
            main.log.report("Attempt to plug s1-eht1 to s6 succeded.")
            if ip_found != None:
                main.log.report("\t IP discovered is ip_found ( " + ip_found + " ).")
                result = main.TRUE
            else:
                main.log.report("\t Found host attached to switch, but no IP address discovered.")
                result = main.FALSE
        else:
            main.log.report( "FAILED to attach s1-eth1 to s6 correctly!")
            result = main.FALSE

        ###### Step to put interface "s1-eth1" back to s1"#####
        main.log.report("Move s1-eth1 back on to s1")
        main.case("Move s1-eth1 back to s1")
        result = main.Mininet1.yank(SW=main.params['YANK']['sw6'],INTF=main.params['YANK']['intf'])
        time.sleep(3)
        retult = main.Mininet1.plug(SW=main.params['PLUG']['sw1'],INTF=main.params['PLUG']['intf'])
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Yank/Plug command suceeded",onfail="Yank/Plug command failed...")
        ping = main.Mininet1.pingHost(src = str(host),target = "10.0.0.254")
        Reststatus, Hoststatus = restcall.find_host(RestIP1,RestPort,url,mac)
        try:
            attachedSW = Hoststatus[0]['attachmentPoint'][0]['switchDPID']
            ip_found = Hoststatus[0]['ipv4'][0]
        except:
            Reststatus = 0
        if Reststatus == 0:
            main.log.report("Attempt to plug s1-eth1 back to s1 FAILED")
            result = main.FALSE
        elif attachedSW == "00:00:00:00:00:00:00:01":
            main.log.report("Attempt to plug s1-eht1 back to s1 succeded.")
            if ip_found != None:
                main.log.report("\t IP discovered is ip_found ( " + ip_found + " ).")
                result = main.TRUE
            else:
                main.log.report("\t Found host attached to switch, but no IP address discovered.")
                result = main.FALSE
        else:
            main.log.report( "FAIL to attach s1-eth1 to s1 correctly!")
            result = main.FALSE

        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="DEVICE DISCOVERY TEST PASSED PLUG/UNPLUG/MOVE TEST",onfail="DEVICE DISCOVERY TEST FAILED")




