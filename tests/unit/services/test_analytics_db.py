"""Unit tests for database module."""

import pytest

from src.services.analytics_db import DatabaseAnalytics


@pytest.mark.unit
class TestDatabaseAnalytics:
    """Test DatabaseAnalytics class."""

    def test_check_database_name_special_cases_under(self):
        db_utils = DatabaseAnalytics("be-x-old")

        assert db_utils.database == "be_x_oldwiki_p"
        assert db_utils.host == "be_x_oldwiki.analytics.db.svc.wikimedia.cloud"
