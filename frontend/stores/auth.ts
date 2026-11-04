import { defineStore } from 'pinia'
import { 
  getAuth, 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword,
  signInWithPopup,
  signInWithRedirect,
  getRedirectResult,
  signOut,
  onAuthStateChanged,
  sendPasswordResetEmail,
  sendEmailVerification,
  confirmPasswordReset,
  verifyPasswordResetCode,
  OAuthProvider,
  type User
} from 'firebase/auth'
import { getApps } from 'firebase/app'
import { getEnvironment } from '~/config/firebase.config'
import { useAdobeTracking } from '~/composables/useAdobeTracking'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    loading: false,
    error: null as string | null,
    initialized: false,
  }),
  
  actions: {
    async init() {
      if (this.initialized) {
        return
      }

      try {
        // Check if Firebase is initialized
        if (!getApps().length) {
          console.warn('Firebase not initialized yet, waiting...')
          // Wait for Firebase to be initialized
          let attempts = 0
          while (!getApps().length && attempts < 50) {
            await new Promise(resolve => setTimeout(resolve, 100))
            attempts++
          }
          
          if (!getApps().length) {
            throw new Error('Firebase initialization timeout')
          }
        }

        const auth = getAuth()
        
        // Check for redirect result from GitLab OAuth
        try {
          const result = await getRedirectResult(auth)
          if (result?.user) {
            this.user = result.user
            
            // Check if this is the first login (signup completion for OAuth redirect)
            const isFirstLogin = !localStorage.getItem(`verified_${result.user.uid}`)
            
            if (isFirstLogin) {
              // Track successful signup completion (first OAuth redirect login)
              const { trackSignup } = useAdobeTracking()
              trackSignup(result.user.uid, 'gitlab_oauth', {
                email: result.user.email || '',
                emailDomain: result.user.email?.split('@')[1] || 'unknown',
                verificationMethod: 'oauth_provider'
              })
              
              // Mark this user as having completed their first login
              localStorage.setItem(`verified_${result.user.uid}`, 'true')
            }
            
            // Track successful GitLab OAuth redirect login
            const { trackLogin } = useAdobeTracking()
            trackLogin(result.user.uid, 'gitlab_oauth', {
              emailDomain: result.user.email?.split('@')[1] || 'unknown',
              loginMethod: 'redirect',
              hasAccessToken: true,
              isFirstLogin: isFirstLogin
            })
          }
        } catch (error: any) {
          console.error('OAuth redirect error:', error)
          this.error = error.message
        }
        
        // Listen for auth state changes
        onAuthStateChanged(auth, (user) => {
          if (user) {
            // Check environment-specific email verification requirements
            const environment = getEnvironment()
            const requireEmailVerification = environment === 'production'
            
            // Check if email is verified or if it's an OAuth user (GitLab)
            const isOAuthUser = user.providerData.some(provider => 
              provider.providerId.includes('oauth') || provider.providerId.includes('gitlab')
            )
            
            // Set user based on environment requirements
            if (!requireEmailVerification || user.emailVerified || isOAuthUser) {
              // Production: requires email verification (unless OAuth)
              // Development: no email verification required
              this.user = user
            } else {
              // Production only: User exists but email not verified - don't set user
              console.log('[Auth Store] Email verification required but not completed in production')
              this.user = null
            }
          } else {
            // No user - clear state
            this.user = null
          }
          
          if (!this.initialized) {
            this.initialized = true
          }
        })

        // Mark as initialized after setting up listener
        this.initialized = true
      } catch (error: any) {
        console.error('Failed to initialize auth store:', error)
        this.error = error.message
        this.initialized = true // Mark as initialized even on error to prevent infinite loops
      }
    },

    async login(email: string, password: string) {
      this.loading = true
      this.error = null
      try {
        const auth = getAuth()
        const { user } = await signInWithEmailAndPassword(auth, email, password)
        
        // Environment-specific email verification check
        const environment = getEnvironment()
        const requireEmailVerification = environment === 'production'
        
        // Check if email is verified (only in production)
        if (requireEmailVerification && !user.emailVerified) {
          // Sign out the user immediately
          await signOut(auth)
          this.user = null
          this.error = 'Please verify your email address before logging in. Check your inbox for a verification email.'
          
          // Track login attempt with unverified email
          const { trackError } = useAdobeTracking()
          trackError('auth_login_unverified_email', 'Login attempt with unverified email address', {
            emailDomain: email.split('@')[1] || 'unknown',
            userId: user.uid,
            userEmail: user.email,
            environment: environment
          })
          
          throw new Error('Email not verified')
        }
        
        this.user = user
        
        // Check if this is the first login after email verification (signup completion)
        const isFirstLogin = !localStorage.getItem(`verified_${user.uid}`)
        
        if (isFirstLogin) {
          // Track successful signup completion (first login after verification)
          const { trackSignup } = useAdobeTracking()
          trackSignup(user.uid, 'email_password', {
            email: email,
            emailDomain: email.split('@')[1] || 'unknown',
            verificationMethod: environment === 'development' ? 'none_dev_mode' : 'email_verification',
            environment: environment
          })
          
          // Mark this user as having completed their first login
          localStorage.setItem(`verified_${user.uid}`, 'true')
        }
        
        // Track successful login
        const { trackLogin } = useAdobeTracking()
        trackLogin(user.uid, 'email_password', {
          emailDomain: email.split('@')[1] || 'unknown',
          emailVerified: user.emailVerified,
          isFirstLogin: isFirstLogin,
          environment: environment,
          emailVerificationRequired: requireEmailVerification
        })
        
        return user
      } catch (error: any) {
        if (error.message !== 'Email not verified') {
          this.error = error.message
        }
        throw error
      } finally {
        this.loading = false
      }
    },

    async loginWithGitLab(usePopup: boolean = true) {
      this.loading = true
      this.error = null
      
      try {
        const auth = getAuth()
        const provider = new OAuthProvider('oauth.gitlab')
        
        // Configure GitLab OAuth scopes
        provider.addScope('read_user')
        provider.addScope('read_repository')
        provider.addScope('api')
        
        // Set custom parameters (optional)
        provider.setCustomParameters({
          // You can add GitLab-specific parameters here
        })

        let result
        if (usePopup) {
          // Use popup for better UX (recommended for desktop)
          result = await signInWithPopup(auth, provider)
        } else {
          // Use redirect for mobile or if popup is blocked
          await signInWithRedirect(auth, provider)
          return // Result will be handled in init()
        }

        this.user = result.user
        
        // Check if this is the first login (signup completion for OAuth)
        const isFirstLogin = !localStorage.getItem(`logged_in_${result.user.uid}`)
        
        if (isFirstLogin) {
          // Track successful signup completion (first OAuth login)
          const { trackSignup } = useAdobeTracking()
          trackSignup(result.user.uid, 'gitlab_oauth', {
            email: result.user.email || '',
            emailDomain: result.user.email?.split('@')[1] || 'unknown',
            registrationMethod: 'gitlab_oauth'
          })
          
          // Mark this user as having logged in before
          localStorage.setItem(`logged_in_${result.user.uid}`, 'true')
        }
        
        // Track successful GitLab login
        const { trackLogin } = useAdobeTracking()
        trackLogin(result.user.uid, 'gitlab_oauth', {
          emailDomain: result.user.email?.split('@')[1] || 'unknown',
          hasAccessToken: true,
          isFirstLogin: isFirstLogin
        })
        
        // Get GitLab access token for API calls
        const credential = OAuthProvider.credentialFromResult(result)
        const accessToken = credential?.accessToken
        
        if (accessToken) {
          // Store token for GitLab API calls
          localStorage.setItem('gitlab_access_token', accessToken)
        }
        
        return result.user
      } catch (error: any) {
        this.error = error.message
        console.error('GitLab OAuth error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async getGitLabAccessToken(): Promise<string | null> {
      return localStorage.getItem('gitlab_access_token')
    },

    async logout() {
      const auth = getAuth()
      const currentUser = this.user
      
      // Track logout before signing out
      if (currentUser) {
        const { trackLogout } = useAdobeTracking()
        trackLogout(currentUser.uid, {
          emailDomain: currentUser.email?.split('@')[1] || 'unknown'
        })
      }
      
      await signOut(auth)
      this.user = null
      // Clear GitLab token on logout
      localStorage.removeItem('gitlab_access_token')
      
      // Clear login tracking (optional - user might want to stay "logged in" across sessions)
      // localStorage.removeItem(`logged_in_${currentUser.uid}`)
    },

    async register(email: string, password: string, options: { sendVerificationEmail?: boolean } = {}) {
      this.loading = true
      this.error = null
      try {
        const auth = getAuth()
        const { user } = await createUserWithEmailAndPassword(auth, email, password)
        
        // Environment-specific email verification behavior
        const environment = getEnvironment()
        const shouldSendVerificationEmail = environment === 'production' ? 
          (options.sendVerificationEmail ?? true) : // Production: default to true (secure)
          false // Development: always false (convenience)
        
        // Send verification email (only in production or when explicitly requested)
        let verificationEmailSent = false
        if (shouldSendVerificationEmail) {
      try {
        
        // Configure action code settings for better reliability
        const actionCodeSettings = {
          url: `${window.location.origin}/verify-email`,
          handleCodeInApp: false // This helps prevent automatic processing
        }
        
        // Use the exact same approach as the working old project with improved settings
        await sendEmailVerification(user, actionCodeSettings)
        verificationEmailSent = true
        
        // Sign out user immediately if verification is required
        await signOut(auth)
        this.user = null
        
        return { 
          success: true, 
          message: 'Registration successful! Please check your email and verify your account before logging in.',
          userId: user.uid,
          verificationEmailSent: true,
          requiresVerification: true
        }
      } catch (verifyError: any) {
        console.error('❌ Verification email failed:', verifyError)
        // Don't continue with normal flow - treat as error
        throw new Error('Failed to send verification email. Please try again.')
      }
    }
        
        // Keep user logged in if no verification required
        if (!shouldSendVerificationEmail || !verificationEmailSent) {
          this.user = user
          
          // Track successful signup (only if not requiring verification)
          const { trackSignup } = useAdobeTracking()
          trackSignup(user.uid, 'email_password', {
            email: email,
            emailDomain: email.split('@')[1] || 'unknown',
            registrationMethod: 'email_password',
            environment: environment,
            emailVerificationRequired: shouldSendVerificationEmail
          })
          
          // Mark this user as having logged in (consistent with login tracking)
          localStorage.setItem(`verified_${user.uid}`, 'true')
          
          const message = environment === 'development' ? 
            'Registration successful! You are now logged in. (Email verification disabled in development)' :
            'Registration successful! You are now logged in.'
          
          return { 
            success: true, 
            message: message,
            userId: user.uid,
            verificationEmailSent: verificationEmailSent,
            requiresVerification: false,
            environment: environment
          }
        }
      } catch (error: any) {
        this.error = error.message
        console.error('🚨 Registration error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async resetPassword(email: string) {
      this.loading = true
      this.error = null
      try {
        const auth = getAuth()
        
        // Use the exact same approach as the working old project
        await sendPasswordResetEmail(auth, email)
        
        // Track successful password reset request
        const { trackPasswordRecovery } = useAdobeTracking()
        trackPasswordRecovery(email, 'request', {
          emailDomain: email.split('@')[1] || 'unknown',
          method: 'simple_reset'
        })
        
        return true
      } catch (error: any) {
        console.error('❌ Password reset email failed:', error)
        
        // Handle specific errors
        if (error.code === 'auth/user-not-found') {
          this.error = 'No account found with this email address.'
        } else if (error.code === 'auth/invalid-email') {
          this.error = 'Please enter a valid email address.'
        } else if (error.code === 'auth/too-many-requests') {
          this.error = 'Too many reset attempts. Please try again later.'
        } else {
          this.error = 'Failed to send password reset email. Please try again.'
        }
        
        // Track failed password reset request
        const { trackPasswordRecovery } = useAdobeTracking()
        trackPasswordRecovery(email, 'reset_failed', {
          emailDomain: email.split('@')[1] || 'unknown',
          errorCode: error.code || 'unknown',
          errorMessage: error.message,
          method: 'simple_reset'
        })
        
        throw error
      } finally {
        this.loading = false
      }
    },

    // Change password for logged-in users (uses email reset method)
    async changePassword() {
      this.loading = true
      this.error = null
      try {
        const auth = getAuth()
        const currentUser = auth.currentUser
        
        if (!currentUser || !currentUser.email) {
          throw new Error('No authenticated user found')
        }
        
        
        // Use the exact same approach as the working old project
        await sendPasswordResetEmail(auth, currentUser.email)
        
        // Track successful password change request
        const { trackPasswordRecovery } = useAdobeTracking()
        trackPasswordRecovery(currentUser.email, 'request', {
          emailDomain: currentUser.email.split('@')[1] || 'unknown',
          method: 'logged_in_change',
          userId: currentUser.uid,
          userWasLoggedIn: true
        })
        
        return {
          success: true,
          message: 'Password change email sent! Please check your inbox and follow the instructions.',
          userEmail: currentUser.email
        }
      } catch (error: any) {
        console.error('❌ Password change email failed:', error)
        
        // Handle specific errors
        if (error.code === 'auth/too-many-requests') {
          this.error = 'Too many requests. Please try again later.'
        } else if (error.code === 'auth/invalid-email') {
          this.error = 'Invalid email address.'
        } else {
          this.error = 'Failed to send password change email. Please try again.'
        }
        
        // Track failed password change request
        const { trackPasswordRecovery } = useAdobeTracking()
        trackPasswordRecovery(this.user?.email || 'unknown', 'reset_failed', {
          emailDomain: this.user?.email?.split('@')[1] || 'unknown',
          errorCode: error.code || 'unknown',
          errorMessage: error.message,
          method: 'logged_in_change',
          userId: this.user?.uid || 'unknown',
          userWasLoggedIn: !!this.user
        })
        
        throw error
      } finally {
        this.loading = false
      }
    },

    async verifyResetCode(code: string) {
      try {
        const auth = getAuth()
        const email = await verifyPasswordResetCode(auth, code)
        return email
      } catch (error: any) {
        this.error = error.message
        throw error
      }
    },

    async confirmPasswordReset(code: string, newPassword: string) {
      this.loading = true
      this.error = null
      try {
        const auth = getAuth()
        await confirmPasswordReset(auth, code, newPassword)
        
        // Track successful password reset completion
        // Note: We can't get user details here since they're not logged in yet
        const { trackPasswordRecovery } = useAdobeTracking()
        trackPasswordRecovery('password_reset_user', 'reset_complete', {
          resetCodeProvided: !!code,
          passwordLength: newPassword.length
        })
        
        return true
      } catch (error: any) {
        this.error = error.message
        
        // Track failed password reset completion
        const { trackPasswordRecovery } = useAdobeTracking()
        trackPasswordRecovery('password_reset_user', 'reset_failed', {
          resetCodeProvided: !!code,
          errorCode: error.code || 'unknown'
        })
        
        throw error
      } finally {
        this.loading = false
      }
    },

    // Simple Email Verification (using working method from other project)
    async sendVerificationEmail(user?: any) {
      this.loading = true
      this.error = null
      try {
        const auth = getAuth()
        const currentUser = user || auth.currentUser
        
        if (!currentUser) {
          throw new Error('No user found to send verification email to')
        }
        
        
        // Configure action code settings for better reliability
        const actionCodeSettings = {
          url: `${window.location.origin}/verify-email`,
          handleCodeInApp: false // This helps prevent automatic processing
        }
        
        // Use the exact same approach as the working old project with improved settings
        await sendEmailVerification(currentUser, actionCodeSettings)
        
        return {
          success: true,
          message: 'Verification email sent successfully!',
          userId: currentUser.uid,
          userEmail: currentUser.email
        }
      } catch (error: any) {
        console.error('❌ Verification email failed:', error)
        
        if (error.code === 'auth/too-many-requests') {
          this.error = 'Too many requests. Please try again later.'
        } else {
          this.error = 'Failed to send verification email. Please try again.'
        }
        
        throw error
      } finally {
        this.loading = false
      }
    },

    // Simple resend verification email (from other project)
    async resendVerificationEmail(email: string, password: string) {
      this.loading = true
      this.error = null
      try {
        const auth = getAuth()
        
        // Sign in temporarily to get the user object
        const { user } = await signInWithEmailAndPassword(auth, email, password)
        
        // Configure action code settings for better reliability
        const actionCodeSettings = {
          url: `${window.location.origin}/verify-email`,
          handleCodeInApp: false // This helps prevent automatic processing
        }
        
        // Send verification email directly - exact same approach as working old project with improved settings
        await sendEmailVerification(user, actionCodeSettings)
        
        // Sign out immediately
        await signOut(auth)
        this.user = null
        
        return {
          success: true,
          message: 'Verification email sent successfully!',
          userId: user.uid,
          userEmail: user.email
        }
      } catch (error: any) {
        this.error = error.message
        console.error('❌ Resend verification email error:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  },

  getters: {
    isAuthenticated: (state) => !!state.user,
    userEmail: (state) => state.user?.email,
    hasGitLabToken: () => !!localStorage.getItem('gitlab_access_token'),
    isInitialized: (state) => state.initialized
  }
})