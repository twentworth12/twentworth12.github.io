---
layout: post
title: "On Cambridge Analytica"
date: 2019-08-06 18:34:09 +0000
categories:
  - "Uncategorized"
---
Last night I watched the [Great Hack on Netflix](https://www.youtube.com/watch?v=iX8GxLP1FHo). Highly recommended. Here's a TL;DR oversimplification on how it all worked: 

SCL Group, the parent company of Cambridge Analytica, created a psychographics-based methodology to manipulate political opinion in developing nations. It worked, and they formed Cambridge Analytica to participate in the US election process.

Their methodology was pretty simple: they used the [Ocean personality model](https://en.wikipedia.org/wiki/Big_Five_personality_traits) to categorize people across 5 factors: openness to experience, conscientiousness, extraversion, agreeableness and neuroticism. Voters were segmented using predictive models created with classic techniques like clustering. Then Cambridge Analytica created highly targeted marketing campaigns for each personality trait to influence voting.

So to this point, nothing is unusual. Marketers have been employing this segmentation strategy since [Claude Hopkins wrote Scientific Advertising](https://www.scientificadvertising.com/ScientificAdvertising.pdf) back in 1923. But wow, the scale they were able to achieve. That's where Facebook comes in.

Cambridge Analytica started by paying Facebook users to complete a lengthy survey called This Is Your Digital Life. This created a complete OCEAN profile for all the users who completed the survey, and it let Cambridge Analytica harvest a bunch of additional data including your likes and even your entire news feed. More importantly, it also let Cambridge Analytica grab all the same data for all your friends who installed the survey app. Facebook wasn't supposed to allow this, more on that later.

So now Cambridge Analytica could build a predictive model (well, 253 different models) based all the training data it captured from users who got paid to complete the survey. Then it could run everyone else who didn't actually complete the survey through the model to classify them into a personality profile. That's how you turn 32,000 survey responses into 87,000,000 voter profiles. According to Cambridge Analytica, their predictive models were only slightly better than a random chance but still, at that scale that's more than enough to influence an election.

With these profiles now in place, the entire Trump Facebook ad budget could go to voters in swing states with very specific messages based on their personality profiles with less ad spend waste. The rest, is history.

This isn't the first time technology was used to influence an election (and it won't be the last). For example, the analytics team on the 2008 Obama campaign pioneered using multivariate optimization to increase donations, and in one test generated an additional \$60m. This result led to the [founding of Optimizely](https://blog.optimizely.com/2010/11/29/how-obama-raised-60-million-by-running-a-simple-experiment/).

But this wasn't some [bullshit user acquisition growth hack gone bad.](https://techcrunch.com/2014/01/03/when-growth-hacking-goes-bad/) It was our election, the foundation of democracy. It's easy to point fingers at Cambridge Analytica, and they obviously bear lots of the blame for this. But in my opinion, it's Facebook that deserves most of the blame. Cambridge Analytica can't happen without data mining millions of Facebook profiles. It seems pretty clear that [lots of people at Facebook knew this was happening](https://thehill.com/policy/technology/456016-facebook-hit-with-new-questions-over-cambridge-analytica), maybe even Mark Zuckerberg. But they did nothing.

This is an extreme, history altering reminder that "if you don't pay for the product, you are the product"
