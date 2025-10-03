import pytest
from src.chatbot import generate_analysis

def test_generate_analysis_with_valid_data(mocker):
    """Test that the chain is invoked correctly with valid data."""
    # Mock the chain's invoke method to avoid actual LLM calls
    mock_chain = mocker.patch("src.chatbot.chain.invoke")
    mock_chain.return_value = "Mocked AI analysis."

    business_data = [{"name": "Test Cafe", "type": "cafe"}]
    result = generate_analysis(business_data, "cafe", "Testville")
    
    # Assert the mock was called and the result is what we expect
    mock_chain.assert_called_once()
    assert result == "Mocked AI analysis."

    # Check if the business_data was formatted correctly for the prompt
    call_args = mock_chain.call_args[0][0]
    assert "- Name: Test Cafe, Type: cafe" in call_args["business_data"]
    assert call_args["business_type"] == "cafe"
    assert call_args["location"] == "Testville"


def test_generate_analysis_with_empty_data():
    """Test the function's response to empty business data."""
    result = generate_analysis([], "cafe", "Emptyville")
    assert "Not enough data" in result

def test_generate_analysis_with_invalid_data():
    """Test the function's response to non-list business data."""
    result = generate_analysis(None, "cafe", "Nullville")
    assert "Not enough data" in result