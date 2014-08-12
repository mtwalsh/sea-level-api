
class SingleDatabaseQueryTestMixin(object):

    def test_that_all_predictions_are_fetched_with_single_database_query(self):
        # Note that first there is a query on Location
        self.assertNumQueries(
            2, lambda: self.client.get(self.EXAMPLE_FULL_PATH))
