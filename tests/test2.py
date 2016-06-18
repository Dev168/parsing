import parsing as m
from tests.t1.test import load_test_data

handicaps_df = load_test_data()

handicaps_df = m.resolve_participant_names(handicaps_df, 1)

