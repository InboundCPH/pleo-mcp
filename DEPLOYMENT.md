# Deployment Guide

This guide explains how to deploy the Pleo MCP server to Railway.

## Prerequisites

1. A [Railway](https://railway.app/) account
2. A Pleo API key (Bearer token)
3. Git installed locally

## Deployment Steps

### Option 1: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Railway project**
   ```bash
   cd pleo-mcp
   railway init
   ```

4. **Set environment variables**
   ```bash
   railway variables set PLEO_API_KEY=your_api_key_here
   ```

5. **Deploy**
   ```bash
   railway up
   ```

### Option 2: Deploy via Railway Dashboard

1. **Create a new project**
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click "New Project"
   - Select "Deploy from GitHub repo"

2. **Connect your repository**
   - Authorize Railway to access your GitHub account
   - Select the `InboundCPH/pleo-mcp` repository

3. **Configure environment variables**
   - In the project settings, go to "Variables"
   - Add a new variable:
     - Name: `PLEO_API_KEY`
     - Value: Your Pleo API key (Bearer token)

4. **Deploy**
   - Railway will automatically detect the configuration and deploy
   - Wait for the deployment to complete

### Option 3: One-Click Deploy

Click the button below to deploy directly to Railway:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/InboundCPH/pleo-mcp)

## Post-Deployment

### Verify Deployment

1. Check the deployment logs in Railway dashboard
2. Ensure the service is running without errors
3. Note the service URL provided by Railway

### Get Your Pleo API Key

1. Log in to your Pleo account
2. Navigate to Settings → Integrations → API Keys
3. Generate a new API key if you don't have one
4. Copy the API key (it will be shown only once)

### Configure MCP Client

To use this MCP server with a compatible client:

1. Add the server configuration to your MCP client settings
2. Use the Railway service URL as the server endpoint
3. The server will authenticate with Pleo using the API key you configured

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PLEO_API_KEY` | Yes | Your Pleo API Bearer token for authentication |

## Monitoring

Railway provides built-in monitoring:

- **Logs**: View real-time logs in the Railway dashboard
- **Metrics**: Monitor CPU, memory, and network usage
- **Health Checks**: Railway automatically monitors service health

## Troubleshooting

### Service Won't Start

1. Check the logs in Railway dashboard for error messages
2. Verify that `PLEO_API_KEY` is set correctly
3. Ensure the API key has the necessary permissions

### API Errors

1. Verify your Pleo API key is valid and not expired
2. Check that your Pleo account has API access enabled
3. Review the Pleo API documentation for rate limits

### Connection Issues

1. Ensure the Railway service is running (check dashboard)
2. Verify the service URL is correct
3. Check Railway's status page for any platform issues

## Updating the Server

### Via GitHub

1. Push changes to the GitHub repository
2. Railway will automatically detect and redeploy

### Via Railway CLI

```bash
railway up
```

## Scaling

Railway automatically handles scaling based on your plan:

- **Hobby Plan**: Single instance, suitable for development
- **Pro Plan**: Auto-scaling based on load

## Cost Estimation

Railway pricing is based on:
- Compute time (CPU/Memory usage)
- Network egress
- Storage

Typical costs for this MCP server:
- **Development**: $0-5/month (Hobby plan)
- **Production**: $5-20/month (Pro plan, depending on usage)

## Security Best Practices

1. **Never commit API keys** to the repository
2. **Use environment variables** for all sensitive data
3. **Rotate API keys** regularly
4. **Monitor access logs** for suspicious activity
5. **Enable Railway's security features** (if available)

## Support

For issues related to:
- **Pleo API**: Contact [Pleo Support](https://help.pleo.io/)
- **Railway**: Check [Railway Documentation](https://docs.railway.app/)
- **This MCP Server**: Open an issue on [GitHub](https://github.com/InboundCPH/pleo-mcp/issues)
