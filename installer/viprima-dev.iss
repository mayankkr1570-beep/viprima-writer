; SPDX-License-Identifier: MPL-2.0
; Development-only installer for a private, already built runtime.
#define AppName "ViPrima Writer Development Preview"
#define AppVersion "0.1.0"
[Setup]
AppId=ViPrima.Writer.Dev
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=ViPrima
DefaultDirName={localappdata}\Programs\ViPrimaWriterDev
DefaultGroupName={#AppName}
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=..\dist
OutputBaseFilename=ViPrima_Writer_v0.1.0_Development_Setup_x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\ViPrimaWriter.exe
CloseApplications=yes
RestartApplications=no
[Files]
Source: "..\stage\ViPrimaWriter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\stage\runtime\*"; DestDir: "{app}\runtime"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\stage\NOTICE.txt"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{group}\ViPrima Writer Development Preview"; Filename: "{app}\ViPrimaWriter.exe"
Name: "{group}\Uninstall ViPrima Writer Development Preview"; Filename: "{uninstallexe}"
[Run]
Filename: "{app}\ViPrimaWriter.exe"; Description: "Launch development preview"; Flags: nowait postinstall skipifsilent unchecked
