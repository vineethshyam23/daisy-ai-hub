import { useAuthStore } from '~/stores/auth'
import { useRoleStore } from '~/stores/roles'

export const useAdobeTracking = () => {
  const authStore = useAuthStore()
  const roleStore = useRoleStore()

  /**
   * Get company name based on user's email domain
   */
  const getCompany = (): string => {
    const userEmail = authStore.user?.email || ''
    const emailDomain = userEmail.split('@')[1]?.toLowerCase() || ''
    
    switch (emailDomain) {
      // Add your organisation's email domains here, e.g.:
      // case 'yourcompany.com':
      //   return 'Your Company Name'
      default:
        return 'Unknown'
    }
  }

  /**
   * Detect current environment based on hostname and runtime config
   */
  const getEnvironment = (): string => {
    if (typeof window === 'undefined') return 'unknown'
    
    try {
      // Check runtime config for environment
      const runtimeConfig = useRuntimeConfig?.() || {};
      const environment = runtimeConfig.public?.environment;
      
      if (environment === 'production') {
        return 'PROD'
      } else if (environment === 'development') {
        return 'DEV'
      }
    } catch (error) {
      // Ignore runtime config errors
    }
    
    // Fallback to hostname-based detection
    const hostname = window.location.hostname
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname.includes('.local')) {
      return 'DEV'
    }
    return 'PROD'
  }

  /**
   * Track pageview event with Adobe DataLayer
   * @param pageTitle - Title of the current page
   */
  const trackPageview = (pageTitle: string) => {
    if (typeof window === 'undefined' || !window.adobeDataLayer) {
      console.warn('Adobe DataLayer not available')
      return
    }

    try {
      // Get user data from stores
      const userId = authStore.user?.uid || 'anonymous'
      const userRole = roleStore.isAdmin ? 'admin' : 'user'

      // Push pageview event to Adobe DataLayer
      const trackingData = {
        event: 'pageview',
        page: {
          title: pageTitle,
          userId: userId,
          userRole: userRole,
          company: getCompany(),
          environment: getEnvironment()
        }
      }

      window.adobeDataLayer.push(trackingData)
    } catch (error) {
      console.error('❌ Adobe Tracking Error:', error)
    }
  }

  /**
   * Track button click events with structured, analyzable data
   * @param eventValue - Clear identifier of button function (e.g., "Generate Images")
   * @param eventInfo - Structured data object with analyzable parameters
   * @param buttonElement - Optional button element for automatic data extraction
   */
  const trackButtonClick = (
    eventValue: string, 
    eventInfo: Record<string, any> = {}, 
    buttonElement?: HTMLElement
  ) => {
    if (typeof window === 'undefined' || !window.adobeDataLayer) {
      console.warn('Adobe DataLayer not available')
      return
    }

    try {
      const userId = authStore.user?.uid || 'anonymous'
      const userRole = roleStore.isAdmin ? 'admin' : 'user'

      // Get current page context
      const currentRoute = useRoute()
      const pageContext = getPageContext(currentRoute.path)

      // Enhance eventInfo with automatic button data if element provided
      const enhancedEventInfo = {
        ...eventInfo,
        ...extractButtonContext(buttonElement),
        pageContext: pageContext,
        timestamp: new Date().toISOString()
      }

      const trackingData = {
        event: 'button_click',
        eventValue: eventValue,
        eventInfo: enhancedEventInfo,
        userId: userId,
        userRole: userRole,
        page: {
          company: getCompany(),
          environment: getEnvironment()
        }
      }

      window.adobeDataLayer.push(trackingData)
      
    } catch (error) {
      console.error('❌ Adobe Tracking Error:', error)
    }
  }

  /**
   * Extract context from button element and surrounding form
   */
  const extractButtonContext = (buttonElement?: HTMLElement): Record<string, any> => {
    if (!buttonElement) return {}

    const context: Record<string, any> = {}

    // Find parent form or container
    const form = buttonElement.closest('form') || buttonElement.closest('[data-tracking-container]')
    
    if (form) {
      // Extract form data (excluding sensitive text inputs)
      const formElements = form.querySelectorAll('select, input[type="checkbox"], input[type="radio"], input[type="range"], input[type="number"]')
      
      formElements.forEach((element) => {
        const input = element as HTMLInputElement | HTMLSelectElement
        const name = input.name || input.getAttribute('data-tracking-name')
        
        if (name && input.value !== '') {
          if (input.type === 'checkbox') {
            context[name] = (input as HTMLInputElement).checked
          } else if (input.type === 'radio' && (input as HTMLInputElement).checked) {
            context[name] = input.value
          } else if (input.type === 'range' || input.type === 'number') {
            context[name] = parseInt(input.value) || input.value
          } else {
            context[name] = input.value
          }
        }
      })
    }

    return context
  }

  /**
   * Get page context for better event categorization
   */
  const getPageContext = (path: string): string => {
    if (path.startsWith('/ai/')) {
      const assistantName = path.split('/')[2]
      return `ai_assistant_${assistantName.replace(/-/g, '_')}`
    } else if (path.startsWith('/search/')) {
      return `search_${path.split('/')[2]}`
    } else if (path.startsWith('/admin/')) {
      return `admin_${path.split('/')[2] || 'overview'}`
    } else if (path === '/') {
      return 'homepage'
    } else {
      return path.replace(/[\/\-]/g, '_').substring(1) || 'unknown'
    }
  }

  /**
   * Track login events
   * @param userId - User ID from Firebase Auth
   * @param loginMethod - Method used for login ('email_password' or 'gitlab_oauth')
   * @param additionalInfo - Additional contextual information
   */
  const trackLogin = (userId: string, loginMethod: 'email_password' | 'gitlab_oauth' = 'email_password', additionalInfo: Record<string, any> = {}) => {
    if (typeof window === 'undefined' || !window.adobeDataLayer) {
      console.warn('Adobe DataLayer not available')
      return
    }

    try {
      const userEmail = authStore.user?.email || ''
      const emailDomain = userEmail.split('@')[1] || 'unknown'

      const trackingData = {
        event: 'login',
        eventValue: userId,
        eventInfo: {
          loginMethod: loginMethod,
          emailDomain: emailDomain,
          company: getCompany(),
          timestamp: new Date().toISOString(),
          environment: getEnvironment(),
          ...additionalInfo
        }
      }

      window.adobeDataLayer.push(trackingData)
    } catch (error) {
      console.error('❌ Adobe Tracking Error:', error)
    }
  }

  /**
   * Track signup/registration events
   * @param userId - User ID from Firebase Auth
   * @param registrationMethod - Method used for registration
   * @param additionalInfo - Additional contextual information
   */
  const trackSignup = (userId: string, registrationMethod: 'email_password' | 'gitlab_oauth' = 'email_password', additionalInfo: Record<string, any> = {}) => {
    if (typeof window === 'undefined' || !window.adobeDataLayer) {
      console.warn('Adobe DataLayer not available')
      return
    }

    try {
      const userEmail = authStore.user?.email || additionalInfo.email || ''
      const emailDomain = userEmail.split('@')[1] || 'unknown'
      
      // For signup, we might need to calculate company from the email in additionalInfo
      const company = userEmail ? getCompany() : (additionalInfo.email ? 
        (() => {
          const domain = additionalInfo.email.split('@')[1]?.toLowerCase() || ''
          switch (domain) {
            // Add your organisation's email domains here
            default: return 'Unknown'
          }
        })() : 'Unknown')

      const trackingData = {
        event: 'signup',
        eventValue: userId,
        eventInfo: {
          registrationMethod: registrationMethod,
          emailDomain: emailDomain,
          company: company,
          timestamp: new Date().toISOString(),
          environment: getEnvironment(),
          emailVerificationRequired: true, // For Firebase Auth
          ...additionalInfo
        }
      }

      window.adobeDataLayer.push(trackingData)
    } catch (error) {
      console.error('❌ Adobe Tracking Error:', error)
    }
  }

  /**
   * Track logout events
   * @param userId - User ID from Firebase Auth
   * @param additionalInfo - Additional contextual information
   */
  const trackLogout = (userId: string, additionalInfo: Record<string, any> = {}) => {
    if (typeof window === 'undefined' || !window.adobeDataLayer) {
      console.warn('Adobe DataLayer not available')
      return
    }

    try {
      const userEmail = authStore.user?.email || ''
      const emailDomain = userEmail.split('@')[1] || 'unknown'

      const trackingData = {
        event: 'logout',
        eventValue: userId,
        eventInfo: {
          emailDomain: emailDomain,
          timestamp: new Date().toISOString(),
          environment: getEnvironment(),
          sessionDuration: additionalInfo.sessionDuration || 'unknown',
          ...additionalInfo
        }
      }

      window.adobeDataLayer.push(trackingData)
    } catch (error) {
      console.error('❌ Adobe Tracking Error:', error)
    }
  }

  /**
   * Track password recovery events
   * @param userIdentifier - User email or ID for password recovery
   * @param recoveryStep - Step in password recovery process
   * @param additionalInfo - Additional contextual information
   */
  const trackPasswordRecovery = (userIdentifier: string, recoveryStep: 'request' | 'reset_complete' | 'reset_failed', additionalInfo: Record<string, any> = {}) => {
    if (typeof window === 'undefined' || !window.adobeDataLayer) {
      console.warn('Adobe DataLayer not available')
      return
    }

    try {
      // For email-based recovery, use email as identifier; for completed resets, use user ID
      const emailDomain = userIdentifier.includes('@') 
        ? userIdentifier.split('@')[1] 
        : (additionalInfo.email?.split('@')[1] || 'unknown')

      const trackingData = {
        event: 'password_recovery',
        eventValue: userIdentifier,
        eventInfo: {
          recoveryStep: recoveryStep,
          emailDomain: emailDomain,
          timestamp: new Date().toISOString(),
          environment: getEnvironment(),
          ...additionalInfo
        }
      }

      window.adobeDataLayer.push(trackingData)
    } catch (error) {
      console.error('❌ Adobe Tracking Error:', error)
    }
  }

  /**
   * Track error events
   * @param errorCategory - Short categorical classification of the error
   * @param errorMessage - Detailed error description
   * @param additionalInfo - Additional contextual information
   */
  const trackError = (errorCategory: string, errorMessage: string, additionalInfo: Record<string, any> = {}) => {
    if (typeof window === 'undefined' || !window.adobeDataLayer) {
      console.warn('Adobe DataLayer not available')
      return
    }

    try {
      const userId = authStore.user?.uid || 'anonymous'
      const userRole = roleStore.isAdmin ? 'admin' : 'user'
      
      // Get current page context
      const currentRoute = useRoute()
      const pageContext = getPageContext(currentRoute.path)

      const trackingData = {
        event: 'error',
        eventValue: errorCategory,
        eventInfo: {
          errorMessage: errorMessage,
          pageContext: pageContext,
          userId: userId,
          userRole: userRole,
          timestamp: new Date().toISOString(),
          environment: getEnvironment(),
          userAgent: window.navigator.userAgent,
          url: window.location.href,
          ...additionalInfo
        }
      }

      window.adobeDataLayer.push(trackingData)
    } catch (error) {
      console.error('❌ Adobe Tracking Error (in error tracking):', error)
    }
  }

  /**
   * Track token usage events
   * @param tokenAmount - Number of tokens used
   * @param toolName - Name of the tool in snake_case (e.g., 'image_generator', 'email_responder')
   * @param additionalInfo - Additional contextual information
   */
  const trackTokenUsage = (tokenAmount: number, toolName: string, additionalInfo: Record<string, any> = {}) => {
    if (typeof window === 'undefined' || !window.adobeDataLayer) {
      console.warn('Adobe DataLayer not available')
      return
    }

    try {
      const userId = authStore.user?.uid || 'anonymous'
      const userRole = roleStore.isAdmin ? 'admin' : 'user'
      
      // Get current page context
      const currentRoute = useRoute()
      const pageContext = getPageContext(currentRoute.path)

      const trackingData = {
        event: 'token_used',
        eventValue: tokenAmount.toString(),
        eventInfo: toolName,
        userId: userId,
        userRole: userRole,
        additionalData: {
          pageContext: pageContext,
          timestamp: new Date().toISOString(),
          environment: getEnvironment(),
          ...additionalInfo
        }
      }

      window.adobeDataLayer.push(trackingData)
      
    } catch (error) {
      console.error('❌ Adobe Tracking Error:', error)
    }
  }

  /**
   * Track custom events (for future use)
   * @param eventName - Name of the event
   * @param eventData - Additional event data
   */
  const trackEvent = (eventName: string, eventData: Record<string, any> = {}) => {
    if (typeof window === 'undefined' || !window.adobeDataLayer) {
      console.warn('Adobe DataLayer not available')
      return
    }

    try {
      const userId = authStore.user?.uid || 'anonymous'
      const userRole = roleStore.isAdmin ? 'admin' : 'user'

      const trackingData = {
        event: eventName,
        userId: userId,
        userRole: userRole,
        page: {
          company: getCompany(),
          environment: getEnvironment()
        },
        ...eventData
      }

      window.adobeDataLayer.push(trackingData)

    } catch (error) {
      console.error('❌ Adobe Tracking Error:', error)
    }
  }

  return {
    trackPageview,
    trackButtonClick,
    trackEvent,
    trackLogin,
    trackSignup,
    trackLogout,
    trackPasswordRecovery,
    trackError,
    trackTokenUsage
  }
} 