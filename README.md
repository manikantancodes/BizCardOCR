# BizCardX: Extracting Business Card Data with OCR

BizCardX is a Streamlit application designed to extract information from business cards using Optical Character Recognition (OCR) technology. This application provides a simple and intuitive user interface for users to upload business card images, extract relevant information, and store it in a database.

## Approach

1. **Install Required Packages**: Ensure Python, Streamlit, easyOCR, and a database management system like SQLite or MySQL are installed.

2. **Design User Interface**: Create a user-friendly interface using Streamlit with widgets like file uploader, buttons, and text boxes to guide users through the process.

3. **Implement Image Processing and OCR**: Utilize easyOCR for text extraction from uploaded business card images. Apply image processing techniques for quality enhancement.

4. **Display Extracted Information**: Present the extracted information in a clean and organized manner within the Streamlit GUI using widgets like tables, text boxes, and labels.

5. **Implement Database Integration**: Integrate a database system like SQLite or MySQL to store extracted information and uploaded business card images. Employ SQL queries for data management tasks.

6. **Test the Application**: Thoroughly test the application to ensure proper functionality. Run it locally using `streamlit run app.py` in the terminal.

7. **Continuous Improvement**: Enhance the application by adding new features, optimizing code, fixing bugs, and implementing user authentication and authorization for improved security.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    ```

2. Navigate to the project directory:
    ```bash
    cd BizCardX
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:
    ```bash
    streamlit run app/main.py
    ```

2. Upload business card images using the provided interface.

3. Extracted information will be displayed in an organized manner.

4. Optionally, modify or delete the extracted data.

## Dependencies

- Python
- Streamlit
- easyOCR
- SQLite or MySQL

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


