import win32com.client

strComputer = "."
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_PnPEntity")
for objItem in colItems:
    if(objItem.Name!=None and objItem.Name=='USB Token'):
        print("Name:" + objItem.Name)
        print("Status:" + objItem.Status)
        print("Manufacturer:" + objItem.Manufacturer)
        print("DeviceID:" + objItem.DeviceID)
        print("Status:" + objItem.Status)
