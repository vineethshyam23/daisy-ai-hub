/**
 * API Token Management using Google Cloud Secret Manager
 * Centralized token management for secure backend communication
 * Tokens are fetched via server-side API for better security
 */

interface TokenCache {
  token: string | null
  expiresAt: number
  isRefreshing: boolean
}

// Token cache - valid for 30 minutes
const tokenCache: TokenCache = {
  token: null,
  expiresAt: 0,
  isRefreshing: false
}

// Cache duration in milliseconds (30 minutes)
const CACHE_DURATION = 30 * 60 * 1000

/**
 * Composable for API Token management
 */
export const useApiToken = () => {
  /**
   * Retrieves the API token via server-side API endpoint
   * This approach is more secure as the Secret Manager client runs on the server
   */
  const fetchTokenFromServer = async (): Promise<string> => {
    try {
      console.log('🔐 Client: Fetching API token from server endpoint')
      console.log('📡 Client: Making request to /api/auth-token')
      
      // Call our server API endpoint
      const response = await $fetch<{
        success: boolean
        token: string
        cached: boolean
        expiresIn: number
      }>('/api/auth-token')
      
      console.log('📦 Client: Server response received')
      console.log(`✅ Client: Response success: ${response.success}`)
      console.log(`💾 Client: Token was cached on server: ${response.cached}`)
      console.log(`⏰ Client: Server token expires in: ${Math.round(response.expiresIn / 1000 / 60)} minutes`)
      console.log(`🔑 Client: Token length: ${response.token?.length || 0} characters`)
      
      if (response.token) {
        console.log(`🔑 Client: Token preview: ${response.token.substring(0, 10)}...${response.token.substring(response.token.length - 4)}`)
      }
      
      if (!response.success || !response.token) {
        console.error('❌ Client: Server returned invalid token response')
        console.error(`🔍 Client: Full response: ${JSON.stringify(response, null, 2)}`)
        throw new Error('Server returned invalid token response')
      }
      
      console.log(`✅ Client: API token successfully retrieved from server (cached: ${response.cached})`)
      return response.token
      
    } catch (error) {
      console.error('❌ Client: Error fetching API token from server:', error)
      
      // Provide helpful error information
      if (error instanceof Error) {
        console.error(`🔍 Client: Error type: ${error.constructor.name}`)
        console.error(`💬 Client: Error message: ${error.message}`)
        
        if (error.message.includes('500')) {
          console.error('💡 Client: Server-side error - check server logs for Secret Manager issues')
        } else if (error.message.includes('404')) {
          console.error('💡 Client: Server API endpoint not found - check if /api/auth-token.get.ts exists')
        } else if (error.message.includes('fetch')) {
          console.error('💡 Client: Network error - check if server is running')
        }
      }
      
      throw new Error(`Failed to retrieve API token from server: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  /**
   * Gets the cached token or fetches a new one if expired
   */
  const getApiToken = async (): Promise<string> => {
    const now = Date.now()
    
    console.log('🎯 Client: getApiToken() called')
    console.log(`📊 Client: Current timestamp: ${now}`)
    console.log(`💾 Client: Cache status - hasToken: ${!!tokenCache.token}, expiresAt: ${tokenCache.expiresAt}, isRefreshing: ${tokenCache.isRefreshing}`)
    
    // Return cached token if still valid
    if (tokenCache.token && now < tokenCache.expiresAt) {
      const expiresIn = tokenCache.expiresAt - now
      console.log(`✅ Client: Returning cached token (expires in ${Math.round(expiresIn / 1000 / 60)} minutes)`)
      console.log(`🔑 Client: Cached token preview: ${tokenCache.token.substring(0, 10)}...${tokenCache.token.substring(tokenCache.token.length - 4)}`)
      return tokenCache.token
    }
    
    console.log('⏰ Client: Token expired or not cached, need to fetch new one')
    
    // Prevent multiple concurrent requests
    if (tokenCache.isRefreshing) {
      console.log('⏳ Client: Token refresh already in progress, waiting...')
      
      // Wait for the ongoing refresh to complete
      let waitCount = 0
      while (tokenCache.isRefreshing) {
        await new Promise(resolve => setTimeout(resolve, 100))
        waitCount++
        if (waitCount % 10 === 0) {
          console.log(`⏳ Client: Still waiting for token refresh (${waitCount * 100}ms elapsed)`)
        }
      }
      
      console.log('✅ Client: Token refresh completed by another request')
      
      // Return the token that was just fetched
      if (tokenCache.token && now < tokenCache.expiresAt) {
        console.log('🔑 Client: Using newly fetched token from concurrent request')
        return tokenCache.token
      }
    }
    
    // Fetch new token
    console.log('🔄 Client: Starting token refresh process')
    tokenCache.isRefreshing = true
    
    try {
      const token = await fetchTokenFromServer()
      
      // Update cache
      tokenCache.token = token
      tokenCache.expiresAt = now + CACHE_DURATION
      
      console.log('💾 Client: Token cached successfully')
      console.log(`⏰ Client: Cache expires at: ${new Date(tokenCache.expiresAt).toISOString()}`)
      console.log(`⏱️ Client: Cache duration: ${CACHE_DURATION / 1000 / 60} minutes`)
      
      return token
    } finally {
      tokenCache.isRefreshing = false
      console.log('🔓 Client: Token refresh lock released')
    }
  }

  /**
   * Creates headers with the API token for backend requests
   */
  const getAuthenticatedHeaders = async (additionalHeaders: Record<string, string> = {}, skipContentType = false): Promise<Record<string, string>> => {
    try {
      console.log('🔑 Client: Creating authenticated headers')
      console.log(`📋 Client: Additional headers: ${JSON.stringify(additionalHeaders)}`)
      console.log(`📋 Client: Skip Content-Type: ${skipContentType}`)
      
      const token = await getApiToken()
      
      const headers: Record<string, string> = {
        'Authorization': `Bearer ${token}`,
        ...additionalHeaders
      }
      
      // Only add Content-Type if not skipped (important for FormData)
      if (!skipContentType) {
        headers['Content-Type'] = 'application/json'
      }
      
      console.log('✅ Client: Authenticated headers created successfully')
      console.log(`🔑 Client: Authorization header preview: Bearer ${token.substring(0, 10)}...${token.substring(token.length - 4)}`)
      console.log(`📋 Client: Final headers: ${JSON.stringify(Object.keys(headers))}`)
      
      return headers
    } catch (error) {
      console.error('❌ Client: Failed to get authenticated headers:', error)
      
      // Return headers without token in case of error
      // This allows the app to continue functioning, but backend will reject unauthorized requests
      const fallbackHeaders: Record<string, string> = {
        ...additionalHeaders
      }
      
      // Only add Content-Type if not skipped
      if (!skipContentType) {
        fallbackHeaders['Content-Type'] = 'application/json'
      }
      
      console.warn('⚠️ Client: Returning fallback headers without authentication token')
      console.log(`📋 Client: Fallback headers: ${JSON.stringify(Object.keys(fallbackHeaders))}`)
      
      return fallbackHeaders
    }
  }

  /**
   * Makes an authenticated API request using $fetch
   */
  const authenticatedFetch = async <T = any>(
    url: string, 
    options: Parameters<typeof $fetch>[1] = {}
  ): Promise<T> => {
    try {
      console.log(`🌐 Client: Making authenticated $fetch request to: ${url}`)
      console.log(`📋 Client: Request method: ${options.method || 'GET'}`)
      console.log(`📦 Client: Has body: ${!!options.body}`)
      
      // Check if body is FormData - if so, skip Content-Type header
      const isFormData = options.body instanceof FormData
      console.log(`📋 Client: Is FormData: ${isFormData}`)
      
      const headers = await getAuthenticatedHeaders(options.headers as Record<string, string>, isFormData)
      
      const requestOptions = {
        ...options,
        headers
      }
      
      console.log('🚀 Client: Sending authenticated request...')
      const startTime = Date.now()
      
      const result = await $fetch<T>(url, requestOptions)
      
      const endTime = Date.now()
      console.log(`✅ Client: Authenticated $fetch completed successfully (${endTime - startTime}ms)`)
      console.log(`📦 Client: Response type: ${typeof result}`)
      
      return result
    } catch (error) {
      console.error('❌ Client: Authenticated fetch failed:', error)
      console.error(`🌐 Client: Failed URL: ${url}`)
      console.error(`📋 Client: Request method: ${options.method || 'GET'}`)
      
      // Re-throw with additional context
      if (error instanceof Error) {
        console.error(`🔍 Client: Error type: ${error.constructor.name}`)
        console.error(`💬 Client: Error message: ${error.message}`)
        throw new Error(`API request failed: ${error.message}`)
      }
      throw error
    }
  }

  /**
   * Makes an authenticated API request using native fetch
   */
  const authenticatedFetchNative = async (
    url: string, 
    options: RequestInit = {}
  ): Promise<Response> => {
    try {
      console.log(`🌐 Client: Making authenticated native fetch request to: ${url}`)
      console.log(`📋 Client: Request method: ${options.method || 'GET'}`)
      console.log(`📦 Client: Has body: ${!!options.body}`)
      
      // Check if body is FormData - if so, skip Content-Type header
      const isFormData = options.body instanceof FormData
      console.log(`📋 Client: Is FormData: ${isFormData}`)
      
      const headers = await getAuthenticatedHeaders(options.headers as Record<string, string>, isFormData)
      
      const requestOptions = {
        ...options,
        headers
      }
      
      console.log('🚀 Client: Sending authenticated native fetch request...')
      const startTime = Date.now()
      
      const response = await fetch(url, requestOptions)
      
      const endTime = Date.now()
      console.log(`📡 Client: Native fetch response received (${endTime - startTime}ms)`)
      console.log(`📊 Client: Response status: ${response.status} ${response.statusText}`)
      console.log(`📋 Client: Response headers: ${JSON.stringify([...response.headers.entries()])}`)
      console.log(`✅ Client: Response ok: ${response.ok}`)
      
      return response
    } catch (error) {
      console.error('❌ Client: Authenticated native fetch failed:', error)
      console.error(`🌐 Client: Failed URL: ${url}`)
      console.error(`📋 Client: Request method: ${options.method || 'GET'}`)
      
      if (error instanceof Error) {
        console.error(`🔍 Client: Error type: ${error.constructor.name}`)
        console.error(`💬 Client: Error message: ${error.message}`)
      }
      
      throw error
    }
  }

  /**
   * Clears the token cache (useful for testing or forced refresh)
   */
  const clearTokenCache = () => {
    console.log('🧹 Client: Clearing token cache...')
    console.log(`📊 Client: Cache before clear - hasToken: ${!!tokenCache.token}, expiresAt: ${tokenCache.expiresAt}, isRefreshing: ${tokenCache.isRefreshing}`)
    
    tokenCache.token = null
    tokenCache.expiresAt = 0
    tokenCache.isRefreshing = false
    
    console.log('✅ Client: Token cache cleared successfully')
  }

  /**
   * Gets token cache status (useful for debugging)
   */
  const getTokenCacheStatus = () => {
    const now = Date.now()
    const status = {
      hasToken: !!tokenCache.token,
      isExpired: now >= tokenCache.expiresAt,
      isRefreshing: tokenCache.isRefreshing,
      expiresIn: Math.max(0, tokenCache.expiresAt - now),
      expiresAt: new Date(tokenCache.expiresAt).toISOString(),
      tokenPreview: tokenCache.token ? `${tokenCache.token.substring(0, 10)}...${tokenCache.token.substring(tokenCache.token.length - 4)}` : null,
      tokenLength: tokenCache.token?.length || 0,
      currentTime: new Date(now).toISOString()
    }
    
    console.log('📊 Client: Token cache status requested')
    console.log(`🔍 Client: Cache status details:`, status)
    
    return status
  }

  return {
    getApiToken,
    getAuthenticatedHeaders,
    authenticatedFetch,
    authenticatedFetchNative,
    clearTokenCache,
    getTokenCacheStatus
  }
}
