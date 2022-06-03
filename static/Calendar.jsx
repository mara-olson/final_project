function Calendar(props) {
  const [calActivities, setCalActivities] = React.useState([]);
  const [today, setToday] = React.useState(new Date());
  const realToday = new Date();

  React.useEffect(() => {
    if (props.userId) {
      fetch(`/api/users/${props.userId}/activities`)
        .then((response) => response.json())
        .then((data) => {
          setCalActivities(data.activities);
        });
    }
  }, [props.userId]);

  const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  const currentMonth = months[today.getMonth()];

  const currentYear = today.getFullYear();

  // console.log(today);
  return (
    <div className="calendar">
      <div className="calendar-header">
        <h2>
          {currentMonth}, {currentYear}
        </h2>
      </div>
      <div className="calendar-body">
        <div className="weekdays-header">
          {weekdays.map((weekday) => {
            return (
              <div key={weekday} className="weekday">
                <p>{weekday}</p>
              </div>
            );
          })}
        </div>
        <CalendarDays
          realToday={realToday}
          today={today}
          setToday={setToday}
          userId={props.userId}
          calActivities={calActivities}
          setCalActivities={setCalActivities}
          setShowModal={props.setShowModal}
          setModalTitle={props.setModalTitle}
          setModalContent={props.setModalContent}
        />
        {/* <CalendarActivities today={today} userId={props.userId} /> */}
      </div>
    </div>
  );
}

function CalendarDays(props) {
  let firstDayOfMonth = new Date(
    props.today.getFullYear(),
    props.today.getMonth(),
    1
  );
  let weekdayOfFirstDay = firstDayOfMonth.getDay();
  const realTodayMonth = props.realToday.getMonth();
  console.log(realTodayMonth);
  const finalTodayMonth = new Date(firstDayOfMonth).toDateString();
  console.log(finalTodayMonth);
  const currentDays = [];

  for (let day = 0; day < 42; day++) {
    if (day === 0 && weekdayOfFirstDay === 0) {
      firstDayOfMonth.setDate(firstDayOfMonth.getDate() - 7);
    } else if (day === 0) {
      firstDayOfMonth.setDate(
        firstDayOfMonth.getDate() + (day - weekdayOfFirstDay)
      );
    } else {
      firstDayOfMonth.setDate(firstDayOfMonth.getDate() + 1);
    }

    const calendarDay = {
      currentMonth: firstDayOfMonth.getMonth() === props.today.getMonth(),
      date: new Date(firstDayOfMonth).toDateString(),
      month: firstDayOfMonth.getMonth(),
      number: firstDayOfMonth.getDate(),
      selected:
        firstDayOfMonth.toDateString() === props.realToday.toDateString(),
      year: firstDayOfMonth.getFullYear(),
    };
    currentDays.push(calendarDay);

    for (const currentDay of currentDays) {
      for (const calActivity of props.calActivities) {
        if (currentDay.date == calActivity.date) {
          currentDay.id == calActivity.id;
          currentDay["activityName"] = calActivity.name;
          currentDay["activityType"] = calActivity.type;
          currentDay["distance"] = calActivity.distance;
        }
      }
    }
  }

  const handleClick = (day) => {
    // evt.preventDefault();
    // props.setSelectedDay(evt.);
    if (day.activityName) {
      const content = (
        <ActivityCard
          name={day.activityName}
          date={day.date}
          type={day.activityType}
          distance={day.distance}
        />
      );
      props.setShowModal(true);
      props.setModalContent(content);
      console.log(day.date);
    }
  };

  const nextMonth = () => {
    props.setToday(new Date(props.today.setMonth(props.today.getMonth() + 1)));
  };

  const prevMonth = () => {
    props.setToday(new Date(props.today.setMonth(props.today.getMonth() - 1)));
    console.log(props.realToday);
    // console.log()
  };

  return (
    <div className="table-content">
      <div className="calendar-nav">
        <button type="link" onClick={nextMonth}>
          Next Month
        </button>
        <button type="link" onClick={prevMonth}>
          Previous Month
        </button>
      </div>
      {currentDays.map((day) => {
        return (
          <button
            className={
              "calendar-day" +
              (day.currentMonth ? " current" : "") +
              (day.selected ? " selected" : "")
            }
            key={day.id}
            onClick={() => handleClick(day)}
          >
            {/* day.activityName &&  */}
            <p>{day.number}</p>
            <div>{day.activityName}</div>
            <div>{day.activityType}</div>
            {day.activityName && <div>{day.distance} miles</div>}
            {/* <Modal
              onClose={() => setShowModal(false)}
              showModal={props.showModal}
              modalTitle={day.activityName}
              modalDate={day.activityDate}
              modalType={day.activityType}
            /> */}
          </button>
        );
      })}
    </div>
  );
}
