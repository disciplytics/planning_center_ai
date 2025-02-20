import asyncio
import pandas as pd
def load_data(pco):
  
  async def fetch_people_data():
    try:
      people_attr_df = []
      people_rels_df = []
      for person in pco.iterate('/people/v2/people?include=addresses,emails,field_data,households,inactive_reason,marital_status,organization,phone_numbers,primary_campus'):
        people_attr_df.append(person['data']['attributes'])
        people_rels_df.append(person['data']['relationships'])
        
      people_attr_df=pd.Dataframe(people_attr_df)
      people_rels_df=pd.Dataframe(people_rels_df)
      
      people_df = people_attr_df.merge(people_rels_df, left_index=True, right_index=True)
      return people_df
    except Exception as e:
      # handle the exception
      error = f'{e.status_code}\n-\n{e.message}\n-\n{e.response_body}'
      return e.status_code
  
  async def fetch_households_data():
    try:
      households_df = []
      for household in pco.iterate('/people/v2/households?include=people'):
        households_df.append(household['data']['attributes'])
      return households_df
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
