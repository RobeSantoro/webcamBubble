https://obsproject.com/forum/resources/command-line-tool-for-obs-websocket-plugin-windows.615/

NOTE: Commands in obs-websocket have changed a lot in version 5. However, built-in OBSCommand commands did not change syntax or wording, this only affects /command and /sendjson commands!
Check the new protocol reference to update your scripts!
Please also note the default port has changed from 4444 to 4455

How to install:
1. Download OBSCommand_v1.6.3.zip
2. Extract the file (you can put the folder "OBSCommand" anywhere you want)
3. In OBS Studio menu, go to "Tools"->"obs-websocket Settings"
4. Uncheck "Enable System Tray Alerts" (unless you want to get spammed)
5. Use OBSCommand.exe to control OBS Studio local or from a remote machine (read the note below if you get an error here)

Note: if you get a message "A fatal error occurred. The required library hostfxr.dll could not be found..." this means you are missing .net Core 3.1 Runtime (for Console Applications), you can download this dependency here: https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/runtime-3.1.30-windows-x64-installer


Also check out the new Noobs Cmdr, a GUI for OBSCommand written by nuttylmao, you can create batch files or vbs scripts for OBSCommand with a few mouse clicks with this tool!

Usage:
OBSCommand /server=127.0.0.1:4455 /password=xxxx /delay=0.5 /setdelay=0.05 /profile=myprofile /scene=myscene /hidesource=myscene/mysource /showsource=myscene/mysource /togglesource=myscene/mysource /toggleaudio=myaudio /mute=myaudio /unmute=myaudio /setvolume=mysource,volume,[delay],[steps] /fadeopacity=mysource,myfiltername,startopacity,endopacity,[fadedelay],[fadestep] /slidesetting=mysource,myfiltername,startvalue,endvalue,[slidedelay],[slidestep] /slideasync=mysource,myfiltername,startvalue,endvalue,[slidedelay],[slidestep] /startstream /stopstream /startrecording /stoprecording /command=mycommand,myparam1=myvalue1... /sendjson=jsonstring


Note: If Server is omitted, default 127.0.0.1:4455 will be used.
Use quotes if your item name includes spaces.
Password can be empty if no password is set in OBS Studio.
You can use the same option multiple times.
If you use Server and Password, those must be the first 2 options!

Examples:
OBSCommand /scene=myscene
OBSCommand /toggleaudio="Desktop Audio"
OBSCommand /mute=myAudioSource
OBSCommand /unmute="my Audio Source"
OBSCommand /setvolume=Mic/Aux,0,50,2
OBSCommand /setvolume=Mic/Aux,100
OBSCommand /fadeopacity=Mysource,myfiltername,0,100,5,2
OBSCommand /slidesetting=Mysource,myfiltername,contrast,-2,0,100,0.01
OBSCommand /slideasync=Mysource,myfiltername,saturation,*,5,100,0.1
OBSCommand /stopstream
OBSCommand /profile=myprofile /scene=myscene /showsource=mysource
OBSCommand /showsource=mysource
OBSCommand /hidesource=myscene/mysource
OBSCommand /togglesource=myscene/mysource
OBSCommand /showsource="my scene"/"my source"

For most of other simpler requests, use the generalized '/command' feature (see syntax below):
OBSCommand /command=SaveReplayBuffer
OBSCommand /command=SaveSourceScreenshot,sourceName=MyScene,imageFormat=png,imageFilePath=C:\OBSTest.png
OBSCommand /command=SetSourceFilterSettings,sourceName="Color Correction",filterName=Opacity,filterSettings=opacity=10
OBSCommand /command=SetInputSettings,inputName="Browser",inputSettings=url='https://www.google.com/search?q=query+goes+there'

For more complex requests, use the generalized '/sendjson' feature:
OBSCommand.exe /sendjson=SaveSourceScreenshot={'sourceName':'MyScource','imageFormat':'png','imageFilePath':'H:\\OBSScreenShot.png'}

You can combine multiple commands like this:
OBSCommand /scene=mysource1 /delay=1.555 /scene=mysource2 ...etc
OBSCommand /setdelay=1.555 /scene=mysource1 /scene=mysource2 ...etc


Options:
--------
/server=127.0.0.1:4455            define server address and port
  Note: If Server is omitted, default 127.0.0.1:4455 will be used.
/password=xxxx                    define password (can be omitted)
/delay=n.nnn                      delay in seconds (0.001 = 1 ms)
/setdelay=n.nnn                   global delay in seconds (0.001 = 1 ms)
                                  (set it to 0 to cancel it)
/profile=myprofile                switch to profile "myprofile"
/scene=myscene                    switch to scene "myscene"
/hidesource=myscene/mysource      hide source "scene/mysource"
/showsource=myscene/mysource      show source "scene/mysource"
/togglesource=myscene/mysource    toggle source "scene/mysource"
  Note:  if scene is omitted, current scene is used
/toggleaudio=myaudio              toggle mute from audio source "myaudio"
/mute=myaudio                     mute audio source "myaudio"
/unmute=myaudio                   unmute audio source "myaudio"
/setvolume=myaudio,volume,delay,  set volume of audio source "myaudio"
steps                             volume is 0-100, delay is in milliseconds
                                  between steps (min. 5, max. 1000) for fading
                                  steps is (1-99), default step is 1
  Note:  if delay is omitted volume is set instant
/fadeopacity=mysource,myfiltername,startopacity,endopacity,[fadedelay],[fadestep]
                                  start/end opacity is 0-100, 0=fully transparent
                                  delay is in milliseconds, step 0-100
             Note: Use * for start- or endopacity for fade from/to current value
/slidesetting=mysource,myfiltername,settingname,startvalue,endvalue,[slidedelay],[slidestep]
                                  start/end value min/max depends on setting!
                                  delay is in milliseconds
                                  step depends on setting (can be x Or 0.x Or 0.0x)
             Note: Use * for start- or end value to slide from/to current value
/slideasync
            The same as slidesetting, only this one runs asynchron!
/startstream                      starts streaming
/stopstream                       stop streaming
/startrecording                   starts recording
/stoprecording                    stops recording

General User Command syntax:

/command=mycommand,myparam1=myvalue1,myparam2=myvalue2...
                                  issues user command,parameter(s) (optional)
/command=mycommand,myparam1=myvalue1,myparam2=myvalue2,myparam3=mysubparam=mysubparamvalue
                                  issues user command,parameters and sub-parameters

                                  Note: Use single quotes if you have arguments with equal sign

                                  https://github.com/REALDRAGNET/OBSCommand