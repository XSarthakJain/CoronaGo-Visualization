from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import bs4
import requests
import pandas as pd
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def Landing(request):
	try:
		return render(request,'Covid/index.Html')
	except:
		return render(request,'Covid/NotFound.HTML')

def FAQ(request):
	try:
		return render(request,'Covid/Covid19FAQ.HTML')
	except:
		return render(request,'Covid/NotFound.HTML')


def IndiaMap(request):
	return render(request,'Covid/IndiaMap.HTML')
def data1(request):
	try:
		import requests
		url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"
		headers = {
		    'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
		    'x-rapidapi-key': ""
		    }

		response = requests.request("GET", url, headers=headers)

		data=response.text
		
		import json
		d2={}
		d2=json.loads(data)
		State_Name=[]
		Confirmed_Name=[]
		deaths_Case=[]
		Recovered_Case=[]
		InfectedCount=0
		DeathCount=0
		RecoveredCount=0
		State_Code=[]
		for i in (d2["state_wise"]):
			if(int(d2["state_wise"][i]["confirmed"])!=0):
				Confirmed_Name.append(int(d2["state_wise"][i]["confirmed"]))
				deaths_Case.append(int(d2["state_wise"][i]["deaths"]))
				Recovered_Case.append(int(d2["state_wise"][i]["recovered"]))
				State_Name.append(d2["state_wise"][i]["statecode"])
				State_Code.append(d2["state_wise"][i]["state"])
				InfectedCount=InfectedCount+int(d2["state_wise"][i]["confirmed"])
				DeathCount=DeathCount+int(d2["state_wise"][i]["deaths"])
				RecoveredCount=RecoveredCount+int(d2["state_wise"][i]["recovered"])
				
		data = {
			'StateName':State_Name,
			'ConfirmedCase':Confirmed_Name,
			'deathsCase':deaths_Case,
			'RecoveredCase':Recovered_Case,
			'InfectedCount':InfectedCount,
			'DeathCount':DeathCount,
			'RecoveredCount':RecoveredCount,
			'State_Code':State_Code
			}
		return JsonResponse(data)
	except:
		return render(request,'Covid/NotFound.HTML')



@csrf_exempt
def data2(request):
	try:
		state=request.POST.get('State','DefaultValue')
		print(state)
		url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"
		headers = {
			'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
			'x-rapidapi-key': "513c39709amshabd759dbcc2c80cp18a79ajsnef11a22431b7"
			}
		response = requests.request("GET", url, headers=headers)
		data=response.text
		
		import json
		d2={}
		d2=json.loads(data)
		State_Name=[]
		Confirmed_Name=[]
		deaths_Case=[]
		Recovered_Case=[]
		InfectedCount=0
		DeathCount=0
		RecoveredCount=0
		State_Code=[]
		District_Name=[]
		flag=True
		for i in (d2["state_wise"]):
			if(i==state):
				for j in (d2["state_wise"][i]["district"]):
					Confirmed_Name.append(int(d2["state_wise"][i]["district"][j]["confirmed"]))
					Recovered_Case.append(int(d2["state_wise"][i]["district"][j]["recovered"]))
					District_Name.append(j)
					flag=False
				if(flag==False):
					break
			if(flag==False):
					break
				
					
		data = {
			'DistrictName':District_Name,
			'ConfirmedCase':Confirmed_Name,
			'RecoveredCase':Recovered_Case
			
			}
		return JsonResponse(data)
	except:
		return render(request,'Covid/NotFound.HTML')



def Visualize(request):
	try:
		url="https://www.worldometers.info/coronavirus/?"
		data=requests.get(url)
		soup=bs4.BeautifulSoup(data.text,'html.parser')
			


		l=0
		totalCase=""
		NewCase=""
		DeathCase=""
		q="Total:"
		l=11
		for i in soup.findAll('td'):
			if(i.getText()==q):
				l=l-1
					
				 
			elif(l==3):
				totalCase=i.getText()
					
				l=l-1
			elif(l==2):
				NewCase=i.getText()
				l=l-1
			elif(l==1):
				DeathCase=i.getText()
				l=l-1
				break
		return render(request,'Covid/Visualization.HTML',{'totalCase':totalCase,"NewCase":NewCase,"DeathCase":DeathCase,"Region":"World"})
	except:
		return render(request,'Covid/NotFound.HTML')

def get_data(request):
	try:
		df=pd.read_excel("CountryCode.xlsx",sheet_name="Sheet1")
		url='https://www.worldometers.info/coronavirus/#c-all%22"'
		data=requests.get(url)
		soup=bs4.BeautifulSoup(data.text,'html.parser')
		code=""
		dfrm=pd.DataFrame()
		top=0
		val=0


		for country in soup.find_all('td'):
			if(code=="All"):
				dfrm.loc[top,val]=country.getText()
				val=val+1
				if val==13:
					top=top+1
					val=0
			   
			else:
				code=country.getText()
		dfrm_dummy=dfrm.loc[:,:4]
		dfrm_dummy.drop_duplicates(subset = 0,keep = 'last', inplace = True)
		dfrm_dummy.reset_index(drop=True,inplace=True)
		flag=False
		for i in range(len(dfrm_dummy)):
			flag=False
			for j in range(len(df)):
				if(dfrm_dummy.loc[i,0]==df.loc[j,3]):
					v11=df.loc[j,1]
					v12=df.loc[j,2]
					dfrm_dummy.loc[i,4]=v11
					dfrm_dummy.loc[i,5]=v12
					break  
		dfrm_dummy=dfrm_dummy[pd.notnull(dfrm_dummy[5])] 
		data = {
			'CountryName':dfrm_dummy[0].tolist(),
			'NewCases':dfrm_dummy[2].tolist(),
			'Death':dfrm_dummy[3].tolist(),
			'longitude':dfrm_dummy[5].tolist(),
			'latitude': dfrm_dummy[4].tolist(),
			'Infected':dfrm_dummy[1].tolist(),
			} 
		
		print("Workingggggggggggggggggggg")
		return JsonResponse(data)
	except:
		return render(request,'Covid/NotFound.HTML')

def ContactUs(request):
	try:
		return render(request,'Covid/ContactUs.Html')
	except:
		return render(request,'Covid/NotFound.HTML')

def AboutProject(request):
	try:
		return render(request,'Covid/AboutProject.Html')
	except:
		return render(request,'Covid/NotFound.HTML')
