import paramiko

ssh_session = {}
channal_session = {}


def get_ssh(ip, username, passwd):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(ip, 22, username, passwd, timeout=30)
    ssh = conn.get_transport()
    return ssh


def get_channal(ip, service_id, project_name):
    if channal_session.has_key(service_id):
        if channal_session[service_id].closed == False:
            print 'session is exist !!!'
        else:
            del channal_session[service_id]
            print 'status has been update !!!'
            channal_session[service_id] = ssh_session[ip].open_session()
            channal_session[service_id].setblocking(0)
            log_command = 'tail -f -n 1  /qingke/tomcats/%s_tomcat/logs/catalina.out' % (project_name)
            channal_session[service_id].exec_command(command=log_command)
    else:
        channal_session[service_id] = ssh_session[ip].open_session()
        channal_session[service_id].setblocking(0)
        log_command = 'tail -f -n 1  /qingke/tomcats/%s_tomcat/logs/catalina.out' % (project_name)
        channal_session[service_id].exec_command(command=log_command)
    return channal_session[service_id]


def manage_channal(ip, username, passwd, service_id, project_name):
    if ssh_session.has_key(ip):
        if ssh_session[ip].active:
            channal_session[service_id] = get_channal(ip, service_id, project_name)
        else:
            ssh_session[ip] = get_ssh(ip, username, passwd)
            channal_session[service_id] = get_channal(ip, service_id, project_name)
    else:
        ssh_session[ip] = get_ssh(ip, username, passwd)
        channal_session[service_id] = get_channal(ip, service_id, project_name)
    return channal_session[service_id]


if channal_session.has_key(1):
    get_channal('192.168.122.3', 1, 'test')
else:
    manage_channal('192.168.122.3', 'root', 'gzq123', 1, 'test')
