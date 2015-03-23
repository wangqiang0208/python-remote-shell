#-*- coding:utf8 -*-
__author__ = 'qiangwang'

import os
import sys
import threading
from optparse import OptionParser


def readhost(filename, hosts):
    fp = open(filename, 'r')
    for line in fp.readlines():
        hosts.append(line.replace('\n', '').replace('\r', ''))
    fp.close()
    return hosts


def formatcommand(cmd):
    if cmd is None:
        return ''
    else:
        cmd = cmd.replace('\\', '\\\\')
        cmd = cmd.replace('\\', '\\\\')
        cmd = cmd.replace('"', '\\"')
        cmd = cmd.replace('$', '\$')
        return cmd


def runcommand(user, passwd, host, cmd):
    shcmd = './run.sh %s %s %s "%s"' % (user, passwd, host, cmd)
    # use popen can get the reponse of shell
    popenCmd = os.popen(shcmd)
    cmdresult = popenCmd.readlines()
    cresult = None
    while True:
        cresult = popenCmd.readlines()
        if not cresult or len(cresult) == 0:
            break
        else:
            cmdresult.append(cresult)

    fp = open(host + '.log', 'w')
    fp.write('[Host:%s]\n' % host)
    # cut the authenticate information
    startline = 0
    if len(cmdresult) > 3:
        startline = 3
    for index in range(0, len(cmdresult)):
        if index >= startline:
            if len(cmdresult[index].replace('\n', '').strip()) > 0:
                fp.write(cmdresult[index])
    fp.close()
    print 'command done at host:%s' % host


def parseOption():
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='file', type='string', help='give the ips file', metavar='iplist.log')
    parser.add_option('-t', '--to', dest='to', type='string', help='give the host ip', metavar='192.168.3.1')
    parser.add_option('-p', '--password', dest='password', type='string', help='give password', metavar='123', default='123')
    parser.add_option('-u', '--user', dest='user', type='string', help='give user name', metavar='wq', default='wq')
    parser.add_option('-c', '--command', dest='command', type='string', help='give command')
    (options, sys.argv[1:]) = parser.parse_args()
    return options


if __name__ == "__main__":

    options = parseOption()
    if options is None or (options.file is None and options.to is None) or options.command is None:
        print 'parameter error'
    else:
        filename = options.file
        user = options.user
        passwd = options.password
        cmd = options.command
        to = options.to

        #format command
        cmd = formatcommand(cmd)
        hosts = []
        if filename is not None:
            readhost(filename, hosts)
        if to is not None:
            hosts.append(to)
        for host in hosts:
            try:
                t = threading.Thread(target=runcommand, args=(user, passwd, host, cmd))
                t.start()
                print 'command at host:%s' % host
            except Exception:
                pass