from parsing.main import replace_names_by_id, replace_names_by_created_id, replace_names_by_similarities
from tests.t1.test import load_test_data

events_df = load_test_data()

bookmaker_id = 1

events_df = replace_names_by_id(events_df, bookmaker_id)

events_df = replace_names_by_similarities(events_df, bookmaker_id)

events_df = replace_names_by_created_id(events_df, bookmaker_id)