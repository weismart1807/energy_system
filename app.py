from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        consumptions = data.get('consumptions', [])
        if len(consumptions) != 6:
            return jsonify({"error": "請提供六期的電量資料"}), 400

        period = int(data.get('period', 30))
        if period not in [30, 60]:
            return jsonify({"error": "期數必須是30或60天"}), 400

        daily_averages = []
        for consumption in consumptions:
            daily = float(consumption) / period
            daily_averages.append(daily)

        min_daily_average = min(daily_averages)
        max_daily_average = max(daily_averages)
        min_index = daily_averages.index(min_daily_average) + 1
        max_index = daily_averages.index(max_daily_average) + 1
        n_times = max_daily_average / min_daily_average

        result = {
            "min_index": min_index,
            "min_daily_average": min_daily_average,
            "max_index": max_index,
            "max_daily_average": max_daily_average,
            "n_times": n_times,
            "consumption": consumptions[min_index - 1],
            "period": period,
            "daily_averages": daily_averages 
        }
    except Exception as e:
        return jsonify({"error": "資料格式錯誤", "details": str(e)}), 400

    return jsonify(result)

if __name__ == '__main__':
    # 若想讓外部網路可連線，將 host 改為 0.0.0.0 並設定好防火牆或路由器轉發
    app.run(debug=True, host='0.0.0.0', port=5001)
