#!/usr/bin/env python
"""工作流执行逻辑"""
import jsonpath
import json
#import url_request
from Function.run_workflow import url_request
import re
import os
import copy


#节点功能调用
class node_function:
	def __init__(self):
		'''节点逻辑'''
		pass
		
	def api_function(self):
		'''api功能'''
		pass

	def rpa_function(self):
		'''rpa功能'''
		pass


	def sql_function(self):
		'''sql功能'''
		pass


#节点逻辑处理
class node_logic:
	def __init__(self):
		'''节点逻辑'''
		pass
		
	def if_logic(self):
		'''判断'''
		if current_id in if_list:#判断属于判断节点,这里用起始端点会出现两次
			print('判断节点')
			if json.dumps(if_node[current_id]['Judgment_node'])=="{}":
				#判断里没有数据
				continue
			else:
				for condition_id in condition:#取出判断节点对应的判断条件数据,这里遍历几条连线
					if current_id==condition_id[:6] and Rear_id==condition_id[-6:]:
						list_state=[]
						for tj in condition[condition_id]:#遍历条件可能有多个
							if tj=="Workflow_name":
								continue
							elif condition[condition_id][tj]=="on":#开启的时候进行判断
								Parsing=if_node[current_id]['Judgment_node'][tj][0]#取出需要效验的判断条件,这个地方得加个表存节点返回数据
								if Parsing["node"] in api_list:
									G_list = api_node[Parsing["node"]]["Ginseng"]
									for G_dict in G_list:
										if Parsing['Ginseng'] == G_dict['title']:
											r_log=list_r_data[Parsing["node"]]#取返回值
											if G_dict['sex']=='JsonPath':
												try:#能转python对象
													r_log=json.loads(r_log['Return_parameter'])
													t1=jsonpath.jsonpath(r_log,G_dict['desc'])[0]#通过表达式取返回值中的参数取一组第一个
												except:
													t1=None
												Parsing['Compare']#0大于1小于2等于
												t2=Parsing['Judgment_value']#判断的值
											elif G_dict['sex']=='re':
												if r_log['Return_parameter']:#返回值没匹配到的时候直接返回
													t1=re.findall( G_dict['desc'] , r_log['Return_parameter'] ,re.M|re.S)[0]
													Parsing['Compare']#0大于1小于2等于
													t2=Parsing['Judgment_value']#判断的值
												
											else:
												print('找到未知的匹配类型')
											
											#大于小于用int等于用str
											if Parsing['Compare']=='0':
												state=int(t1)>int(t2)
											elif Parsing['Compare']=='1':
												state=int(t1)<int(t2)
											elif Parsing['Compare']=='2':
												state=str(t1).strip()==str(t2).strip()#转换成字符串且去除前后空格
											else:
												print('抓到一个未知的判断条件')
											
											list_state.append(state)
										
									
						
						#这里判断最终的是否通过,不通过则递归获取子节点添加到list
						state_i=True
						for state_j in list_state:
							state_i=state_i and state_j
						if not state_i:#这里添加到list
							def tortoise(data):
								tortoise_list.append(data)
								for  node_index_t in connections:
									current_id_t = connections[node_index_t]['current']#起点
									Rear_id_t = connections[node_index_t]['Rear']#终点
									if data==current_id_t:
										return tortoise(Rear_id_t)
									else:
										return
							tortoise(current_id)
		else:
			return None
							
		
		
	def merge_logic(self):
		'''合并'''
		if current_id in merge_list:#这是合并节点			
			condition_dict=copy.copy(merge_node[current_id])
			del condition_dict['Workflow_name']
			for i in condition_dict:
				if i in node_id_error:
					#当前触发Rear_id放递归
					def tortoise(data):
						tortoise_list.append(data)
						for  node_index_t in connections:
							current_id_t = connections[node_index_t]['current']#起点
							Rear_id_t = connections[node_index_t]['Rear']#终点
							if data==current_id_t:
								return tortoise(Rear_id_t)
							else:
								return
					tortoise(Rear_id)
					break
		else:
			return None
		
		
	def end_logic(self):
		'''终点'''
		if Rear_id not in list_current_id:#前置节点为判断的结束节点
			print('前置节点为判断的结束节点')
			if Rear_id not in tortoise_list:#判断不通过的子节点不走
				#这里走执行
				return True
		else:
			return None
		
		

#流程逻辑处理
class workflow(node_logic,node_function):
	def __init__(self,data):
		'''数据初始化处理'''
		WORK_DATA=json.loads(data['Workflwow_obj'])[list(json.loads(data['Workflwow_obj']).keys())[0]]
		#print(WORK_DATA,'WORK_DATA')
		self.list_r_data={}#存返回值
		self.node_id_error=[]#存返回状态做判断
		if WORK_DATA['api_node']!="None":
			self.api_node=json.loads(WORK_DATA['api_node'])
		else:
			self.api_node=WORK_DATA['api_node']
		
		if WORK_DATA['if_node']!="None":
			self.if_node=json.loads(WORK_DATA['if_node'])
		else:
			self.if_node=WORK_DATA['if_node']
		
		if WORK_DATA['rpa_node']!="None":
			self.rpa_node=json.loads(WORK_DATA['rpa_node'])
		else:
			self.rpa_node=WORK_DATA['rpa_node']
		
		if WORK_DATA['merge_node']!="None":
			self.merge_node=json.loads(WORK_DATA['merge_node'])
		else:
			self.merge_node=WORK_DATA['merge_node']
		
		if WORK_DATA['condition']!="None":
			self.condition=json.loads(WORK_DATA['condition'])
		else:
			self.condition=WORK_DATA['condition']
		

		self.connections=json.loads(WORK_DATA['connections'])
		self.list_current_id=[]#左端点
		self.list_Rear_id=[]#右端点
		if len(self.connections.keys()) > 0:#有连线时取出左右端点的放入list后面得用
			#遍历流程
			for node_index in self.connections:
				current_id = self.connections[node_index]['current']#起点
				Rear_id = self.connections[node_index]['Rear']#终点
				self.list_current_id.append(current_id)
				self.list_Rear_id.append(Rear_id)
			
		#拿到判断节点的id后面流程做判断
		self.if_list=[]
		for if_val in self.if_node:
			self.if_list.append(if_val)
		
		#拿到合并节点的id后面流程做判断
		self.merge_list=[]
		for merge_val in self.merge_node:
			self.merge_list.append(merge_val)
		print(self.merge_node,'-----node-------',self.merge_list)
		
		#apilist
		self.api_list=[]
		for api_val in self.api_node:
			self.api_list.append(api_val)
		
		#rpa_list
		self.rpa_list=[]
		for  rpa_val in self.rpa_node:
			self.rpa_list.append(rpa_val)
		
		#判断的节点id
		self.tortoise_list=[]
		
				
	def run_node(self,Rear_id,obj):
		'''执行节点'''
		if Rear_id in self.api_list:#属于api节点
			api_node_dict={}
			api_node_dict[Rear_id] = api_node[Rear_id]
			#这里调api的东西
			r_p=url_request.Deal_with()
			try:
				r_text=r_p.request_data(api_node_dict)
				status="Success"
			except:
				status="error"
				r_text=None
			Return_val={
				"node_id":Rear_id,
				"Return_parameter":r_text,
				"status":status
			}
			self.list_r_data[Rear_id]=Return_val#添加每个节点的返回值到dict
			obj(list_r_data)#传给回调函数

			#obj(Return_val)#这个地方参数吐出去做节点状态变更

		elif Rear_id in self.rpa_list:#属于rpa节点
			try:
				os.system('python ./static/rpa_py/%s.py' % self.rpa_node[Rear_id]['file_name'])
				status='Success'
				rp='None'
			except e:
				status='error'
				rp=e
				self.node_id_error.append(Rear_id)
			Return_val={
			   "node_id":Rear_id,
				"Return_parameter":rp,
				"status":status
			}
			self.list_r_data[Rear_id]=Return_val#添加每个节点的返回值到dict
			obj(list_r_data)#传给回调函数

			#obj(Return_val)#这个地方参数吐出去做节点状态变更
				
				
	def run_logic(self,data,obj):
		'''执行'''
		if len(self.connections.keys())>0:#多个节点时场景
			#遍历流程
			for  node_index in self.connections:
				current_id = self.connections[node_index]['current']#起点
				Rear_id = self.connections[node_index]['Rear']#终点
				#执行节点前先判断属于判断/合并,结尾节点
				
				#if_logic()
				#merge_logic()
				#end_logic()
				#run_node()
				
				
				
		else:#单节点场景


