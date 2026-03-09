---
name: x-twitter-scraper
description: Extract X/Twitter data using the Xquik MCP server. Use when user needs to fetch tweets, user profiles, followers, following lists, search results, community posts, or any X/Twitter data. Activates on mentions of Twitter, X, tweets, followers, following, likes, retweets, or social media data extraction.
---

# X/Twitter Scraper

Extract X/Twitter data through the Xquik MCP server with 76 REST API endpoints and 20 extraction tools.

## When to Use

- User asks to fetch tweets, replies, or quote tweets
- User needs user profiles, followers, or following lists
- User wants to search tweets by keyword, hashtag, or query
- User needs to extract likes, retweets, or bookmarks
- User asks about monitoring X/Twitter accounts
- User wants to run giveaway draws from tweet engagement
- User needs to export X/Twitter data for analysis
- Context mentions Twitter, X, tweets, or social media scraping

## Setup

Configure the MCP server in your Claude Code settings:

```json
{
  "mcpServers": {
    "xquik": {
      "command": "npx",
      "args": ["-y", "@xquik/mcp-server@latest"],
      "env": {
        "XQUIK_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Get an API key at [xquik.com](https://xquik.com).

## Available MCP Tools

- `search_tweets` - Search tweets by keyword or query
- `get_user_profile` - Get user profile by username
- `get_user_tweets` - Get recent tweets from a user
- `get_tweet_replies` - Get replies to a specific tweet
- `get_tweet_retweets` - Get users who retweeted
- `get_tweet_likes` - Get users who liked a tweet
- `get_followers` - Get followers of a user
- `get_following` - Get accounts a user follows

## Resources

- [Documentation](https://xquik.com)
- [GitHub](https://github.com/Xquik-dev/x-twitter-scraper)
- [npm](https://www.npmjs.com/package/@xquik/mcp-server)
