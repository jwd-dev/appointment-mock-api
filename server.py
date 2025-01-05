import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/available_timeslots', methods=['GET'])
def available_timeslots():
    date_str = request.args.get('date')
    if date_str:
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
    else:
        now = datetime.datetime.now()
        date = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)

    timeslots = []
    for i in range(20):
        timeslot_start = date + datetime.timedelta(minutes=30 * i)
        timeslot_end = timeslot_start + datetime.timedelta(minutes=30)
        timeslots.append({
            'start_time': timeslot_start.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': timeslot_end.strftime('%Y-%m-%d %H:%M:%S')
        })

   
    return jsonify( timeslots)

@app.route('/schedule_appointment', methods=['POST'])
def schedule_appointment():
    data = request.get_json()
    date_str = data.get('date')

    if not date_str:
        return jsonify({'error': 'Date is required.'}), 400

    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS.'}), 400

    return jsonify({'message': 'Appointment scheduled successfully.', 'date': date_str})


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')