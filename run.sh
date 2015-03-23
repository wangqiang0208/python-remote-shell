#!/usr/bin/expect
#qiangwang

set user [lindex $argv 0]
set passwd [lindex $argv 1]
set host [lindex $argv 2]
set cmd [lindex $argv 3]
set yesnoflag 0
set timeout 30
for {} {1} {} {
spawn ssh -l $user $host "$cmd"
#spawn ssh -l $user $host "cd /data/log/wapsoso;head -n 10 kv_access_log | awk 'BEGIN{FS=\"\\\\|\\\\|\"}{print \$2}'"
expect {
        "assword:" {
                send "$passwd\r"
                break;
        }
        "yes/no)?" {
                set yesnoflag 1
                send "yes\r"
                break;
        }
}
}
if { $yesnoflag == 1 } {
        expect {
                "assword:" {
                        send "$passwd\r"
                }
                "yes/no)?" {
                        set yesnoflag 2
                        send "yes\r"
                }
        }
}
if { $yesnoflag == 2 } {
        expect {
                "assword:" {
                    send "$passwd\r"
                }
        }
}
interact
