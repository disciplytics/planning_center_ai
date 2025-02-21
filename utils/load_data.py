import asyncio
import pandas as pd

def load_data(pco):
  async def fetch_peopl_data(query_date = None):
    try:
      people_data_df = pd.DataFrame()
      people_include_df = pd.DataFrame()
      for person in pco.iterate('/people/v2/people?include=addresses,emails,field_data,households,inactive_reason,marital_status,organization,phone_numbers,primary_campus,school'):
        people_data_df = pd.concat([people_data_df, pd.json_normalize(person['data'])])
        people_include_df = pd.concat([people_include_df, pd.json_normalize(person['included'])])

      people_data_df = people_data_df.reset_index(drop=True)
      people_include_df = people_include_df.reset_index(drop=True)
      return people_data_df
    except Exception as e:
      # handle the exception
      error = f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}'
      return e.status_code

  async def fetch_headcounts_data(query_date = None):
    try:
      headcounts_data_df = pd.DataFrame()
      headcounts_include_df = pd.DataFrame()
      for headcount in pco.iterate('/check-ins/v2/headcounts?include=attendance_type,event_time'):
        headcounts_data_df = pd.concat([headcounts_data_df, pd.json_normalize(headcount['data'])])
        headcounts_include_df = pd.concat([headcounts_include_df, pd.json_normalize(headcount['included'])])

      headcounts_data_df = headcounts_data_df.reset_index(drop=True)
      headcounts_include_df = headcounts_include_df.reset_index(drop=True).drop_duplicates()

      headcounts_df = pd.merge(
                        headcounts_data_df, 
                        headcounts_include_df[headcounts_include_df['type'] == 'EventTime'],
                        left_on = 'relationships.event_time.data.id',
                        right_on = 'id',
                        suffixes=('_data', '_et')
                                          )

      headcounts_df = pd.merge(
                        headcounts_df, 
                        headcounts_include_df[headcounts_include_df['type'] == 'AttendanceType'],
                        left_on = 'relationships.attendance_type.data.id',
                        right_on = 'id',
                        suffixes=('', '_at')
                                          )
        
      return headcounts_df
    except Exception as e:
      # handle the exception
      error = f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}'
      return e.status_code


  

  async def fetch_donations_data():
    try:
      donations_df = []
      for donation in pco.iterate('/giving/v2/donations?include=designations,labels,note,refund&where[updated_at][gte]=2024-01-01T12:00:00Z'):
        donations_df.append(donation)
      return donations_df
    except Exception as e:
      # handle the exception
      error = f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}'
      return e.status_code
    
  async def main():
    return await fetch_headcounts_data()

  
  return asyncio.run(main())
