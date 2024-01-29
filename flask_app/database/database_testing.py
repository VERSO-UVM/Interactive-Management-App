'''
FROM ISM DIRECTORY RUN THIS COMMAND
python3 -m flask_app.database.database_testing
'''

from flask_app.database.Alchemy import ParticipantTBL, FactorTBL, RatingsTBL, ResultsTBL
from flask_app.lib.dTypes.Participant import Participant
from flask_app.lib.dTypes.Factor import Factor
from flask_app.database.Alchemy import initialize_database_connection
from flask_app.database.database_access import insert_factor, insert_participant, insert_rating, insert_result    # database connector
from sqlalchemy import text

__DATABASE_CONNECTION = initialize_database_connection()

first_test_factor = Factor(
    title='first_test_factor', 
    description='first_test_description', 
    label='first_test_label')

second_test_factor = Factor(
    title='second_test_factor', 
    description='second_test_description', 
    label='second_test_label')

test_participant = Participant(
    u_name='test_user', 
    f_name='test_first', 
    l_name='test_last', 
    email='test_email', 
    job_title='test_job_title', 
    address='test_address', 
    state='test_state', 
    city='test_city', 
    zip_code='test_zip_code', 
    country='test_country', 
    p_type='test_p_type', 
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

print('inserting first test factor')
print(insert_factor(first_test_factor))
print('inserting second test factor')
print(insert_factor(second_test_factor))
print('inserting test participant')
print(insert_participant(test_participant))
print('inserting test rating')
print(insert_rating(factor_leading=first_test_factor, factor_following=second_test_factor, rating=3, p=test_participant))
print('inserting test result')
print(insert_result(factor_leading=first_test_factor, factor_following=second_test_factor, rating=1))
