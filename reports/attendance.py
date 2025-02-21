from streamlit import bar_chart
def attendance_trend(data):
  data['Headcount Type'] = data['attributes.name_at'
  return bar_chart(data=data, x='attributes.starts_at_at', y='attributes.total', x_label='Date', y_label='Headcounts', color='Headcount Type', horizontal=False, stack=None, width=None, height=None, use_container_width=True)
