// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";
import { config } from 'dotenv';

// Load .env file explicitly
config();

export default defineNuxtConfig({
  ssr: false,
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  modules: [
    '@nuxt/ui',
    '@pinia/nuxt',
  ],
  colorMode: {
    preference: 'dark',
    fallback: 'dark',
  },
  runtimeConfig: {
    // Server-side environment variables
    // These can be overridden at runtime with NUXT_GOOGLE_CLOUD_PROJECT_ID etc.
    googleCloudProjectId: process.env.GOOGLE_CLOUD_PROJECT_ID || '',
    apiTokenSecretName: process.env.API_TOKEN_SECRET_NAME || 'ai-hub-api-token',
    
    public: {
      environment: process.env.ENV || 'development',
      
      // Firebase Development Configuration
      // These can be overridden at runtime with NUXT_PUBLIC_FIREBASE_DEV_* env vars
      firebaseDevApiKey: process.env.FIREBASE_DEV_API_KEY || '',
      firebaseDevAuthDomain: process.env.FIREBASE_DEV_AUTH_DOMAIN || '',
      firebaseDevProjectId: process.env.FIREBASE_DEV_PROJECT_ID || '',
      firebaseDevStorageBucket: process.env.FIREBASE_DEV_STORAGE_BUCKET || '',
      firebaseDevMessagingSenderId: process.env.FIREBASE_DEV_MESSAGING_SENDER_ID || '',
      firebaseDevAppId: process.env.FIREBASE_DEV_APP_ID || '',
      firebaseDevMeasurementId: process.env.FIREBASE_DEV_MEASUREMENT_ID || '',
      
      // Firebase Production Configuration  
      // These can be overridden at runtime with NUXT_PUBLIC_FIREBASE_PROD_* env vars
      firebaseProdApiKey: process.env.FIREBASE_PROD_API_KEY || '',
      firebaseProdAuthDomain: process.env.FIREBASE_PROD_AUTH_DOMAIN || '',
      firebaseProdProjectId: process.env.FIREBASE_PROD_PROJECT_ID || '',
      firebaseProdStorageBucket: process.env.FIREBASE_PROD_STORAGE_BUCKET || '',
      firebaseProdMessagingSenderId: process.env.FIREBASE_PROD_MESSAGING_SENDER_ID || '',
      firebaseProdAppId: process.env.FIREBASE_PROD_APP_ID || '',
      firebaseProdMeasurementId: process.env.FIREBASE_PROD_MEASUREMENT_ID || ''
    }
  },
  app: {
    head: {
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg?v=2' },
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico?v=2' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/favicon.svg?v=2' },
        { rel: 'shortcut icon', href: '/favicon.svg?v=2' },
        { 
          rel: 'preconnect', 
          href: 'https://fonts.googleapis.com' 
        },
        { 
          rel: 'preconnect', 
          href: 'https://fonts.gstatic.com', 
          crossorigin: '' 
        },
        { 
          rel: 'stylesheet', 
          href: 'https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap' 
        }
      ]
    }
  }
})
