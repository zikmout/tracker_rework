
function getCurrentDate(fmt, delta) {
	// delta is the time to add in seconds, by defaul 0
	delta = delta || 0;
	if (delta != 0) {
		currentDate = moment().add(delta, 's').format(fmt);
	}
	else {
		currentDate = moment().format(fmt);
	}
	// fmt example : "MM ddd, YYYY hh:mm:ss a"
	return currentDate;
}