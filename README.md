# 480-web
A web interface for the Kenwood TS-480

![480-web](images/480-web.png)

### Startup
When remote.html loads, it will set the transciever to the following:
 - VFO A - CWR with 200Hz DSP filter
 - VFO B - CW with 2000Hz DSP filter
 - split mode operation

### Power On
### Power Off
### Set Simplex USB
 - sets VFO A to RX and TX (simplex) and USB Mode
 - mainly useful to set the rig for digi mode use by other software

### ToggleVFO
 - switches the RX and TX functions of VFO A and B
 - sets the filter bandwidth values for each from the input boxes

### ToggleCWR
 - toggles CW or CWR for the current RX VFO

### VFO (Set ->)
 - Set the frequency of the VFO from the input box

### Fine Tuning (UP / DOWN)
 - Increment or Decrement this VFO frequency by 100Hz

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

### Audio Gain
 - Set the Audio Gain (0 - 255)
