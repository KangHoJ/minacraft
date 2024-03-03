CREATE VIEW test_view2 AS 
SELECT a.*, b.name AS resident_name
FROM TOWNY_TOWNS a
LEFT OUTER JOIN TOWNY_RESIDENTS b ON a.mayor = b.name;

select * from test_view2;
drop view my_view; # view 삭제

select * from TOWNY_RESIDENTS;
select * from MoneyTable;

CREATE VIEW my_view3 AS
SELECT a.name as a_name, a.*, b.name as b_name, b.*
FROM plugin_lighteconomy.MoneyTable as a
LEFT JOIN plugin_towny.TOWNY_RESIDENTS as b ON a.name = b.name;

SELECT a_name, a.*, b_name, b.* FROM my_view3;



select * from plugin_loginsecurity.ls_players;
select * from plugin_lighteconomy.MoneyTable;
select * from plugin_lighteconomy.BankTable;

-- CREATE VIEW bank_money AS 
SELECT b.uuid,b.name,b.money as bankmoney,b.level as banklevel , m.isPlayer , m.money as usermoney , ls.registration_date as registrate , ls.last_login
FROM plugin_lighteconomy.BankTable as b
LEFT JOIN plugin_lighteconomy.MoneyTable as m ON b.uuid = m.uuid
LEFT join plugin_loginsecurity.ls_players as ls ON b.uuid = ls.unique_user_id;

CREATE VIEW uesrs AS 
SELECT b.uuid,b.name,b.money as bankmoney,b.level as banklevel , m.isPlayer , m.money as usermoney , ls.registration_date as registrate , ls.last_login
FROM plugin_loginsecurity.ls_players as ls
LEFT JOIN plugin_lighteconomy.MoneyTable as m ON ls.last_name = m.name
LEFT JOIN plugin_lighteconomy.BankTable as b ON ls.last_name = b.name;

select * from uesrs;






