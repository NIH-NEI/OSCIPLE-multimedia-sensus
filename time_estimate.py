import time, datetime

def printTimeEstimate(count, total, startTime):
	percentDone = count / total
	elapsedTime = time.time() - startTime
	try:
		totalEstimate = elapsedTime / percentDone
	except ZeroDivisionError:
		totalEstimate = -1
	print ("current/total: {a}/{b}   elapsed time: {c}   percent done: {d}%   total estimate: {e}".format(a=count,b=total, c=str(datetime.timedelta(seconds=elapsedTime)), d=round(percentDone * 100, 4), e=str(datetime.timedelta(seconds=totalEstimate))))