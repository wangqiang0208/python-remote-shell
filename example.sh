#get top 20 ip list in the file of "kv_access_log"
python runtool.py -f wapsoso_ips -u mqq -p mqq2005 -c "cd /data/log/wapsoso; awk 'BEGIN{FS=\"\\|\\|\"}{for(i=1;i<=NF;i++){if(\$i~\"^ip=\")print \$i}}' kv_access_log | sort | uniq -c | sort -nr | head -n 20"