// Global Google Search Widget Manager
declare global {
  interface Window {
    __googleSearchReady?: boolean
    __googleSearchLoading?: boolean
    __googleSearchCallbacks?: (() => void)[]
  }
}

export default defineNuxtPlugin(() => {
  // Only run on client side
  if (process.server) return

  // Initialize global state
  window.__googleSearchReady = false
  window.__googleSearchLoading = false
  window.__googleSearchCallbacks = []

  // Add reCAPTCHA hiding CSS
  const style = document.createElement('style')
  style.textContent = `
    /* Hide Google reCAPTCHA */
    .grecaptcha-badge {
      display: none !important;
    }
    
    /* Hide any reCAPTCHA related elements */
    iframe[src*="recaptcha"] {
      display: none !important;
    }
    
    /* Hide reCAPTCHA container */
    div[class*="recaptcha"] {
      display: none !important;
    }
    
    /* Additional reCAPTCHA hiding */
    .g-recaptcha {
      display: none !important;
    }
    
    /* Hide any Google verification badges */
    div[style*="visibility: visible"][style*="opacity: 1"] iframe {
      display: none !important;
    }
    
    /* Target specific reCAPTCHA positioning */
    div[style*="position: fixed"][style*="bottom: 14px"][style*="right: 14px"] {
      display: none !important;
    }
  `
  document.head.appendChild(style)

  // Function to load Google script once
  const loadGoogleScript = () => {
    if (window.__googleSearchReady || window.__googleSearchLoading) {
      return
    }

    window.__googleSearchLoading = true

    const script = document.createElement('script')
    script.src = 'https://cloud.google.com/ai/gen-app-builder/client?hl=en_US'
    script.async = true
    
    script.onload = () => {
      window.__googleSearchReady = true
      window.__googleSearchLoading = false
      
      // Execute all waiting callbacks
      if (window.__googleSearchCallbacks) {
        window.__googleSearchCallbacks.forEach(callback => callback())
        window.__googleSearchCallbacks = []
      }
    }
    
    script.onerror = () => {
      console.error('❌ Failed to load Google Search Script')
      window.__googleSearchLoading = false
    }
    
    document.head.appendChild(script)
  }

  // Global function to register callbacks
  window.onGoogleSearchReady = (callback: () => void) => {
    if (window.__googleSearchReady) {
      callback()
    } else {
      window.__googleSearchCallbacks = window.__googleSearchCallbacks || []
      window.__googleSearchCallbacks.push(callback)
      
      // Start loading if not already loading
      if (!window.__googleSearchLoading) {
        loadGoogleScript()
      }
    }
  }

  // Start loading immediately
  loadGoogleScript()
})

// TypeScript declarations
declare global {
  interface Window {
    onGoogleSearchReady: (callback: () => void) => void
  }
}