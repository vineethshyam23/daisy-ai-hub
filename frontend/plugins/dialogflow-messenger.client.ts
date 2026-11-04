// Extend Window interface for TypeScript
declare global {
  interface Window {
    __dialogflowCleanup?: () => void
    __dialogflowScriptLoaded?: boolean
    __dialogflowScriptLoading?: boolean
  }
}

export default defineNuxtPlugin(async () => {
  // Only run on client side
  if (process.server) return

  // Import environment detection
  const { getEnvironment } = await import('~/config/firebase.config')
  const environment = getEnvironment()

  // Function to check if current page should show chatbot
  const shouldShowChatbot = () => {
    const currentPath = window.location.pathname
    const hiddenPaths = ['/login', '/signup', '/reset-password', '/verify-email']
    return !hiddenPaths.includes(currentPath)
  }

  // Function to load Dialogflow Messenger
  const loadDialogflowMessenger = () => {
    // Check if we should show chatbot on current page
    if (!shouldShowChatbot()) {
      return
    }

    // Check if already loaded
    if (document.querySelector('df-messenger')) {
      return
    }

    // Check if script is already loaded or loading
    if (window.__dialogflowScriptLoaded || window.__dialogflowScriptLoading) {
      // If script is loaded but no messenger element, create it
      if (window.__dialogflowScriptLoaded) {
        createMessengerElement()
      }
      return
    }

    // Mark as loading
    window.__dialogflowScriptLoading = true

    // Add CSS (only if not already added)
    if (!document.querySelector('link[href*="df-messenger-default.css"]')) {
      const link = document.createElement('link')
      link.rel = 'stylesheet'
      link.href = 'https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/themes/df-messenger-default.css'
      document.head.appendChild(link)
    }

    // Add Script (only if not already added)
    if (!document.querySelector('script[src*="df-messenger.js"]')) {
      const script = document.createElement('script')
      script.src = 'https://www.gstatic.com/dialogflow-console/fast/df-messenger/prod/v1/df-messenger.js'
      script.onload = () => {
        window.__dialogflowScriptLoaded = true
        window.__dialogflowScriptLoading = false
        createMessengerElement()
      }
      
      script.onerror = () => {
        console.error('Failed to load Dialogflow Messenger script')
        window.__dialogflowScriptLoading = false
      }
      
      document.head.appendChild(script)
    }
  }

  // Function to create the messenger element
  const createMessengerElement = () => {
    // Check if we should show chatbot on current page
    if (!shouldShowChatbot()) {
      return
    }

    // Don't create if already exists
    if (document.querySelector('df-messenger')) {
      return
    }

    try {
      // Create Dialogflow Messenger element with new configuration
      const messenger = document.createElement('df-messenger')
      messenger.setAttribute('location', 'europe-west3')
      messenger.setAttribute('project-id', 'customersupport-voice-bot-prod')
      messenger.setAttribute('agent-id', '9c19a6bc-8f02-40cd-913c-f429f9d33fd4')
      messenger.setAttribute('language-code', 'en')
      messenger.setAttribute('max-query-length', '-1')

      // Create chat bubble with new title
      const chatBubble = document.createElement('df-messenger-chat-bubble')
      chatBubble.setAttribute('chat-title', 'Chat with AI Hub')
      messenger.appendChild(chatBubble)

      // Add error event listener
      messenger.addEventListener('df-messenger-error', (event) => {
        const customEvent = event as CustomEvent
        console.error('Dialogflow Messenger Error:', customEvent.detail)
        
        // Check if it's an auth error
        if (customEvent.detail?.error?.code === 'AUTH_ERROR') {
          console.error('AUTH_ERROR Details:', {
            message: customEvent.detail.error.message,
            status: customEvent.detail.error.status,
            environment: environment,
            domain: window.location.hostname,
            origin: window.location.origin
          })
          
          // Show user-friendly error in development
          if (environment === 'development') {
            console.warn(`
🤖 CHATBOT CONFIGURATION ISSUE:
The Dialogflow chatbot is getting a 403 AUTH_ERROR. This usually means:

1. The chatbot isn't configured to allow requests from this domain (${window.location.hostname})
2. The project-id or agent-id might be incorrect
3. The Dialogflow Messenger integration isn't properly enabled

To fix this, you need to:
1. Go to Google Cloud Console → Dialogflow
2. Select your agent: customersupport-voice-bot-prod
3. Go to Integrations → Dialogflow Messenger
4. Add '${window.location.origin}' to the allowed origins
5. Make sure the integration is enabled

Current config:
- Project ID: customersupport-voice-bot-prod
- Agent ID: 9c19a6bc-8f02-40cd-913c-f429f9d33fd4
- Location: europe-west3
            `)
          }
        }
      })

      // Add to body
      document.body.appendChild(messenger)

      // Add custom styles matching the provided configuration (only if not already added)
      if (!document.querySelector('style[data-dialogflow-styles]')) {
        const style = document.createElement('style')
        style.setAttribute('data-dialogflow-styles', 'true')
        style.textContent = `
          df-messenger {
            z-index: 999;
            position: fixed;
            --df-messenger-font-color: #000;
            --df-messenger-font-family: Lato;
            --df-messenger-chat-background: #f3f6fc;
            --df-messenger-message-user-background: #ed6938;
            --df-messenger-message-bot-background: #fff;
            bottom: 16px;
            right: 16px;
          }

          /* Hide on mobile devices smaller than 768px */
          @media (max-width: 767px) {
            df-messenger {
              display: none;
            }
          }

          /* Show error indicator in development */
          ${environment === 'development' ? `
          df-messenger[data-error="true"] {
            border: 2px solid #ef4444;
            opacity: 0.7;
          }
          ` : ''}
        `
        document.head.appendChild(style)
      }

    } catch (error) {
      console.error('Error creating Dialogflow Messenger element:', error)
    }
  }

  // Function to remove Dialogflow Messenger
  const removeDialogflowMessenger = () => {
    const messenger = document.querySelector('df-messenger')
    if (messenger) {
      messenger.remove()
    }
  }

  // Function to handle route changes
  const handleRouteChange = () => {
    if (shouldShowChatbot()) {
      loadDialogflowMessenger()
    } else {
      removeDialogflowMessenger()
    }
  }

  // Initialize chatbot
  const initializeWidget = () => {
    // Initial load based on current route
    handleRouteChange()
    
    // Listen for route changes (Nuxt's client-side navigation)
    // This works for both Vue Router and Nuxt routing
    if (typeof window !== 'undefined') {
      // Listen for popstate events (back/forward buttons)
      window.addEventListener('popstate', handleRouteChange)
      
      // Listen for Nuxt route changes
      window.addEventListener('nuxt:page:finish', handleRouteChange)
      
      // Fallback: periodically check route changes
      let lastPath = window.location.pathname
      setInterval(() => {
        if (window.location.pathname !== lastPath) {
          lastPath = window.location.pathname
          handleRouteChange()
        }
      }, 1000)
    }
  }

  // Initialize when ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeWidget)
  } else {
    initializeWidget()
  }

  // Cleanup function for hot reload in development
  if (process.env.NODE_ENV === 'development') {
    const cleanup = () => {
      const messenger = document.querySelector('df-messenger')
      if (messenger) {
        messenger.remove()
      }
      // Reset loading flags
      window.__dialogflowScriptLoading = false
      // Note: We don't reset __dialogflowScriptLoaded because the script is still in the DOM
    }

    // Store cleanup function globally for hot reload
    window.__dialogflowCleanup = cleanup
  }
}) 