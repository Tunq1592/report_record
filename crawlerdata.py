#!/usr/bin/python3.6

import paramiko
import time
import sys
import os
import sqlite3
import datetime

def cur_datetime_ops(): # Lấy date curent -1
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.1.16', username= 'tu.nguyen', password = 'Pc057e1tc@151192')
    stdin, stdout, stderr = client.exec_command ('''date -d '1 day ago' +%Y-%m-%d''')
    for i in stdout:
        cur_date = i.strip('\n')
    return cur_date
def dtime_pbx_log():
    list_data_log = []
    data_logfile = []
    list_contain_log = []
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.1.16', username= 'tu.nguyen', password = 'Pc057e1tc@151192')
    cur_date = cur_datetime_ops()
    list_log_folder = ['/volume1/Log/PBX/log_rsyn_db_pbx18/', '/volume1/Log/PBX/log_rsyn_NAS02/', '/volume1/Log/PBX/log_rsyn_NAS/', '/volume1/Log/PBX/log_rsyn_pbx18/']
    for folder in list_log_folder:
        stdin_amount_file_pbx, stdout_amount_file_pbx, stderr_amount_file_pbx = client.exec_command('''ls %s'''%(folder))
        for amount_file_pbx in stdout_amount_file_pbx:
            list_data_log.append(amount_file_pbx.strip('\n'))
        data_date_pbx = list_data_log[-1].strip('.log').split('_')[-1][:4] + '-' + list_data_log[-1].strip('.log').split('_')[-1][4:6] + '-' + list_data_log[-1].strip('.log').split('_')[-1][6:8]
        print(data_date_pbx)
        stdin_logfile_pbx_header, stdout_logfile_pbx_header, stderr_logfile_pbx_header = client.exec_command("head -n 2 " + folder + list_data_log[-1])
        for contain_log_header in stdout_logfile_pbx_header:
            list_contain_log.append(contain_log_header)
        stdin_logfile_pbx_footer, stdout_logfile_pbx_footer, stderr_logfile_pbx_footer = client.exec_command("tail -n 2 " + folder + list_data_log[-1])
        for contain_log_footer in stdout_logfile_pbx_footer:
            list_contain_log.append(contain_log_footer)
        with open('/opt/web_rp/log_info.log', 'w') as f:
            f.write(list_data_log[-1])
            for i in list_contain_log:
                f.write('-' + i + '\n')
    if cur_date == data_date_pbx:
        return (data_date_pbx)
    else:
        with open('/opt/web_rp/log_error.log', 'w') as f:
            f.write( ' %s not found log record - %s' %(cur_date, data_date_pbx))
        return None

def dtime_genesys_log():
    list_data_log = []
    data_logfile = []
    list_contain_log = []
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.1.16', username= 'tu.nguyen', password = 'Pc057e1tc@151192')
    stdin, stdout, stderr = client.exec_command ('''date -d '1 day ago' +%Y-%m-%d''')
    for i in stdout:
        cur_date = i.strip('\n')
    list_log_folder = ['/volume1/Log/Genesys/log_genesys_NAS02/', '/volume1/Log/Genesys/log_genesys_NAS01/']
    for folder in list_log_folder:
        stdin_amount_file_pbx, stdout_amount_file_pbx, stderr_amount_file_pbx = client.exec_command('''ls %s'''%(folder))
        for amount_file_pbx in stdout_amount_file_pbx:
            list_data_log.append(amount_file_pbx.strip('\n'))
        data_date_genesys = list_data_log[-1].strip('.log').split('_')[-1][:4] + '-' + list_data_log[-1].strip('.log').split('_')[-1][4:6] + '-' + list_data_log[-1].strip('.log').split('_')[-1][6:8]
        stdin_logfile_genesys_header, stdout_logfile_genesys_header, stderr_logfile_genesys_header = client.exec_command("head -n 2 " + folder + list_data_log[-1])
        for contain_log_header in stdout_logfile_genesys_header:
            list_contain_log.append(contain_log_header)
        stdin_logfile_genesys_footer, stdout_logfile_genesys_footer, stderr_logfile_genesys_footer = client.exec_command("tail -n 2 " + folder + list_data_log[-1])
        for contain_log_footer in stdout_logfile_genesys_footer:
            list_contain_log.append(contain_log_footer)
        with open('/opt/web_rp/log_info.log', 'w') as f:
            f.write(list_data_log[-1])
            for i in list_contain_log:
                f.write('-' + i + '\n')
    if cur_date == data_date_genesys:
        return (data_date_genesys)
    else:
        with open('/opt/web_rp/log_error.log', 'w') as f:
            f.write( ' %s not found log record - %s' %(cur_date, data_date_genesys))
        return None
def Check_record():
    result = []
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('192.168.1.16', username= 'tu.nguyen', password = 'Pc057e1tc@151192')
    stdin_amount_file_pbx, stdout_amount_file_pbx, stderr_amount_file_pbx = client.exec_command('''ls /volume1/Bk-Record/PBX/`date +%Y`/`date +%m`/`date -d '1 day ago' +%d` -l|wc -l''')
    for amount_file_pbx in stdout_amount_file_pbx:
        result.append(amount_file_pbx.strip('\n'))
    stdin_size_file_pbx, stdout_size_file_pbx, stderr_size_file_pbx = client.exec_command('''du -m /volume1/Bk-Record/PBX/`date +%Y`/`date +%m`/`date -d '1 day ago' +%d` ''')
    for size_file_pbx in stdout_size_file_pbx:
        result.append(size_file_pbx.split('\t')[0])

    stdin_amount_file_genesys, stdout_amount_file_genesys, stderr_amount_file_genesys = client.exec_command('''ls /volume1/Bk-Record/Genesys/`date +%Y`/`date +%m.%Y`/`date -d '1 day ago' +%Y-%m-%d` -l|wc -l''')
    for amount_file_genesys in stdout_amount_file_genesys:
        result.append(amount_file_genesys)
    stdin_size_file_genesys, stdout_size_file_genesys, stderr_size_file_genesys = client.exec_command('''du -m /volume1/Bk-Record/Genesys/`date +%Y`/`date +%m.%Y`/`date -d '1 day ago' +%Y-%m-%d`''')
    for size_file_genesys in stdout_size_file_genesys:
        result.append(size_file_genesys.split('\t')[0])
    return result
def main():
    con = sqlite3.connect('/opt/web_rp/database/record_rp.db')
    cursor = con.cursor()

    if dtime_pbx_log() != None:
        stt_log = 'True'
        data_record = Check_record()
        date_cur = dtime_pbx_log()
        with open('/opt/web_rp/log_info.log', 'r') as f:
            data_log_info = f.readlines()
        cursor.execute("INSERT INTO report_pbx(datetime, record_amount_pbx, storage_record_pbx, status_log, Note) VALUES (?, ?, ?, ?, ?)",
        (date_cur, str(int(data_record[0]) - 1), data_record[1], stt_log, '\n'.join(data_log_info)))
        con.commit()
    else:
        stt_log = 'False'
        date_cur = cur_datetime_ops()
        with open ('/opt/web_rp/log_error.log', 'r') as f:
            contain_log = f.readline()
        cursor.execute("INSERT INTO report_pbx(datetime, status_log, Note) VALUES (?, ?, ?)",(date_cur, stt_log, contain_log))
        con.commit()

    if dtime_genesys_log() != None:
        stt_log = 'True'
        data_record = Check_record()
        date_cur = dtime_genesys_log()
        with open('/opt/web_rp/log_info.log', 'r') as f:
            data_log_info = f.readlines()
        cursor.execute("INSERT INTO report_genesys(datetime, record_amount_genesys, storage_record_genesys, status_log, Note) VALUES (?, ?, ?, ?, ?)",
        (date_cur, str(int(data_record[2]) - 1), data_record[3], stt_log, '\n'.join(data_log_info)))
        con.commit()
    else:
        stt_log = 'False'
        date_cur = cur_datetime_ops()
        with open ('/opt/web_rp/log_error.log', 'r') as f:
            contain_log = f.readline()
        cursor.execute("INSERT INTO report_genesys(datetime, status_log, Note) VALUES (?, ?, ?)",(date_cur, stt_log, contain_log))
        con.commit()
if __name__ == "__main__":
    main()

