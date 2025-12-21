/************************************************************************/
/*  FILENAME: CodeTag17.CPP                                                 */
/*  FUNCTION: CodeTag driver                                                */
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
TCodeTag* PCodeTagThis=NULL; // Static pointer to the TCodeTag object instance
WORD hRS232=0;

/************************************************************************/
/* DEVICE DRIVER INITIALISATION FUNCTIONS                               */
/*                                                                      */
/************************************************************************/

// Construct a TCodeTag object
/************************************************************************/
/* CONSTRUCTOR: TCodeTag                                                 */
/* Purpose    : Creates an instance of a CodeTag device driver object    */
/************************************************************************/
TCodeTag::TCodeTag() : TMachine()
{

}

/************************************************************************/
/* CONSTRUCTOR: Initialise                                              */
/* Purpose    : Must be called before any of TCodeTags methods are used  */
/************************************************************************/
BOOL TCodeTag::Initialise(char * IniFileName)
{
  IsInitialised = IOPort.Initialise(MachineName, IniFileName) AND TMachine::Initialise(IniFileName);
  ReadIniFile(IniFileName);
  lpfnStatusCB = NULL;
  PCodeTagThis = this;

  if (NOT InputCommands(CommandFileName))
  {
	 char Message[80];
	 lstrcpy(Message, "Fatal error: Could not input\ncommands from file 'codetag.cmd'");
	 MessageBox(NULL, Message, MachineName, MB_OK | MB_TASKMODAL);
	 IsInitialised = FALSE;
  }
  CodeTagLink.Load("dmtcomms.dll");
  if (NOT CodeTagLink.IsLoaded())
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
/* DESTRUCTOR : TCodeTag                                                 */
/* Purpose    : terminates a TCodeTag instance                           */
/************************************************************************/
TCodeTag::~TCodeTag()
{

}

//const INVALIDBIT = 255;
BOOL TCodeTag::ReadIniFile(char * IniFileName)
{
  BOOL res;
  res = TMachine::ReadIniFile(IniFileName);
  RS232.ReadIniFile(IniFileName);
  GetPrivateProfileString("FILES", "Commands File", "", CommandFileName, MAX_FILE_NAME, IniFileName);
  SamplgInterval = GetPrivateProfileInt("TIMER" ,"Sampling Interval" ,1000 , IniFileName);
  return res;
}

/************************************************************************/
/* FUNCTION   : Reset                                                   */
/* Purpose    : Reset the device driver                                 */
/************************************************************************/
void TCodeTag::Reset()
{
	if(hRS232)
	{
		CodeTagLink.CloseChannel(hRS232);
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
void TCodeTag::Start(HINSTANCE hInstance)   // Application instance
{
  if (NOT IsInitialised)
	 return;
  Reset();
  Timer.Register(hInstance, SamplgInterval, // Set Timer for timeout
					 (FARPROC) TCodeTag::TimerCallBack);
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
BOOL TCodeTag::RegCallBack(STATUSPROC ArgCallBack)
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
BOOL TCodeTag::InputCommands(char * CmdFileName)
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
BOOL TCodeTag::CheckStatus(void)
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
			hRS232 = CodeTagLink.OpenChannel(MachineName, "dmtrs232.dll",
														RS232.PortStr,
														RS232.SettingsStr,
														RS232.FlagsStr,
														RS232.InBufferSize,
														RS232.OutBufferSize);
		count++;
		if(count==5)
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

void  TCodeTag::GoIdle()
{
	if(hRS232)
	{
		CodeTagLink.FlushInput(hRS232);
		CodeTagLink.FlushOutput(hRS232);
		//SendInstrucn(hRS232, "O");
		CodeTagLink.CloseChannel(hRS232); // close the RS232 channel
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
BOOL TCodeTag::CheckForIdle(WORD hRS232)
{
	BOOL res=FALSE;
	char argstring[5];
	char InStr[10];
	char *buf1 = "idle" ;
	char *buf2 = "IDLE" ;
	BOOL Start=FALSE;
	int Count=0;
	if (hRS232)
	{
		if(ReceiveInstrucn(hRS232, argstring, 4))
		{
			/*for (int i = 0; i<10; i++)
			{
			  if((InStr[i]==buf1[Count])||(InStr[i]==buf2[Count]))
				 Start=TRUE;
			  else
			  {
				  Count = 0;
				  Start=FALSE;
			  }
			  if (Start)
				  argstring[Count++]=InStr[i];
			  if (Count==4)
				  break;
			} */
			argstring[4]='\0';
			res=(strcmpi(argstring, buf1)==0);
			//MessageBox(0, argstring, 0, 0);
		}
		CodeTagLink.FlushInput(hRS232);
		CodeTagLink.FlushOutput(hRS232);
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
void TCodeTag::UpdateState(void)
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
void TCodeTag::NotifyStatusChange(void)
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
BOOL TCodeTag::DoCommand(WORD cmdnum, char * argstring)
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
		CurrCommand = CodeTagCmdsEnum(cmdnum);
		CheckStatus(); // send device driver busy
		if(WriteToCodeTag(Telegram)) // do dialogue with code tag
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
/* FUNCTION   : WriteToCodeTag                                          */
/* Purpose    : Sets up an RS232 connection to the CodeTag              */
/************************************************************************/
BOOL TCodeTag::WriteToCodeTag(char* argstring)
{
	BOOL res=TRUE; // assume everything will go swimingly...
	//WORD hRS232 = FALSE;
	if (!hRS232)
	{
	hRS232 = CodeTagLink.OpenChannel(MachineName, "dmtrs232.dll",
														RS232.PortStr,
														RS232.SettingsStr,
														RS232.FlagsStr,
														RS232.InBufferSize,
														RS232.OutBufferSize);
	}
	if (hRS232)
	{
		CodeTagLink.FlushInput(hRS232);
		CodeTagLink.FlushOutput(hRS232);
		if(!SendInstrucn(hRS232, argstring)) // SEND argument
		{
			CmdError.Set(4, "Cannot send argument");
			res=FALSE;
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
BOOL TCodeTag::SendInstrucn(WORD hRS232, char FAR * argstring) // Instruction string to send
{
  WORD numchsent;
  MSG msg;

  numchsent = CodeTagLink.Write(hRS232, argstring, 2); // send it out

  DWORD t, tout, ticks=GetTickCount();
  tout=ticks+2000L; // time out is 2 seconds
  while(((t=GetTickCount())<tout) && (CodeTagLink.OutQSize(hRS232) != 0))
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
BOOL TCodeTag::ReceiveInstrucn(WORD hRS232, char FAR * argstring, int expected)
{
	char c= '\0';
	int bufferlen=0;
	argstring[0] = '\0'; // empty the buffer
	CodeTagLink.FlushInput(hRS232);
	CodeTagLink.FlushOutput(hRS232);
	while(bufferlen<expected)
	{
		if(!Listen(hRS232))
			return FALSE;
		else
		{
			CodeTagLink.Read(hRS232, &c, 1); // read one character
			argstring[bufferlen++]=c; // append
		}
	}
	//MessageBox(0, argstring, 0, 0);
	return TRUE;
}

BOOL TCodeTag::Listen(WORD hRS232)
{
  MSG msg;
  DWORD t, tout, ticks=GetTickCount();
  tout=ticks+2000L; // time out is 2 seconds
  while(((t=GetTickCount())<tout) && (CodeTagLink.InQSize(hRS232))==0)
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
void FAR PASCAL TCodeTag::TimerCallBack(
  HWND hwnd,	  //* handle of window for timer messages
  UINT msg,	    //* WM_TIMER message
  UINT idTimer,	//* timer identifier
  DWORD dwTime)	//* current system time
{
  PCodeTagThis->CheckStatus();
}



