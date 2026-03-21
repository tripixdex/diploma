'Main Task for Boldman / Denford Linear Slide
'Date 19th October 2003
'Utilising Berger Lahr TLD132F Servodrive
'SER 3913 4L 5S Servomotor
'2003 Version using MC202 + CAN I/O module

RUN "CONFIG"
WA(1000)

GOSUB init

loop:

IF IN(local) THEN
'Local Operation
  OP(ready,0)
  OP(io_in_order,0)
  OP(busy,0)
  OP(ref,0)

  IF home_done = 0 THEN
    WHILE IN(function) = 0
      OP(19,1)
      WA(100)
      OP(19,0)
      WA(100)
    WEND
    GOSUB home_routine
  ENDIF

  IF IN(jog) THEN
    IF IN(shift) THEN
      REVERSE
    ELSE
      FORWARD
    ENDIF
  ENDIF
  WHILE IN(jog)
    SPEED = (((IN AND sp_1) / sp_2) * 540)
    IF SPEED < 20 THEN SPEED = 100
  WEND
  CANCEL

  IF IN(position) AND IN(shift) THEN
    tws = ((IN AND l_pos_1) / l_pos_2)
    IF tws = 0 THEN
      VR(tws) = 0
    ELSE
      VR(tws) = MPOS
    ENDIF
    VR(tws + 10) = (((IN AND sp_1) / sp_2) * 540)
    IF VR(tws + 10) < 300 THEN VR(tws + 10) = 540
    FLASHVR(tws)
    FLASHVR(tws + 10)
  ENDIF

  IF IN(position) AND IN(shift)=0 THEN
    tws = ((IN AND l_pos_1) / l_pos_2)
    SPEED = VR(tws + 10)
    IF SPEED > 20 THEN
      MOVEABS(VR(tws))
      WAIT IDLE
    ENDIF
  ENDIF

  IF IN(function) THEN
    IF IN(shift) THEN
      GOSUB sequence
    ELSE
      GOSUB home_routine
    ENDIF
  ENDIF

ELSE
'Remote Operation
  OP(ready,1)
  OP(io_in_order,1)
  OP(busy,0)

  IF home_done THEN OP(ref,1)

  IF IN(pos) THEN
    tws_1 = 0
    IF IN(bit_1) THEN tws_1 = tws_1 + 1
    IF IN(bit_2) THEN tws_1 = tws_1 + 2
    IF IN(bit_4) THEN tws_1 = tws_1 + 4
    WA(200)
    tws = 0
    IF IN(bit_1) THEN tws = tws + 1
    IF IN(bit_2) THEN tws = tws + 2
    IF IN(bit_4) THEN tws = tws + 4

    IF tws_1 = tws THEN
      IF tws = 0 THEN
        OP(busy,1)
        OP(ready,0)
        OP(io_in_order,0)
        GOSUB home_routine
        OP(ref,1)
      ELSE
        IF home_done THEN
          SPEED = VR(tws + 10)
          IF SPEED > 20 THEN
            MOVEABS(VR(tws))
            OP(busy,1)
            OP(ready,0)
            OP(io_in_order,0)
            WAIT IDLE
          ENDIF
        ENDIF
      ENDIF
    ENDIF
  ENDIF


ENDIF


GOTO loop


sequence:
  index = 1
  WHILE (VR(index) <> 0) AND (VR(index+10)>100)
    SPEED = VR(index + 10)
    MOVEABS(VR(index))
    WAIT IDLE
    index = index +1
    WAIT UNTIL IN(function)
  WEND

  WAIT UNTIL IN(function) = 0

RETURN

home_routine:
  SPEED = 1000
  REV_IN = -1: WA(50)
  DATUM_IN = 0: WA(50)
  DATUM(6)
  WAIT IDLE
  WA(1000)
  DEFPOS(0)
  DATUM_IN = -1: WA(50)
  REV_IN = 0
  home_done = 1
RETURN

init:

'This block sets up constants

  l_pos_1 = 983040
  l_pos_2 = 65536
  sp_1 = 15728640
  sp_2 = 1048576


'This block sets up the inputs

  local = 2

  jog = 8
  position = 9
  function = 10
  shift = 11

  pos = 24
  ref = 25
  io_in_order = 26
  ready = 27
  busy = 28

  bit_1 = 29
  bit_2 = 30
  bit_4 = 31
  home_done =0

RETURN

