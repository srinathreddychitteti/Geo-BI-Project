
import streamlit as st
from locationFetcher import get_business_data
from chatbot import generate_analysis

def initialize_state():
    """Initializes the session state for the application."""
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None

def render_header():
    """Renders the main header and description of the application."""
    st.title("🗺️ Geo-Spatial Business Intelligence Chatbot")
    st.markdown(
        "Enter a location and business type to generate an AI-powered market analysis "
        "using OpenStreetMap data and a Hugging Face LLM."
    )
    st.divider()

def render_form():
    """
    Renders the input form for location and business type and returns the user's input.
    """
    with st.form("analysis_form"):
        col1, col2 = st.columns(2)
        with col1:
            location_query = st.text_input(
                "Enter a Location",
                "Banjara Hills, Hyderabad",
                help="Be specific, e.g., 'Ameerpet, Hyderabad'"
            )
        with col2:
            business_type_query = st.text_input(
                "Enter a Business Type",
                "cafe",
                help="Use OSM tags like 'restaurant', 'supermarket', 'bank'"
            )
        
        submitted = st.form_submit_button("Analyze Market", type="primary", use_container_width=True)
    
    return submitted, location_query, business_type_query

def display_results():
    """Displays the analysis results stored in the session state."""
    if not st.session_state.last_result:
        return

    result = st.session_state.last_result
    st.divider()
    st.header(f"Analysis for '{result['type']}' in '{result['location']}'")

    if result["status"] == "success":
        st.markdown(result["analysis"])
        with st.expander("View Raw Business Data"):
            st.write(f"Found {len(result['data'])} businesses:")
            st.json(result['data'])
    
    elif result["status"] == "no_results":
        st.warning("Query successful, but no businesses of that type were found in the OpenStreetMap database for this specific area.")
        st.info("💡 Try a broader location or a different business type.")
    
    else:  # Status is "error"
        st.error(f"An error occurred: {result['analysis']}")

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="Geo-Spatial Business Intelligence Chatbot",
        layout="wide"
    )
    initialize_state()
    render_header()
    
    submitted, location_query, business_type_query = render_form()

    if submitted:
        if not location_query or not business_type_query:
            st.error("⚠️ Please enter both a location and a business type.")
            return

        with st.spinner(f"Analyzing the market for '{business_type_query}' in '{location_query}'..."):

            business_data = get_business_data(location_query, business_type_query)
            
            result_dict = {"location": location_query, "type": business_type_query}

            if isinstance(business_data, list):
                if business_data:
                    
                    analysis_result = generate_analysis(business_data, business_type_query, location_query)
                    result_dict.update({
                        "data": business_data,
                        "analysis": analysis_result,
                        "status": "success"
                    })
                else:
                    result_dict["status"] = "no_results"
            else: 
                result_dict.update({"analysis": business_data, "status": "error"})
            
            st.session_state.last_result = result_dict
    
    display_results()

if __name__ == "__main__":
    main()