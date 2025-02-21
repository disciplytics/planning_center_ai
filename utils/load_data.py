import asyncio
import pandas as pd
def load_data(pco):
  
  async def fetch_people_data():
    try:
      people_data_df = pd.DataFrame()
      people_include_df = pd.DataFrame()
      for person in pco.iterate('/people/v2/people?include=addresses,emails,field_data,households,inactive_reason,marital_status,organization,phone_numbers,primary_campus'):
        people_data_df = pd.concat([people_data_df, pd.json_normalize(person['data'])])
        people_include_df = pd.concat([people_include_df, pd.json_normalize(person['included'])])

      """
      Household:
      join to people_data_df. == people_include_df[people_include_df['type'] == 'Household'].dropna(axis=1, how='all')['id']
      Keep columns: ['id', 'attributes.member_count', 'attributes.primary_contact_id', 'attributes.primary_contact',
                     'relationships.people.data', 'attributes.name']
      Drop columns: ['type', 'attributes.created_at', 'attributes.updated_at', 'links.self', 'attributes.avatar',
                     'relationships.primary_contact.data.type', 'relationships.primary_contact.data.id',]

      """
      # Email, Address: has people id, Household: id

      return people_include_df[people_include_df['type'] == 'Email'].dropna(axis=1, how='all')#{'data':people_data_df.columns, 'included':people_include_df.columns}
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
