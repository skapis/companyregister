# Company Register Parser

In this directory is a very simple app, which requests a Czech business register and parses data from the response to the table in HTML. Users can download fetched data from the register. The app uses the Django framework for the backend and Django Templates for the frontend. 

## Dashboard
The first screen which the user can see after login to his account. On this page, users can see all available registers and the remaining requests. ARES and RES limits reset every day.

![Dashboard](https://github.com/skapis/appscreenshots/blob/main/Company%20Register/Dashboard.png)


## ARES
On this page, users can type the ids of companies which he wants to search. Company Ids have to be delimited by enter sign. After that, the application sends requests to the register and shows the response in the table. Users can download these results in CSV. If the user reaches his daily limit, the application will be blocked and he will not be able to send requests until limit will be reset.

![Ares - blank](https://github.com/skapis/appscreenshots/blob/main/Company%20Register/Ares%20-%20blank.png)

**ARES with response**

![Ares with response](https://github.com/skapis/appscreenshots/blob/main/Company%20Register/Ares%20with%20response.png)

