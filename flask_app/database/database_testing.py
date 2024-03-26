'''
FROM ISM DIRECTORY RUN THIS COMMAND
python3 -m flask_app.database.database_testing
'''

from flask_app.database.Alchemy import ParticipantTBL, FactorTBL, RatingsTBL, ResultsTBL
from flask_app.lib.dTypes.Participant import Participant
from flask_app.lib.dTypes.Factor import Factor
from flask_app.database.Alchemy import initialize_database_connection
from flask_app.database.database_access import insert_factor, insert_participant, insert_rating, insert_result, fetch, calculate_average_rating    # database connector

from sqlalchemy import text, select
import io

__DATABASE_CONNECTION = initialize_database_connection()

first_test_factor = Factor(
    title='first_test_factor',)

second_test_factor = Factor(
    title='second_test_factor',)

first_participant = Participant(
    f_name='test_first', 
    l_name='test_last', 
    email='test_email', 
    telephone='test_telephone')

second_participant = Participant(
    f_name='test_first', 
    l_name='test_last', 
    email='test_email', 
    telephone='test_telephone')


# drop all tables
__DATABASE_CONNECTION.execute(text('DROP TABLE IF EXISTS participants'))
__DATABASE_CONNECTION.execute(text('DROP TABLE IF EXISTS factors'))
__DATABASE_CONNECTION.execute(text('DROP TABLE IF EXISTS ratings'))
__DATABASE_CONNECTION.execute(text('DROP TABLE IF EXISTS results'))
__DATABASE_CONNECTION.execute(text('DROP TABLE IF EXISTS ideas'))
__DATABASE_CONNECTION.execute(text('DROP TABLE IF EXISTS categories'))
__DATABASE_CONNECTION.commit()

# create all tables
__DATABASE_CONNECTION.execute(text('CREATE TABLE IF NOT EXISTS participants (id TEXT PRIMARY KEY, u_name TEXT, f_name TEXT, l_name TEXT, email TEXT, job_title TEXT, address TEXT, state TEXT, city TEXT, zip_code TEXT, country TEXT, p_type TEXT, telephone TEXT)'))
__DATABASE_CONNECTION.execute(text('CREATE TABLE IF NOT EXISTS factors (id TEXT PRIMARY KEY, title TEXT, label TEXT, description TEXT, votes INTEGER)'))
__DATABASE_CONNECTION.execute(text('CREATE TABLE IF NOT EXISTS ratings (id TEXT PRIMARY KEY, factor_leading TEXT, factor_following TEXT, rating FLOAT, participant_id TEXT)'))
__DATABASE_CONNECTION.execute(text('CREATE TABLE IF NOT EXISTS results (id TEXT PRIMARY KEY, factor_leading TEXT, factor_following TEXT, rating FLOAT)'))
__DATABASE_CONNECTION.commit()

# print('inserting first test factor')
# print(insert_factor(1, first_test_factor.title))
# print('inserting second test factor')
# print(insert_factor(2, second_test_factor.title))
# print('inserting test participant')
# print(insert_participant(first_participant.id, first_participant.f_name, first_participant.l_name, first_participant.email, first_participant.telephone))
# print('inserting test ratings')
# print(insert_rating(1, factor_leading=first_test_factor, factor_following=second_test_factor, rating=3, participant_id=first_participant.id))
# print(insert_rating(2, factor_leading=first_test_factor, factor_following=second_test_factor, rating=9, participant_id=second_participant.id))
# print('inserting test result')
# print(insert_result(1, factor_leading=first_test_factor.id, factor_following=second_test_factor.id, weight=1))

# print('selecting all factors')
# print(fetch(FactorTBL))
# print('selecting all participants')
# print(fetch(ParticipantTBL))
# print('selecting all ratings')
# print(fetch(RatingsTBL))

# average_ratings = calculate_average_rating()

# print('selecting all results')
# print(fetch(ResultsTBL))

# __DATABASE_CONNECTION.close()

# import csv
# from flask import Response

# def query_results_to_csv_string(data, header):
#     """Convert query results into a CSV string."""
#     si = io.StringIO()
#     cw = csv.writer(si)
#     cw.writerow(header)  # Write the header row
#     for datum in data:
#         datum = datum[0]
#         datum = str(datum).split(',')
#         # keep data to the right of : 
#         datum = list(map(lambda x: x.split(':')[1], datum))
#         # remove leading whitespace
#         datum = list(map(lambda x: x.strip(), datum))
#         cw.writerows(datum)
#     return si.getvalue()

# data = fetch(ResultsTBL)

# print(query_results_to_csv_string(data, ['id', 'factor_leading', 'factor_following', 'rating']))