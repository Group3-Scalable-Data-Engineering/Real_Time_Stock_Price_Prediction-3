import matplotlib.pyplot as plt
from flask import Flask, request, render_template_string, jsonify
from utils import plot_prediction

app = Flask(__name__)


selected_stock = 'GOOGL'

@app.route('/', methods=['GET'])
def index():
    return render_template_string('''
        <html>
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <form id="stock-select">
                <label for="stock">Select a stock:</label>
                <select name="stock">
                    <option value="GOOGL" {{ 'selected' if selected_stock == 'GOOGL' else '' }}>GOOGL</option>
                    <option value="TSLA" {{ 'selected' if selected_stock == 'TSLA' else '' }}>TSLA</option>
                    <option value="META" {{ 'selected' if selected_stock == 'META' else '' }}>META</option>
                    <option value="MSFT" {{ 'selected' if selected_stock == 'MSFT' else '' }}>MSFT</option>
                    <option value="NFLX" {{ 'selected' if selected_stock == 'NFLX' else '' }}>NFLX</option>
                    <option value="AAPL" {{ 'selected' if selected_stock == 'AAPL' else '' }}>AAPL</option>
                    <option value="QCOM" {{ 'selected' if selected_stock == 'QCOM' else '' }}>QCOM</option>
                </select>
            </form>
            <div id="plot"></div>
            <script>
                // Get the current stock name from the global variable
                var selectedStock = '{{ selected_stock }}';

                // Function to update the plot based on the selected stock
                function updatePlot() {
                    var stockSelect = document.getElementById('stock-select');
                    var newStock = stockSelect.elements['stock'].value;
                    selectedStock = newStock;
                    Plotly.d3.json('/plot_data?stock=' + newStock, function(err, data) {
                        if (err) return console.warn(err);
                        Plotly.newPlot('plot', data);
                    });
                }

                // Attach an event listener to the selection menu to update the plot when the user changes the selection
                var stockSelect = document.getElementById('stock-select');
                stockSelect.addEventListener('change', updatePlot);

                // Initialize the plot with the default stock (AAPL)
                Plotly.d3.json('/plot_data?stock=' + selectedStock, function(err, data) {
                    if (err) return console.warn(err);
                    Plotly.newPlot('plot', data);
                });
            </script>
        </body>
        </html>
    ''')

@app.route('/plot_data', methods=['GET'])
def plot_data():
    global selected_stock
    stock_name = request.args.get('stock')
    selected_stock = stock_name
    fig = plot_prediction(stock_name)
    plot_data = []
    for ax in fig.get_axes():
        for line in ax.get_lines():
            x_data = line.get_xdata()
            
            x_data = [str(x) for x in x_data]
            plot_data.append({
                'x': x_data,
                'y': list(line.get_ydata()),
                'name': line.get_label(),
                'mode': 'lines',
                'type': 'scatter'
            })
    return jsonify(plot_data)



if __name__ == '__main__':
    app.run()
