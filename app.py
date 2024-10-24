from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import time
from apriori_algorithm import apriori, read_transactions, format_final_output

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the file upload
        file = request.files['file']
        min_sup = int(request.form['min_sup'])

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Read the transactions from the uploaded file
            transactions = read_transactions(file_path)

            # Start timing the execution
            start_time = time.time()

            # Run the Apriori algorithm
            frequent_itemsets, _ = apriori(transactions, min_sup)

            # Generate the final formatted output
            formatted_itemsets = "{" + "}{".join(map(str, sorted(frequent_itemsets))) + "}"

            # Calculate total running time
            running_time = time.time() - start_time

            # Render the results
            return render_template('results.html',
                                   itemsets=formatted_itemsets,
                                   filename=filename,
                                   min_sup=min_sup,
                                   running_time=f"{running_time:.6f}",
                                   total_items=len(frequent_itemsets))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
