#Spongo

Spontaneous Travel Web Application

So, let's say that one day you wake up and think to yourself, "Man, I wish I could travel more".

The sentiment is a nice one, but then you think of all the evil subclauses related with your dream of being more spontanous:

    I wish I had more time.
    I wish I wouldn't blow all my money over a weekend.
    It's too much effort to plan a flight, accommodation, food, fun, and inner-city transit stuff if I only have a few days off or a free weekend.

Spongo is the real-time solution to all your pseudo-spontaneity travel problems.

In a clear, intuitive, user interface our web application integrates a budget over a 'free-time' interval. It then plans a complete, spontanous travel package for the user; while taking into account flight, accomodation, food and beverage, and transit costs for each potential travel destination.

#Spongoloid Python API Wrapper for SkyScanner

The spongoloid.py file in SpongoApp is a wrapper that simplifies the SkyScanner API process, which we discovered to be both convoluted and extremely redundant at times. As we began approaching the challenge of building our application, we ultimately came to the realization that it would be necessary to build an API helper if we wanted to make effective use of SkyScanner's API. During the presentation, we can show some of our favorite oddities.

After the conference, we will be releasing the Spongoloid wrapper for the public to use with minimal effort. In its present form, it contains almost everything you need to make a query between two IATA airports, minus an API key. You're supposed to bring that yourself, or possibly just steal it from us for the next few minutes because we violated all sorts of security practices by storing the API key directly in the repo. Duncan, feel free to invalidate our API key after the presentation and to issue a new one if we're going to continue development. 