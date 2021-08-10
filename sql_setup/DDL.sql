--清空資料庫
USE master;
GO
DROP DATABASE IF EXISTS KIT_DB;
GO

--資料庫
-- with utf8 enabled( sql server 2019+)
CREATE DATABASE KIT_DB COLLATE Latin1_General_100_CS_AS_SC_UTF8;
GO

--切換使用中的資料庫
USE KIT_DB;
GO

--建立tables
CREATE TABLE dbo.survey
(
survey_id   INT     IDENTITY,
age_type    INT     NOT NULL,
survey_type INT     NOT NULL,
wave        INT     NOT NULL,
release     INT     NOT NULL DEFAULT 0,

CONSTRAINT PK_survey PRIMARY KEY CLUSTERED ( survey_id)
);

CREATE TABLE dbo.problems
(
problem_id      INT     IDENTITY,
problem_name    VARCHAR( 4000)  NOT NULL,
topic           VARCHAR( 4000)  NOT NULL,
survey_id       INT     NOT NULL,
class           VARCHAR( 900)  NOT NULL DEFAULT 'no_group',
subclass        VARCHAR( 900)  NOT NULL DEFAULT 'no_group',

CONSTRAINT PK_problems PRIMARY KEY CLUSTERED ( problem_id),
CONSTRAINT FK_survey FOREIGN KEY (survey_id) REFERENCES dbo.survey ( survey_id)
);

CREATE TABLE dbo.account
(
account_id      INT             IDENTITY,
account_name    VARCHAR( 4000)  NOT NULL,
email           VARCHAR( 320)   NOT NULL,
password        VARCHAR( 4000)  NOT NULL,
auth            INT             NOT NULL DEFAULT 2,

CONSTRAINT PK_account PRIMARY KEY CLUSTERED ( account_id)
);

CREATE TABLE dbo.shop_cart
(
account_id  INT     NOT NULL,
problem_id  INT     NOT NULL,

-- CONSTRAINT PK_shop_cart PRIMARY KEY CLUSTERED ( account_id, problem_id),
-- CONSTRAINT FK_shop_cart_account FOREIGN KEY ( account_id) REFERENCES dbo.account ( account_id),
-- CONSTRAINT FK_shop_cart_problems FOREIGN KEY ( problem_id) REFERENCES dbo.problems ( problem_id)
);

GO

USE master;
GO
