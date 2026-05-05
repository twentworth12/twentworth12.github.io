---
layout: post
title: "What I Learned Building an App on the Drift Platform"
date: 2017-12-15 23:15:36 +0000
categories:
  - "Uncategorized"
tags:
  - "Drift"
  - "JavaScript"
  - "Marketing"
---
A long time ago <a href="https://cs.illinois.edu" target="_blank" rel="noopener">in a galaxy far, far away</a> — I was a Computer Science major at the University of Illinois. I grew up programming in BASIC on a variety of hardware, including my beloved <a href="http://oldcomputers.net/ti994a.html" target="_blank" rel="noopener">TI 99/4A</a> and then later a Commodore Amiga. My parents came up with a brilliant strategy to get me to learn to program — you want to play games on the computer? Build them.

But after graduating college I realized I was pretty awful programmer. I was <a href="https://fcw.com/articles/1997/07/06/asymetrix-aimtech-combine-for-multimedia-training-apps.aspx?m=1" target="_blank" rel="noopener">working in QA at a software company</a>, and I found out pretty quickly that I better find something other way to make a living. Since I was better at talking about technology than building it, I ended up becoming a sales engineer and then later, a marketer.

I’ve always felt that my tech background has helped my marketing career, a phenominon <a href="https://medium.com/u/30626bc3c085" target="_blank" rel="noopener">Scott Brinker</a> <a href="http://chiefmartec.com/2008/03/marketing-and-c/" target="_blank" rel="noopener">wrote about way back in 2008</a>. Marketing as a discipline sits at the center of science and humanity, and I’ve tried to balance the two in my career.

But sometimes you just feel the need to build.

#### Building a App on the Drift Platform

The <a href="https://medium.com/u/5a3bd01d25cc" target="_blank" rel="noopener">Drift</a> platform is a new set of APIs to allow developers to <a href="https://blog.drift.com/drift-platform/" target="_blank" rel="noopener">create and publish apps on Drift</a>. I wanted to find a way to make it easier for our team at RapidMiner to learn more about the people we’re having conversations with.

I’ve been wanting to get back into coding as a \#sidehustle thing, so I took at look at at <a href="https://github.com/Driftt/Driffy" target="_blank" rel="noopener">one of the sample applications</a> that launched with the Drift platform and decided to give it a try.

Every time we start talking to someone with Drift, we try and look them up in Salesforce to learn about them so we can make the converation more relavant. Salesforce has all of the usual information, but more importantly for us, it has all of the information about how people are using our products.

Our process with Drift at RapidMiner was to cut+paste the email address into Salesforce to look up a user. Sounds easy, but it takes time, and disrupts the flow of the conversation especially when we are juggling lots of simultaneous conversions.

So, I decided I’d try and build an app called <a href="https://github.com/twentworth12/salesforce-lookup" target="_blank" rel="noopener">salesforce-lookup</a> that would make it easier to pull data from Salesforce into Drift. It takes the email address of the current user and returns a bunch of useful information from Salesforce directly into the Drift conversation. It looks like this inside Drift:

<figure>
<p><img src="/assets/uploads/2017/12/febf7-1u4eiP_vzfy6iJMhDlKy2Vg.png" data-width="766" data-height="478" /></p>
</figure>

The app will automatically generates a direct link to the user in Salesforce, and returns information about the user, including the number of times and the last time they used RapidMiner. Simple for sure, but it saves a bunch of time for the team and lets us have more relevant conversions.

Here’s how I did it, and what I learned in the process.

#### Creating a GitHub Account

Okay, I <a href="https://github.com/twentworth12/salesforce-lookup" target="_blank" rel="noopener">already had a GitHub account</a>, but had never used it before. Wow, GitHub is simple and useful. I can’t compare it to the all the old ways to manage code because I never used them, but it sure beats vi and a filesystem.

Apparently people still do use vi (and emacs). And there’s even a <a href="https://en.wikipedia.org/wiki/Editor_war" target="_blank" rel="noopener">Wikipedia on editor wars</a>. (I’m team vi, for the record).

#### Setting up Heroku

Heroku is an obvious place to run nodeJS apps, so I gave it a try. It was super easy to setup, and connects right to GitHub. Every time I pushed my code to GitHub it would automatically redeploy the app.

<figure>
<p><img src="/assets/uploads/2017/12/81fac-1t-pVgsF8nPz19sbmBeMTXg.png" data-width="776" data-height="468" /></p>
</figure>

#### Learning nodeJS and Asynchronous JavaScript

Okay, now the hard part — building the app in nodeJS.

I’ve used client side Javascript extensively during my time as a sales engineer, but I never really appreciated how much its has evolved for server-side applications.

My breakthrough was learning that Javascript can be asynchronous, and that means it requires a bit more planning when building the app.

I had to string a serious of function calls together to make sure that I had all the information I needed at each step. That meant I had to learn all about callback functions (shoutout to <a href="https://team.drift.com/jbarna" target="_blank" rel="noopener">Joel on the Drift team</a> for explaining this to me).

For example, here’s a function that finds the Drift Contact Id for the user in the current converation.

\

In an asynchronous Javascript world, you don’t really have the Drift Contact Id variable until you execute the callback function *GetContactId*. Once I figured this out, I was able to chain together a series of API calls to Drift and Salesforce.

The Drift APIs were easy to use, but Salesforce was a bit harder. One of the best parts of nodeJS is the ecosystem, and I found a <a href="https://jsforce.github.io" target="_blank" rel="noopener">robust library called JSforce</a> to help with the Salesforce query.

The hardest part was logging into Salesforce using OAuth. I had never looked at OAuth before, so I had to learn enough about it to access both the Salesforce and Drift APIs. Authentication to Salesforce is a little bit more difficult as you have to handle tokens that can expire.

Once I was able to authenticate, it’s just a simple SQL-like query to return what I needed for my app — the users name, company, and some details about their RapidMiner product usage. I can query any field we have inside Salesforce.

    conn.query("SELECT Id, Email, FirstName, LastName, Company, Academics__c, Total_RM_Studio_starts__c, Last_RM_Studio_usage__c FROM Lead where Email = '" + emailAddress + "'", function(err, result) {

Then I put together the message…

    // Build the Drift reply body

    body = "<a target='_blank' href=https://na52.salesforce.com/" + Id + ">" + firstName + " " + lastName + "</a><br/>" + "Company: " + Company + "<br/>Total RM Studio Starts: " + totalStudioStarts + "<br/>Last RM Studio Usage: " + lastStudioUsage + "<br/>Academic: " + Academic

And lastly send the message back to the Drift conversion.

    // Send the message

    return request.post(CONVERSATION_API_BASE + `/${conversationId}/messages`)

    .set('Content-Type', 'application/json')

    .set(`Authorization`, `bearer ${DRIFT_TOKEN}`)

    .send(message)

    .catch(err => console.log(err))

I was glad to learn that the best way to debug things is still to output stuff to the console. That hasn’t changed since my days of debugging BASIC. At one point, I basically had a console.log every other line.

<figure>
<p><img src="/assets/uploads/2017/12/669e8-1rPSCAybvHC4UO1zRo0HDQQ.png" data-width="1288" data-height="392" /></p>
</figure>

#### All marketers should learn to program

When I finally made this work (at 2am last night, just like in college!) it felt really great. There’s nothing like building something and seeing it actually work. Heck, someone has even forked my code already (looking at you <a href="https://medium.com/u/18756d04f2c7" target="_blank" rel="noopener">Brian Whalley</a>, good luck!). I’m sure my code is awful, but it does something useful, and it was really fun to build.

Steve Jobs once said <a href="https://www.youtube.com/watch?v=mCDkxUbalCw" target="_blank" rel="noopener">everyone should learn to program a computer</a>, and I agree. It helps you develop logical thinking (hey asyncronous Javascript), and many of the same concepts you learn in programming apply to lots of things we see as marketers. For example, your Marketo, Pardot, or HubSpot segmentation lists are just a complex boolean expression.

The advent of applications like GitHub and Heroku plus the availability of a massive variety of training resources make getting started with programming today easier than ever. Seriously, imagine getting a CS degree today without StackOverflow — yeah, that’s what my generation had to do.

``` wp-block-code
function getContactId(conversationId, callbackFn, orgId) {
// Get the contact from Drift
request
.get(CONVERSATION_API_BASE + `${conversationId}`)
.set('Content-Type', 'application/json')
.set(`Authorization`, `bearer ${DRIFT_TOKEN}`)
.end(function(err, res){
callbackFn(res.body.data.contactId, conversationId, orgId)
});
}
// call back function
function GetContactId(contactId, conversationId, orgId) {
return getContactEmail(contactId, GetContactEmail, conversationId, orgId);
}
```
