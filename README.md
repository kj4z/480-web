# 480-web
A web interface for the Kenwood TS-480

### Startup
When remote.html loads, it will set the transciever to the following:
 - VFO A - CWR with 200Hz DSP filter
 - VFO B - CW with 2000Hz DSP filter
 - split mode operation


### ToggleVFO
 - switches the RX and TX functions of VFO A and B
 - sets the filter bandwidth values for each from the input boxes

### ToggleCWR
 - toggles CW or CWR for the current RX VFO

### VFO (Set ->)
 - Set the frequency of the VFO from the input box

### Clone (FreqAtoB or FreqBtoA)
 - "Pushes" one VFO frequency into the other VFO

### Tune
 - runs the transmitter Tune fuction for 2 seconds
 - reads and displays the SWR

### Send
 - send callsign or report from the input box

### ToggleVox
 - toggle the Vox setting On / Off
 - displays the Vox status

### CW Speed
 - Set CW speed from the input box
