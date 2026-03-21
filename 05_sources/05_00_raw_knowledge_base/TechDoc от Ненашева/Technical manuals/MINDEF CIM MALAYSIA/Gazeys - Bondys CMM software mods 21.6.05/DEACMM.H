/************************************************************************/
/*  FILENAME: DeaCMM.H                                                   */
/*  FUNCTION: Prototype DeaCMM machine driver                              */
/*  USAGE   : Run from windows                                          */
/*  Version : 1-00                                                      */
/*  Author  : Roger Bovill, Denford Machine Tools, Brighouse.           */
/*  Date    :  7 May  1993                                              */
/* Language : Turbo   C++ 3.1                                           */
/************************************************************************/
/*      Maintenance Log                                                 */
/*      ---------------                                                 */
/*                                                                      */
/*  Date            Action                                              */
/*  ----            ------                                              */
/*                                                                      */
/*  23 Aug  1993    Created version 1-00                                */
/*                                                                      */
/************************************************************************/
/************************************************************************/


#ifndef DeaCMM_H
#define DeaCMM_H

#include <windows.h>
#include "\devel\include\macros.h"
#include "\devel\comms\comms30.h"
#include "\devel\classes\timer\timer10.h"
#include "\devel\devdriv\machine\mach24.h"
#include "\devel\devdriv\machine\ilkobj.h"
#include "\devel\devdriv\machine\machio.h"
#include "\devel\devdriv\machine\cparam10.h"
#include "\devel\mcommand\mcommd20.h"

const MAX_NUM_COMMANDS = 3;

enum DeaCMMCmdsEnum {
  NoCmd = 0,
  WriteCmd  = 1,
  ReadCmd  = 2,
  VerifyCmd  = 3,
  Cmd4  = 4,
  Cmd5  = 5,
  Cmd6  = 6,
};

typedef void (FAR PASCAL * STATUSPROC)(WORD, WORD, WORD, WORD, char FAR *, char FAR *);

class TDeaCMM : public TMachine
{
private:
  void NotifyStatusChange(void);
  TIMERPROC lpfnTimerCallBack; // Pointer to a timer call back routine
  char CommandFileName[MAX_FILE_NAME]; // Name of commands file
  STATUSPROC lpfnStatusCB;  // Pointer to status call back routine
  TCommsDLL  DeaCMMLink; // RS232 link to DEACMM
  MachineCmd CommandList[MAX_NUM_COMMANDS]; //  Command List
  UINT SamplgInterval;  // Time between checking machine status
  TTimer Timer;         // Timer process
  CommsStruc  RS232;
  char RequestStr[MAX_LINE_LENGTH];
  BOOL FlushInputBetweenChecks;
  BOOL FlushInputAfterChecking;
  BOOL KeepChannelOpen;
  int PollingCount;
  char ReplyString[MAX_FILE_NAME];
  char ReceiveString[255];
  int ReceiveTimeout;
public:
  TDeaCMM();
  TDeaCMM(char *);
  virtual ~TDeaCMM();

  BOOL Initialise(char *);
  BOOL ReadIniFile(char*);
  void Reset();
  void Start(HINSTANCE);

  BOOL RegCallBack(STATUSPROC ArgCallBack);

  BOOL InputCommands(char * CmdFileName);
  int  GetNumCmds() { return NumCmds; };
  void GetCmdDescription(int ix, char * Temp, int TempLen)
  {
		lstrcpyn(Temp, CommandList[ix].Description(), TempLen);
  };
  WORD GetCmdId(int ix)
  {
	 return CommandList[ix].Id();
  }

  void UpdateState(void);
  BOOL CheckStatus(void);
  BOOL DoCommand(
	 WORD cmdnum,      // Command to be implemented
	 char* argstring);  // Command Argument

  BOOL CheckForIdle(WORD hRS232);
  void GoIdle();
  BOOL WriteToDeaCMM(char* argstring);
  BOOL SendInstrucn(WORD, char FAR *);
  BOOL ReceiveInstrucn(WORD, char FAR *, int);
  BOOL Listen(WORD hRS232);

  static  void FAR PASCAL _export  CALLBACK TimerCallBack(
	 HWND hwnd,	  //* handle of window for timer messages
	 UINT msg,	    //* WM_TIMER message
	 UINT idTimer,	//* timer identifier
	 DWORD dwTime);//* current system time

};

#endif