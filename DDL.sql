--清空資料庫
USE Master;
GO
DROP DATABASE IF EXISTS big_DB;
GO

--資料庫
CREATE DATABASE big_DB;

--切換使用中的資料庫
USE big_DB;
GO

--建立tables
CREATE TABLE dbo.survey
(
survey_id int,  
age_type int,
survey_type int,
year int,
wave int
)

CREATE TABLE dbo.survey_problem
(
survey_id int,
problem_id varchar( 30),
)

CREATE TABLE dbo.answer
(
answer_id bigint,
problem_id varcahr( 30),
survey_id int,
answer nvarchar( 4000)
)


CREATE TABLE dbo.problems
(
problem_id varchar( 4000),
description nvarchar( 4000),
class_id int,
problem_type nvarchar( 4000)
);
    

CREATE TABLE dbo.tag_value
(
problem_id nvarchar( 4000),
tag_value int,
tag_name nvarchar( 4000)
);

CREATE TABLE dbo.account
(
user_id int,
account_name nvarchar( 4000),
email nvarchar( 4000),
password varchar( 4000),
group int
);

CREATE TABLE dbo.auth_group
(
class_id int,
class nvarchar( 4000),
min_auth_group int
);

CREATE TABLE dbo.group_change_log
(
datetime datetime,
admin_id int,
user_id int,
old_group int,
new_group int,
reason nvarchar( 4000)
);

GO
