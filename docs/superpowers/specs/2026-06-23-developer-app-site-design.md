# Developer App Website Design

## Overview

Build a bilingual promotional website for the independent developer **羽浩 邓** that turns the App Store developer page into an SEO-friendly acquisition funnel. The site should surface the developer brand, explain each app clearly, rank for long-tail search queries, and push visitors toward App Store downloads.

Apps to feature:

- **Noteit - AI Journal Notes Diary**
- **知了，RSS智能聚合阅读**
- **Mahjong AI - Mahjong Assistant**
- **FitPretty**

## Goals

1. Increase organic search visibility with indexable pages and useful content.
2. Convert visitors into App Store clicks and downloads.
3. Present the developer as a credible independent creator with a coherent product line.
4. Support both Chinese and English users without duplicating effort.

## Non-goals

- Native iOS app development
- User login, payments, or backend account systems
- Content automation or CMS integration in phase one
- Social/community features

## Site structure

### 1. Home page

Purpose: establish brand, summarize all apps, and route traffic to the right destination.

Sections:

- Hero with developer name, short value proposition, and primary App Store CTA
- App grid with the four featured apps
- “Why these apps” section for search relevance
- FAQ section for long-tail SEO
- Footer with language links and download links

### 2. App detail pages

One page per app. Each page should include:

- App summary
- Key features
- Use cases
- Screenshot/gallery area
- Download CTA
- Related FAQs
- Internal links to supporting articles

### 3. SEO content pages

Create topic pages that target search intent around the apps and their categories. Examples:

- AI journal app for daily reflection
- RSS reader for information overload
- Mahjong helper / practice assistant
- Fitness tracking for aesthetic body goals

These pages should explain the problem, how the app helps, and why the app is worth downloading.

## Content strategy

The site should not read like a thin app listing. Each app page and article should add genuinely useful context:

- What problem the app solves
- Who it is for
- How it differs from generic alternatives
- Common questions and objections
- Clear next step: download the app

Copy should be written in **Chinese first**, with **English parallel text** for key headings, summaries, and CTAs.

## SEO requirements

Each page must include:

- Unique `title`
- Unique `meta description`
- Canonical URL
- Open Graph metadata
- `hreflang` for Chinese and English versions
- Structured data using `SoftwareApplication` where applicable

Internal linking rules:

- Home page links to all app pages
- App pages link to related articles
- Articles link back to the relevant app page and download CTA

## Design requirements

- Clean, independent-developer aesthetic
- Fast-loading, mobile-first layout
- Strong visual hierarchy for download buttons
- Minimal animation, no heavy effects
- Consistent card, section, and CTA patterns across pages

## Implementation approach

Use a static site architecture with shared header/footer, reusable content sections, and per-page metadata. Keep the first version simple so the site is easy to extend with more articles and app pages later.

Recommended initial implementation:

- Static HTML/CSS/JS or an equivalent static site setup
- Shared content data source for app metadata
- Separate files for home, app pages, and article pages

## Success criteria

- The site has a clear homepage and dedicated pages for each app.
- Every page has SEO metadata and at least one App Store CTA.
- The site can support bilingual content without clutter.
- Search-oriented pages exist for the main app categories.
- The structure is extensible for future apps and articles.

