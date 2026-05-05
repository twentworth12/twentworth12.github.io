---
layout: post
title: "Vibe coding an iOS app + deploying to the App Store"
date: 2025-07-22 20:30:24 +0000
categories:
  - "Uncategorized"
---
<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;"><iframe src="https://www.loom.com/embed/ecaf982f2e5245cc8274d013f824daab" frameborder="0" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;"></iframe></div>

## 

Let me be clear: no one asked for this. But I’m going to walk you through how I built and published an iOS app using Claude Code, Xcode, and pure vibes.

I don’t know Swift. I’ve never written a real line of Swift in my life. But I’ve now shipped four apps to the App Store, mostly by telling AI what I wanted and watching it make the magic happen.

This post isn’t a tutorial in the traditional sense. It’s a field report from the future, where anyone with an idea and some time can build software without writing code.

Let’s get into it.

------------------------------------------------------------------------

### **🧰 What You Need (It’s Not Much)**

You’ll need just two things to get started:

- **Claude Code** – Download it from [Anthropic’s site](https://www.anthropic.com/).
- **Xcode** – Apple’s all-in-one IDE for building and submitting apps.

That’s it. No Swift knowledge. No CS degree. No excuses.

------------------------------------------------------------------------

### **🧪 My App Idea: A Data Sheet, But Make It an App**

I hate product data sheets. PDFs that no one reads, packed with boilerplate and buzzwords. What if, instead, you could open a beautiful, interactive app that explains what your product actually does?

That’s what I set out to build: an interactive data sheet for [incident.io](https://www.incident.io/), the company where I’m CMO.

So I created a new iOS project in Xcode and named it (very creatively) incident-io-datasheet. Then I opened Claude Code, pointed it at my project folder, and told it what I wanted:

> “Build a beautiful, interactive iOS app that showcases the four products incident.io offers. Make it look like Apple made it. It should be WWDC-award-worthy.”

A tall order. But Claude said “Yes.”

------------------------------------------------------------------------

### **🔧 Vibe Coding in Real Time**

Here’s what happened next:

1.  Claude scanned the project and figured out I was building an iOS app in Swift.
2.  It asked to initialize the Claude project and created a claude.md instruction file.
3.  I gave it the prompt above. It broke the job into 5 steps: research incident.io, design the app, create the data model, build a Swift UI interface, and add interactivity.

It wrote real Swift code. Created product cards. Designed a sidebar. Built the views. Even added animated transitions.

I watched the whole thing unfold like it was Christmas morning. No clue what the code did, but it looked legit.

------------------------------------------------------------------------

### **🐛 Fixing Errors (The Lazy Way)**

Like any good dev, Claude got some stuff wrong. Build failed. A bunch of red errors in Xcode.

But unlike normal devs, I didn’t debug anything. I just copied the error messages into Claude. It fixed them.

Rinse. Repeat. Eventually: **build succeeded**.

Then came the moment of truth: I hit play in the iOS simulator.

And there it was: a real app.

------------------------------------------------------------------------

### **📱 The App Actually Worked (?!)**

It had:

- A home screen with our tagline: *“Move fast when you break things.”*
- Tabs for each product (Alerting, Response, Status Pages, Postmortems)
- Beautiful floating bullet points with key features and benefits
- A sidebar nav that just… showed up on iPad, like it knew it belonged there

I even told Claude to add a flame emoji next to the company name. It tried. It was the wrong emoji, but hey, it tried.

------------------------------------------------------------------------

### **📤 Publishing to the App Store**

Building the app was surprisingly easy.

Getting it on the App Store? Slightly trickier, but still totally doable.

Here’s what I had to do:

- **Join Apple’s Developer Program** (\$99/year)
- **Create an App Store Connect record** (name, description, screenshots, pricing)
- **Archive the app in Xcode**
- **Generate and add an icon** (Claude vibe-created a 1024x1024 flame emoji PNG—somehow perfectly sized on the first try)
- **Fix minor metadata and compliance things**
- **Submit for review**

It took about 45 minutes total to go from working app to “Waiting for Review.”

------------------------------------------------------------------------

### **🏁 Final Thoughts: You Can Actually Do This**

Vibe coding is real.

I didn’t know Swift. I barely touched Xcode. I just told Claude what I wanted and helped it fix the errors it created along the way. The end result? A working, beautiful app that’s now on the App Store.

You can do this. Whether it’s a data sheet, a dumb game, or a side hustle you’ve been sitting on... Claude Code and Xcode are enough to get something shipped.

And if you’re lucky, maybe your flame emoji app will win a WWDC award. Or at least confuse a few Apple reviewers.

------------------------------------------------------------------------
