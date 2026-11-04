export default defineNuxtPlugin({
  name: 'adobe-tracking-plugin',
  order: 100, // Run after router and auth are ready
  setup(nuxtApp) {
    // Only run on client side
    if (process.server) return

    // Wait for router to be available
    nuxtApp.hook('app:mounted', () => {
      const router = useRouter()
      const { trackPageview } = useAdobeTracking()

      // Track initial page load with delay
      setTimeout(() => {
        try {
          const route = useRoute()
          const pageTitle = getPageTitle(route)
          trackPageview(pageTitle)
        } catch (error) {
          console.error('[Adobe Tracking] Error tracking initial page:', error)
        }
      }, 2000) // Increased delay to ensure everything is ready

      // Track page changes
      router.afterEach((to) => {
        nextTick(() => {
          setTimeout(() => {
            try {
              const pageTitle = getPageTitle(to)
              trackPageview(pageTitle)
            } catch (error) {
              console.error('[Adobe Tracking] Error tracking page change:', error)
            }
          }, 500)
        })
      })
    })

    /**
     * Generate page title from route
     */
    function getPageTitle(route: any): string {
      // Check if page has meta title
      if (route.meta?.title) {
        return route.meta.title
      }

      // Generate title from route path
      const pathSegments = route.path.split('/').filter(Boolean)
      
      if (pathSegments.length === 0) {
        return 'DAISY - Home'
      }

      // Handle specific routes
      switch (pathSegments[0]) {
        case 'ai':
          if (pathSegments[1]) {
            const assistantName = pathSegments[1]
              .split('-')
              .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1))
              .join(' ')
            return `DAISY - ${assistantName}`
          }
          return 'DAISY - AI Assistants'
        
        case 'search':
          if (pathSegments[1]) {
            const searchType = pathSegments[1]
              .charAt(0).toUpperCase() + pathSegments[1].slice(1)
            return `DAISY - ${searchType} Search`
          }
          return 'DAISY - Search'
        
        case 'admin':
          if (pathSegments[1]) {
            const adminPage = pathSegments[1]
              .charAt(0).toUpperCase() + pathSegments[1].slice(1)
            return `DAISY - Admin ${adminPage}`
          }
          return 'DAISY - Admin'
        
        case 'profile':
          return 'DAISY - Profile'
        
        case 'login':
          return 'DAISY - Login'
        
        case 'reset-password':
          return 'DAISY - Reset Password'
        
        default:
          const pageName = pathSegments[0]
            .charAt(0).toUpperCase() + pathSegments[0].slice(1)
                      return `DAISY - ${pageName}`
      }
    }
  }
}) 