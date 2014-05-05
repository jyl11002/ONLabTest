
class ShreyaTestBackup :

    def __init__(self) :
        self.default = ''

  
    def CASE1(self,main) :
        main.case("Testing Floodlight")
        main.step("Testing isup() function")
        result = main.Floodlight1.isup()
        main.step("Verifying result")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Floodlight connected",onfail="Floodlight not connected")

    def CASE2(self,main) :

        main.case("Testing the configuration of the host")
        main.step("Host IP Checking using checkIP")
        result = main.Mininet1.checkIP(main.params['CASE1']['destination'])
        main.step("Verifying the result")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="Host h2 IP address configured",onfail="Host h2 IP address didn't configured")

    def CASE3(self,main) :
        main.case("Testing OVX")
        main.step("Testing isup() function of OVX")
        result = main.OVX1.isup()
        main.step("Verifying result")
        utilities.assert_equals(expect=main.TRUE,actual=result,onpass="OVX connected",onfail="OVX not connected")

