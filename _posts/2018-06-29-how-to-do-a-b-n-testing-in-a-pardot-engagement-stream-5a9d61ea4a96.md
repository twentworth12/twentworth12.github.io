---
layout: post
title: "How to do A/B/N testing in a Pardot Engagement Stream"
date: 2018-06-29 14:16:29 +0000
categories:
  - "Uncategorized"
tags:
  - "Salesforce"
---
Want to do A/B testing in a Pardot Engagement Stream? You can’t :( Well, not without a little bit of customization. Here’s a simple workaround for doing A/B/N testing in a Pardot engagement stream using a Salesforce APEX trigger. I won’t get into the details of building an APEX trigger, so if you aren’t comfortable with adding code to Salesforce, ask your admin nicely for help. But it’s really pretty easy to do. The process looks like this:

1.  Create a new Lead field in Salesforce. Mine is called *abRandom*.
2.  Create an APEX trigger with the code below and deploy it.
3.  Create a new custom Prospect field in Pardot and sync it with Salesforce
4.  Add a rule to your Engagement Stream to branch on the random number you’ve generated.

Here’s the APEX trigger code to generate a number between 1–4 so that I can have up to 4 variations inside an Engagement Stream:

    trigger assignRandom on Lead (before insert, before update) {
        for (Lead lead : Trigger.new) {
            if (lead.Testing__c == NULL) {
                lead.Testing__c = ( (Math.random() * (4-1) + 1));
                lead.Testing__c = lead.Testing__c.setscale(0);
                }
        }
    }

*Testing\_\_C* is the API name for a Salesforce field I created called *abRandom* (I probably should update that name, eh?). This function will look to see if the *abRandom* field is empty and if it is, it will generate a random number for every Salesforce Lead. You can create a random number in any range by changing the values below i.e. if you wanted a number between 1 and 2 you’d change it to:

    (Math.random() * (2-1) + 1)

Once the APEX trigger is deployed, all of your Leads will get be assigned a random number that will be synced to Pardot. Here’s what a Pardot Engagement Stream looks like with A\|B branching based on the random number. This example will split test two emails.

<figure class="wp-caption">
<img src="/assets/uploads/2018/06/c743f-1-2_-Wk6GEBQNymbPtY9NHA.png" data-width="818" data-height="550" />
<figcaption>Pardot Engagement Stream w/ an A/B test</figcaption>
</figure>

That’s it. I hope this helps! Maybe someday Pardot will add support for native A/B testing without workarounds like this :)
