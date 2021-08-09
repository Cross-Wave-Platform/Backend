-- change to database
USE KIT_DB;
GO

-- create query user that can only select from problem and survey

-- drop user if exists
DROP USER IF EXISTS query;
GO

-- create login
USE master;
GO

-- renew login
IF EXISTS ( SELECT name FROM sys.server_principals WHERE name = 'query')
BEGIN
    DROP LOGIN query;
END
GO

CREATE LOGIN query WITH PASSWORD = 'ASDASDzxc123';
USE KIT_DB;
GO

--create restrictive user
CREATE USER query FOR LOGIN query;
GO

-- grant permission to view tables
GRANT SELECT ON dbo.survey TO query;
GRANT SELECT ON dbo.problems TO query;
GO


-- create shopcart user to insert and delete shopcart items

-- change to database
USE KIT_DB;
GO

-- drop user if exists
DROP USER IF EXISTS shopcart;
GO

-- create login
USE master;
GO

-- renew login
IF EXISTS ( SELECT name FROM sys.server_principals WHERE name = 'shopcart')
BEGIN
    DROP LOGIN shopcart;
END
GO

CREATE LOGIN shopcart WITH PASSWORD = 'ASDASDzxc123';
USE KIT_DB;
GO

--create restrictive user
CREATE USER shopcart FOR LOGIN shopcart;
GO

-- grant permission to insert and delete tables
GRANT DELETE ON dbo.shop_cart TO shopcart;
GRANT INSERT ON dbo.shop_cart TO shopcart;
GO


-- create account user to add new account only

-- change to database
USE KIT_DB;
GO

-- drop user if exists
DROP USER IF EXISTS account;
GO

-- create login
USE master;
GO

-- renew login
IF EXISTS ( SELECT name FROM sys.server_principals WHERE name = 'account')
BEGIN
    DROP LOGIN account;
END
GO

CREATE LOGIN account WITH PASSWORD = 'ASDASDzxc123';
USE KIT_DB;
GO

--create restrictive user
CREATE USER account FOR LOGIN account;
GO

-- grant permission to insert tables
GRANT INSERT ON dbo.account TO account;
GO
