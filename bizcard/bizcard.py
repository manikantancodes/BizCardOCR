import streamlit as st
import psycopg2
import pandas as pd
from PIL import Image
import numpy as np
import easyocr
import re
import io

# Function to connect to PostgreSQL database
def connect_to_db():
    mydb = psycopg2.connect(
        host="localhost",
        user="postgres",
        port="5432",
        database="bizcard",
        password="mani94"
    )
    return mydb

# Function to upload multiple images and extract text
def upload_and_extract_text():
    uploaded_files = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    extracted_data = []

    if uploaded_files:
        for uploaded_file in uploaded_files:
            text_image, input_img = image_to_text(uploaded_file)
            text_dict = extracted_text(text_image)

            if text_dict:
                extracted_data.append(text_dict)

                # Display image and extracted text
                st.image(input_img, caption="Uploaded Image", use_column_width=True)
                st.write("### Extracted Text:")
                

    return extracted_data

# Function to extract text from image
def image_to_text(path):
    input_img = Image.open(path)
    image_arr = np.array(input_img)
    reader = easyocr.Reader(['en'])
    text = reader.readtext(image_arr, detail=0)
    return text, input_img

# Function to extract relevant details from extracted text
def extracted_text(texts):
    extrd_dict = {"NAME": [], "DESIGNATION": [], "COMPANY_NAME": [], "CONTACT": [], "EMAIL": [], "WEBSITE": [],
                  "ADDRESS": [], "PINCODE": []}

    extrd_dict["NAME"].append(texts[0])
    extrd_dict["DESIGNATION"].append(texts[1])

    for i in range(2, len(texts)):
        if texts[i].startswith("+") or (texts[i].replace("-", "").isdigit() and '-' in texts[i]):
            extrd_dict["CONTACT"].append(texts[i])
        elif "@" in texts[i] and ".com" in texts[i]:
            extrd_dict["EMAIL"].append(texts[i])
        elif "WWW" in texts[i] or "www" in texts[i] or "Www" in texts[i] or "wWw" in texts[i] or "wwW" in texts[i]:
            small = texts[i].lower()
            extrd_dict["WEBSITE"].append(small)
        elif "Tamil Nadu" in texts[i] or "TamilNadu" in texts[i] or texts[i].isdigit():
            extrd_dict["PINCODE"].append(texts[i])
        elif re.match(r'^[A-Za-z]', texts[i]):
            extrd_dict["COMPANY_NAME"].append(texts[i])
        else:
            remove_colon = re.sub(r'[,;]', '', texts[i])
            extrd_dict["ADDRESS"].append(remove_colon)

    for key, value in extrd_dict.items():
        if len(value) > 0:
            concadenate = " ".join(value)
            extrd_dict[key] = [concadenate]
        else:
            value = "NA"
            extrd_dict[key] = [value]

    return extrd_dict

# Main function
def main():
    conn = connect_to_db()
    cursor = conn.cursor()

    st.set_page_config(layout="wide")
    st.title("EXTRACTING BUSINESS CARD DATA WITH OCR")

    # Sidebar menu
    with st.sidebar:
        home_button = st.button("Home", key="home_button")
        st.markdown("---")
        st.markdown("---")
        st.markdown("**Main Menu**")
        other_buttons = ["Upload & Modifying", "Preview Database", "Modify", "Delete"]
        selected_option = st.radio("", other_buttons)

    # Display content based on selected option
    if home_button:
        st.markdown("### :blue[**Technologies Used :**] Python, easy OCR, Streamlit, PostgreSQL, Pandas")
        st.write("### :green[**About :**] Bizcard is a Python application designed to extract information from business cards.")
        st.write("### The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.")
    elif selected_option == "Upload & Modifying":
        # Upload and modify functionality
        extracted_data = upload_and_extract_text()

        # Save button
        if st.button("Save", key="save_button", help="Click to save the extracted data to the database"):
            # Save extracted data to the database
            for data in extracted_data:
                df = pd.DataFrame(data)
                # Assuming your table in the database is named 'bizcardinfo'
                # Replace column names as needed in the INSERT INTO statement
                for index, row in df.iterrows():
                    cursor.execute("""
                        INSERT INTO bizcardinfo (name, designation, company_name, contact, email, website, address, pincode)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        row['NAME'], 
                        row['DESIGNATION'], 
                        row['COMPANY_NAME'], 
                        row['CONTACT'], 
                        row['EMAIL'], 
                        row['WEBSITE'], 
                        row['ADDRESS'], 
                        row['PINCODE']
                    ))

            conn.commit()
            cursor.close()
            conn.close()

    elif selected_option == "Preview Database":
        try:
            cursor.execute("SELECT * FROM bizcardinfo")
            table = cursor.fetchall()
            table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE",
                                                    "ADDRESS", "PINCODE", "IMAGE"))
            st.dataframe(table_df)
        except psycopg2.Error as e:
            st.error(f"Error fetching data from PostgreSQL database: {e}")

    elif selected_option == "Modify":
        try:
            cursor.execute("SELECT * FROM bizcardinfo")
            table = cursor.fetchall()
            table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE",
                                                    "ADDRESS", "PINCODE", "IMAGE"))

            selected_name = st.selectbox("Select the name", table_df["NAME"])

            df_3 = table_df[table_df["NAME"] == selected_name]
            df_4 = df_3.copy()

            col1, col2 = st.columns(2)
            with col1:
                mo_name = st.text_input("Name", df_3["NAME"].unique()[0])
                mo_desi = st.text_input("Designation", df_3["DESIGNATION"].unique()[0])
                mo_com_name = st.text_input("Company_name", df_3["COMPANY_NAME"].unique()[0])
                mo_contact = st.text_input("Contact", df_3["CONTACT"].unique()[0])
                mo_email = st.text_input("Email", df_3["EMAIL"].unique()[0])

                df_4["NAME"] = mo_name
                df_4["DESIGNATION"] = mo_desi
                df_4["COMPANY_NAME"] = mo_com_name
                df_4["CONTACT"] = mo_contact
                df_4["EMAIL"] = mo_email

            with col2:
                mo_website = st.text_input("Website", df_3["WEBSITE"].unique()[0])
                mo_addre = st.text_input("Address", df_3["ADDRESS"].unique()[0])
                mo_pincode = st.text_input("Pincode", df_3["PINCODE"].unique()[0])
                mo_image = st.text_input("Image", df_3["IMAGE"].unique()[0])

                df_4["WEBSITE"] = mo_website
                df_4["ADDRESS"] = mo_addre
                df_4["PINCODE"] = mo_pincode
                df_4["IMAGE"] = mo_image

            st.dataframe(df_4)

            button_3 = st.button("Modify", key="modify_button")
            if button_3:
                try:
                    cursor.execute(f"DELETE FROM bizcardinfo WHERE NAME = '{selected_name}'")
                    conn.commit()
                    insert_query = '''INSERT INTO bizcardinfo(name, designation, company_name, contact, email, website, address, pincode, image)
                                      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                    datas = tuple(df_4.values[0])
                    cursor.execute(insert_query, datas)
                    conn.commit()
                    st.success("MODIFIED SUCCESSFULLY")
                except psycopg2.Error as e:
                    st.error(f"Error modifying data: {e}")
        except psycopg2.Error as e:
            st.error(f"Error fetching data from PostgreSQL database: {e}")

    elif selected_option == "Delete":
        try:
            cursor.execute("SELECT NAME FROM bizcardinfo")
            table1 = cursor.fetchall()
            names = [i[0] for i in table1]
            name_select = st.selectbox("Select the name", names)

            select_query = f"SELECT DESIGNATION FROM bizcardinfo WHERE NAME = '{name_select}'"
            cursor.execute(select_query)
            table2 = cursor.fetchall()
            designations = [j[0] for j in table2]
            designation_select = st.selectbox("Select the designation", options=designations)

            if st.button("Delete", key="delete_button"):
                try:
                    cursor.execute(f"DELETE FROM bizcardinfo WHERE NAME = '{name_select}' AND DESIGNATION = '{designation_select}'")
                    conn.commit()
                    st.warning("DELETED")
                except psycopg2.Error as e:
                    st.error(f"Error deleting data: {e}")
        except psycopg2.Error as e:
            st.error(f"Error fetching data from PostgreSQL database: {e}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
