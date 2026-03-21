/************************************************************************/
/*  FILENAME: DeaCMM.CPP                                                */
/*  FUNCTION: DeaCMM driver                                             */
/*  USAGE   : Run from windows                                          */
/*  Version : 1-50                                                      */
/*  Author  : Roger Bovill, Denford Machine Tools, Brighouse.           */
/*  Date    :  7 May  1993                                              */
/*  Language: Turbo   C++ 3.1                                           */
/************************************************************************/
/*      Maintenance Log                                                 */
/*      ---------------                                                 */
/*                                                                      */
/*  Date            Action                                              */
/*  ----            ------                                              */
/*                                                                      */
/*   7 May  1993    Created version 1-00                                */
/*                                                                      */
/*                                                                      */
/*  23 Aug  1993    Ver 1-00. Created                                   */
/*                                                                      */
/************************************************************************/
/************************************************************************/


#include <strstrea.h>
#include "\devel\devdriv\dea\deacmm.h"

TInterlockMgrDLL InterlockMgr; // Global interlock manager
TDeaCMM* PDeaCMMThis=NULL; // Static pointer to the TDeaCMM object instance
WORD hRS232=0;

/************************************************************************/
/* DEVICE DRIVER INITIALISATION FUNCTIONS                               */
/*                                                                      */
/************************************************************************/

// Construct a TDeaCMM object
/************************************************************************/
/* CONSTRUCTOR: TDeaCMM                                                 */
/* Purpose    : Creates an instance of a DeaCMM device driver object    */
/************************************************************************/
TDeaCMM::TDeaCMM() : TMachine()
{

}

/************************************************************************/
/* CONSTRUCTOR: Initialise                                              */
/* Purpose    : Must be called before any of TDeaCMMs methods are used  */
/************************************************************************/
BOOL TDeaCMM::Initialise(char * IniFileName)
{
  IsInitialised = TMachine::Initialise(IniFileName);
  ReadIniFile(IniFileName);
  lpfnStatusCB = NULL;
  PDeaCMMThis = this;

  if (NOT InputCommands(CommandFileName))
  {
	 char Message[80];
	 lstrcpy(Message, "Fatal error: Could not input\ncommands from file 'CMM.cmd'");
	 MessageBox(NULL, Message, MachineName, MB_OK | MB_TASKMODAL);
	 IsInitialised = FALSE;
  }
  DeaCMMLink.Load("dmtcomms.dll");
  if (NOT DeaCMMLink.IsLoaded())
  {
	 char Message[80];
	 lstrcpy(Message, "Fatal error: Could not load\n'dmtcomms.dll'");
	 MessageBox(NULL, Message, MachineName, MB_OK | MB_APPLMODAL | MB_ICONSTOP);
	 IsInitialised = FALSE;
  }
  CmdRequestStr[0] = '\0';
  return IsInitialised;
}

/************************************************************************/
/* DESTRUCTOR : TDeaCMM                                                 */
/* Purpose    : terminates a TDeaCMM instance                           */
/************************************************************************/
TDeaCMM::~TDeaCMM()
{

}

//const INVALIDBIT = 255;
BOOL TDeaCMM::ReadIniFile(char * IniFileName)
{
  BOOL res;
  res = TMachine::ReadIniFile(IniFileName);
  RS232.ReadIniFile(IniFileName);
  GetPrivateProfileString("FILES", "Commands File", "", CommandFileName, MAX_FILE_NAME, IniFileName);
  SamplgInterval = GetPrivateProfileInt("TIMER" ,"Sampling Interval" ,1000 , IniFileName);
  // Extras added by JHB for Malaysia...
  FlushInputBetweenChecks = (GetPrivateProfileInt("COMMS" ,"FlushInputBetweenChecks" ,1 , IniFileName) == 1);
  FlushInputAfterChecking = (GetPrivateProfileInt("COMMS" ,"FlushInputAfterChecking" ,1 , IniFileName) == 1);
  KeepChannelOpen = (GetPrivateProfileInt("COMMS" ,"KeepChannelOpen" ,1 , IniFileName) == 1);
  PollingCount = GetPrivateProfileInt("COMMS" ,"PollingCount" ,5 , IniFileName);
  GetPrivateProfileString("COMMS", "Reply", "", ReplyString, sizeof (ReplyString), IniFileName);
  ReceiveTimeout = GetPrivateProfileInt("COMMS" ,"ReceiveTimeout" ,2000 , IniFileName);
  return res;
}

/************************************************************************/
/* FUNCTION   : Reset                                                   */
/* Purpose    : Reset the device driver                                 */
/************************************************************************/
void TDeaCMM::Reset()
{
	if(hRS232)
	{
		DeaCMMLink.CloseChannel(hRS232);
		hRS232=0;
	}
	CurrCommand    =  PrevCommand = 0;
	CurrCmdState = PrevCmdState = CS_Ready;
	CmdError.Set(0, "");
	CmdRequestStr[0] = '\0';
	UpdateState();
}


/************************************************************************/
/* FUNCTION   : Start                                                   */
/* Purpose    : Starts device driver                                    */
/************************************************************************/
void TDeaCMM::Start(HINSTANCE hInstance)   // Application instance
{
  if (NOT IsInitialised)
	 return;
  Reset();
  Timer.Register(hInstance, SamplgInterval, // Set Timer for timeout
					 (FARPROC) TDeaCMM::TimerCallBack);
  TMachine::Start(hInstance);
}

/************************************************************************/
/* DEVICE DRIVER METHODS                                                */
/*                                                                      */
/************************************************************************/

#include <stdlib.h>   // atoi()

/************************************************************************/
/* FUNCTION   : RegCallBack                                             */
/* Purpose    : Register a status call back routine                     */
/************************************************************************/
// returns 0 if unsuccessful
BOOL TDeaCMM::RegCallBack(STATUSPROC ArgCallBack)
{
  if (NOT lpfnStatusCB)
  {
	 lpfnStatusCB = ArgCallBack;
	 return TRUE;
  }
  return FALSE;
}

/************************************************************************/
/* FUNCTION   : InputCommands                                           */
/* Purpose    : Read in Robot Command information                       */
/************************************************************************/
BOOL TDeaCMM::InputCommands(char * CmdFileName)
{
  char linestr[MAXLINELENGTH];
  UINT rowcount = 0;
  UINT numrows = 0;
  ifstream  CmdFile; // Command file input stream
  NumCmds = 0;
  CmdFile.open(CmdFileName);
  if (CmdFile.fail()) return FALSE;
  CmdFile.getline(linestr, MAXLINELENGTH, LINE_TERMNTR); // Rows
  numrows = atoi(linestr);
  CmdFile.getline(linestr, MAXLINELENGTH, LINE_TERMNTR); // Columns
  CmdFile.getline(linestr, MAXLINELENGTH, LINE_TERMNTR); // Headings
  CmdFile.getline(linestr, MAXLINELENGTH, LINE_TERMNTR); // Format Code
  // Check format is readable by the current driver
  if (atoi(linestr) NOTEQUAL -1) // !! CHANGE TO
  // if (FormatCode < MinCode OR FormatCode > MaxCode)
  {
	 char tempStr[81];
	 wsprintf(tempStr, "ERROR: Command File \'%s\' has invalid format", CmdFileName);
	 MessageBox(NULL, tempStr, MachineName, MB_OK | MB_APPLMODAL | MB_ICONSTOP);
	 return FALSE;
  }
  INC(rowcount);
  while ((rowcount < numrows) AND (NOT CmdFile.eof())	AND (NumCmds < MAX_NUM_COMMANDS))
  {
	 CmdFile >> CommandList[NumCmds++];
	 rowcount += 3;
  }
  return TRUE;
}


/************************************************************************/
/* FUNCTION   : CheckStatus                                             */
/* Purpose    : Called whenever a check of the device's state is        */
/*              required                                                */
/************************************************************************/
BOOL TDeaCMM::CheckStatus(void)
{
	static int count=0;
  // IF state has changed
  if(CurrCommand!=PrevCommand || CurrCmdState != PrevCmdState)
  {
	 PrevCmdState = CurrCmdState;
	 UpdateState();
	 PrevCommand    = CurrCommand; //1
	 return TRUE;
  }
  if(CurrState==MS_BUSY) // if we're busy...
  {
		if(!hRS232) // if the RS232 channel is not open, open it
			hRS232 = DeaCMMLink.OpenChannel(MachineName, "dmtrs232.dll",
														RS232.PortStr,
														RS232.SettingsStr,
														RS232.FlagsStr,
														RS232.InBufferSize,
														RS232.OutBufferSize);
		count++;
		if(count>=PollingCount)
		{
			count=0;
			if(CheckForIdle(hRS232)) // ... check for idle signal on the RS232
			{
				GoIdle();
			}
		}
  }
  return FALSE;
}

void  TDeaCMM::GoIdle()
{
	if(hRS232 & !KeepChannelOpen)
	{
		SendInstrucn(hRS232, "O");
		DeaCMMLink.CloseChannel(hRS232); // close the RS232 channel
		hRS232=0; // reset the channel to 0
	}
	CurrState=MS_IDLE;
	CurrCommand=NoCmd;
	CurrCmdState=CS_Ready;
	CheckStatus(); //adjust status
	UpdateState();
	UpdateData(); // send message back to client
}

/************************************************************************/
/* FUNCTION   : CheckForIdle                                            */
/* Purpose    : Reads RS232 to check for Idle signal                    */
/************************************************************************/
BOOL TDeaCMM::CheckForIdle(WORD hRS232)
{
	BOOL res=FALSE;
	char argstring[255];
	if (hRS232)
	{
		if(ReceiveInstrucn(hRS232, argstring, 1))
		{
			if (strlen (ReplyString) == 0)   // if we're just looking for any old character coming in
				res=TRUE;
			else                             // otherwise try to match the string with the INI file entry
			{
			  strcat (ReceiveString, argstring);
			  if (strcmpi (ReceiveString, ReplyString) == 0)
				 res=TRUE;
			}
			if (FlushInputAfterChecking)
			  DeaCMMLink.FlushInput(hRS232);
		}
	}
	else
	{
		CmdError.Set(3, "Cannot open read RS232 link");
		res=FALSE;
	}
	return res;
}

/************************************************************************/
/* FUNCTION   : UpdateState                                             */
/* Purpose    : Updates device status information                       */
/************************************************************************/
void TDeaCMM::UpdateState(void)
{
	if (CmdError.Num NOTEQUAL 0) // if there was an error...
	{
		CurrState = MS_ERROR; // ...State is error, finish
		NotifyStatusChange();
		return;
	}

	// IF the current command has been completed...
	if (CurrCommand == NoCmd)
	{
		CurrCmdState = CS_Ready; // ...State is ready
		CurrState = MS_IDLE;
	}
	else
		CurrState = MS_BUSY;

	NotifyStatusChange();
}

/************************************************************************/
/* FUNCTION   : NotifyStatusChange                                      */
/* Purpose    : Notifies User Interface of any change in device's state */
/************************************************************************/
void TDeaCMM::NotifyStatusChange(void)
{
  switch (CurrState)
  {
	 case MS_BUSY:
		lstrcpy(MachineStatusStr, "BUSY");
		if (CmdRequestStr[0])
		{
		  lstrcat(MachineStatusStr," ");
		  lstrcat(MachineStatusStr, CmdRequestStr );
		}
	 break;
	 case MS_IDLE:
		lstrcpy(MachineStatusStr, "IDLE");
		if (CmdRequestStr[0])
		{
		  lstrcat(MachineStatusStr," ");
		  lstrcat(MachineStatusStr, CmdRequestStr );
		}
	 break;
	 case MS_ERROR:
		wsprintf(MachineStatusStr,"ERROR %s", CmdError.CauseStr );
	 break;
	 case MS_MANUALCTRL:
		lstrcpy(MachineStatusStr,"LOCAL CONTROL ONLY");
	 break;
  }

  if (CurrState NOTEQUAL PrevState)
  {
	 UpdateData(); // send message back to client
	 HistFile.Append(MachineStatusStr);
  }
  if (lpfnStatusCB)
	 (*lpfnStatusCB)(StatusChange, CurrState, 0, 0, MachineStatusStr, CmdRequestStr);
}


#include "\devel\dongle\dongle.h"
extern char Message[256]; // defined in codeu17. Its used for displaying the message to the user
/************************************************************************/
/* FUNCTION   : DoCommand                                               */
/* Purpose    : Requests the device object to implement command         */
/************************************************************************/
// RETURNS TRUE if command request was granted
BOOL TDeaCMM::DoCommand(WORD cmdnum, char * argstring)
{
	BOOL result = FALSE;
	if(CurrCmdState NOTEQUAL CS_Ready)
		return FALSE;

	BOOL dg = FALSE;
	DONGLECHECK(littlepig, _DeviceDrivers_Offset, _Lathe_Bit, dg);
	if(NOT dg)
		return FALSE;

	char Telegram[256], temp[300];
	strstream s;
	s << argstring;

	switch(cmdnum)
	{
	case 1: // write
		s.getline(Telegram, 255);
		CurrCmdState = CS_Activating;
		CurrCommand = DeaCMMCmdsEnum(cmdnum);
		CheckStatus(); 					// send device driver busy
		if(WriteToDeaCMM(Telegram)) 	// do dialogue with CMM
			result = TRUE;
		else
			CurrCommand = NoCmd;
		break;
	default:
		CmdError.Set(2, "Unrecognised command"); CurrCommand = NoCmd;
	}
	return result;
}

/************************************************************************/
/* FUNCTION   : WriteToDeaCMM                                          */
/* Purpose    : Sets up an RS232 connection to the CodeTag              */
/************************************************************************/
BOOL TDeaCMM::WriteToDeaCMM(char* argstring)
{
	BOOL res=TRUE; // assume everything will go swimingly...
//	WORD hRS232 = FALSE;
	if(!hRS232)
		hRS232 = DeaCMMLink.OpenChannel(MachineName, "dmtrs232.dll",
														RS232.PortStr,
														RS232.SettingsStr,
														RS232.FlagsStr,
														RS232.InBufferSize,
														RS232.OutBufferSize);
	if (hRS232)
	{
		DeaCMMLink.FlushInput(hRS232);
		strset (ReceiveString, '/0');
		DeaCMMLink.FlushOutput(hRS232);
		if(!SendInstrucn(hRS232, argstring)) // SEND argument
		{
			CmdError.Set(4, "Cannot send argument");
			res=FALSE;
		}
		if (!KeepChannelOpen)
		{
		  DeaCMMLink.CloseChannel(hRS232);
		  hRS232 = 0;
		}
	}
	else
	{
		CmdError.Set(3, "Cannot open write RS232 link");
		res=FALSE;
	}
	return res;
}

/************************************************************************/
/* FUNCTION   : SendInstrucn                                            */
/* Purpose    : Sends a string to RS232 channel                         */
/************************************************************************/
BOOL TDeaCMM::SendInstrucn(WORD hRS232, char FAR * argstring) // Instruction string to send
{
  WORD numchsent;
  MSG msg;

  numchsent = DeaCMMLink.Write(hRS232, argstring, 4); // send it out

  DWORD t, tout, ticks=GetTickCount();
  tout=ticks+2000L; // time out is 2 seconds
  while((t=GetTickCount())<tout && DeaCMMLink.OutQSize(hRS232) != 0)
  {
	 if(PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) // if there is a message
	 {
		TranslateMessage(&msg); // send it on its way
		DispatchMessage(&msg);
	 }
  }
  if(t>=tout)
  {
	 MessageBox(NULL, "Write Timeout", "RS232", MB_OK | MB_TASKMODAL);
	 return FALSE;
  }
  return TRUE;
}

/************************************************************************/
/* FUNCTION   : ReceiveInstrucn                                         */
/* Purpose    : Receives a string from RS232 channel                    */
/************************************************************************/
BOOL TDeaCMM::ReceiveInstrucn(WORD hRS232, char FAR * argstring, int expected)
{
	char c;
	int bufferlen=0;
	argstring[0] = '\0'; // empty the buffer
	if (FlushInputBetweenChecks)
	  DeaCMMLink.FlushInput(hRS232);
	while(bufferlen<expected)
	{
		if(!Listen(hRS232))
			return FALSE;
		else
		{
			DeaCMMLink.Read(hRS232, &c, 1); // read one character
			argstring[bufferlen++]=c; // append
		}
	}
	return TRUE;
}

BOOL TDeaCMM::Listen(WORD hRS232)
{
  MSG msg;
  DWORD t, tout, ticks=GetTickCount();
  tout = ticks + ReceiveTimeout; // time out is 2 seconds
  while((t=GetTickCount())<tout && DeaCMMLink.InQSize(hRS232)==0)
  {
	 if(PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) // if there is a message
	 {
		TranslateMessage(&msg); // send it on its way
		DispatchMessage(&msg);
	 }
  }
  if(t>=tout)
	 return FALSE;
  return TRUE;
}

/************************************************************************/
/* FUNCTION   : TimerCallBack                                           */
/* Purpose    : Windows calls this method whenever a timer timeout event*/
/*              occurs                                                  */
/************************************************************************/
void FAR PASCAL TDeaCMM::TimerCallBack(
  HWND hwnd,	  //* handle of window for timer messages
  UINT msg,	    //* WM_TIMER message
  UINT idTimer,	//* timer identifier
  DWORD dwTime)	//* current system time
{
  PDeaCMMThis->CheckStatus();
}



