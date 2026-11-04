import { getEnvironment } from '~/config/firebase.config'

export default defineNuxtPlugin({
  name: 'adobe-launch-plugin',
  order: 50, // Run before adobe-tracking but after basic setup
  setup() {
    // Only run on client side
    if (typeof window === 'undefined') return

    // Initialize Adobe Data Layer if not exists
    window.adobeDataLayer = window.adobeDataLayer || []
    
    // Use environment detection from firebase config (called at runtime)
    const isDevelopment = getEnvironment() === 'development'
    const scriptSrc = isDevelopment 
      ? 'https://assets.adobedtm.com/de391e1809aa/5b34f11368eb/launch-251ab9c5f7ce-development.min.js'
      : 'https://assets.adobedtm.com/de391e1809aa/5b34f11368eb/launch-02c881f1f927.min.js'
    
    
    // Load Adobe Launch script
    const script = document.createElement('script')
    script.src = scriptSrc
    script.async = true
    script.onload = () => {
      console.log(`[Adobe Launch] ✅ Script loaded successfully (${isDevelopment ? 'DEV' : 'PROD'} environment)`)
    }
    script.onerror = () => {
      console.error('[Adobe Launch] ❌ Failed to load script')
    }
    
    document.head.appendChild(script)
  }
})

// TypeScript declarations
declare global {
  interface Window {
    adobeDataLayer: any[]
  }
} 