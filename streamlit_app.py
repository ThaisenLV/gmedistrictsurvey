import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title('GME District Field Staff Survey')
df = pd.read_csv('data.csv')

def getFilterValues(df,f,f1=".*",f2='.*'):
    if f1==None or f2==None:
        return []
    else:
        return df[(df['Filter1'].str.contains(f1)) & (df['Filter2'].str.contains(f2))][f].drop_duplicates().to_list()


def generateChart(df,list_sort):


    #find category sort order
    dfs = df[df['Headers'] == list_sort[0]]
    dfs = dfs.sort_values('Value',ascending=False)
    
    cat_sort = dfs['Label'].to_list()
    list_sort = list_sort.reverse()
    
    df['Value'] = df['Value'].round(1)
    bars = alt.Chart().mark_bar().encode(
        alt.X("Value:Q", title=" "),
        alt.Y("Headers:O", title=" ", axis=None, sort=list_sort),
        color = alt.Color('Headers:N',
                          sort=list_sort, 
                          legend=alt.Legend(title=" ")
                          ),
        tooltip = alt.Tooltip('Value:Q'),
    ).properties(height=50,width=1000)
    
    texts = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='Value',
    )
        
    chart = alt.layer(bars, texts, data=df).facet(
        row=alt.Row('Label:N',header=alt.Header(labelAngle=0, labelAlign='left'), sort=cat_sort, title=" ")
    )
    
    chart = chart.configure_axis(grid=False, domain=False)
    
    st.altair_chart(chart, use_container_width=False, theme="streamlit") 


c1, c2, c3 = st.columns(3)


with c1:
    s1x1 = st.selectbox('SortBy Type', getFilterValues(df,'Filter1'), index=None)
    s2x1 = st.selectbox('Include1 Type', getFilterValues(df,'Filter1'), index=None)
    s3x1 = st.selectbox('Include2 Type', getFilterValues(df,'Filter1'), index=None)
    s4x1 = st.selectbox('Include3 Type', getFilterValues(df,'Filter1'), index=None)
    
with c2:
    s1x2 = st.selectbox('SortBy Group/Individual', getFilterValues(df,'Filter2',s1x1), index=None)
    s2x2 = st.selectbox('Include1 Group/Individual', getFilterValues(df,'Filter2',s2x1), index=None)
    s3x2 = st.selectbox('Include2 Group/Individual', getFilterValues(df,'Filter2',s3x1), index=None)
    s4x2 = st.selectbox('Include3 Group/Individual', getFilterValues(df,'Filter2',s4x1), index=None)

with c3:
    s1x3 = st.selectbox('SortBy Value', getFilterValues(df,'Filter3',s1x1,s1x2), index=None)
    s2x3 = st.selectbox('Include1 Value', getFilterValues(df,'Filter3',s2x1,s2x2), index=None)
    s3x3 = st.selectbox('Include2 Value', getFilterValues(df,'Filter3',s3x1,s3x2), index=None)
    s4x3 = st.selectbox('Include3 Value', getFilterValues(df,'Filter3',s4x1,s4x2), index=None)


list_filter = []
list_sort = []

if s1x3 != None:
    list_filter.append(s1x1 + '-' + s1x2 + '-' + s1x3)
    list_sort.append(s1x2 + '-' + s1x3)
    
if s2x3 != None:
    list_filter.append(s2x1 + '-' + s2x2 + '-' + s2x3)
    list_sort.append(s2x2 + '-' + s2x3)

if s3x3 != None:
    list_filter.append(s3x1 + '-' + s3x2 + '-' + s3x3)
    list_sort.append(s3x2 + '-' + s3x3)

if s4x3 != None:
    list_filter.append(s4x1 + '-' + s4x2 + '-' + s4x3)
    list_sort.append(s4x2 + '-' + s4x3)

list_sort = list(dict.fromkeys(list_sort))

st.markdown('##')
if s1x3 == None:
    st.write("You must identify a sort field to generate a chart!")
else:
    df['Filter'] = df['Filter1'].astype(str) + '-' + df['Filter2'].astype(str) + '-' + df['Filter3'].astype(str)
    df['Headers'] = df['Filter2'].astype(str) + '-' + df['Filter3'].astype(str)
    df = df[df['Filter'].isin(list_filter)]
    df = df[['Label','Headers','Value']]
    generateChart(df,list_sort)
