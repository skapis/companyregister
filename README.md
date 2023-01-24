# Company Register Parser

In this directory is very simple app, which request czech business register and parse data from response to table in HTML. User can download fetched data from register. App uses Django framework for backend and Django Templates for frontend. 

## Dashboard
First screen, which user can see after login to his account. On this screen user can see all register, which is available to use and remaining requests. The reset of limits is based on reset date, which is specific to each register. ARES and RES limits reset every day.

![Dashboard](https://github.com/skapis/appscreenshots/blob/main/Company%20Register/Dashboard.png)


## ARES
On this site user can type ids of companies, which he wants to search. Company Ids have to be delimited by Enter value. After that the application send requests to the register and show response in table. User can download this results in CSV. If the user reached his daily limit, application will be blocked and he will not be able to send request until limit will be reset.

![Ares - blank](https://github.com/skapis/appscreenshots/blob/main/Company%20Register/Ares%20-%20blank.png)

**ARES with response**

![Ares with response](https://github.com/skapis/appscreenshots/blob/main/Company%20Register/Ares%20with%20response.png)

