import asyncio
import pandas as pd

def load_data(pco):
  async def fetch_campus_data():
    try:
      campus_data_df = pd.DataFrame()
      for campus in pco.iterate('/people/v2/campuses'):
        campus_data_df = pd.concat([campus_data_df, pd.json_normalize(campus['data'])])
        
      campus_data_df = campus_data_df.reset_index(drop=True)
      return campus_data_df
    except Exception as e:
      # handle the exception
      error = f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}'
      return e.status_code
      
  async def fetch_people_data(query_date = None):
    try:
      people_data_df = pd.DataFrame()
      people_include_df = pd.DataFrame()
      
      for person in pco.iterate('/people/v2/people?include=addresses,emails,field_data,households,inactive_reason,marital_status,organization,phone_numbers,primary_campus,school'):
        people_data_df = pd.concat([people_data_df, pd.json_normalize(person['data'])])
        people_include_df = pd.concat([people_include_df, pd.json_normalize(person['included'])])

      people_data_df = people_data_df.reset_index(drop=True)
      people_include_df = people_include_df.reset_index(drop=True)

      

      #people_data_df = pd.merge(people_data_df, people_include_df[people_include_df['Type']=='Household'][['relationships.person.data.id', '']])
      #people_data_df = people_data_df.explode('relationships.households.data')        
      #people_data_df['relationships.households.data.id'] = people_data_df['relationships.households.data'].apply(lambda x: pd.Series(x['id']))

      
      return people_include_df[people_include_df['type']=='Household'].dropna(axis=1, how='all')
    except Exception as e:
      # handle the exception
      error = f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}'
      return e.status_code

  async def fetch_headcounts_data(query_date = None):
    try:
      headcounts_data_df = pd.DataFrame()
      headcounts_include_df = pd.DataFrame()

      if query_date:
        url_string = f'/check-ins/v2/headcounts?include=attendance_type,event_time&where[updated_at][gte]={query_date}'
      else:
        url_string = '/check-ins/v2/headcounts?include=attendance_type,event_time&where[updated_at][gte]=2024-01-01'
      for headcount in pco.iterate(url_string):
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

      event_data_df = pd.DataFrame()
      for event in pco.iterate('/check-ins/v2/events'):
        event_data_df = pd.concat([event_data_df, pd.json_normalize(event['data'])])

      
      headcounts_df = pd.merge(headcounts_df, event_data_df[['id', 'attributes.name', 'attributes.frequency']].rename(columns={'attributes.name':'Event', 'attributes.frequency': 'Event Frequency'}),
                               left_on = 'relationships.event.data.id_at', right_on = 'id')
      return headcounts_df
    except Exception as e:
      # handle the exception
      error = f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}'
      return e.status_code


  

  async def fetch_donations_data(query_date = None):
    try:
      donations_data_df = pd.DataFrame()
      donations_include_df = pd.DataFrame()

      funds_data_df = pd.DataFrame()
      
      if query_date:
        url_string = f'/giving/v2/donations?include=designations,labels,note,refund&where[updated_at][gte]={query_date}'
      else:
        url_string = '/giving/v2/donations?include=designations,labels,note,refund&where[updated_at][gte]=2024-01-01T12:00:00Z'
      for donation in pco.iterate(url_string):
        donations_data_df = pd.concat([donations_data_df, pd.json_normalize(donation['data'])])
        donations_include_df = pd.concat([donations_include_df, pd.json_normalize(donation['included'])])

      donations_data_df = donations_data_df.reset_index(drop=True)
      donations_include_df = donations_include_df.reset_index(drop=True)

      donations_data_df = donations_data_df.drop('attributes.amount_cents', axis=1)
      
      donations_data_df = donations_data_df.explode('relationships.designations.data')        
      donations_data_df['relationships.designations.data.id'] = donations_data_df['relationships.designations.data'].apply(lambda x: pd.Series(x['id']))

      donations_include_df = donations_include_df[['id', 'attributes.amount_cents', 'relationships.fund.data.id']].rename(columns={'id':'relationships.designations.data.id'})

      for fund in pco.iterate('/giving/v2/funds'):
        funds_data_df = pd.concat([funds_data_df, pd.json_normalize(fund['data'])])

      funds_data_df = funds_data_df[['id', 'attributes.name']].rename(columns={'id':'relationships.fund.data.id', 'attributes.name':'Fund'})

      donations_include_df = pd.merge(donations_include_df, funds_data_df, on='relationships.fund.data.id')

      donations_df = pd.merge(donations_data_df, donations_include_df, on = 'relationships.designations.data.id',)
      return donations_df
    except Exception as e:
      # handle the exception
      error = f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}'
      return e.status_code
    
  async def main():
    return await asyncio.gather(fetch_headcounts_data(), fetch_donations_data(), fetch_people_data(), fetch_campus_data())

  
  return asyncio.run(main())
