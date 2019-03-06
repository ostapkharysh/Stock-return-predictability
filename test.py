#SQLALCHEMY
from sqlalchemy import create_engine
from sqlalchemy import inspect, select, MetaData, and_
import datetime
import pandas as pd

db_uri = 'postgresql://ostap:12345@localhost:5432/goog'
engine = create_engine(db_uri)
conn = engine.connect()

inspector = inspect(engine)

# Get table information

meta = MetaData(engine,reflect=True)
table = meta.tables['news']

#print(inspector.get_table_names())
#print(inspector.get_columns('news'))

select_st = select([table.c.DATE, table.c.TONE, table.c.DOCUMENTIDENTIFIER, table.c.SOURCECOMMONNAME, table.c.GCAM]).where(and_(table.c.DATE < '20160300000000' , table.c.DATE > '20160131234500'))

res = conn.execute(select_st).fetchall()

news = dict()
news['date'] = [datetime.datetime.strptime(el[0], '%Y%m%d%H%M%S') for el in res if '.' not in el[0]]
news['tone'] = [el[1] for el in res if '.' not in el[0]]
news['source'] = [el[2] for el in res if '.' not in el[0]]
news['agency'] = [el[3] for el in res if '.' not in el[0]]
news['words'] = [el[4] for el in res if '.' not in el[0]]

TONE = pd.DataFrame.from_dict(news)
#TONE = TONE[['date', 'tone', 'source']]
del res


TONE_15_M = pd.DataFrame({'date': [], 'tone': [], 'source': [],  'agency': [], 'words': []})

for idx, el in enumerate(list(set(TONE.date))):
    one_p_tones = TONE.loc[TONE.date==el].tone.values
    one_p_words = TONE.loc[TONE.date==el].words.values
    one_p_source = TONE.loc[TONE.date==el].source.values
    one_p_agency = TONE.loc[TONE.date==el].agency.values
    TONE_15_M.loc[idx] = pd.Series({"date": el, "tone": one_p_tones, "source": one_p_source , 'agency': one_p_agency, "words": one_p_words})

TONE_15_M = TONE_15_M.sort_values(by=['date'])
print(TONE_15_M.head())


TONE_15_M = TONE_15_M.reset_index()

tonality = pd.DataFrame(
    columns=['date', 'tone', 'positive', 'negative', 'polarity', 'active_den', 'self_den', 'agency'])
count = 0
for el in TONE_15_M.values:
    date = el[2]
    # min_15 = list(set(el[4]))
    # min_15 = [x for x in min_15 if abs(float(x.split(',')[0])) > 1]
    min_15 = el[4]
    min_15 = [x.split(',') for x in min_15]

    for el in min_15:
        tonality.loc[count] = pd.Series({'date': date, 'tone': float(el[0]), 'positive': float(el[1]),
                                         'negative': float(el[2]), 'polarity': float(el[3]),
                                         'active_den': float(el[4]),
                                         'self_den': float(el[5]),
                                         'agency': el[1]})
        count += 1


print(tonality.head())