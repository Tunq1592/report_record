#!/usr/bin/python3.6
import paramiko
import sys
import sqlite3
import datetime


def cur_datetime_ops(): # Lấy date curent -1
	con = sqlite3.connect('/opt/web_rp/database/record_rp.db')
	cursor = con.cursor()
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('192.168.1.16', username= 'tu.nguyen', password = 'Pc057e1tc@151192')
	stdin, stdout, stderr = client.exec_command ('''date -d '1 day ago' +%Y-%m-%d''')
	for i in stdout:
		cur_date = i.strip('\n')
		_execute_pbx = '''INSERT INTO report_pbx(datetime) VALUES ('%s')'''%(cur_date)
	cursor.execute(_execute_pbx)
	_execute_genesys = '''INSERT INTO report_genesys(datetime) VALUES ('%s')'''%(cur_date)
	cursor.execute(_execute_genesys)
	con.commit()
	return cur_date

def Check_record_pbx(path, datetimes):
	con = sqlite3.connect('/opt/web_rp/database/record_rp.db')
	cursor = con.cursor()
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('192.168.1.16', username= 'tu.nguyen', password = 'Pc057e1tc@151192')
	stdin_amount_file_pbx, stdout_amount_file_pbx, stderr_amount_file_pbx = client.exec_command('''ls %s -l|wc -l''' %(path))
	for amount_file_pbx in stdout_amount_file_pbx:
		cursor.execute(
						"UPDATE report_pbx SET record_amount_pbx = ? WHERE datetime = ?",
						(int(amount_file_pbx) - 1, datetimes)
					)
	con.commit()
	stdin_size_file_pbx, stdout_size_file_pbx, stderr_size_file_pbx = client.exec_command('''du -m %s''' %(path))
	for size_file_pbx in stdout_size_file_pbx:
		cursor.execute(
						"UPDATE report_pbx  SET storage_record_pbx = ? WHERE datetime = ?",
						(size_file_pbx.strip('\n').split('\t')[0], datetimes)
					)
	con.commit()
	outbound_bops = 0
	outbound_col = 0
	inbound_cs = 0
	inbound_col = 0
	stdin_files_record_pbx, stdout_files_record_pbx, stderr_files_record_pbx = client.exec_command("ls %s"%(path))
	for files_record in stdout_files_record_pbx:
		try:
			if 'out' == files_record.split('-')[0] or 'internal' == files_record.split('-')[0]:
				if '9' == files_record.split('-')[1][0]:
					outbound_bops +=1
				else:
					outbound_col +=1
			elif 'external' in files_record.split('-')[0] or '19002204'in files_record.split('-')[1]:
				inbound_cs +=1
			elif 'q' in files_record.split('-')[0]:
				if 'q-4001' in files_record:
					inbound_col +=1
				else:
					inbound_cs +=1
			elif 'in' in files_record.split('-')[0]:
				if '842871068684' in files_record.split('-')[1]:
					inbound_col +=1
				else:
					inbound_cs +=1
		except:
			continue
		cursor.execute(
						"UPDATE report_pbx SET outbound_ops = ?, outbound_col = ?, inbound_cs = ?, inbound_col = ? WHERE datetime = ? ", 
						(outbound_bops, outbound_col, inbound_cs, inbound_col, datetimes)
					)
	con.commit()



def Check_record_genesys(path, datetimes):
	list_team_rs= ['mai.truong', 'phuc.ngo', 'thao.vuong', 'ngan.pham', 'hien.le', 'trang.nguyen5', 'vu.nguyen2', 'huyen.duong', 'thao.tran']
	con = sqlite3.connect('/opt/web_rp/database/record_rp.db')
	cursor = con.cursor()
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('192.168.1.16', username= 'tu.nguyen', password = 'Pc057e1tc@151192')
	stdin_amount_file_genesys, stdout_amount_file_genesys, stderr_amount_file_genesys = client.exec_command('''ls %s -l|wc -l''' %(path))
	for amount_file_genesys in stdout_amount_file_genesys:
		_execute = '''UPDATE report_genesys SET record_amount_genesys = %d WHERE datetime = '%s' '''%(int(amount_file_genesys.strip('\n')) - 1, datetimes)
		cursor.execute(_execute)
	con.commit()

	stdin_size_file_genesys, stdout_size_file_genesys, stderr_size_file_genesys = client.exec_command('''du -m %s''' %(path))
	for size_file_genesys in stdout_size_file_genesys:
		cursor.execute(
						"UPDATE report_genesys  SET storage_record_genesys = ? WHERE datetime = ? ",
						(size_file_genesys.strip('\n').split('\t')[0], datetimes)
					)
	con.commit()
	auto_dials_call_amount_rs = 0
	auto_dials_call_amount = 0
	inbound_call_amount = 0
	manual_call_amount = 0
	stdin_files_record_genesys, stdout_files_record_genesys, stderr_files_record_genesys = client.exec_command("ls %s"%(path))
	for file_record in stdout_files_record_genesys:
		if len(file_record.split('_')) == 9: #check len record == 7 ==> auto_dials_call_amount
			if file_record.split('_')[7]  in list_team_rs:
				auto_dials_call_amount_rs +=1
			else:
				auto_dials_call_amount +=1
		elif len(file_record.split('_')) == 7: #check len record == 7 ==> inbound_call_amount or manual_call_amount
			if '84' in file_record.split('_')[2][:2]: #check value string '84' co trong vi tri [:2] phan tu thu 2
				inbound_call_amount +=1
			elif '5' in file_record.split('_')[2][0]: # check value string '5' co trong vi tri 0 phan tu thu 2
				manual_call_amount +=1
	cursor.execute(
					"UPDATE report_genesys SET autodiler = ?, autodiler_rs = ? , inbound= ?, manual= ? WHERE datetime = ?",
					(auto_dials_call_amount, auto_dials_call_amount_rs, inbound_call_amount, manual_call_amount, datetimes)
				)
	con.commit()

def scan_foldermonth_genesys(path):
	con = sqlite3.connect('/opt/web_rp/database/record_rp.db')
	cursor = con.cursor()
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('192.168.1.16', username= 'tu.nguyen', password = 'Pc057e1tc@151192')
	stdin_folder_genesys, stdout_folder_genesys, stderr_folder_genesys = client.exec_command('''ls %s'''%(path))
	for date in stdout_folder_genesys:
		_execute = '''INSERT INTO report_genesys(datetime) VALUES ('%s')'''%(date.strip('\n'))
		cursor.execute(_execute)
		con.commit()
		Check_record_genesys(path + date.strip('\n'), date.strip('\n'))


def scan_foldermonth_pbx(path):
	con = sqlite3.connect('/opt/web_rp/database/record_rp.db')
	cursor = con.cursor()
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('192.168.1.16', username= 'tu.nguyen', password = 'Pc057e1tc@151192')
	stdin_folder_pbx, stdout_folder_pbx, stderr_folder_pbx = client.exec_command('''ls %s'''%(path))
	for date in stdout_folder_pbx:
		datetimes = '-'.join((path + date).split('/')[4:7]).strip('\n')
		_execute = '''INSERT INTO report_pbx(datetime) VALUES ('%s')'''%(datetimes)
		cursor.execute(_execute)
		con.commit()
		Check_record_pbx(path + date.strip('\n'), datetimes)

def main():
	#if int(sys.argv[1]) == 1 :
	#	scan_foldermonth_pbx(sys.argv[1])
	#	scan_foldermonth_genesys(sys.argv[2])
	#elif int(sys.argv[1]) == 2 :
	datetimes = cur_datetime_ops()
	path_genesys = '/volume1/Bk-Record/Genesys/' + datetimes.split('-')[0] + '/' + datetimes.split('-')[1] + '.' + datetimes.split('-')[0] + '/' + datetimes 
	path_pbx = '/volume1/Bk-Record/PBX/' + datetimes.split('-')[0] + '/' + datetimes.split('-')[1] + '/' + datetimes.split('-')[2]
	Check_record_genesys(path_genesys, datetimes)
	Check_record_pbx(path_pbx, datetimes)
		
if __name__ == "__main__":
	main()

