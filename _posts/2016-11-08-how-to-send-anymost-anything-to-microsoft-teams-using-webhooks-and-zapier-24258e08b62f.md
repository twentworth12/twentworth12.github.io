---
layout: post
title: "How to Send Almost Anything to Microsoft Teams using Webhooks and Zapier"
date: 2016-11-08 16:43:26 +0000
categories:
  - "Uncategorized"
tags:
  - "Collaboration"
  - "Microsoft"
  - "Slack"
---
<a href="https://blogs.office.com/2016/11/02/introducing-microsoft-teams-the-chat-based-workspace-in-office-365/" target="_blank" rel="noopener">Microsoft Teams</a> is set to take on the new breed of collaboration apps like Slack and Hipchat. Each collaboration area is called a Team — and each Team can have multiple channels. Within a channel you have all the basics like chat (with emojis!) and document sharing, but it really gets interesting when you connect Teams to other applications. Microsoft Teams launched with a bunch of connectors to popular apps like Trello, Jira, Zendesk, and many more — but it’s really easy to integrate almost anything with Teams using <a href="https://zapier.com" target="_blank" rel="noopener">Zapier</a> and Webhooks. <a href="https://sendgrid.com/blog/whats-webhook/" target="_blank" rel="noopener">Webhooks</a> are a type of event-driven API that lets you push and pull information between different types of apps. Lots of popular applications support Webhooks, including both Slack and Microsoft Teams. My objective was to create a channel for my marketing team at <a href="http://rapidminer.com" target="_blank" rel="noopener">RapidMiner</a> that would let me aggregate customer feedback — the NPS data we capture from <a href="https://www.surveymonkey.com/mp/take-a-tour/" target="_blank" rel="noopener">SurveyMonkey</a>. The first step is to add a Webhook to your Microsoft Teams channel. You’ll give the channel a name and a custom logo. Then your Webhook will provide a unique URL to receive the information you push from other apps like Zapier:

<figure>
<img src="/assets/uploads/2016/11/fa5ad-1XN3h4_bUZiPlKGMYdLvHkQ.png" data-width="1484" data-height="838" />
</figure>

Now that you have a URL for your Webhook, you can use Zapier to start pushing information into your Microsoft Teams channel. Starting with my SurveyMonkey example, you’ll use the built-in SurveyMonkey Zapier trigger to start the Zapier process.

<figure>
<img src="/assets/uploads/2016/11/43a2d-1L9n9w0-oJL4-XClS5yamdQ.png" data-width="766" data-height="519" />
</figure>

Then you’ll use “Webhooks by Zapier” to publish the chat transcript to Microsoft Teams. I prefer to use the *Custom Request* type for its flexibility. More on that later.

<figure>
<img src="/assets/uploads/2016/11/ad704-1whq43AbWGtd5QJfy5JndWA.png" data-width="771" data-height="109" />
</figure>

Now select the POST method and then add the URL of your Webhook. The Data section is where you’ll configure the messaging what you want to send. Since we selected Custom Request, we need to format the JSON using the Microsoft Teams Card format. Here’s what I use:

    {
     “summary”:”NPS Survey Response”, 
     “sections”:[
     {
     “activityTitle”:”<b>NPS Survey Response</b>”,
     “activityImage”: “https://secure.surveymonkey.com/assets/userweb/smlib.globaltemplates/5.8.0/assets/sm_logo_fb.png"
     },
     {
     “facts”:[
     {
     “name”:”Name”,
     “value”:”{{configure_this_in_Zapier}}”
     },
     {
     “name”:”Company”,
     “value”:”{{configure_this_in_Zapier}}”
     },
     {
     “name”:”NPS Score”,
     “value”:”{{configure_this_in_Zapier}}”
     },
     {
     “name”:”Needed for a Higher Rating”,
     “value”:”{{configure_this_in_Zapier}}”
     }
     ]
     }
     ],
     “potentialAction”:[
     {
     “@context”:”http://schema.org”,
     “@type”:”ViewAction”,
     “name”:”View in Salesforce”,
     “target”:[
     “your_salesforce_url}}”
     ]
     },
     ]
    }

This creates a card in Microsoft Teams using your webhook.

<figure class="wp-caption">
<img src="/assets/uploads/2016/11/a0914-14eXW5FNE47KK7CrvsyuDKw.png" data-width="1638" data-height="652" />
<figcaption>Microsoft Teams Card</figcaption>
</figure>

These are really simple examples, and you can do much more including <a href="https://dev.outlook.com/Connectors/GetStarted#posting-more-complex-cards" target="_blank" rel="noopener">adding markdown formatting and action buttons</a>.
