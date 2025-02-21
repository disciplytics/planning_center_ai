from streamlit import bar_chart
def attendance_trend(data):
  data['Headcount Type'] = data['attributes.name_at']
  data['attributes.total'] = data['attributes.total'].astype('int32')
  data['attributes.starts_at_at'] = data['attributes.starts_at_at'].astype('datetime64[ns]')
  #bar_chart(data=data, x='attributes.starts_at_at', y='attributes.total', x_label='Date', y_label='Headcounts', color='Headcount Type',)# horizontal=False, stack=None, width=None, height=None, use_container_width=True)
  return data
