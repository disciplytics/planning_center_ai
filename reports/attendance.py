def attendance_trend(data):
  return st.bar_chart(data=data, x='attributes.start_at', y='attributes.total', x_label='Date', y_label='Headcounts', color='attributes.name_at', horizontal=False, stack=None, width=None, height=None, use_container_width=True)
