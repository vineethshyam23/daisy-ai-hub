import { useAdobeTracking } from '~/composables/useAdobeTracking'

export default defineNuxtPlugin({
  name: 'button-tracking-plugin',
  order: 200, // Run after other essential plugins
  setup(nuxtApp) {
    // Only run on client side
    if (process.server) return

    const { trackButtonClick } = useAdobeTracking()

    // Global click handler for automatic button tracking
    const handleButtonClick = (event: Event) => {
      const target = event.target as HTMLElement
      const button = target.closest('[data-track-button]') as HTMLElement
      
      if (!button) return

      const eventValue = button.getAttribute('data-track-button')
      const eventInfoAttr = button.getAttribute('data-track-info')
      
      if (eventValue) {
        let eventInfo = {}
        
        // Parse JSON event info if provided
        if (eventInfoAttr) {
          try {
            eventInfo = JSON.parse(eventInfoAttr)
          } catch (error) {
            console.warn('[Button Tracking] Invalid JSON in data-track-info:', eventInfoAttr)
          }
        }

        // Track the button click
        trackButtonClick(eventValue, eventInfo, button)
      }
    }

    // Add global click listener after app is mounted
    nuxtApp.hook('app:mounted', () => {
      document.addEventListener('click', handleButtonClick)
    })
  }
}) 