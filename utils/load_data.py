def load_data():

  async def fetch_people_data():
    people_df = []
    for person in pco.iterate('/people/v2/people?include=addresses,emails,field_data,households,inactive_reason,marital_status,organization,phone_numbers,primary_campus'):
      people_df.append(person)
    return people_df
  
  async def fetch_households_data():
    households_df = []
    for household in pco.iterate('/people/v2/households?include=people'):
      households_df.append(household)
    return households_df

  return fetch_people_data().result(), fetch_households_data().result()
