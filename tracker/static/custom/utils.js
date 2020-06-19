
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

function clearLocalStorage()
{
	// local storage (keeping unfinished task from live view that should be still shown to the user) must be cleared
	// But need to keep the showTutorial variable in order to keep user preferences regarding tutorial showing or not
	for (var i = 0; i < localStorage.length; i++)
	{
		var key = localStorage.key(i);
		var item = localStorage.getItem(key) ;
		
		if (key == 'totalFetched')
		{
			localStorage.removeItem(key);
		}
		else if (item[0] == '<')
		{
			localStorage.removeItem(key);
		}
	}
}


function cleanLocalStorage()
{
	// local storage (keeping unfinished task from live view that should be still shown to the user) must be cleared
	// But need to keep the showTutorial variable in order to keep user preferences regarding tutorial showing or not
	for (var i = 0; i < localStorage.length; i++)
	{
		var key = localStorage.key(i);
		var item = localStorage.getItem(key) ;
		
		if (key.startsWith('proxy-'))
		{
			localStorage.removeItem(key);
		}
		// else if (item[0] == '<')
		// {
		// 	localStorage.removeItem(key);
		// }
	}
}

function fillLocalStorage(input)
{
	console.log('FILL LOCAL STORAGE --');
	// local storage (keeping unfinished task from live view that should be still shown to the user) must be cleared
	// But need to keep the showTutorial variable in order to keep user preferences regarding tutorial showing or not
	// for (var i = 0; i < input.length; i++)
	// {
	// 	var key = localStorage.key(i);
	// 	var item = localStorage.getItem(key) ;
		
	// 	if (key.startsWith('proxy-'))
	// 	{
	// 		localStorage.removeItem(key);
	// 	}
		// else if (item[0] == '<')
		// {
		// 	localStorage.removeItem(key);
		// }
	// }
}