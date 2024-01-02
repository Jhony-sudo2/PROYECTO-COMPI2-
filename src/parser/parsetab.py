
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADD ALTER AND ARROBA AS BASE BEGIN BOOL CADENA CASE CAST COLUMN COMA CONCATENA CONTAR CREATE DATA DATE DATETIME DECIMAL DECIMAL1 DECLARE DELETE DIFERENTE DIVIDE DROP ELSE END EQUALS EXEC FROM FUNCTION HOY ID IF INSERT INT INTO KEY LPAREN MAYORIQ MAYORQ MENORIQ MENORQ MINUS NCHAR NOT NOT1 NULL NUMBER NVARCHAR OR PCOMA PLUS PRIMARY PROCEDURE PUNTO REFERENCES RETURN RPAREN SELECT SET SUBSTRAER SUMA TABLE THEN TIMES TRUNCATE UPDATE USAR VALUES WHEN WHERE\n    initial : produccion initial\n            | produccion\n    \n    seleccionardb : USAR ID\n    \n    produccion  : create PCOMA\n                | createdb PCOMA\n                | compartidas PCOMA\n                | seleccionardb PCOMA\n                | funcion\n                | procedure\n                | llamado PCOMA\n    \n    compartidas : insert\n                | select\n                | update\n                | truncate\n                | drop\n                | alter\n                | delete\n    \n    createdb : CREATE DATA BASE ID      \n    \n    create      : CREATE TABLE ID LPAREN  defcreate RPAREN      \n    \n    defcreate   : campo COMA defcreate\n                | campo\n    \n        campo   : ID tipodato restriccion\n                | ID tipodato\n    \n    restriccion   : NOT NULL\n            | PRIMARY KEY foranea\n            | PRIMARY KEY\n            | foranea      \n    \n    foranea : REFERENCES ID LPAREN ID RPAREN\n    \n    tipodato  : INT\n                | DECIMAL\n                | BOOL\n                | NVARCHAR LPAREN NUMBER RPAREN\n                | NCHAR LPAREN NUMBER RPAREN\n                | DATE\n                | DATETIME\n    \n    select  : SELECT funcionesdefinidas\n            | SELECT selectmultiple\n    \n    selectmultiple  : listacolumn FROM valores WHERE condiciones\n                    | listacolumn FROM valores\n    \n    listacolumn : valorescolumna COMA listacolumn\n                | valorescolumna\n                | TIMES\n    \n    valorescolumna  : ID PUNTO ID\n                    | ID\n                    | funcionesdefinidas\n                    | llamado\n    \n    funcionesdefinidas :  CONCATENA LPAREN factor COMA factor RPAREN\n                    |  SUBSTRAER LPAREN CADENA COMA NUMBER COMA NUMBER RPAREN\n                    |  HOY LPAREN RPAREN\n                    |  CONTAR LPAREN TIMES RPAREN FROM ID\n                    |  SUMA LPAREN ID RPAREN FROM ID\n                    |  CAST\n    \n    alter   : ALTER TABLE ID ADD COLUMN ID tipodato\n            | ALTER TABLE ID DROP COLUMN ID\n    \n    truncate    : TRUNCATE TABLE ID \n    \n    drop : DROP TABLE ID\n         | DROP COLUMN ID  \n    \n    insert      : INSERT INTO ID parametrosi VALUES entradas\n    \n    parametrosi  : LPAREN valores RPAREN\n    \n    entradas  : LPAREN valentradas RPAREN\n    \n    valentradas  : expression COMA valentradas\n                 | expression\n    \n    valores : ID COMA valores\n            | ID     \n    \n    update  : UPDATE ID SET cambios WHERE ID EQUALS expression\n            | UPDATE ID SET cambios WHERE condiciones\n    \n    cambios : campocambios COMA cambios\n            | campocambios    \n    \n    campocambios : ID EQUALS expression   \n    \n    delete  : DELETE FROM ID WHERE ID EQUALS expression\n    \n        variable : DECLARE ARROBA ID tipodato\n                | SET ARROBA ID EQUALS valorvar\n    \n    valorvar : expression\n            | funcionesdefinidas\n    \n    initial2 : opespeciales initial2\n            | opespeciales\n    \n    opespeciales : if PCOMA\n                | variable PCOMA\n                | compartidas PCOMA\n                | case PCOMA\n    \n    funcion  : CREATE FUNCTION ID LPAREN parametros RPAREN RETURN tipodato AS BEGIN initial2 RETURN expression PCOMA END\n    \n    parametros  : ARROBA ID tipodato COMA parametros\n                | ARROBA ID tipodato\n    \n    procedure  : CREATE PROCEDURE ID LPAREN parametros RPAREN  AS BEGIN initial2 END\n    \n    llamado : EXEC ID entradas\n            | ID entradas\n            | ID LPAREN RPAREN\n    \n    if  : IF LPAREN condiciones RPAREN BEGIN initial2 END\n        | IF LPAREN condiciones RPAREN BEGIN initial2 END ELSE BEGIN initial2 END\n    \n    condiciones : condicion\n                | condicion explogicas condiciones\n    \n    condicion : expression toperador expression\n    \n    toperador    : EQUALS\n                | DIFERENTE\n                | MAYORQ\n                | MENORQ\n                | MAYORIQ\n                | MENORIQ\n    \n    explogicas  : AND\n                | OR\n                | NOT1\n    \n    case : CASE casos END\n         | CASE casos ELSE THEN initial2 END\n    \n    casos  : WHEN condiciones THEN initial2 casos\n           | WHEN condiciones THEN initial2\n    \n    expression : expression PLUS term\n               | expression MINUS term\n               | term\n    \n    term : term TIMES factor2\n         | term DIVIDE factor2\n         | factor2\n    \n    factor2 : LPAREN expression RPAREN\n            | factor\n    \n    factor : NUMBER\n           | DECIMAL1\n           | CADENA\n           | ARROBA ID\n           | ID PUNTO ID\n           | ID\n    '
    
_lr_action_items = {'CREATE':([0,2,7,8,29,30,31,32,33,243,279,],[10,10,-8,-9,-4,-5,-6,-7,-10,-84,-81,]),'USAR':([0,2,7,8,29,30,31,32,33,243,279,],[19,19,-8,-9,-4,-5,-6,-7,-10,-84,-81,]),'EXEC':([0,2,7,8,22,29,30,31,32,33,88,243,279,],[20,20,-8,-9,20,-4,-5,-6,-7,-10,20,-84,-81,]),'ID':([0,2,7,8,19,20,22,23,29,30,31,32,33,34,36,37,39,42,57,58,59,60,61,63,67,77,79,81,85,86,87,88,89,95,99,102,103,104,105,106,109,125,130,141,145,146,147,148,149,150,151,162,170,171,182,187,198,199,200,201,202,203,204,205,206,207,208,209,225,243,249,250,251,253,262,265,279,],[11,11,-8,-9,40,41,50,56,-4,-5,-6,-7,-10,62,64,65,66,80,90,91,92,93,94,96,66,107,66,66,114,115,117,50,120,126,132,66,66,66,66,66,117,152,164,66,66,117,66,177,120,180,181,126,196,197,66,214,66,-99,-100,-101,66,-93,-94,-95,-96,-97,-98,66,241,-84,66,257,258,66,66,66,-81,]),'INSERT':([0,2,7,8,29,30,31,32,33,219,231,242,243,245,246,247,248,266,267,269,279,282,],[21,21,-8,-9,-4,-5,-6,-7,-10,21,21,21,-84,-77,-78,-79,-80,21,21,21,-81,21,]),'SELECT':([0,2,7,8,29,30,31,32,33,219,231,242,243,245,246,247,248,266,267,269,279,282,],[22,22,-8,-9,-4,-5,-6,-7,-10,22,22,22,-84,-77,-78,-79,-80,22,22,22,-81,22,]),'UPDATE':([0,2,7,8,29,30,31,32,33,219,231,242,243,245,246,247,248,266,267,269,279,282,],[23,23,-8,-9,-4,-5,-6,-7,-10,23,23,23,-84,-77,-78,-79,-80,23,23,23,-81,23,]),'TRUNCATE':([0,2,7,8,29,30,31,32,33,219,231,242,243,245,246,247,248,266,267,269,279,282,],[24,24,-8,-9,-4,-5,-6,-7,-10,24,24,24,-84,-77,-78,-79,-80,24,24,24,-81,24,]),'DROP':([0,2,7,8,29,30,31,32,33,93,219,231,242,243,245,246,247,248,266,267,269,279,282,],[25,25,-8,-9,-4,-5,-6,-7,-10,124,25,25,25,-84,-77,-78,-79,-80,25,25,25,-81,25,]),'ALTER':([0,2,7,8,29,30,31,32,33,219,231,242,243,245,246,247,248,266,267,269,279,282,],[26,26,-8,-9,-4,-5,-6,-7,-10,26,26,26,-84,-77,-78,-79,-80,26,26,26,-81,26,]),'DELETE':([0,2,7,8,29,30,31,32,33,219,231,242,243,245,246,247,248,266,267,269,279,282,],[27,27,-8,-9,-4,-5,-6,-7,-10,27,27,27,-84,-77,-78,-79,-80,27,27,27,-81,27,]),'$end':([1,2,7,8,28,29,30,31,32,33,243,279,],[0,-2,-8,-9,-1,-4,-5,-6,-7,-10,-84,-81,]),'PCOMA':([3,4,5,6,9,12,13,14,15,16,17,18,38,40,43,44,52,66,68,71,72,73,74,75,76,78,90,91,92,96,101,107,112,116,117,132,133,135,136,137,138,154,155,156,159,160,161,166,172,173,175,178,181,194,196,197,210,211,221,222,223,226,227,232,233,234,235,240,259,264,268,270,271,272,277,280,284,],[29,30,31,32,33,-11,-12,-13,-14,-15,-16,-17,-86,-3,-36,-37,-52,-119,-87,-108,-111,-113,-114,-115,-116,-85,-55,-56,-57,-18,-60,-117,-49,-39,-64,-118,-112,-106,-107,-109,-110,-29,-30,-31,-34,-35,-19,-58,-38,-90,-63,-66,-54,-47,-50,-51,-53,-70,-91,-92,-65,-32,-33,245,246,247,248,-48,-102,-71,275,-72,-73,-74,-103,-88,-89,]),'TABLE':([10,24,25,26,],[34,57,58,60,]),'DATA':([10,],[35,]),'FUNCTION':([10,],[36,]),'PROCEDURE':([10,],[37,]),'LPAREN':([11,39,41,45,46,47,48,50,51,62,64,65,67,79,80,102,103,104,105,106,139,145,147,148,157,158,182,198,199,200,201,202,203,204,205,206,207,208,209,214,236,249,253,262,265,],[39,67,79,81,82,83,84,39,86,95,97,98,67,67,109,67,67,67,67,67,79,67,67,67,188,189,67,67,-99,-100,-101,67,-93,-94,-95,-96,-97,-98,67,225,249,67,67,67,67,]),'INTO':([21,],[42,]),'CONCATENA':([22,88,265,],[45,45,45,]),'SUBSTRAER':([22,88,265,],[46,46,46,]),'HOY':([22,88,265,],[47,47,47,]),'CONTAR':([22,88,265,],[48,48,48,]),'SUMA':([22,88,265,],[51,51,51,]),'CAST':([22,88,265,],[52,52,52,]),'TIMES':([22,66,71,72,73,74,75,76,84,88,107,132,133,135,136,137,138,177,],[49,-119,105,-111,-113,-114,-115,-116,113,49,-117,-118,-112,105,105,-109,-110,-119,]),'COLUMN':([25,123,124,],[59,150,151,]),'FROM':([27,38,43,49,50,52,53,54,55,68,78,101,112,114,118,119,143,144,194,196,197,240,],[61,-86,-45,-42,-44,-52,87,-41,-46,-87,-85,-60,-49,-43,-40,-45,170,171,-47,-50,-51,-48,]),'BASE':([35,],[63,]),'COMA':([38,43,50,52,54,55,66,68,70,71,72,73,74,75,76,78,101,107,110,111,112,114,117,119,122,128,132,133,135,136,137,138,153,154,155,156,159,160,169,176,183,186,192,194,196,197,212,213,224,226,227,240,254,],[-86,-45,-44,-52,88,-46,-119,-87,102,-108,-111,-113,-114,-115,-116,-85,-60,-117,141,142,-49,-43,146,-45,149,162,-118,-112,-106,-107,-109,-110,-23,-29,-30,-31,-34,-35,195,-69,-22,-27,218,-47,-50,-51,-24,-26,-25,-32,-33,-48,-28,]),'RPAREN':([39,66,69,70,71,72,73,74,75,76,83,100,107,113,115,117,127,128,129,131,132,133,134,135,136,137,138,140,153,154,155,156,159,160,168,173,175,183,186,190,192,212,213,215,216,220,221,222,224,226,227,229,241,254,256,],[68,-119,101,-62,-108,-111,-113,-114,-115,-116,112,133,-117,143,144,-64,161,-21,163,165,-118,-112,-61,-106,-107,-109,-110,167,-23,-29,-30,-31,-34,-35,194,-90,-63,-22,-27,-20,-83,-24,-26,226,227,240,-91,-92,-25,-32,-33,-82,254,-28,263,]),'NUMBER':([39,67,79,81,102,103,104,105,106,141,142,145,147,148,182,188,189,195,198,199,200,201,202,203,204,205,206,207,208,209,249,253,262,265,],[74,74,74,74,74,74,74,74,74,74,169,74,74,74,74,215,216,220,74,-99,-100,-101,74,-93,-94,-95,-96,-97,-98,74,74,74,74,74,]),'DECIMAL1':([39,67,79,81,102,103,104,105,106,141,145,147,148,182,198,199,200,201,202,203,204,205,206,207,208,209,249,253,262,265,],[75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,-99,-100,-101,75,-93,-94,-95,-96,-97,-98,75,75,75,75,75,]),'CADENA':([39,67,79,81,82,102,103,104,105,106,141,145,147,148,182,198,199,200,201,202,203,204,205,206,207,208,209,249,253,262,265,],[76,76,76,76,111,76,76,76,76,76,76,76,76,76,76,76,-99,-100,-101,76,-93,-94,-95,-96,-97,-98,76,76,76,76,76,]),'ARROBA':([39,67,79,81,97,98,102,103,104,105,106,141,145,147,148,182,198,199,200,201,202,203,204,205,206,207,208,209,218,237,238,249,253,262,265,],[77,77,77,77,130,130,77,77,77,77,77,77,77,77,77,77,77,-99,-100,-101,77,-93,-94,-95,-96,-97,-98,77,130,250,251,77,77,77,77,]),'PUNTO':([50,66,177,],[85,99,99,]),'SET':([56,219,231,242,245,246,247,248,266,267,269,282,],[89,238,238,238,-77,-78,-79,-80,238,238,238,238,]),'DIVIDE':([66,71,72,73,74,75,76,107,132,133,135,136,137,138,177,],[-119,106,-111,-113,-114,-115,-116,-117,-118,-112,106,106,-109,-110,-119,]),'PLUS':([66,70,71,72,73,74,75,76,100,107,132,133,135,136,137,138,174,176,177,211,222,223,268,271,],[-119,103,-108,-111,-113,-114,-115,-116,103,-117,-118,-112,-106,-107,-109,-110,103,103,-119,103,103,103,103,103,]),'MINUS':([66,70,71,72,73,74,75,76,100,107,132,133,135,136,137,138,174,176,177,211,222,223,268,271,],[-119,104,-108,-111,-113,-114,-115,-116,104,-117,-118,-112,-106,-107,-109,-110,104,104,-119,104,104,104,104,104,]),'EQUALS':([66,71,72,73,74,75,76,107,120,132,133,135,136,137,138,152,174,177,258,],[-119,-108,-111,-113,-114,-115,-116,-117,147,-118,-112,-106,-107,-109,-110,182,203,209,265,]),'DIFERENTE':([66,71,72,73,74,75,76,107,132,133,135,136,137,138,174,177,],[-119,-108,-111,-113,-114,-115,-116,-117,-118,-112,-106,-107,-109,-110,204,-119,]),'MAYORQ':([66,71,72,73,74,75,76,107,132,133,135,136,137,138,174,177,],[-119,-108,-111,-113,-114,-115,-116,-117,-118,-112,-106,-107,-109,-110,205,-119,]),'MENORQ':([66,71,72,73,74,75,76,107,132,133,135,136,137,138,174,177,],[-119,-108,-111,-113,-114,-115,-116,-117,-118,-112,-106,-107,-109,-110,206,-119,]),'MAYORIQ':([66,71,72,73,74,75,76,107,132,133,135,136,137,138,174,177,],[-119,-108,-111,-113,-114,-115,-116,-117,-118,-112,-106,-107,-109,-110,207,-119,]),'MENORIQ':([66,71,72,73,74,75,76,107,132,133,135,136,137,138,174,177,],[-119,-108,-111,-113,-114,-115,-116,-117,-118,-112,-106,-107,-109,-110,208,-119,]),'WHERE':([66,71,72,73,74,75,76,94,107,116,117,121,122,132,133,135,136,137,138,175,176,179,],[-119,-108,-111,-113,-114,-115,-116,125,-117,145,-64,148,-68,-118,-112,-106,-107,-109,-110,-63,-69,-67,]),'AND':([66,71,72,73,74,75,76,107,132,133,135,136,137,138,173,222,],[-119,-108,-111,-113,-114,-115,-116,-117,-118,-112,-106,-107,-109,-110,199,-92,]),'OR':([66,71,72,73,74,75,76,107,132,133,135,136,137,138,173,222,],[-119,-108,-111,-113,-114,-115,-116,-117,-118,-112,-106,-107,-109,-110,200,-92,]),'NOT1':([66,71,72,73,74,75,76,107,132,133,135,136,137,138,173,222,],[-119,-108,-111,-113,-114,-115,-116,-117,-118,-112,-106,-107,-109,-110,201,-92,]),'THEN':([66,71,72,73,74,75,76,107,132,133,135,136,137,138,173,221,222,260,261,],[-119,-108,-111,-113,-114,-115,-116,-117,-118,-112,-106,-107,-109,-110,-90,-91,-92,266,267,]),'ADD':([93,],[123,]),'VALUES':([108,167,],[139,-59,]),'INT':([126,164,180,191,257,],[154,154,154,154,154,]),'DECIMAL':([126,164,180,191,257,],[155,155,155,155,155,]),'BOOL':([126,164,180,191,257,],[156,156,156,156,156,]),'NVARCHAR':([126,164,180,191,257,],[157,157,157,157,157,]),'NCHAR':([126,164,180,191,257,],[158,158,158,158,158,]),'DATE':([126,164,180,191,257,],[159,159,159,159,159,]),'DATETIME':([126,164,180,191,257,],[160,160,160,160,160,]),'NOT':([153,154,155,156,159,160,226,227,],[184,-29,-30,-31,-34,-35,-32,-33,]),'PRIMARY':([153,154,155,156,159,160,226,227,],[185,-29,-30,-31,-34,-35,-32,-33,]),'REFERENCES':([153,154,155,156,159,160,213,226,227,],[187,-29,-30,-31,-34,-35,187,-32,-33,]),'AS':([154,155,156,159,160,165,217,226,227,],[-29,-30,-31,-34,-35,193,228,-32,-33,]),'RETURN':([163,231,244,245,246,247,248,255,],[191,-76,-75,-77,-78,-79,-80,262,]),'NULL':([184,],[212,]),'KEY':([185,],[213,]),'BEGIN':([193,228,263,281,],[219,242,269,282,]),'IF':([219,231,242,245,246,247,248,266,267,269,282,],[236,236,236,-77,-78,-79,-80,236,236,236,236,]),'DECLARE':([219,231,242,245,246,247,248,266,267,269,282,],[237,237,237,-77,-78,-79,-80,237,237,237,237,]),'CASE':([219,231,242,245,246,247,248,266,267,269,282,],[239,239,239,-77,-78,-79,-80,239,239,239,239,]),'END':([230,231,244,245,246,247,248,252,273,274,275,276,278,283,],[243,-76,-75,-77,-78,-79,-80,259,277,-105,279,280,-104,284,]),'WHEN':([231,239,244,245,246,247,248,274,],[-76,253,-75,-77,-78,-79,-80,253,]),'ELSE':([231,244,245,246,247,248,252,274,278,280,],[-76,-75,-77,-78,-79,-80,260,-105,-104,281,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'initial':([0,2,],[1,28,]),'produccion':([0,2,],[2,2,]),'create':([0,2,],[3,3,]),'createdb':([0,2,],[4,4,]),'compartidas':([0,2,219,231,242,266,267,269,282,],[5,5,234,234,234,234,234,234,234,]),'seleccionardb':([0,2,],[6,6,]),'funcion':([0,2,],[7,7,]),'procedure':([0,2,],[8,8,]),'llamado':([0,2,22,88,],[9,9,55,55,]),'insert':([0,2,219,231,242,266,267,269,282,],[12,12,12,12,12,12,12,12,12,]),'select':([0,2,219,231,242,266,267,269,282,],[13,13,13,13,13,13,13,13,13,]),'update':([0,2,219,231,242,266,267,269,282,],[14,14,14,14,14,14,14,14,14,]),'truncate':([0,2,219,231,242,266,267,269,282,],[15,15,15,15,15,15,15,15,15,]),'drop':([0,2,219,231,242,266,267,269,282,],[16,16,16,16,16,16,16,16,16,]),'alter':([0,2,219,231,242,266,267,269,282,],[17,17,17,17,17,17,17,17,17,]),'delete':([0,2,219,231,242,266,267,269,282,],[18,18,18,18,18,18,18,18,18,]),'entradas':([11,41,50,139,],[38,78,38,166,]),'funcionesdefinidas':([22,88,265,],[43,119,272,]),'selectmultiple':([22,],[44,]),'listacolumn':([22,88,],[53,118,]),'valorescolumna':([22,88,],[54,54,]),'valentradas':([39,79,102,],[69,69,134,]),'expression':([39,67,79,102,145,147,148,182,198,202,209,249,253,262,265,],[70,100,70,70,174,176,174,211,174,222,223,174,174,268,271,]),'term':([39,67,79,102,103,104,145,147,148,182,198,202,209,249,253,262,265,],[71,71,71,71,135,136,71,71,71,71,71,71,71,71,71,71,71,]),'factor2':([39,67,79,102,103,104,105,106,145,147,148,182,198,202,209,249,253,262,265,],[72,72,72,72,72,72,137,138,72,72,72,72,72,72,72,72,72,72,72,]),'factor':([39,67,79,81,102,103,104,105,106,141,145,147,148,182,198,202,209,249,253,262,265,],[73,73,73,110,73,73,73,73,73,168,73,73,73,73,73,73,73,73,73,73,73,]),'parametrosi':([80,],[108,]),'valores':([87,109,146,],[116,140,175,]),'cambios':([89,149,],[121,179,]),'campocambios':([89,149,],[122,122,]),'defcreate':([95,162,],[127,190,]),'campo':([95,162,],[128,128,]),'parametros':([97,98,218,],[129,131,229,]),'tipodato':([126,164,180,191,257,],[153,192,210,217,264,]),'condiciones':([145,148,198,249,253,],[172,178,221,256,261,]),'condicion':([145,148,198,249,253,],[173,173,173,173,173,]),'restriccion':([153,],[183,]),'foranea':([153,213,],[186,224,]),'explogicas':([173,],[198,]),'toperador':([174,],[202,]),'initial2':([219,231,242,266,267,269,282,],[230,244,255,273,274,276,283,]),'opespeciales':([219,231,242,266,267,269,282,],[231,231,231,231,231,231,231,]),'if':([219,231,242,266,267,269,282,],[232,232,232,232,232,232,232,]),'variable':([219,231,242,266,267,269,282,],[233,233,233,233,233,233,233,]),'case':([219,231,242,266,267,269,282,],[235,235,235,235,235,235,235,]),'casos':([239,274,],[252,278,]),'valorvar':([265,],[270,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> initial","S'",1,None,None,None),
  ('initial -> produccion initial','initial',2,'p_initial','parser.py',31),
  ('initial -> produccion','initial',1,'p_initial','parser.py',32),
  ('seleccionardb -> USAR ID','seleccionardb',2,'p_seleccionardb','parser.py',40),
  ('produccion -> create PCOMA','produccion',2,'p_produccion','parser.py',48),
  ('produccion -> createdb PCOMA','produccion',2,'p_produccion','parser.py',49),
  ('produccion -> compartidas PCOMA','produccion',2,'p_produccion','parser.py',50),
  ('produccion -> seleccionardb PCOMA','produccion',2,'p_produccion','parser.py',51),
  ('produccion -> funcion','produccion',1,'p_produccion','parser.py',52),
  ('produccion -> procedure','produccion',1,'p_produccion','parser.py',53),
  ('produccion -> llamado PCOMA','produccion',2,'p_produccion','parser.py',54),
  ('compartidas -> insert','compartidas',1,'p_compartidas','parser.py',60),
  ('compartidas -> select','compartidas',1,'p_compartidas','parser.py',61),
  ('compartidas -> update','compartidas',1,'p_compartidas','parser.py',62),
  ('compartidas -> truncate','compartidas',1,'p_compartidas','parser.py',63),
  ('compartidas -> drop','compartidas',1,'p_compartidas','parser.py',64),
  ('compartidas -> alter','compartidas',1,'p_compartidas','parser.py',65),
  ('compartidas -> delete','compartidas',1,'p_compartidas','parser.py',66),
  ('createdb -> CREATE DATA BASE ID','createdb',4,'p_createdb','parser.py',74),
  ('create -> CREATE TABLE ID LPAREN defcreate RPAREN','create',6,'p_create','parser.py',83),
  ('defcreate -> campo COMA defcreate','defcreate',3,'p_defcreate','parser.py',93),
  ('defcreate -> campo','defcreate',1,'p_defcreate','parser.py',94),
  ('campo -> ID tipodato restriccion','campo',3,'p_campo','parser.py',107),
  ('campo -> ID tipodato','campo',2,'p_campo','parser.py',108),
  ('restriccion -> NOT NULL','restriccion',2,'p_restriccion','parser.py',123),
  ('restriccion -> PRIMARY KEY foranea','restriccion',3,'p_restriccion','parser.py',124),
  ('restriccion -> PRIMARY KEY','restriccion',2,'p_restriccion','parser.py',125),
  ('restriccion -> foranea','restriccion',1,'p_restriccion','parser.py',126),
  ('foranea -> REFERENCES ID LPAREN ID RPAREN','foranea',5,'p_foranea','parser.py',141),
  ('tipodato -> INT','tipodato',1,'p_tipodato','parser.py',148),
  ('tipodato -> DECIMAL','tipodato',1,'p_tipodato','parser.py',149),
  ('tipodato -> BOOL','tipodato',1,'p_tipodato','parser.py',150),
  ('tipodato -> NVARCHAR LPAREN NUMBER RPAREN','tipodato',4,'p_tipodato','parser.py',151),
  ('tipodato -> NCHAR LPAREN NUMBER RPAREN','tipodato',4,'p_tipodato','parser.py',152),
  ('tipodato -> DATE','tipodato',1,'p_tipodato','parser.py',153),
  ('tipodato -> DATETIME','tipodato',1,'p_tipodato','parser.py',154),
  ('select -> SELECT funcionesdefinidas','select',2,'p_select','parser.py',172),
  ('select -> SELECT selectmultiple','select',2,'p_select','parser.py',173),
  ('selectmultiple -> listacolumn FROM valores WHERE condiciones','selectmultiple',5,'p_selectmultiple','parser.py',180),
  ('selectmultiple -> listacolumn FROM valores','selectmultiple',3,'p_selectmultiple','parser.py',181),
  ('listacolumn -> valorescolumna COMA listacolumn','listacolumn',3,'p_listacolumn','parser.py',193),
  ('listacolumn -> valorescolumna','listacolumn',1,'p_listacolumn','parser.py',194),
  ('listacolumn -> TIMES','listacolumn',1,'p_listacolumn','parser.py',195),
  ('valorescolumna -> ID PUNTO ID','valorescolumna',3,'p_valorescolumna','parser.py',206),
  ('valorescolumna -> ID','valorescolumna',1,'p_valorescolumna','parser.py',207),
  ('valorescolumna -> funcionesdefinidas','valorescolumna',1,'p_valorescolumna','parser.py',208),
  ('valorescolumna -> llamado','valorescolumna',1,'p_valorescolumna','parser.py',209),
  ('funcionesdefinidas -> CONCATENA LPAREN factor COMA factor RPAREN','funcionesdefinidas',6,'p_funcionesefinidas','parser.py',220),
  ('funcionesdefinidas -> SUBSTRAER LPAREN CADENA COMA NUMBER COMA NUMBER RPAREN','funcionesdefinidas',8,'p_funcionesefinidas','parser.py',221),
  ('funcionesdefinidas -> HOY LPAREN RPAREN','funcionesdefinidas',3,'p_funcionesefinidas','parser.py',222),
  ('funcionesdefinidas -> CONTAR LPAREN TIMES RPAREN FROM ID','funcionesdefinidas',6,'p_funcionesefinidas','parser.py',223),
  ('funcionesdefinidas -> SUMA LPAREN ID RPAREN FROM ID','funcionesdefinidas',6,'p_funcionesefinidas','parser.py',224),
  ('funcionesdefinidas -> CAST','funcionesdefinidas',1,'p_funcionesefinidas','parser.py',225),
  ('alter -> ALTER TABLE ID ADD COLUMN ID tipodato','alter',7,'p_alter','parser.py',247),
  ('alter -> ALTER TABLE ID DROP COLUMN ID','alter',6,'p_alter','parser.py',248),
  ('truncate -> TRUNCATE TABLE ID','truncate',3,'p_truncate','parser.py',259),
  ('drop -> DROP TABLE ID','drop',3,'p_drop','parser.py',267),
  ('drop -> DROP COLUMN ID','drop',3,'p_drop','parser.py',268),
  ('insert -> INSERT INTO ID parametrosi VALUES entradas','insert',6,'p_insert','parser.py',275),
  ('parametrosi -> LPAREN valores RPAREN','parametrosi',3,'p_parametrosi','parser.py',283),
  ('entradas -> LPAREN valentradas RPAREN','entradas',3,'p_entradas','parser.py',289),
  ('valentradas -> expression COMA valentradas','valentradas',3,'p_valentradas','parser.py',295),
  ('valentradas -> expression','valentradas',1,'p_valentradas','parser.py',296),
  ('valores -> ID COMA valores','valores',3,'p_valores','parser.py',305),
  ('valores -> ID','valores',1,'p_valores','parser.py',306),
  ('update -> UPDATE ID SET cambios WHERE ID EQUALS expression','update',8,'p_update','parser.py',318),
  ('update -> UPDATE ID SET cambios WHERE condiciones','update',6,'p_update','parser.py',319),
  ('cambios -> campocambios COMA cambios','cambios',3,'p_cambios','parser.py',329),
  ('cambios -> campocambios','cambios',1,'p_cambios','parser.py',330),
  ('campocambios -> ID EQUALS expression','campocambios',3,'p_campocambios','parser.py',341),
  ('delete -> DELETE FROM ID WHERE ID EQUALS expression','delete',7,'p_delete','parser.py',350),
  ('variable -> DECLARE ARROBA ID tipodato','variable',4,'p_variable','parser.py',358),
  ('variable -> SET ARROBA ID EQUALS valorvar','variable',5,'p_variable','parser.py',359),
  ('valorvar -> expression','valorvar',1,'p_valorvar','parser.py',371),
  ('valorvar -> funcionesdefinidas','valorvar',1,'p_valorvar','parser.py',372),
  ('initial2 -> opespeciales initial2','initial2',2,'p_initial2','parser.py',380),
  ('initial2 -> opespeciales','initial2',1,'p_initial2','parser.py',381),
  ('opespeciales -> if PCOMA','opespeciales',2,'p_opespeciales','parser.py',389),
  ('opespeciales -> variable PCOMA','opespeciales',2,'p_opespeciales','parser.py',390),
  ('opespeciales -> compartidas PCOMA','opespeciales',2,'p_opespeciales','parser.py',391),
  ('opespeciales -> case PCOMA','opespeciales',2,'p_opespeciales','parser.py',392),
  ('funcion -> CREATE FUNCTION ID LPAREN parametros RPAREN RETURN tipodato AS BEGIN initial2 RETURN expression PCOMA END','funcion',15,'p_funcion','parser.py',399),
  ('parametros -> ARROBA ID tipodato COMA parametros','parametros',5,'p_parametros','parser.py',406),
  ('parametros -> ARROBA ID tipodato','parametros',3,'p_parametros','parser.py',407),
  ('procedure -> CREATE PROCEDURE ID LPAREN parametros RPAREN AS BEGIN initial2 END','procedure',10,'p_procedure','parser.py',416),
  ('llamado -> EXEC ID entradas','llamado',3,'p_llamado','parser.py',423),
  ('llamado -> ID entradas','llamado',2,'p_llamado','parser.py',424),
  ('llamado -> ID LPAREN RPAREN','llamado',3,'p_llamado','parser.py',425),
  ('if -> IF LPAREN condiciones RPAREN BEGIN initial2 END','if',7,'p_if','parser.py',439),
  ('if -> IF LPAREN condiciones RPAREN BEGIN initial2 END ELSE BEGIN initial2 END','if',11,'p_if','parser.py',440),
  ('condiciones -> condicion','condiciones',1,'p_condiciones','parser.py',452),
  ('condiciones -> condicion explogicas condiciones','condiciones',3,'p_condiciones','parser.py',453),
  ('condicion -> expression toperador expression','condicion',3,'p_condicion','parser.py',462),
  ('toperador -> EQUALS','toperador',1,'p_toperador','parser.py',469),
  ('toperador -> DIFERENTE','toperador',1,'p_toperador','parser.py',470),
  ('toperador -> MAYORQ','toperador',1,'p_toperador','parser.py',471),
  ('toperador -> MENORQ','toperador',1,'p_toperador','parser.py',472),
  ('toperador -> MAYORIQ','toperador',1,'p_toperador','parser.py',473),
  ('toperador -> MENORIQ','toperador',1,'p_toperador','parser.py',474),
  ('explogicas -> AND','explogicas',1,'p_explogicas','parser.py',480),
  ('explogicas -> OR','explogicas',1,'p_explogicas','parser.py',481),
  ('explogicas -> NOT1','explogicas',1,'p_explogicas','parser.py',482),
  ('case -> CASE casos END','case',3,'p_case','parser.py',490),
  ('case -> CASE casos ELSE THEN initial2 END','case',6,'p_case','parser.py',491),
  ('casos -> WHEN condiciones THEN initial2 casos','casos',5,'p_casos','parser.py',502),
  ('casos -> WHEN condiciones THEN initial2','casos',4,'p_casos','parser.py',503),
  ('expression -> expression PLUS term','expression',3,'p_expression','parser.py',514),
  ('expression -> expression MINUS term','expression',3,'p_expression','parser.py',515),
  ('expression -> term','expression',1,'p_expression','parser.py',516),
  ('term -> term TIMES factor2','term',3,'p_term','parser.py',529),
  ('term -> term DIVIDE factor2','term',3,'p_term','parser.py',530),
  ('term -> factor2','term',1,'p_term','parser.py',531),
  ('factor2 -> LPAREN expression RPAREN','factor2',3,'p_factor2','parser.py',544),
  ('factor2 -> factor','factor2',1,'p_factor2','parser.py',545),
  ('factor -> NUMBER','factor',1,'p_factor','parser.py',554),
  ('factor -> DECIMAL1','factor',1,'p_factor','parser.py',555),
  ('factor -> CADENA','factor',1,'p_factor','parser.py',556),
  ('factor -> ARROBA ID','factor',2,'p_factor','parser.py',557),
  ('factor -> ID PUNTO ID','factor',3,'p_factor','parser.py',558),
  ('factor -> ID','factor',1,'p_factor','parser.py',559),
]
