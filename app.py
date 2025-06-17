import streamlit as st
from database import (
    create_field,
    list_fields,
    create_form,
    list_forms,
    link_field_to_form,
    get_form,
    get_fields_for_form,
    start_response,
    save_answer,
    submit_response,
    get_responses_for_form,
)

st.set_page_config(page_title="Simplified Google Forms", layout="wide")
st.title("📝 Simplified Google Forms")

menu = st.sidebar.radio("Select Action", ["Create Field", "Create Form", "Fill Form", "View Responses"])

# ------------------- Create Field -------------------
if menu == "Create Field":
    st.header("Create New Field")
    field_name = st.text_input("Field Name")
    field_type = st.selectbox("Field Type", ["text", "number", "date"])

    if st.button("Save Field"):
        if field_name.strip() == "":
            st.warning("Please enter a field name.")
        else:
            create_field(field_name, field_type)
            st.success(f"Field '{field_name}' of type '{field_type}' created successfully!")

# ------------------- Create Form -------------------
elif menu == "Create Form":
    st.header("Create New Form")
    form_name = st.text_input("Form Name")
    fields = list_fields()
    selected_field_ids = st.multiselect("Select Fields to Include", options=[f[0] for f in fields],
                                        format_func=lambda x: next(f[1] for f in fields if f[0] == x))

    if st.button("Create Form"):
        if form_name.strip() == "":
            st.warning("Please enter a form name.")
        elif not selected_field_ids:
            st.warning("Please select at least one field.")
        else:
            form_id = create_form(form_name)
            for field_id in selected_field_ids:
                link_field_to_form(form_id, field_id)
            st.success(f"Form '{form_name}' created with {len(selected_field_ids)} fields.")

# ------------------- Fill Form -------------------
elif menu == "Fill Form":
    st.header("Fill a Form")
    forms = list_forms()
    if forms:
        form_dict = {f[1]: f[0] for f in forms}
        selected_form_name = st.selectbox("Choose a Form", list(form_dict.keys()))
        selected_form_id = form_dict[selected_form_name]

        fields = get_fields_for_form(selected_form_id)
        response = start_response(selected_form_id)

        for field_id, field_name, field_type in fields:
            if field_type == "text":
                val = st.text_input(field_name)
            elif field_type == "number":
                val = st.number_input(field_name)
            elif field_type == "date":
                val = st.date_input(field_name)
            else:
                val = st.text_input(field_name)
            save_answer(response, field_name, val)

        if st.button("Submit"):
            submit_response(response)
            st.success("Response submitted successfully!")
    else:
        st.warning("No forms found. Create one first.")

# ------------------- View Responses -------------------
elif menu == "View Responses":
    st.header("View Responses")
    forms = list_forms()
    if forms:
        form_dict = {f[1]: f[0] for f in forms}
        selected_form_name = st.selectbox("Choose a Form to View Responses", list(form_dict.keys()))
        selected_form_id = form_dict[selected_form_name]

        responses = get_responses_for_form(selected_form_id)
        if responses:
            st.subheader(f"Responses for '{selected_form_name}':")
            for i, resp in enumerate(responses, 1):
                st.write(f"**Response {i}:** {resp[0]}")
        else:
            st.info("No responses yet.")
    else:
        st.warning("No forms available.")
