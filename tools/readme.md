- WinAppDriverUIRecorder.zip
    WinAppDriver UI Recorder v1.0 RC を使用
    https://github.com/microsoft/WinAppDriver/releases/tag/UiR_v1.0-RC
    xpath 取得に必須で必要。展開するだけ。インストール不要
    ※inspect.exe で対応できる可能性もあるが、element Nameが重複するとテストケース作成が面倒なので使わない
      C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64 のように色々なバージョンがインストール済みのはず
- WindowsApplicationDriver-1.2.99-win-x64.exe
    WinAppDriver v1.3 Release Candidate 1 (1.2.99) を使用
    winappdriveruirecorder 本体。
    インストールすると以下に配置される。2024/05/31 現在は1.2.99_x64版のみで動作確認した。（1.2.1では動作しない）
    "C:\Program Files\Windows Application Driver\WinAppDriver.exe"
- inspect_win10.x64.7z
    Windows10 64bit環境にインストールされていた inspect.exe
    C:\Program Files (x86)\Windows Kits\10\bin 配下に色々なバージョンがインストールされているはず。
    
