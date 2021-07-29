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
year        INT     NOT NULL,
wave        INT     NOT NULL,
release     INT     NOT NULL DEFAULT 0,

CONSTRAINT PK_survey PRIMARY KEY CLUSTERED ( survey_id)
);

CREATE TABLE dbo.auth
(
class       VARCHAR( 900) NOT NULL,
min_auth    INT           NOT NULL DEFAULT 2, --admin as default

CONSTRAINT PK_auth PRIMARY KEY CLUSTERED ( class)
);

CREATE TABLE dbo.problems
(
problem_id      VARCHAR( 30)    NOT NULL,
topic           VARCHAR( 4000)  NOT NULL,
class           VARCHAR( 900)  NOT NULL DEFAULT 'no_group',

CONSTRAINT PK_problems PRIMARY KEY CLUSTERED ( problem_id),
CONSTRAINT FK_problems_auth FOREIGN KEY ( class) REFERENCES dbo.auth ( class)
);

CREATE TABLE dbo.survey_problems
(
survey_id   INT             NOT NULL,
problem_id  VARCHAR( 30)    NOT NULL,

CONSTRAINT PK_survey_problems PRIMARY KEY CLUSTERED ( survey_id, problem_id),
CONSTRAINT FK_survey_problems_survey FOREIGN KEY ( survey_id) REFERENCES dbo.survey ( survey_id),
CONSTRAINT FK_survey_problems_problems FOREIGN KEY ( problem_id) REFERENCES dbo.problems ( problem_id)
);

CREATE TABLE dbo.answers
(
answer_id   BIGINT          NOT NULL,
problem_id  VARCHAR( 30)    NOT NULL,
survey_id   INT             NOT NULL,
answer      VARCHAR( 4000),

CONSTRAINT PK_answers PRIMARY KEY CLUSTERED ( answer_id, problem_id),
CONSTRAINT FK_answers_survey FOREIGN KEY ( survey_id) REFERENCES dbo.survey ( survey_id),
CONSTRAINT FK_answers_problems FOREIGN KEY ( problem_id) REFERENCES dbo.problems ( problem_id)
);

CREATE TABLE dbo.tag_values
(
problem_id  VARCHAR( 30)    NOT NULL,
tag_value   INT             NOT NULL,
tag_name    VARCHAR( 4000) NOT NULL,

CONSTRAINT PK_tag_values PRIMARY KEY CLUSTERED ( problem_id, tag_value),
CONSTRAINT FK_tag_values_problems FOREIGN KEY ( problem_id) REFERENCES dbo.problems ( problem_id)
);

CREATE TABLE dbo.account
(
user_id         INT             IDENTITY,
account_name    VARCHAR( 4000)  NOT NULL,
email           VARCHAR( 320)   NOT NULL,
password        VARCHAR( 4000)  NOT NULL,
auth            INT             NOT NULL DEFAULT 4,

CONSTRAINT PK_account PRIMARY KEY CLUSTERED ( user_id)
);

CREATE TABLE dbo.auth_change_log
(
log_time    datetime        NOT NULL,
admin_id    INT             NOT NULL,
user_id     INT             NOT NULL,
old_auth    INT             NOT NULL,
new_auth    INT             NOT NULL,
reason      VARCHAR( 4000)  NOT NULL,

CONSTRAINT PK_auth_change_log PRIMARY KEY CLUSTERED ( log_time),
CONSTRAINT FK_auth_change_log_admin_account FOREIGN KEY ( admin_id) REFERENCES dbo.account ( user_id),
CONSTRAINT FK_auth_change_log_user_account FOREIGN KEY ( user_id) REFERENCES dbo.account ( user_id)
);

CREATE TABLE dbo.shop_cart
(
user_id     INT              NOT NULL,
survey_id   INT              NOT NULL,
problem_id  VARCHAR( 30)     NOT NULL,

CONSTRAINT PK_shop_cart PRIMARY KEY CLUSTERED ( user_id, survey_id, problem_id),
CONSTRAINT FK_shop_cart_account FOREIGN KEY ( user_id) REFERENCES dbo.account ( user_id),
CONSTRAINT FK_shop_cart_survey FOREIGN KEY ( survey_id) REFERENCES dbo.survey ( survey_id),
CONSTRAINT FK_shop_cart_problems FOREIGN KEY ( problem_id) REFERENCES dbo.problems ( problem_id)
);

GO

USE master;
GO
