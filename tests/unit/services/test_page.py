"""Test MDWiki page service."""

from unittest.mock import Mock, patch

import pytest

from src.services.page import PageMWClient, get_page_title, initialize_site_connection


@pytest.mark.unit
def test_get_page_title_language():
    """Test page title generation for language-specific report."""
    title = get_page_title("ar", "2025")
    assert title == "WikiProjectMed:WikiProject_Medicine/Stats/Top_medical_editors_2025/ar"


@pytest.mark.unit
def test_get_page_title_global():
    """Test page title generation for global report."""
    title = get_page_title("", "2025", is_global=True)
    assert title == "WikiProjectMed:WikiProject_Medicine/Stats/Top_medical_editors_2025_(all)"


@pytest.mark.unit
@patch("src.services.page.MDWIKI_USERNAME", "testuser")
@patch("src.services.page.MDWIKI_PASSWORD", "testpass")
@patch("src.services.page.mwclient.Site")
def test_initialize_site_connection(mock_site):
    """Test site connection initialization."""
    mock_site_instance = Mock()
    mock_site.return_value = mock_site_instance

    # Clear cache
    initialize_site_connection.cache_clear()

    site = initialize_site_connection("testuser", "testpass")

    assert site == mock_site_instance
    mock_site_instance.login.assert_called_once_with("testuser", "testpass")


@pytest.mark.unit
@patch("src.services.page.MDWIKI_USERNAME", "testuser")
@patch("src.services.page.MDWIKI_PASSWORD", "testpass")
@patch("src.services.page.initialize_site_connection")
def test_page_mwclient_init(mock_init):
    """Test PageMWClient initialization."""
    mock_site = Mock()
    mock_page = Mock()
    mock_site.pages = {"Test:Page": mock_page}
    mock_init.return_value = mock_site

    page = PageMWClient("Test:Page")

    assert page.title == "Test:Page"
    assert page.site_mw == mock_site


@pytest.mark.unit
@patch("src.services.page.MDWIKI_USERNAME", "testuser")
@patch("src.services.page.MDWIKI_PASSWORD", "testpass")
@patch("src.services.page.initialize_site_connection")
def test_page_exists(mock_init):
    """Test page existence check."""
    mock_site = Mock()
    mock_page = Mock()
    mock_page.exists = True
    mock_site.pages = {"Test:Page": mock_page}
    mock_init.return_value = mock_site

    page = PageMWClient("Test:Page")

    assert page.exists() is True


@pytest.mark.unit
@patch("src.services.page.MDWIKI_USERNAME", "testuser")
@patch("src.services.page.MDWIKI_PASSWORD", "testpass")
@patch("src.services.page.initialize_site_connection")
def test_page_save(mock_init):
    """Test page save operation."""
    mock_site = Mock()
    mock_page = Mock()
    mock_page.save.return_value = {"result": "Success"}
    mock_site.pages = {"Test:Page": mock_page}
    mock_init.return_value = mock_site

    page = PageMWClient("Test:Page")
    result = page.save("New content", "Test edit")

    mock_page.save.assert_called_once_with("New content", summary="Test edit")
    assert result["result"] == "Success"


@pytest.mark.unit
@patch("src.services.page.MDWIKI_USERNAME", "")
@patch("src.services.page.MDWIKI_PASSWORD", "")
def test_page_mwclient_no_credentials():
    """Test PageMWClient initialization without credentials."""
    with pytest.raises(ValueError) as exc_info:
        PageMWClient("Test:Page")

    assert "MDWiki credentials not configured" in str(exc_info.value)


@pytest.mark.unit
@patch("src.services.page.MDWIKI_USERNAME", "testuser")
@patch("src.services.page.MDWIKI_PASSWORD", "testpass")
@patch("src.services.page.initialize_site_connection")
def test_page_get_text(mock_init):
    """Test getting page text."""
    mock_site = Mock()
    mock_page = Mock()
    mock_page.text.return_value = "Test content"
    mock_site.pages = {"Test:Page": mock_page}
    mock_init.return_value = mock_site

    page = PageMWClient("Test:Page")
    content = page.get_text()

    assert content == "Test content"


@pytest.mark.unit
@patch("src.services.page.MDWIKI_USERNAME", "testuser")
@patch("src.services.page.MDWIKI_PASSWORD", "testpass")
@patch("src.services.page.initialize_site_connection")
def test_page_create(mock_init):
    """Test page create operation (alias for save)."""
    mock_site = Mock()
    mock_page = Mock()
    mock_page.save.return_value = {"result": "Success"}
    mock_site.pages = {"Test:NewPage": mock_page}
    mock_init.return_value = mock_site

    page = PageMWClient("Test:NewPage")
    result = page.create("Initial content", "Creating new page")

    mock_page.save.assert_called_once_with("Initial content", summary="Creating new page")
    assert result["result"] == "Success"
