import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
external_stylesheets = [dbc.themes.DARKLY]
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')
gss_markdown_text = '''
Gender Wage Gap is part of Discrimination and is the focus of our push for Gender Equality. It is a complex concept and according to Wikipedia, we can define it as the average difference in pay for different gender groups in the workforce. However, when we simply calculate their average, the gap is very large, but we have to take into account factors such as working hours, job hazards, etc. After controlling for variables, the results show that we still have a Gender Wage Gap, but at the same time show that we're gradually making progress. We know that it is still common in our society that men are generally paid more than women, and there are historical and cultural reasons behind this, but we need to work together to eliminate this inequality.


Specifically for the U.S., Anna Brown, Amanda Barroso, and Carolina Aragão from the Pew Reachearch Center did a tracking analysis of gender-specific pay in the U.S. over the last 20 years in 2019. Their study criticizes the slow progress of the U.S. push to eliminate the Gender Wage Gap over the past 20 years, and their results show that much of the increase in average pay for women in the U.S. has depended on the efforts of the women's group itself, rather than help from society. At the same time, they point out that U.S. women face invisible discrimination in management and leadership jobs and pressure from their families.


The General Social Survey (GSS) is a non-partisan social research study organized by the University of Chicago since 1972, which focuses on adults nationwide in the United States and collects data on American society over a period of time. The GSS is a comprehensive, factual, complete, and consistent survey that allows us to use these data to study many social issues in the United States and to make comparisons over an 80-year period. For our current lab, we will be using the 2019 GSS data to visualize a dashboard of sections about the Gender Wage Gap in the United States.

(Resources: 

https://en.wikipedia.org/wiki/Gender_pay_gap

https://www.pewresearch.org/short-reads/2023/03/01/gender-pay-gap-facts/

https://www.gss.norc.org/About-The-GSS )
'''
gss_table = gss_clean.copy()
gss_table = gss_clean.groupby(['sex']).agg({'income': 'mean',
                                           'job_prestige': 'mean',
                                           'socioeconomic_index': 'mean',
                                           'education': 'mean',})
gss_table = gss_table.reset_index().rename(columns={'sex': 'Sex',
                                                  'income': 'Average Annual Income',
                                                  'job_prestige': 'Average Job Prestige',
                                                  'socioeconomic_index': 'Average Socioeconomic Index',
                                                  'education': 'Average Years of Education'})
gss_table = gss_table.round(2)
gss_table = ff.create_table(gss_table)

gss_clean2 = gss_clean.copy()
gss_clean2 = gss_clean2[['job_prestige', 'income', 'sex','education','socioeconomic_index']]
gss_clean2 = gss_clean2.rename(columns={'sex': 'Sex',
                                        'socioeconomic_index': 'Average Socioeconomic Index',
                                        'education': 'Average Years of Education'})
gss_scat = px.scatter(gss_clean2, x='job_prestige', y='income', color='Sex',
                      trendline='ols', height=500, width=800,
                      labels={'job_prestige': 'Average Job Prestige',
                              'income': 'Average Annual Income'},
                      hover_data=['Average Years of Education', 'Average Socioeconomic Index'])

gss_box = px.box(gss_clean2, x='income', y='Sex', color='Sex',
                 labels={'income': 'Average Annual Income', 'Sex':' '})
gss_box.update_layout(showlegend=False)

gss_box1 = px.box(gss_clean2, x='job_prestige', y='Sex', color='Sex',
                 labels={'job_prestige': 'Average Job Prestige', 'Sex':' '})
gss_box1.update_layout(showlegend=False)

gss_clean3 = gss_clean.copy()
gss_clean3 = gss_clean3[['income', 'sex', 'job_prestige']]
gss_clean3['Job Prestige Level'] = pd.cut(gss_clean3['job_prestige'], bins=6, labels=['very low', 'low', 'lower medium', 'higher medium', 'high', 'very high'])
gss_clean3 = gss_clean3.dropna()
gss_clean3['Job Prestige Level'] = pd.Categorical(gss_clean3['Job Prestige Level'], categories=['very low', 'low', 'lower medium', 'higher medium', 'high', 'very high'], ordered=True)
gss_clean3.sort_values('Job Prestige Level', inplace=True)
gss_box2 = px.box(gss_clean3, y='income', x='sex', facet_col='Job Prestige Level', facet_col_wrap=2,labels={'income': 'Average Annual Income', 'sex':' '},
                  height=1200, width=700, color='sex')
gss_box2.update_layout(showlegend=False)
gss_box2.update_yaxes(range=[0, 180000])
gss_box2.for_each_annotation(lambda a: a.update(text=a.text.replace("Job Prestige Level=", "")))

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        html.H1('Exploring the Gender Wage Gap using 2019 GSS Survey'),
        dcc.Markdown(children = gss_markdown_text),
        html.H2("Comparing Male and Female Working Status"),
        dcc.Graph(figure=gss_table),
        html.H2("Income vs Job Prestige by Gender"),
        dcc.Graph(figure=gss_scat),
        html.Div([
            html.H2("Distribution of Income By Gender"),
            dcc.Graph(figure=gss_box)
        ], style = {'width':'48%', 'float':'left'}),
        html.Div([
            html.H2("Distribution of Job Prestige By Gender"),
            dcc.Graph(figure=gss_box1)
        ], style = {'width':'48%', 'float':'right'}),
        html.H2("Distribution of income for Male and Female By Job Prestige"),
        dcc.Graph(figure=gss_box2),
        html.Div([
            html.H3("Display Category"),
            dcc.Dropdown(id='cat1',
                         options=['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork'],
                         value='male_breadwinner'),
            html.H3("Group by Category"),
            dcc.Dropdown(id='cat2',
                         options=['sex', 'region', 'education'],
                         value='sex'),
        ], style={'width': '25%', 'float': 'left'}),
        html.Div([
            dcc.Graph(id="barplot")
        ], style={'width': '70%', 'float': 'right'})
    ]
)
@app.callback(Output(component_id="barplot",component_property="figure"), 
                  [Input(component_id='cat1',component_property="value"),
                   Input(component_id='cat2',component_property="value")])
def barplot(x, z):
        gss_clean4 = gss_clean.copy()
        gss_clean4 = gss_clean4[['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork', 'sex', 'region', 'education']]
        gss_clean4 = gss_clean4.dropna()
        gss_clean4 = gss_clean4.groupby([x, z]).size().reset_index(name='count')
        if x == 'satjob':
                gss_clean4[x] = pd.Categorical(gss_clean4[x], categories=["very satisfied", "mod. satisfied", "a little dissat", "very dissatisfied"], ordered=True)
                gss_clean4.sort_values(x, inplace=True)
        else:
                gss_clean4[x] = pd.Categorical(gss_clean4[x], categories=["strongly agree", "agree", "disagree", "strongly disagree"], ordered=True)
                gss_clean4.sort_values(x, inplace=True)
        barplot = px.bar(gss_clean4, x=x, y='count', color=z, text='count', barmode='group')
        barplot.update_layout(showlegend=True)
        return barplot
if __name__ == '__main__':
    app.run_server(mode='inline', debug=True)
