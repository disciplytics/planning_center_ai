import asyncio
import pandas as pd

def load_data(pco):
  
  async def fetch_people_data(query_date: None):
    try:
      people_data_df = pd.DataFrame()
      people_include_df = pd.DataFrame()
      for person in pco.iterate('/people/v2/people?include=addresses,emails,field_data,households,inactive_reason,marital_status,organization,phone_numbers,primary_campus'):
        people_data_df = pd.concat([people_data_df, pd.json_normalize(person['data'])])
        people_include_df = pd.concat([people_include_df, pd.json_normalize(person['included'])])
        
      return people_data_df
    except Exception as e:
      # handle the exception
      error = f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}'
      return e.status_code

  async def fetch_donations_data():
    try:
      donations_df = []
      for donation in pco.iterate('/giving/v2/donations?include=designations,labels,note,refund&where[updated_at]=2024-01-01T12:00:00Z'):
        donations_df.append(donation)
      return donations_df
    except Exception as e:
      # handle the exception
      error = f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}'
      return e.status_code
    
  async def main():
    return await fetch_people_data(), await fetch_households_data(), await fetch_donations_data()

  
  return asyncio.run(main())
