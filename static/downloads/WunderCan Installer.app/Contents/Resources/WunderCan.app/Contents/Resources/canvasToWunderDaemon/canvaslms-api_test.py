import canvaslms.api

#authToken = canvaslms.api.getAuthTokenFromFile("../canvas_token.txt")
authToken = "5296~rJO92RTZgVb9WKIdaCr7TXde1xBGani0XP9xoFsBzbeXmjxOfA52P6260wkg1NhL"

apiObj = canvaslms.api.CanvasAPI("nuevaschool.instructure.com",authToken)

results = apiObj.allPages("users/self/courses")

print(results)
