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
      Where statement:
      people_household_df = people_include_df[people_include_df['type'] == 'Household'].drop_duplicates()

      Join:
      people_data_df['id'] == people_household_df['']
      
      Keep columns: ['id', 'attributes.member_count', 'attributes.primary_contact_id', 'attributes.primary_contact',
                     'relationships.people.data', 'attributes.name']
                     
      Drop columns: ['type', 'attributes.created_at', 'attributes.updated_at', 'links.self', 'attributes.avatar',
                     'relationships.primary_contact.data.type', 'relationships.primary_contact.data.id',]

      Email:
      Where statement:
      people_email_df = people_include_df[people_include_df['type'] == 'Email'].drop_duplicates()

      Join:
      people_data_df['id'] == people_email_df['relationships.person.data.id']
      
      Keep columns: ['attributes.address', 'attributes.blocked', 'attributes.location', 
                     'attributes.primary', 'relationships.people.data.id']
                     
      Drop columns: ['type', 'id', 'attributes.created_at', 'attributes.updated_at', 
                     'links.self', 'relationships.person.data.type']

      Address:
      Where statement:
      people_address_df = people_include_df[people_include_df['type'] == 'Address'].drop_duplicates()

      Join:
      people_data_df['id'] == people_address_df['relationships.person.data.id']

      Keep columns: ['attributes.address', 'attributes.primary', 'relationships.people.data.id',
                     'attributes.street_line_1', 'attributes.street_line_2', 'attributes.city',
                     'attributes.state', 'attributes.zip', 'attributes.country_code', 'attributes.country_name']
                     
      Drop columns: ['type', 'id', 'attributes.created_at', 'attributes.updated_at', 'attributes.location', 
                     'links.self', 'relationships.person.data.type']

      MaritalStatus:
      Where statement:
      people_maritalstatus_df = people_include_df[people_include_df['type'] == 'MaritalStatus'].drop_duplicates()

      Join:
      people_data_df['relationships.marital_status.data.id'] == people_maritalstatus_df['id']
      
      Keep columns: ['id', 'attributes.value']
                     
      Drop columns: ['type', 'links.self']

      Organization:
      Where statement:
      people_organization_df = people_include_df[people_include_df['type'] == 'Organization'].drop_duplicates()

      Join:
      people_data_df['relationships.organization.data.id'] == people_organization_df['id']
      
      Keep columns: ['id', 'attributes.name']
                     
      Drop columns: ['type', 'links.self', 'attributes.created_at', 'attributes.country_code',
                     'attributes.date_format', 'attributes.time_zone', 'attributes.contact_website',
                     'attributes.avatar_url']

      PhoneNumber:
      Where statement:
      people_phonenumber_df = people_include_df[people_include_df['type'] == 'PhoneNumber'].drop_duplicates()

      Join:
      people_data_df['id'] == people_phonenumber_df['relationships.person.data.id']
      
      Keep columns: ['id', 'attributes.location', 'attributes.primary', 'relationships.person.data.id'
                     'attributes.number']
                     
      Drop columns: ['type', 'id', 'links.self', 'attributes.created_at', 'attributes.updated_at',
                     'relationships.person.data.type', 'attributes.country_code', 'attributes.carrier',
                     'attributes.e164', 'attributes.international', 'attributes.national']
      """
      people_data_df['relationships.households.data'] = pd.json_normalize(people_data_df['relationships.households.data'])
      return people_data_df.explode('relationships.households.data')#people_include_df[people_include_df['type'] == 'PhoneNumber'].dropna(axis=1, how='all').drop_duplicates()
      
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
