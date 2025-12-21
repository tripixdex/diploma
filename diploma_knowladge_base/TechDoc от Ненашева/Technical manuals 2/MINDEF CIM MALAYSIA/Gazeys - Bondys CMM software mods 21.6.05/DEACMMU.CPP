/************************************************************************/
/*  FILENAME: DEACMMU.CPP                                               */
/*  FUNCTION: DeaCMM device driver                                        */
/*  USAGE   : Run from windows                                          */
/*  Version : 2-20                                                      */
/*  Author  : Steve Owen, Denford Machine Tools, Brighouse.           */
/*  Date    : 24 June 1992                                              */
/*  Language: Turbo   C++ 3.0                                           */
/************************************************************************/
/*      Maintenance Log                                                 */
/*      ---------------                                                 */
/*                                                                      */
/*  Date            Action                                              */
/*  ----            ------                                              */
/*                                                                      */
/*   1 Sep  1993    Created version 1-00 // Roger Bovill                */
/*   1 Mar  1996    Created version 2-00 // Steve Owen                  */
/*                                                                      */
/*                                                                      */
/************************************************************************/
/************************************************************************/
#include <windows.h>
#include <ctl3d.h>
#include <stdlib.h>	// atoi
#include "\devel\winclass\tdlg12.h"
#include "\devel\include\macros.h"
#include "\devel\custcont\bmpct\bmpct12.h"
#include "\devel\devdriv\dea\ids.h"
#include "\devel\help\cellhelp.h"
#include "\devel\devdriv\dea\deacmm.h"

HINSTANCE InstanceHdl ;
inline HINSTANCE GetHInstance()
{
	return InstanceHdl;
}

BOOL CALLBACK WriteDlgProc(HWND hwndDlg, UINT msg, WPARAM wParam, LPARAM lParam);

TDeaCMM DeaCMM;
char Message[256];

char * IniFileName  = ".\\DEACMM.INI";
//char * IniFileName  = "c:\\cim\\other\\DEACMM.INI";

class  TDeviceDialog: public TDialog
{
private:
  TBmpControl* pMachineBCtl;
  HBITMAP hMachineBmp;
  STATUSPROC lpfnStatusCB;   // Pointer to call back routine
  BOOL  PASCAL  MessageProc(HWND, UINT, WPARAM, LPARAM);
public:
  static  WORD FAR PASCAL _export StatusCallBack(WORD, WORD, WORD, WORD, char FAR *, char FAR *);
  void UpdateUIF(WORD, WORD, WORD, WORD, char FAR *, char FAR *);
  char   CmdStr[81];
  TDeviceDialog();
  virtual ~TDeviceDialog();
  virtual void PASCAL SetupWindow();
  void PASCAL GetWindowClass(WNDCLASS& AWndClass);
  LPSTR PASCAL GetClassName();
  void ActivateCommand(void);
};

TDeviceDialog* pDeviceDialogthis=NULL;

BOOL PASCAL TDeviceDialog::MessageProc(HWND hwnd, UINT msg, WPARAM wparam, LPARAM lparam)
{
  switch(msg)
  {
	 case WM_COMMAND:
		switch (wparam)
		{
		  case CM_RESET:
			 DeaCMM.Reset();
		  return 0;
		  case CM_DISCONNECT:
			 DeaCMM.Disconnect();
		  return 0;
		  case ID_ACTIVATE:
			 ActivateCommand();
		  return 0;
		  case CM_EXIT:
			 SendMessage(hwnd, WM_CLOSE, 0, 0);
		  return 0;
		  case CM_CONTENTS_HLP:
        		DeaCMM.GoIdle();
		  //			 WinHelp(hwnd, HelpFileNameStr, HELP_CONTEXT, Contents); // This identifier is defined in cell.hh
		  return 0;
		  case CM_CONTROLS_HLP:
			 WinHelp(hwnd, HelpFileNameStr, HELP_CONTEXT, Device_Driver_Controls); // This identifier is defined in cell.hh
		  return 0;
		  case CM_ARCHITECTURE_HLP:
			 WinHelp(hwnd, HelpFileNameStr, HELP_CONTEXT, Cell_Architecture_Overview); // This identifier is defined in cell.hh
		  return 0;
		}
	 break;
	 case WM_DESTROY:
		WinHelp(hwnd, HelpFileNameStr, HELP_QUIT, 0L);
	 break;
  };
  return FALSE;
}


/************************************************************************/
/* FUNCTION   : GetWindowClass                                          */
/* Purpose    : Initialises the window class                            */
/************************************************************************/
// Return window "class" information
void PASCAL TDeviceDialog::GetWindowClass(WNDCLASS& AWndClass)
{
  TDialog::GetWindowClass(AWndClass);
  if (GetPrivateProfileInt ("MAIN", "NO CLOSE", 0, IniFileName) == 1)
	 AWndClass.style |= CS_NOCLOSE;
  AWndClass.hIcon = LoadIcon(GetHInstance(), MAKEINTRESOURCE(ID_ICON));
}

// Return window "class" name
LPSTR PASCAL TDeviceDialog::GetClassName()
{
  return "DeaCMM";//Dialog resource Class Name;
}

void TDeviceDialog::ActivateCommand(void)
{
  DWORD CommdNum = SendDlgItemMessage(HWindow, IDC_COMBOBOX, CB_GETCURSEL, 0, 0L);
  if(CommdNum>=0 && CommdNum<DeaCMM.GetNumCmds())
  {
	 DLGPROC dlgprc;
	 switch(CommdNum)
	 {
		case 0: // writing
			dlgprc = (DLGPROC) MakeProcInstance((FARPROC)WriteDlgProc, GetHInstance());
			if(DialogBox(GetHInstance(), MAKEINTRESOURCE(2), HWindow, dlgprc)!=IDOK)
			{
				FreeProcInstance((FARPROC) dlgprc);
				return;
			}
			FreeProcInstance((FARPROC) dlgprc);
			break;
	 }
	 BOOL res=DeaCMM.DoCommand(CommdNum+1, Message);
  }
}


/************************************************************************/
/* FUNCTION   : StatusCallBack                                          */
/* Purpose    : The DeaCMMs device driver invokes this method whenever */
/*              a change in the DeaCMM's status occurs                 */
/************************************************************************/
// returns 1 if already invoked
//         0 if call back was successful
WORD FAR PASCAL TDeviceDialog::StatusCallBack(
  WORD updateType,     // Type of update
  WORD unsigned1Arg,    // unsigned parameter 1
  WORD unsigned2Arg,    // unsigned parameter 2
  WORD unsigned3Arg,    // unsigned parameter 3
  char FAR * arg1Str,  // 1st string parameter
  char FAR * arg2Str)  // 2nd string parameter
{
  static BYTE syssem = 0;  // System semaphore
  // If status callback already invoked, return immediately
  if (syssem)
	 return 0;
  (syssem++);       // Set system semaphore
  pDeviceDialogthis->UpdateUIF(
	 updateType,     // Type of update
	 unsigned1Arg,    // unsigned parameter 1
	 unsigned2Arg,    // unsigned parameter 2
	 unsigned3Arg,    // unsigned parameter 3
	 arg1Str,        // 1st string parameter
	 arg2Str);       // 2nd string parameter
  syssem--;         // Reset system semaphore
  return 1;
}


/************************************************************************/
/* FUNCTION   : UpdateUIF                                               */
/* Purpose    : The routine updates the user inteface according         */
/*              to what has been received in the callback routine       */
/************************************************************************/
void TDeviceDialog::UpdateUIF(
  WORD updateType,     // Type of update
  WORD unsigned1Arg,    // 1st unsigned parameter
  WORD unsigned2Arg,    // 2nd unsigned parameter
  WORD unsigned3Arg,    // 3rd unsigned parameter
  char * arg1Str,      // 1st string parameter
  char * arg2Str)      // 2nd string parameter
{
  char MStatusStr[80];
  switch (UpdateTypeEnum(updateType))
  {
	 case StatusChange:
	 {
		EnableWindow(GetDlgItem(HWindow, ID_ACTIVATE), MachineStateEnum(unsigned1Arg) ISEQUAL MS_IDLE);
		EnableWindow(GetDlgItem(HWindow, IDC_COMBOBOX), MachineStateEnum(unsigned1Arg) ISEQUAL MS_IDLE);
		SetDlgItemText(HWindow, ID_STATUS_TEXT, arg1Str);
		SetDlgItemText(HWindow, IDC_COMBOBOX, arg2Str);
	 }
	 break;
  }
}

// TDeviceDialog
// Construct a TDeviceDialog object
TDeviceDialog::TDeviceDialog() : TDialog()
{
  WNDCLASS wndclass;
  pDeviceDialogthis = this;
  hMachineBmp = LoadBitmap(GetHInstance(), MAKEINTRESOURCE(MACHINE_BMP));
  pMachineBCtl = new TBmpControl(NULL, MACHINE_BMP_CTR, hMachineBmp);
  pMachineBCtl->Register(wndclass);
}


#include "\devel\dongle\dongle.h"

// Perform TDeviceDialog initializations requiring window handle
void PASCAL TDeviceDialog::SetupWindow()
{
  TDialog::SetupWindow();
  // Because the Bitmap controls are 'AUTO-CREATED' Need to associate
  // the window handle of each to an object. Use GetDlgItem to get the
  // control's window handle
  pMachineBCtl->AssignThisPtr(GetDlgItem(HWindow, MACHINE_BMP_CTR));
  // Set up Status Callback
  lpfnStatusCB = (STATUSPROC) TDeviceDialog::StatusCallBack;
  if (DeaCMM.Initialise(IniFileName))
  {
	 DeaCMM.RegCallBack(lpfnStatusCB);
	 char Temp[MAX_TEXT_SIZE];
	 DeaCMM.GetMachineName(Temp, sizeof(Temp));
	 SetWindowText(HWindow, Temp);
	 int  NumCmds = DeaCMM.GetNumCmds();
	 for (int ix = 0; ix < NumCmds; ix++)
	 {
		  DeaCMM.GetCmdDescription(ix, Temp, sizeof(Temp));
		  SendDlgItemMessage(HWindow, IDC_COMBOBOX, CB_INSERTSTRING,
							  WPARAM(DeaCMM.GetCmdId(ix)-1), LPARAM(Temp));
	 }
	 DeaCMM.Start(GetHInstance());
  }
  else
	 PostQuitMessage(-1);
  BOOL res = FALSE;
  DONGLECHECK(littlepig, _CIM_Offset, _CIM_Bit, res);
  if (NOT res)
	 PostQuitMessage(-3);
}

TDeviceDialog::~TDeviceDialog()
{
	if (pMachineBCtl)
		delete pMachineBCtl;
	if (hMachineBmp)
		DeleteObject(hMachineBmp);
}
/////////////////////////////////////////////////////////////


BOOL CALLBACK WriteDlgProc(HWND hwndDlg, UINT msg, WPARAM wParam, LPARAM lParam)
{
	char tmp[5];
	switch(msg)
	{
		case WM_INITDIALOG:
			return TRUE;
		case WM_COMMAND:
			if(wParam==IDOK)
			{
				GetDlgItemText(hwndDlg, 102, Message, sizeof(Message));
				EndDialog(hwndDlg, IDOK);
			}
			if(wParam==IDCANCEL)
				EndDialog(hwndDlg, IDCANCEL);
	};
	return FALSE;
}

int PASCAL WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmd, int nCmdShow)
{
Initialise:
  InstanceHdl = hInstance;
  WNDCLASS wndclass;
  MSG msg;
  HWND hDlg = NULL;
#ifdef CTL3D_SUBCLASS
  Ctl3dRegister(hInstance);
  Ctl3dAutoSubclass(hInstance);
#endif
  TDeviceDialog UserIface;
ProgramBody:
  if (hPrevInstance)
  {
	 MessageBox(NULL, "Already running", "Driver", MB_OK | MB_APPLMODAL | MB_ICONSTOP);
	 goto Terminate;
  }
  else
  {
	 if (NOT UserIface.Register(wndclass))
		goto Terminate;
  }
  hDlg = UserIface.Create(InstanceHdl,	MAKEINTRESOURCE(ID_DIALOG), NULL);
  if (NOT hDlg)
	 goto Terminate;

  UserIface.Show(nCmdShow);
  UserIface.Update();

  while (GetMessage (&msg, NULL, 0, 0))
  {
	 if (NOT IsDialogMessage(hDlg, &msg))
	 {
		TranslateMessage(&msg);
		DispatchMessage(&msg);
	 }
  }
Terminate:
#ifdef CTL3D_SUBCLASS
  Ctl3dUnregister(hInstance);
#endif
}

