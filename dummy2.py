import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

# Connect to MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="reha8795",
  database="esd"
)

# Create cursor
mycursor = mydb.cursor()

# Define API endpoints
@app.route('/employees', methods=['GET'])
def get_employees():
    # Execute SQL query
    mycursor.execute("SELECT * FROM emp")
    # Fetch all rows
    rows = mycursor.fetchall()
    # Convert rows to list of dictionaries
    employees = []
    for row in rows:
        employee = {
            "id": row[0],
            "name": row[1],
            "salary": row[2]
        }
        employees.append(employee)
    # Return JSON response
    return jsonify(employees)

@app.route('/employees', methods=['POST'])
def add_employee():
    # Get employee data from request body
    data = request.get_json()
    name = data['name']
    salary = data['salary']
    # Execute SQL query
    sql = "INSERT INTO emp (name, salary) VALUES (%s, %s)"
    val = (name, salary)
    mycursor.execute(sql, val)
    mydb.commit()
    # Return success message
    return jsonify({"message": "Employee added successfully"})

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    # Get employee data from request body
    data = request.get_json()
    name = data['name']
    salary = data['salary']
    # Execute SQL query
    sql = "UPDATE emp SET name = %s, salary = %s WHERE id = %s"
    val = (name, salary, id)
    mycursor.execute(sql, val)
    mydb.commit()
    # Return success message
    return jsonify({"message": "Employee updated successfully"})

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    # Execute SQL query
    sql = "DELETE FROM emp WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    # Return success message
    return jsonify({"message": "Employee deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)