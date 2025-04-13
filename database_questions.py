import sqlite3

# Create a new SQLite database
db_path = "course_questions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Define course table names
course_tables = {
    "DS_3841": "Mgmt_Information_Systems",
    "DS_3850": "Business_Applications_Develop",
    "DS_4510": "Bus_Intel_Analytics_Capstone",
    "FIN_3210": "Principles_Managerial_Fin"
}

# Define the schema for the questions table
def create_course_table(course_code):
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {course_code} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL CHECK(correct_answer IN ('A', 'B', 'C', 'D'))
        )
    """)

# Create tables for each course
for code in course_tables:
    create_course_table(code)

# Commit and close connection
conn.commit()
conn.close()

db_path



# Reconnect to the database to insert questions
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sample questions for each course
sample_questions = {
    "DS_3841": [
        ("What does MIS stand for?", "Management Information Systems", "Marketing Information System", "Managerial Intelligence System", "Modern Info Structure", "A"),
        ("Which component is NOT part of MIS?", "Hardware", "Software", "People", "Ecosystem", "D"),
        ("What is the primary goal of MIS?", "To automate manual processes", "To collect and process data", "To entertain users", "To create websites", "B"),
        ("Which of these is a type of MIS?", "DSS", "OSS", "WSS", "PSS", "A"),
        ("ERP stands for?", "Enterprise Resource Planning", "Enterprise Record Process", "Efficient Resource Planning", "Essential Resource Programming", "A"),
        ("A TPS system is used for?", "Transaction Processing", "Technical Planning", "Trend Prediction", "Total Processing", "A"),
        ("Data becomes information when it is?", "Encrypted", "Sorted", "Processed", "Stored", "C"),
        ("MIS supports which level of management?", "Top", "Middle", "Lower", "All", "D"),
        ("Which is not a characteristic of MIS?", "Timeliness", "Accuracy", "Repetitiveness", "Relevance", "C"),
        ("The output of MIS is used for?", "Programming", "Decision Making", "Designing", "Recruitment", "B")
    ],
    "DS_3850": [
        ("What is a business application?", "A game", "Software solving business needs", "A shopping website", "A calculator", "B"),
        ("Which language is commonly used for web apps?", "HTML", "Python", "JavaScript", "All of the above", "D"),
        ("CRUD stands for?", "Create, Read, Update, Delete", "Copy, Rewrite, Undo, Deploy", "Create, Render, Upload, Download", "Connect, Reset, Update, Drive", "A"),
        ("Which database is widely used in applications?", "Oracle", "MongoDB", "MySQL", "All", "D"),
        ("Front-end deals with?", "Back-end services", "User Interface", "Database", "Security", "B"),
        ("Back-end languages include?", "HTML", "CSS", "Java", "Photoshop", "C"),
        ("Which is an IDE?", "Chrome", "VS Code", "Facebook", "Slack", "B"),
        ("MVC stands for?", "Model View Controller", "Most Valuable Code", "Manage Visual Components", "Modular View Control", "A"),
        ("APIs are used for?", "Connecting systems", "Formatting data", "Deleting files", "Compressing images", "A"),
        ("Which of these is a cloud platform?", "Google Docs", "Azure", "Photoshop", "Dropbox", "B")
    ],
    "DS_4510": [
        ("What does BI stand for?", "Business Input", "Business Intelligence", "Basic Info", "Big Integration", "B"),
        ("Which tool is used for analytics?", "Excel", "Tableau", "Power BI", "All", "D"),
        ("ETL stands for?", "Extract, Transform, Load", "Enter, Test, Learn", "Encrypt, Transfer, Log", "Evaluate, Track, Log", "A"),
        ("KPI means?", "Key Performance Indicator", "Known Performance Index", "Keep Process Insight", "Key Project Input", "A"),
        ("Which is NOT a BI tool?", "Power BI", "Tableau", "Notepad", "QlikView", "C"),
        ("Dashboards are used to?", "Play videos", "Display data visually", "Run commands", "Record audio", "B"),
        ("Data warehouse is for?", "Storing raw data", "Reporting", "Transactional operations", "Games", "B"),
        ("Predictive analytics is used for?", "Looking back", "Predicting future", "Current events", "Random trends", "B"),
        ("Which is an open-source BI tool?", "QlikView", "Pentaho", "Power BI", "Excel", "B"),
        ("Data cleansing means?", "Formatting PCs", "Cleaning files", "Removing incorrect data", "Resetting DB", "C")
    ],
    "FIN_3210": [
        ("Finance is mainly concerned with?", "Programming", "Money Management", "Data Mining", "Construction", "B"),
        ("What is ROI?", "Return on Investment", "Rate of Interest", "Revenue Over Income", "Run Of Interest", "A"),
        ("Balance Sheet includes?", "Income", "Assets & Liabilities", "Investments", "Customers", "B"),
        ("Which is a type of financial statement?", "Budget", "Income Statement", "Invoice", "Memo", "B"),
        ("NPV stands for?", "Net Present Value", "New Purchase Value", "Noted Present Volume", "Nominal Payment Value", "A"),
        ("A budget is?", "An invoice", "A spending plan", "A tax record", "A law", "B"),
        ("What is liquidity?", "Earning profits", "Paying taxes", "Availability of cash", "Investing", "C"),
        ("Depreciation is?", "Value increase", "Value decrease", "Profit", "Loss", "B"),
        ("Stockholders are?", "Employees", "Owners", "Customers", "Auditors", "B"),
        ("Dividends are paid to?", "Employees", "Managers", "Stockholders", "Government", "C")
    ]
}

# Insert the questions into each table
for table, questions in sample_questions.items():
    cursor.executemany(
        f"""
        INSERT INTO {table} (question_text, option_a, option_b, option_c, option_d, correct_answer)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        questions
    )

# Commit changes and close connection
conn.commit()
conn.close()

"Questions inserted successfully into all course tables."
