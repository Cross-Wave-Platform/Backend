BULK INSERT dbo.auth
FROM '/home/linux/Desktop/MSSQL/test.csv'
WITH ( CODEPAGE='RAW', FIRSTROW=2, FORMAT='CSV');
