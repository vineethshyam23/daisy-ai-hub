import { useAuthStore } from '~/stores/auth'
import { initializeApp, getApps } from 'firebase/app'
import { getAuth, connectAuthEmulator } from 'firebase/auth'
import { getFirebaseConfig, validateFirebaseConfig, getEnvironment } from '~/config/firebase.config'

export default defineNuxtPlugin({
  name: 'auth-plugin',
  order: 10, // Run after Pinia (order 0) but before most other plugins
  async setup(nuxtApp) {
    // Only run on client side
    if (process.server) {
      return
    }

    try {
      // Get Firebase config from runtime config (now in Nuxt context)
      const firebaseConfig = getFirebaseConfig()
      const isDevelopment = getEnvironment() === 'development'
      
      // Validate config
      if (!validateFirebaseConfig(firebaseConfig)) {
        throw new Error('Invalid Firebase configuration - check environment variables')
      }

      // Initialize Firebase app if not already done
      let app
      if (!getApps().length) {
        app = initializeApp(firebaseConfig)
      } else {
        app = getApps()[0]
      }

      // Initialize Firebase Auth
      const auth = getAuth(app)

      // Wait a bit to ensure Firebase is fully ready
      await new Promise(resolve => setTimeout(resolve, 100))

      // Ensure Pinia is available before using stores
      if (!nuxtApp.$pinia) {
        console.warn('[Auth Plugin] Pinia not yet available, waiting...')
        let attempts = 0
        while (!nuxtApp.$pinia && attempts < 50) {
          await new Promise(resolve => setTimeout(resolve, 100))
          attempts++
        }
        
        if (!nuxtApp.$pinia) {
          throw new Error('Pinia initialization timeout')
        }
      }

      // Initialize auth store after Firebase and Pinia are ready
      const authStore = useAuthStore()
      await authStore.init()
      
    } catch (error) {
      console.error('[Auth Plugin] Failed to initialize Firebase:', error)
      // Don't throw error to prevent app crash, just log it
      console.error('[Auth Plugin] Continuing without auth initialization')
    }
  }
}) 