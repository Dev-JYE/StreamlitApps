# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 14:37:52 2023

@author: PC-2308003!
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import pandas as pd
import streamlit as st
from gspread_dataframe import set_with_dataframe
from datetime import datetime, timedelta


def get_gsheet(date):
  scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
  # Create a connection object.
  credentials = service_account.Credentials.from_service_account_info(
      st.secrets["gcp_service_account"],
      scopes=[
          "https://www.googleapis.com/auth/spreadsheets",
          'https://spreadsheets.google.com/feeds', 
          'https://www.googleapis.com/auth/drive'
      ],
  )
  client = gspread.authorize(credentials)

  # 작업자별 누적 작업량이 기록된 시트 이름
  sheet_name = 'hpr_static'

# 현재 날짜를 가져오고, 이전 날짜를 계산
  sheet1_name = date
  today = datetime.strptime(date,'%y%m%d')
  
  weekago = datetime.strptime(date, '%y%m%d') - timedelta(days=7)
  
# 이전 날짜에 해당하는 시트 불러오기
  sheet1_name = date
  sheet2_name = weekago.strftime('%y%m%d')
  sheet1 = client.open(sheet_name).worksheet(sheet1_name)
  sheet2 = client.open(sheet_name).worksheet(sheet2_name)
# 데이터 읽어오기
  data1 = sheet1.get_all_records()
  data2 = sheet2.get_all_records()


  #미배분 파일 가져오기 (파일명 - key)
  df_t = pd.DataFrame(data1)
  df_l = pd.DataFrame(data2)
  
  
  df_l['작업수량'] = df_l['재할당']+df_l['검수 대기']+df_l['검수 완료']
  df_t['작업수량'] = df_t['재할당']+df_t['검수 대기']+df_t['검수 완료']

  df_l = df_l[['Domain','ID','작업수량']]
  df_t = df_t[['Domain','ID','작업수량']]


  tmp = pd.merge(df_t, df_l, how = 'left', on = ['Domain','ID'])

  tmp = tmp.fillna(0)

  tmp['일작업량'] = tmp['작업수량_x'] - tmp['작업수량_y']
  result = tmp.groupby('ID')['일작업량'].sum().reset_index()
  result = result.sort_values('일작업량', ascending=False)
  
  return result

# df_t, df_l = get_gsheet() # this week , last week



# df_l['작업수량'] = df_l['재할당']+df_l['검수 대기']+df_l['검수 완료']
# df_t['작업수량'] = df_t['재할당']+df_t['검수 대기']+df_t['검수 완료']

# df_l = df_l[['Domain','ID','작업수량','계']]
# df_t = df_t[['Domain','ID','작업수량','계']]


# tmp = pd.merge(df_t, df_l, how = 'left', on = ['Domain','ID'])

# tmp = tmp.fillna(0)

# tmp['일작업량'] = tmp['작업수량_x'] - tmp['작업수량_y']
# result = tmp.groupby('ID')['일작업량'].sum().reset_index()
# result = result.sort_values('일작업량', ascending=False)

# result['일작업량'].sum()

df4 = get_gsheet('231113')
df3 = get_gsheet('231120')

df4.to_excel('231113.xlsx')
df3.to_excel('231120.xlsx')





scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
  # Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
        ],
    )

client = gspread.authorize(credentials)

sheet_name = 'hpr_static'


df_1001 = client.open(sheet_name).worksheet('231001')
df_1010 = client.open(sheet_name).worksheet('231010')

df_1001 = df_1001.get_all_records()
df_1010 = df_1010.get_all_records()


#미배분 파일 가져오기 (파일명 - key)
df_1001 = pd.DataFrame(df_1001)
df_1010 = pd.DataFrame(df_1010)

df_1001['작업수량'] = df_1001['재할당']+df_1001['검수 대기']+df_1001['검수 완료']
df_1010['작업수량'] = df_1010['재할당']+df_1010['검수 대기']+df_1010['검수 완료']

df_1001 = df_1001[['Domain','ID','작업수량','계']]
df_1010 = df_1010[['Domain','ID','작업수량','계']]

tmp10 = pd.merge(df_1010, df_1001, how = 'outer', on = ['ID'])

tmp10 = tmp10.fillna(0)



tmp10['일작업량'] = tmp10['작업수량_x'] - tmp10['작업수량_y']
result = tmp.groupby('ID')['일작업량'].sum().reset_index()
result = result.sort_values('일작업량', ascending=False)

tmp = pd.merge(tmp, tmp10, how='outer', on= ['ID]'])


tmp.to_excel('weekly.xlsx', index=False)


df_10_1 = get_gsheet('231009')

def write_result_to_sheet(result_df):
    # 인증 설정
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            'https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive'
        ],
    )
    client = gspread.authorize(credentials)
    
    # 스프레드시트 열기
    spreadsheet = client.open("weekly") 
    
    
    worksheet = spreadsheet.worksheet('weekly')
    worksheet.clear()  # 시트 초기화
    set_with_dataframe(worksheet, result_df)  # 데이터프레임을 시트에 쓰기


write_result_to_sheet(tmp)
## get_gsheet()를 각 주마다 하고, pd.merge를 통해 주차별 result를 조인, xlsx로 뽑기.








