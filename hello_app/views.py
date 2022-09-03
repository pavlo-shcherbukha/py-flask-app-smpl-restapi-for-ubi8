from datetime import datetime
from operator import truediv
from flask import Flask, render_template, request
import json
import logging
import datetime
import base64
import sys
import os


application = Flask(__name__)


# ============================================================================
# Формування RestAPi відповіді з помилкою у випадку не коректних вхідних даних 
# ============================================================================
class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, code, message, target=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.code = code 
        if target is not None:
            self.target = target
        else:
            self.target = ""
        self.payload = payload

    def to_dict(self):
        errdsc = {}
        errdsc["code"] = self.code
        errdsc["description"] = self.message
        errdsc["target"] = self.target
        rv={}
        rv["Error"]=errdsc
        rv["Error"]["Inner"]=dict(self.payload or ())
        return rv


# ============================================================================
# Формування RestAPi відповіді з помилкою у випадку не коректного методу
# ============================================================================
class UnexpectedHttpMethod(Exception):
    status_code = 404

    def __init__(self, code, message, target=None, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.code = code 
        if target is not None:
            self.target = target
        else:
            self.target = ""
        self.payload = payload

    def to_dict(self):
        errdsc = {}
        errdsc["code"] = self.code
        errdsc["description"] = self.message
        errdsc["target"] = self.target
        rv={}
        rv["Error"]=errdsc
        rv["Error"]["Inner"]=dict(self.payload or ())
        return rv




# =======================================================
# Перехоплювач помилок API  та формування відповіді
# =======================================================

@application.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    r=e.to_dict()
    return json.dumps(r), e.status_code, {'Content-Type':'application/json'}



@application.errorhandler( UnexpectedHttpMethod)
def unexpected_http_method_error(e):
    r=e.to_dict()
    return json.dumps(r), e.status_code, {'Content-Type':'application/json'}



logging.basicConfig(filename='myapp.log', level=logging.DEBUG)

#===================================================
# Функціф внутрішнього логера
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#===================================================
def log( a_msg='NoMessage', a_label='logger' ):
	dttm = datetime.datetime.now()
	ls_dttm = dttm.strftime('%d-%m-%y %I:%M:%S %p')
	logging.info(' ['+ls_dttm+'] '+ a_label + ': '+ a_msg)
	print(' ['+ls_dttm+'] '+ a_label + ': '+ a_msg)

log("This is log recird")


#=================================================
# Головна сторінка
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================
@application.route("/")
def home():
    log("render home.html" )
    return render_template("home.html")


#=================================================
# Про програму
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#=================================================
@application.route("/about/")
def about():
    return render_template("about.html")





#===========================================================================
#    *********** Сервісні  АПІ для роботи EDS ******************************
#===========================================================================

# =================================================================================
# Метод health check
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Повертає {'success':True} якщо контейнер працює
# =================================================================================
@application.route("/api/health", methods=["GET"])
def health():
    log('Health check', 'health')
    return json.dumps({'success':True}), 200, {'Content-Type':'application/json'}


# ================================================
# Імітація crud API для таблиці branch
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# POST: 
#   req: {  "brn_code": "01234", "brn_name": "Branch Name 1"} 
#   res: { "brn_id": "ertyyuyu" }
# ================================================
@application.route("/api/branch", methods=["GET","POST"])
def branch_srvc():
    l_label='branch_srvc'
    l_step='Start'
    log(l_step, l_label)
    body=None
    body_dict=None

    if request.method=='POST':
        l_label=l_label + '_' + request.method
        try:
            l_step='отримую тіло запиту'
            log(l_step, l_label)
            body = request.get_json()
            l_step='Розбираю тіло запиту в dict' + json.dumps(  body )
            log(l_step, l_label)
            body_dict = dict(body)
        except Exception as e:
            ex_code=e.code
            ex_name=e.name
            ex_dsc=e.description
            raise InvalidAPIUsage(  "InvalidAPIRequest",  "Помилка при отриманні запиту", target=l_label, status_code=ex_code, payload = {"code": ex_name, "description": ex_dsc} )              

        l_step='Перевіряю наявність  brn_code'
        log(l_step, l_label)
        if not 'brn_code' in body_dict:
            raise InvalidAPIUsage( "InvalidAPIRequestParams",  "No key [brn_code]", target=l_label,status_code=422, payload = {"code": "NoKey", "description": l_step } )
        
        l_step='Перевіряю наявність  brn_name'
        log(l_step, l_label)
        if not 'brn_name' in body_dict:
            raise InvalidAPIUsage( "InvalidAPIRequestParams",  "No key [brn_name]", target=l_label,status_code=422, payload = {"code": "NoKey", "description": l_step } )
        
        l_step='Готую результат'
        log(l_step, l_label)
        res={}
        res["brn_id"]="1234-5678-0001"
        l_step='Поветаю результат: ' +  json.dumps(  res ) 
        log(l_step, l_label)
        return json.dumps(  res ), 200, {'Content-Type':'application/json'}

    elif request.method=='GET':
        l_label=l_label + '_' + request.method
        l_step='Готую результат'
        log(l_step, l_label)
        res=[]
        brnx={}
        brnx["brn_id"]="1234-5678-0001"
        brnx["brn_code"]="001"
        brnx["brn_name"]="Head q"
        res.append(  brnx )

        brnx={}
        brnx["brn_id"]="2222-2222-2222-2222"
        brnx["brn_code"]="002"
        brnx["brn_name"]="Cheald 1"
        res.append(  brnx )

        brnx={}
        brnx["brn_id"]="3333-3333-3333-3333"
        brnx["brn_code"]="004"
        brnx["brn_name"]="Cheald 2"
        res.append(  brnx )


        l_step='Поветаю результат: ' +  json.dumps(  res ) 
        log(l_step, l_label)
        return json.dumps(  res ), 200, {'Content-Type':'application/json'}



    else:
        log('возвращаю ошибку о недопустимомо методе')
        raise UnexpectedHttpMethod( "UnexpectedHttpMethod",  "Не допустимий http метод", target='/api/sigdocument',status_code=404 )



@application.route("/api/branch/<brn_id>", methods=["GET","DELETE", "PUT"])
def branch_srvc_id(brn_id=None):
    l_label='branch_srvc_id'
    l_step='Start'
    log(l_step, l_label)
    if request.method=='DELETE':
        l_label=l_label + '_' + request.method
        print(brn_id)
        l_step='Видаляю параметр по brn_id=' + brn_id 
        log(l_step, l_label)
        res={}
        res['ok']=True
        return json.dumps(  res ), 200, {'Content-Type':'application/json'}
    elif request.method=='GET': 
        res={}
        res["brn_id"]=int(brn_id)
        res["brn_code"]="001"
        res["brn_name"]="Head q"
        return json.dumps(  res ), 200, {'Content-Type':'application/json'}

    elif request.method=='PUT':
        l_label=l_label + '_' + request.method
        try:
            l_step='отримую тіло запиту'
            log(l_step, l_label)
            body = request.get_json()
            l_step='Розбираю тіло запиту в dict' + json.dumps(  body )
            log(l_step, l_label)
            body_dict = dict(body)
        except Exception as e:
            ex_code=e.code
            ex_name=e.name
            ex_dsc=e.description
            raise InvalidAPIUsage(  "InvalidAPIRequest",  "Помилка при отриманні запиту", target=l_label, status_code=ex_code, payload = {"code": ex_name, "description": ex_dsc} )              

        l_step='Перевіряю наявність  brn_code'
        log(l_step, l_label)
        if not 'brn_code' in body_dict:
            raise InvalidAPIUsage( "InvalidAPIRequestParams",  "No key [brn_code]", target=l_label,status_code=422, payload = {"code": "NoKey", "description": l_step } )
        
        l_step='Перевіряю наявність  brn_name'
        log(l_step, l_label)
        if not 'brn_name' in body_dict:
            raise InvalidAPIUsage( "InvalidAPIRequestParams",  "No key [brn_name]", target=l_label,status_code=422, payload = {"code": "NoKey", "description": l_step } )
        
        l_step='Готую результат'
        log(l_step, l_label)
        res={}
        res["brn_id"]=int(brn_id)
        res["brn_code"]=body_dict["brn_code"]
        res["brn_name"]=body_dict["brn_name"]
        l_step="Відправляю результат " + json.dumps(  res )
        log(l_step, l_label)
        return json.dumps(  res ), 200, {'Content-Type':'application/json'}    



@application.route("/api/branchstat", methods=["GET"])
def branch_stat_with_params():
    l_label='branch_stat'
    l_step='Start'
    log(l_step, l_label)
    brn_id = request.args.get('brn_id')
    dts = request.args.get('dts')
    dtf = request.args.get('dtf')
    mode = request.args.get('mode')
    l_step='Перевіряю наявність  brn_id'
    log(l_step, l_label)
    if brn_id == None:
        raise InvalidAPIUsage( "InvalidAPIRequestParams",  "No key [brn_id]", target=l_label,status_code=422, payload = {"code": "NoKey", "description": l_step } )

    l_step='Перевіряю наявність dts'
    log(l_step, l_label)
    if dts == None:
        raise InvalidAPIUsage( "InvalidAPIRequestParams",  "No key [dts]", target=l_label,status_code=422, payload = {"code": "NoKey", "description": l_step } )

    l_step='Перевіряю наявність dtf'
    log(l_step, l_label)
    if dtf == None:
        raise InvalidAPIUsage( "InvalidAPIRequestParams",  "No key [dtf]", target=l_label,status_code=422, payload = {"code": "NoKey", "description": l_step } )

    l_step='Перевіряю наявність mode'
    log(l_step, l_label)
    if mode == None:
        raise InvalidAPIUsage( "InvalidAPIRequestParams",  "No key [mode]", target=l_label,status_code=422, payload = {"code": "NoKey", "description": l_step } )

    res={}
    res["brn_id"]=brn_id
    res["dts"]=dts
    res["dtf"]=dtf
    res["mode"]=mode
    l_step='Поветаю результат: ' +  json.dumps(  res ) 
    log(l_step, l_label)
    return json.dumps(  res ), 200, {'Content-Type':'application/json'}







