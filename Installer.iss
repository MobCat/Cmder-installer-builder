; Script generated by the Inno Setup Script Wizard.
; Modifyed badley by MobCat for Cmder Installer Builder

#define MyAppName "Cmder"
#define MyAppVersion "1.3.24"
#define MyAppPublisher "Cmderdev"
#define MyAppURL "https://cmder.app/"
#define MyAppExeName "Cmder.exe"
#define InstallType "full"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{BBD2EFDF-ACD2-42E0-BCD1-7B6CF1CDBBCC}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={commonpf64}\{#MyAppName}
DisableProgramGroupPage=yes
InfoBeforeFile=info.txt
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
PrivilegesRequired=admin
OutputDir=Build
OutputBaseFilename=Cmder_{#MyAppVersion}_{#InstallType}_Installer
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Dirs]
Name: "{commonpf64}\{#MyAppExeName}"; Permissions: everyone-full

[Files]
Source: "Cmder\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "Cmder\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
;Filename: "{app}\{#MyAppName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
; Lol no idea
Filename: "{app}\cmder.exe"; Parameters: "/REGISTER ALL"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent


