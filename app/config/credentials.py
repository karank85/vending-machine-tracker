import yaml

cred = yaml.load(open('../cred.yaml'), Loader=yaml.Loader)

mysql_host = cred['mysql_host']
mysql_user = cred['mysql_user']
mysql_password = cred['mysql_password']
mysql_db = cred['mysql_db']
