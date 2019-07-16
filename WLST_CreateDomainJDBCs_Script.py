
import sys
from java.lang import System
from java.io import FileInputStream

envproperty=""
if (len(sys.argv) > 1):
	envproperty=sys.argv[1]
else:
	print "Environment Property file not specified"
	sys.exit(2)

propInputStream = FileInputStream(envproperty)
configProps = Properties()
configProps.load(propInputStream)

print "Starting the script ..."

def CreateDataSource(DSnam,JNDIName,Url,DriverName,User,Pass,ConnectTimeOut,MaxCap,MinCap,InitialCap,ShrinkFS,InacConToutSec,ConCreRetFrecSec,StatChacheSize,TestFreqSec,LoginDelaySec,SecsToTrust,TargetsList,modifyConfigFlag,XaTxTimeout) :

	RESOURCE='/JDBCSystemResources/'+DSnam+'/JDBCResource/'+DSnam
	mb = getMBean(RESOURCE)
	if mb:
		print (DSnam + ' already exists')
	else:
		modifyConfigFlag = '1'

		print('Creating Data source: ' +DSnam)
		cd('/')
		cmo.createJDBCSystemResource(DSnam)
		#RESOURCE='/JDBCSystemResources/'+DSnam+'/JDBCResource/'+DSnam
		cd(RESOURCE)
		set('Name',DSnam)

		#Setting JNDI name
		cd(RESOURCE+'/JDBCDataSourceParams/'+DSnam)
		print(RESOURCE+'/JDBCDataSourceParams/'+DSnam)
		set('JNDINames',jarray.array([String(JNDIName)], String))

		cd(RESOURCE+'/JDBCDriverParams/'+DSnam)
		print (RESOURCE+'/JDBCDriverParams/'+DSnam)
		cmo.setUrl(Url)
		cmo.setDriverName(DriverName)
		cmo.setPassword(Pass);
  
		cd(RESOURCE+'/JDBCConnectionPoolParams/'+DSnam)
		print (RESOURCE+'/JDBCConnectionPoolParams/'+DSnam)
		cmo.setTestTableName('SQL SELECT 1 FROM DUAL\r\n')
  
		#Setting USER name
		cd(RESOURCE+'/JDBCDriverParams/'+DSnam+'/Properties/'+DSnam)
		cmo.createProperty('user')

		cd(RESOURCE+'/JDBCDriverParams/'+DSnam+'/Properties/'+DSnam+'/Properties/user')
		cmo.setValue(User)
  
		#Setting CONNECT_TIMEOUT
		timeout = ConnectTimeOut
		strConnectTimeOut = ConnectTimeOut
		if timeout in ('0') :
			print 'CONNECT_TIMEOUT property not created'
		else :
			cd(RESOURCE+'/JDBCDriverParams/'+DSnam+'/Properties/'+DSnam)
			cmo.createProperty('oracle.net.CONNECT_TIMEOUT')
			cd(RESOURCE+'/JDBCDriverParams/'+DSnam+'/Properties/'+DSnam+'/Properties/oracle.net.CONNECT_TIMEOUT')
			cmo.setValue(strConnectTimeOut)
  
		cd(RESOURCE+'/JDBCDataSourceParams/'+DSnam)
		print (RESOURCE+'/JDBCDataSourceParams/'+DSnam)
		cmo.setGlobalTransactionsProtocol('TwoPhaseCommit')
	
	if modifyConfigFlag in ('1'):
		print (DSnam + ' will be modified')
		dataSourceBean = getMBean('/JDBCSystemResources/'+DSnam)
		TargetsArray = String(TargetsList).split(":")
		for Target in TargetsArray:
			TargetInfo = String(Target).split(",")
			if TargetInfo[1] in ('S','s'):
				print "- Adding Server Target: " + TargetInfo[0]
				cd("/Servers/"+TargetInfo[0])
				targetToSet=cmo
				cd("../..")
				dataSourceBean.addTarget(targetToSet)
			if TargetInfo[1] in ('C','c'):
				print "- Adding Cluster Target: " + TargetInfo[0]
				cd("/Clusters/"+TargetInfo[0])
				targetToSet=cmo
				cd("../..")
				dataSourceBean.addTarget(targetToSet)
			
		cd(RESOURCE+'/JDBCConnectionPoolParams/'+DSnam)
		print (RESOURCE+'/JDBCConnectionPoolParams/'+DSnam)
		cmo.setMaxCapacity(int(MaxCap))
		cmo.setMinCapacity(int(MinCap))
		cmo.setInitialCapacity(int(InitialCap))
		cmo.setShrinkFrequencySeconds(int(ShrinkFS))
		cmo.setInactiveConnectionTimeoutSeconds(int(InacConToutSec))
		cmo.setConnectionCreationRetryFrequencySeconds(int(ConCreRetFrecSec))
		cmo.setStatementCacheSize(int(StatChacheSize))
		cmo.setTestFrequencySeconds(int(TestFreqSec))
		cmo.setLoginDelaySeconds(int(LoginDelaySec))
		cmo.setSecondsToTrustAnIdlePoolConnection(int(SecsToTrust))
		cmo.setTestConnectionsOnReserve(true)
		cmo.setTestTableName('SQL SELECT 1 FROM DUAL\r\n')
		save()
		
		cd(RESOURCE+'/JDBCXAParams/'+DSnam)
		cmo.setXaSetTransactionTimeout(true)
		cmo.setXaTransactionTimeout(int(XaTxTimeout))
		save()

	if modifyConfigFlag in ('1'):
		print('DataSource ' + DSnam + ' successfully created or modified')
	else:
		print ('DataSource ' + DSnam + ' already exists and no changes were made')

print('############################################')
print('      WEBLOGIC CONSOLE CONNECTION           ')
print('############################################')

hostNameConsoleWL = configProps.get("hostName.ConsoleWL")
portConsoleWL = configProps.get("port.ConsoleWL")
userNameAdmin = raw_input('Type the Admin user (' + hostNameConsoleWL + ':' + portConsoleWL + '):')
passWordAdmin = raw_input('Type the password for Admin user (' + hostNameConsoleWL + ':' + portConsoleWL + '):')

connect(userNameAdmin,passWordAdmin,'t3://' + hostNameConsoleWL + ':' + portConsoleWL) 

#############################################################################
#				 				 DATA SOURCES								#
#############################################################################

print('#######################################################')
print('                 DATA SOURCES CREATION                 ')
print('#######################################################')

edit()
startEdit()

dsCount=1
totalDsCount=configProps.get("total.Ds.Count")
while (dsCount <= int(totalDsCount)) :
	dsName = configProps.get("ds.Name."+ str(dsCount))
	dsJNDI = configProps.get("ds.JNDI."+ str(dsCount))
	dsUrl = configProps.get("ds.Url."+ str(dsCount))
	dsUser = configProps.get("ds.User."+ str(dsCount))
	dsPassword = configProps.get("ds.Password."+ str(dsCount))
	dsDriverName = configProps.get("ds.DriverName."+ str(dsCount))
	dsConectTimeOutProperty = configProps.get("ds.ConectTimeOutProperty."+ str(dsCount))
	dsInitialCapacity = configProps.get("ds.InitialCapacity."+ str(dsCount))
	dsMinCapacity = configProps.get("ds.MinCapacity."+ str(dsCount))
	dsMaxCapacity = configProps.get("ds.MaxCapacity."+ str(dsCount))
	dsSecsToTrust = configProps.get("ds.SecsToTrust."+ str(dsCount))
	dsShrinkFS = configProps.get("ds.ShrinkFS."+ str(dsCount))
	dsInactiveConnectionTO = configProps.get("ds.InactiveConnectionTO."+ str(dsCount))
	dsConnectionCreationRet = configProps.get("ds.ConnectionCreationRet."+ str(dsCount))
	dsStatementCacheSize = configProps.get("ds.StatementCacheSize."+ str(dsCount))
	dsTestFrequency = configProps.get("ds.TestFrequency."+ str(dsCount))
	dsLogginDelay = configProps.get("ds.LogginDelay."+ str(dsCount))
	dsTargetsList = configProps.get("ds.TargetsList."+ str(dsCount))
	dsModifyConfigFlag = configProps.get("ds.ModifyConfigFlag."+ str(dsCount))
	dsXaTxTimeout = configProps.get("ds.XaTxTimeout."+ str(dsCount))
	print "Creating "+ dsName +"..."
	CreateDataSource(dsName,dsJNDI,dsUrl,dsDriverName,dsUser,dsPassword,dsConectTimeOutProperty,dsMaxCapacity,dsMinCapacity,dsInitialCapacity,dsShrinkFS,dsInactiveConnectionTO,dsConnectionCreationRet,dsStatementCacheSize,dsTestFrequency,dsLogginDelay,dsSecsToTrust,dsTargetsList,dsModifyConfigFlag,dsXaTxTimeout)
	dsCount = dsCount + 1

try:
	save()
	activate(block="true")
	print "Script returns SUCCESS"   
except:
	print "Error while trying to save and/or activate!!!"
	cancelEdit()
	dumpStack()
exit()
