from django.shortcuts import render,redirect,HttpResponse
import json
from app import My_Forms
from app import models
from app import MyJSONEncoder
from Function.run_workflow import url_request
from Function.run_workflow import sql
#from Function.run_workflow import run_workflow
from Function.run_workflow import run_workflow_a
from django.db import connection
import pymysql
import time
from django.db.models import Max 
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator
import os
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
import random
from json_data import workfliow_json
import math
import shutil
# from app import Timed_task

# Create your views here.



	
	
def home_000(request):
    #主界面
    return render(request,"home_000.html")
		
def rpa_000(request):
    #rpa节点
    return render(request,"rpa_000.html")
	
def rpa_Recording_000(request):
    #rpa录制接口
    if request.method=="POST":
        file_name=request.POST.get("file_name")
        file_url=request.POST.get("file_url")
        result=os.system("python -m playwright codegen --target python -o ./static/rpa_py/%s.py -b chromium %s" % (file_name,file_url))
        with open('./static/rpa_py/%s.py' % file_name, 'r', encoding='utf-8') as f:
            str_file=f.read()
            #f.read()
        data = {"code": 0, "msg":"成功", "data":str_file}
        return HttpResponse(json.dumps(data),content_type="application/json")
	
def rpa_test_000(request):
    #rpa测试接口
    if request.method=="POST":
        file_name=request.POST.get("file_name")
        result=os.system('python ./static/rpa_py/%s.py' % file_name)
        data = {"code": 0, "msg":"成功"}
        return HttpResponse(json.dumps(data),content_type="application/json")
	

def rpa_updata_000(request):
    #rpa文件更新接口
    if request.method=="POST":
        file_name=request.POST.get("file_name")
        rpa_txt=request.POST.get("rpa_txt")
        with open('./static/rpa_py/%s.py' % file_name, 'w', encoding='utf-8') as f:
            f.write(rpa_txt)
        data = {"code": 0, "msg":"成功", "data":[]}
        return HttpResponse(json.dumps(data),content_type="application/json")
	


def url_000(request):
    #api节点
    return render(request,"url_000.html")
		
def ui_000(request):
    #工作流界面
    if request.method=="GET":
        id=request.GET.get('id','None')
        print(id)
    json_data=workfliow_json.json_data
    return render(request,"ui_000.html",{"json_data":json_data,"id":{'id':id},"echo_val":json_data['workfliow']})
	
def mysql_000(request):
    return render(request,"mysql_000.html")
	
	
def mysql_000_test(request):
    '''mysql测试'''
    if request.method=="POST":
        host=request.POST.get('host')
        port=request.POST.get('port')
        user=request.POST.get('user')
        passwd=request.POST.get('passwd')
        db=request.POST.get('db')
        str_sql=request.POST.get('str_sql')
        print(host,int(port),user,passwd,db,'喊口号',str_sql)
        sql_val=sql.sql_lave(host,int(port),user,passwd,db).run_sql(str_sql)
        if sql_val[0]:
            print('我也不知道呀呀呀')
            val=MyJSONEncoder.MYSQL_JSON(sql_val[0],sql_val[1])
            data = {"code": 200, "msg":"成功", "data":val}
        else:
            data = {"code": 201, "msg":"成功", "data":str(sql_val[1])}
        return HttpResponse(json.dumps(data),content_type="application/json")
    data = {"code": 500, "msg":"失败"}
    return HttpResponse(json.dumps(data),content_type="application/json")
	
	
def mysql_000_connect(request):
    '''mysql连接'''
    if request.method=="POST":
        host=request.POST.get('host')
        port=request.POST.get('port')
        user=request.POST.get('user')
        passwd=request.POST.get('passwd')
        db=request.POST.get('db')
        try:
            sql.sql_lave(host,int(port),user,passwd,db)
            status=True
        except:
            status=False

    #data = {"code": 0, "msg":"成功", "data":r_text}
    data = {"code": 0, "msg":"成功","data":status}
    return HttpResponse(json.dumps(data),content_type="application/json")
	
	
def url_000_test(request):
    #接口验证
    if request.method=="POST":
        value=json.loads(request.POST.get('data'))

        r_p=url_request.Deal_with()
        r_text=r_p.request_data(value)

        data = {"code": 0, "msg":"成功", "data":r_text}
        return HttpResponse(json.dumps(data),content_type="application/json")
	
	
def if_000(request):
    #分支
    return render(request,"if_000.html")
	
	
def merge_000(request):
    #合并
    return render(request,"merge_000.html")


def condition_000(request):
    #连线判断
    return render(request,"condition_000.html")

def data_000(request):
    #参数配置界面
    return render(request,"data_000.html")


def Workflow_save(request):#保存的时候rpa没有对py文件进行更新在节点保存的时候更新比较好
    #保存工作流数据
    if request.method=="POST":
        Workflow_id=request.POST.get('Workflow_id')
        Workflow_name=request.POST.get('Workflow_name')
        Workflwow_obj=request.POST.get('Workflwow_obj')
        print(Workflwow_obj,'--------------------')
        Date=request.POST.get('Date')
        workfliow_json.json_data['workfliow'][Workflow_id]={
            "Workflow_id":Workflow_id,
            "Workflow_name":Workflow_name,
            "Workflwow_obj":Workflwow_obj,
            "Date":Date,
		}
		
        json_str=json.dumps(workfliow_json.json_data)
        if not workfliow_json.json_data['json_file_url']:
            #判断文件有没有保存或选择,没得的话让用户给文件命名
            data = {"code": 301, "msg":"成功","data":json_str}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            json_file_url=workfliow_json.json_data['json_file_url']
            with open(json_file_url, 'w') as f:
                f.write(json.dumps(json_str))
            data = {"code": 200, "msg":"成功"}
            return HttpResponse(json.dumps(data),content_type="application/json")
    data = {"code": 500, "msg":"失败"}
    return HttpResponse(json.dumps(data),content_type="application/json")

def Workflow_del(request):
    #删除工作流数据
    if request.method=="GET":
        Workflow_id=request.GET.get('id')
        if len(workfliow_json.json_data['workfliow'][Workflow_id])<2:
            data = {"code": 500, "msg":"工作流小于2个时无法被删除"}
            return HttpResponse(json.dumps(data),content_type="application/json")

        del workfliow_json.json_data['workfliow'][Workflow_id]
		
        json_str=json.dumps(workfliow_json.json_data)
        if not workfliow_json.json_data['json_file_url']:
            #判断文件有没有保存或选择,没得的话让用户给文件命名
            data = {"code": 301, "msg":"成功","data":json_str}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            json_file_url=workfliow_json.json_data['json_file_url']
            with open(json_file_url, 'w') as f:
                f.write(json.dumps(json_str))
            data = {"code": 200, "msg":"成功"}
            #return HttpResponse(json.dumps(data),content_type="application/json")
            return redirect("/ui_000/")
			
    data = {"code": 500, "msg":"失败"}
    return HttpResponse(json.dumps(data),content_type="application/json")


def Workflow_Reset(request):
    #重置工作流
    if request.method=="GET":
        Workflow_id=request.GET.get('id')
        print(workfliow_json.json_data['log'],"workfliow_json.json_data['log']")
		
        if not workfliow_json.json_data['log'].get(Workflow_id,None):
            data = {"code": 500, "msg":"没有执行结果"}
            return HttpResponse(json.dumps(data),content_type="application/json")
		
        del workfliow_json.json_data['log'][Workflow_id]
		
        json_str=json.dumps(workfliow_json.json_data)
        if not workfliow_json.json_data['json_file_url']:
            #判断文件有没有保存或选择,没得的话让用户给文件命名
            data = {"code": 301, "msg":"成功","data":json_str}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            json_file_url=workfliow_json.json_data['json_file_url']
            with open(json_file_url, 'w') as f:
                f.write(json.dumps(json_str))
            data = {"code": 200, "msg":"成功"}
            return HttpResponse(json.dumps(data),content_type="application/json")
            #return redirect("/ui_000/")
			
    data = {"code": 500, "msg":"失败"}
    return HttpResponse(json.dumps(data),content_type="application/json")






def file_server(request):
    #文件服务器
    if request.method=="POST":
        pass
    return render(request,"file_server.html")




def file_save(request):
    #保存文件file_name
    if request.method=="POST":
        file_name=request.POST.get('file_name')
        file_data=json.loads(request.POST.get('data'))
        print(file_name,'--------保存文件---------',file_data['json_file_url'])
        json_file_url="./json_data/json_file/%s.json" % file_name
        file_data['json_file_url']=json_file_url
        workfliow_json.json_data['json_file_url']=json_file_url
        with open(json_file_url, 'w') as f:
            f.write(json.dumps(file_data))	
        data = {"code": 200, "msg":"成功"}
        return HttpResponse(json.dumps(data),content_type="application/json")
    data = {"code": 500, "msg":"失败"}
    return HttpResponse(json.dumps(data),content_type="application/json")








def file_del(request):
    #删除文件
    if request.method=="GET":
        file_name=request.GET.get('file_name')
        print(json.loads(file_name)['Slist'],json.loads(file_name),'file_name-------------------')
        
        for i in json.loads(file_name)['Slist']:
            dirPath="./json_data/json_file/%s" % i
            #判断文件是否存在
            if(os.path.exists(dirPath)):
                os.remove(dirPath)
                
        data = {"code": 200, "msg":"成功"}
        return HttpResponse(json.dumps(data),content_type="application/json")




def file_import(request):
    #导入文件file_name
    if request.method=="GET":
        file_name=request.GET.get('file_name')
        print(file_name,'WENJ')
        json_file_url="./json_data/json_file/%s" % file_name
        with open(json_file_url, 'r', encoding='utf-8') as f:
            str_file=f.read()

        if isinstance(json.loads(str_file),str):
            workfliow=json.loads(json.loads(str_file))
        else:
            workfliow=json.loads(str_file)
        print(workfliow['workfliow'],'filefffffffffffffffffffffffffffffffffffff')
        workfliow_json.json_data['workfliow']=workfliow['workfliow']
        data = {"code": 200, "msg":"成功"}
        return HttpResponse(json.dumps(data),content_type="application/json")
    data = {"code": 500, "msg":"失败"}
    return HttpResponse(json.dumps(data),content_type="application/json")


def file_copy(request):
    #复制文件
    if request.method=="GET":
        file_name=request.GET.get('file_name')
        a=file_name[:-5]
        print(file_name,a,'分隔文件')
        source="./json_data/json_file/%s" % file_name
        target="./json_data/json_file/%s(副本).json" % file_name[:-5]

        try:
            shutil.copy(source, target)
            data = {"code": 200, "msg":"成功"}
            return HttpResponse(json.dumps(data),content_type="application/json")
        except IOError as e:
            print("Unable to copy file. %s" % e)
            data = {"code": 500, "msg":"Unable to copy file. %s" % e}
            return HttpResponse(json.dumps(data),content_type="application/json")
        except:
            print("Unexpected error:", sys.exc_info())		
            data = {"code": 500, "msg":"Unexpected error:%s" % os.sys.exc_info()}
            return HttpResponse(json.dumps(data),content_type="application/json")


def file_merge(request):
    #合并文件
    if request.method=="GET":
        file_name=request.GET.get('file_name')
        updata_name=request.GET.get('updata_name')
        updata_name="./json_data/json_file/%s.json" % updata_name



        new_workfliow={}
        new_log={}
        for i in json.loads(file_name)['Slist']:
            json_file_url="./json_data/json_file/%s" % i
            #workfliow_json.json_data['json_file_url']=json_file_url
            with open(json_file_url, 'r', encoding='utf-8') as f:
                str_file=f.read()
				
            if new_workfliow:
                #print(json.loads(str_file),'1111111111111111111111111111111111111111111111111111111',type(json.loads(str_file)))
                b=json.loads(str_file)['workfliow']
                new_workfliow.update(b)
                #print(new_workfliow,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
				
            else:
                #print(json.loads(str_file),'str_file',type(json.loads(str_file)))
                new_workfliow=json.loads(str_file)['workfliow']
				
				
            if new_log:
                #print(json.loads(str_file),'1111111111111111111111111111111111111111111111111111111',type(json.loads(str_file)))
                l=json.loads(str_file)['log']
                new_log.update(l)
                #print(new_log,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            else:
                #print(json.loads(str_file),'jjjjjjjjjjjjjjjjj',type(json.loads(str_file)))
                new_log=json.loads(str_file)['log']
                #print('sssssssssssssssssssssssssssssssss',new_log)
        #print(new_workfliow,'sssssssssssssssssssssssssssssssss',new_log)
        json_data={
            "workfliow":new_workfliow,
            "log":new_log,
            "json_file_url":updata_name
        }
        print(updata_name,'updata_nameupdata_nameupdata_name')
		
        #json_file_url="./json_data/json_file/%s.json" % updata_name
		
        #workfliow_json.json_data['json_file_url']=json_file_url
        with open(updata_name, 'w') as f:
            f.write(json.dumps(json_data))
		
		
        
        print(json_data,'sssssssssssssssssssssssssssssssss')

			
				
        data = {"code": 200, "msg":"成功"}
        return HttpResponse(json.dumps(data),content_type="application/json")
    data = {"code": 500, "msg":"失败"}
    return HttpResponse(json.dumps(data),content_type="application/json")


# def file_updata(request):
    # #编辑文件
    # if request.method=="GET":
        # file_name=request.GET.get('file_name')

        # json_file_url="./json_data/json_file/%s" % file_name
        # workfliow_json.json_data['json_file_url']=json_file_url
        # workfliow_json.json_data['json_file_url']=json_file_url
		
        # os.rename(src, dst)
		
        # data = {"code": 200, "msg":"成功"}
        # return HttpResponse(json.dumps(data),content_type="application/json")
    # data = {"code": 500, "msg":"失败"}
    # return HttpResponse(json.dumps(data),content_type="application/json")





def file_updata(request):
    #编辑文件
    if request.method=="GET":
        file_name=request.GET.get('file_name')
        updata_name=request.GET.get('updata_name')
        print(file_name,updata_name,'还有期待')
        file_name="./json_data/json_file/%s" % file_name
        updata_name="./json_data/json_file/%s.json" % updata_name
        os.rename(file_name, updata_name)
        data = {"code": 200, "msg":"成功"}
        return HttpResponse(json.dumps(data),content_type="application/json")
    data = {"code": 500, "msg":"失败"}
    return HttpResponse(json.dumps(data),content_type="application/json")







def Local_file(request):
    #本地文件管理
    json_file_url="./json_data/json_file/"
    file_list=[]
    print(os.walk(json_file_url),'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    for k in os.walk(json_file_url):
        print(k[2],'1111111111111111111111111111111111')
        for s in k[2]:
            file_name=s
            url=json_file_url+file_name
            # filePath = unicode(url,'utf8')
            dot=2
            size = os.path.getsize(url)
            #kb
            if 0 <= size < 1:
                human_size = str(round(size / 0.125, dot)) + 'b'
            # 字节 字节 Byte
            elif 1 <= size < 1024:
                human_size = str(round(size, dot)) + 'B'
            # 千字节 千字节 Kilo Byte
            elif math.pow(1024, 1) <= size < math.pow(1024, 2):
                human_size = str(round(size / math.pow(1024, 1), dot)) + 'KB'
            # 兆字节 兆 Mega Byte
            elif math.pow(1024, 2) <= size < math.pow(1024, 3):
                human_size = str(round(size / math.pow(1024, 2), dot)) + 'MB'
            # 吉字节 吉 Giga Byte
            elif math.pow(1024, 3) <= size < math.pow(1024, 4):
                human_size = str(round(size / math.pow(1024, 3), dot)) + 'GB'
			
            t = os.path.getmtime(url)
            timeArray = time.localtime(t)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            print(file_name,human_size,otherStyleTime,'ttttttttttttttttttt')
            file_dict={
                "file_name":file_name,
                "human_size":human_size,
                "otherStyleTime":otherStyleTime,
            }
            file_list.append(file_dict)
    return render(request,"file.html",{"file_list":file_list})




def run_workflow_api(request):
    #运行工作流
    if request.method=="GET":
        id=request.GET.get('id')
        val=workfliow_json.json_data.get('workfliow').get(id)
        workfliow_json.json_data['log'][id]={}#清空日志
        print(id,val,'骗鬼')
        # def list_r_data(data):
            # workfliow_json.json_data['log'][id]=data
        # #run_workflow.run_workflow().w_run(val,list_r_data)
        # run_workflow_a.run_data(val,list_r_data)

        def list_r_data(data):
            print(workfliow_json.json_data['log'],'------------------------',data)
            if workfliow_json.json_data['log']:#有参数则追加没有就新增
                data_dict={**workfliow_json.json_data['log'][id], **data}
                workfliow_json.json_data['log'][id]=data_dict
            else:
                workfliow_json.json_data['log'][id]=data
        run_workflow_a.run_data(val,list_r_data)

			
        json_file_url=workfliow_json.json_data['json_file_url']
        print(json_file_url,'json_file_url')
        file_data=json.dumps(workfliow_json.json_data)
        with open(json_file_url, 'w') as f:
            f.write(file_data)				
        data = {"code": 200, "msg":"成功"}
        return HttpResponse(json.dumps(data),content_type="application/json")
    data = {"code": 500, "msg":"失败"}
    return HttpResponse(json.dumps(data),content_type="application/json")


def Node_status(request):
    #执行时状态日志返回
    if request.method=="GET":
        id=request.GET.get('id')
        val=workfliow_json.json_data.get('workfliow').get(id)
        r_data=workfliow_json.json_data['log'].get(id,None)
        print(r_data,'r_datar_datar_datar_datar_datar_data')
        data = {"code": 200, "msg":"成功","data":r_data,"id":workfliow_json.json_data['log']}
        return HttpResponse(json.dumps(data),content_type="application/json")
    data = {"code": 500, "msg":"失败"}
    return HttpResponse(json.dumps(data),content_type="application/json")


#http://192.168.3.83:8063/TEST_POST/

#http://192.168.3.83:8063/emali/
#{"configId":247,"queryFields":[],"emali_url":"1104541868@qq.com"}
#http://api.qingyunke.com/api.php?key=free&appid=0&msg=你好


#api节点入参切换问题
#api节点回显貌似有问题,得重现
#hede body 状态没有回显
#保存时检查节点是否保存