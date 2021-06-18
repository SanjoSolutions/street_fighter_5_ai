#include <AutoItConstants.au3>
#include <Timers.au3>

Func time()
   Return @YEAR & '-' & @MON & '-' & @MDAY & ' ' & @HOUR & ':' & @MIN & ':' & @SEC & ':' & @MSEC
EndFunc

WinActivate('StreetFighterV')
Sleep(1000)
Send('{LWINDOWN}{G down}{G up}{LWINUP}')
Sleep(1000)
ConsoleWrite(time() & @CRLF)
MouseClick($MOUSE_CLICK_LEFT, 261, 139, 1, 0)
ConsoleWrite(time() & @CRLF)
