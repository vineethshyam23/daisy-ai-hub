<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-gradient-to-br from-orange-500 to-amber-500 rounded-xl flex items-center justify-center mx-auto mb-4">
          <img
            src="/favicon.svg"
            alt="DAISY"
            class="w-10 h-10"
            @error="logoError = true"
          />
          <div v-if="logoError" class="text-white font-bold text-lg">AI</div>
        </div>
        <h1 class="text-2xl font-bold text-gray-900">Email Verification</h1>
      </div>

      <div class="bg-white/90 backdrop-blur-sm rounded-xl shadow-lg p-8 border border-orange-100">
        
        <!-- Confirmation Step (to prevent email preview issues) -->
        <div v-if="!userConfirmed && !isVerifying && !verificationSuccess && !verificationError" class="text-center py-8">
          <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-heroicons-envelope-open" class="w-6 h-6 text-blue-600" />
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Verify Your Email Address</h3>
          <p class="text-gray-600 mb-6">
            Click the button below to complete your email verification. This extra step helps prevent automatic email scanners from interfering with the process.
          </p>
          <button
            @click="confirmVerification"
            class="w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white font-medium rounded-lg shadow-lg hover:from-blue-600 hover:to-indigo-600 transition-all cursor-pointer"
          >
            Verify My Email
          </button>
          <p class="text-sm text-gray-500 mt-4">
            If you didn't request this verification, you can safely ignore this page.
          </p>
        </div>
        
        <!-- Verifying State -->
        <div v-if="isVerifying" class="text-center py-8">
          <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-heroicons-arrow-path" class="w-6 h-6 text-orange-600 animate-spin" />
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Verifying your email...</h3>
          <p class="text-gray-600">Please wait while we verify your email address.</p>
        </div>

        <!-- Success State -->
        <div v-else-if="verificationSuccess" class="text-center py-8">
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-heroicons-check-circle" class="w-6 h-6 text-green-600" />
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Email Verified Successfully!</h3>
          <p class="text-gray-600 mb-6">
            Your email has been verified. You can now log in to your DAISY account.
          </p>
          <button
            @click="() => { 
              trackButtonClick('Navigate to Login from Verification Success', { 
                verificationSuccessful: true,
                fromPage: 'verify_email'
              }); 
              window.location.href = '/login'; 
            }"
            class="w-full px-6 py-3 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-medium rounded-lg shadow-lg hover:from-orange-600 hover:to-amber-600 transition-all cursor-pointer"
          >
            Continue to Login
          </button>
        </div>

        <!-- Error State -->
        <div v-else-if="verificationError" class="text-center py-8">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <UIcon name="i-heroicons-x-circle" class="w-6 h-6 text-red-600" />
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Verification Failed</h3>
          <div class="text-gray-600 mb-6 space-y-2">
            <div v-for="line in getErrorMessage(verificationError).split('\n')" :key="line" class="text-sm">
              {{ line }}
            </div>
          </div>
          <div class="space-y-3">
            <button
              @click="() => { 
                trackButtonClick('Navigate to Login from Verification Error', { 
                  verificationSuccessful: false,
                  errorType: verificationError,
                  fromPage: 'verify_email'
                }); 
                navigateTo('/login'); 
              }"
              class="w-full px-6 py-3 bg-gradient-to-r from-orange-500 to-amber-500 text-white font-medium rounded-lg shadow-lg hover:from-orange-600 hover:to-amber-600 transition-all cursor-pointer"
            >
              Back to Login
            </button>
            <button
              @click="() => { 
                trackButtonClick('Navigate to Register from Verification Error', { 
                  verificationSuccessful: false,
                  errorType: verificationError,
                  fromPage: 'verify_email'
                }); 
                navigateTo('/login?tab=register'); 
              }"
              class="w-full px-6 py-3 border border-orange-200 text-orange-600 font-medium rounded-lg hover:bg-orange-50 transition-all cursor-pointer"
            >
              Register Again
            </button>
          </div>
        </div>
      </div>

      <!-- Back to Hub -->
      <div class="text-center mt-6">
        <button
          @click="() => { 
            trackButtonClick('Navigate Back to Hub', { 
              verificationStatus: verificationSuccess ? 'success' : (verificationError ? 'error' : 'verifying'),
              fromPage: 'verify_email'
            }); 
            window.location.href = '/'; 
          }"
          class="text-orange-600 hover:text-orange-500 font-medium text-sm flex items-center justify-center mx-auto cursor-pointer"
        >
          ← Back to DAISY
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth'
import { useAdobeTracking } from '~/composables/useAdobeTracking'
import { getAuth, applyActionCode } from 'firebase/auth'

const authStore = useAuthStore()
const route = useRoute()

// Adobe Tracking
const { trackButtonClick, trackError } = useAdobeTracking()

// State
const logoError = ref(false)
const userConfirmed = ref(false)
const isVerifying = ref(false)
const verificationSuccess = ref(false)
const verificationError = ref(null)

// Methods
const confirmVerification = () => {
  userConfirmed.value = true
  verifyEmail()
}

const verifyEmail = async () => {
  const actionCode = route.query.oobCode
  
  if (!actionCode) {
    verificationError.value = 'No verification code provided'
    isVerifying.value = false
    
    // Track missing verification code error
    trackError('auth_verification_missing_code', 'Email verification attempted without action code', {
      hasActionCode: false,
      queryParams: Object.keys(route.query).length > 0 ? Object.keys(route.query).join(',') : 'none',
      referrer: document.referrer || 'unknown',
      verificationMethod: 'email_link'
    })
    
    return
  }

  isVerifying.value = true

  try {
    const auth = getAuth()
    
    
    // Try to apply the verification code with improved error handling
    await applyActionCode(auth, actionCode)
    
    // Email verification successful
    verificationSuccess.value = true
    
    // Track email verification success
    trackButtonClick('Email Verification Completed', {
      verificationMethod: 'email_link_user_confirmed',
      actionCode: !!actionCode,
      userAgent: navigator.userAgent.substring(0, 100),
      isBot: /bot|crawler|spider/i.test(navigator.userAgent)
    })
    
  } catch (error) {
    console.error('❌ Email verification failed:', error)
    
    // Enhanced error handling for common cases
    if (error.code === 'auth/expired-action-code') {
      verificationError.value = 'auth/expired-action-code'
    } else if (error.code === 'auth/invalid-action-code') {
      verificationError.value = 'auth/invalid-action-code'
    } else {
      verificationError.value = error.message
    }
    
    // Track email verification error with more details
    trackError('auth_verification_failed', getErrorMessage(error.message || error.toString()), {
      hasActionCode: !!actionCode,
      errorCode: error.code || 'unknown',
      verificationMethod: 'email_link',
      referrer: document.referrer || 'unknown',
      userAgent: navigator.userAgent.substring(0, 100),
      isBot: /bot|crawler|spider/i.test(navigator.userAgent),
      actionCodeLength: actionCode ? actionCode.length : 0,
      timeFromLoad: Date.now() - (window.pageLoadTime || Date.now())
    })
  } finally {
    isVerifying.value = false
  }
}

const getErrorMessage = (error) => {
  const errorMap = {
    'auth/expired-action-code': 'Try verifying your email again\nYour request to verify your email has expired or the link has already been used.\n\nThis often happens when:\n• Your email client automatically scanned the link\n• The link was clicked multiple times\n• Too much time has passed since registration\n\nPlease log in and request a new verification email.',
    'auth/invalid-action-code': 'Try verifying your email again\nYour request to verify your email has expired or the link has already been used.\n\nThis link may have been:\n• Already used successfully\n• Automatically accessed by your email client\n• Corrupted during forwarding\n\nPlease try logging in or request a new verification email.',
    'auth/user-disabled': 'This account has been disabled. Please contact support.',
    'auth/user-not-found': 'No account found with this email address. Please register first.',
    'auth/operation-not-allowed': 'Email verification is currently disabled. Please contact support.',
    'auth/too-many-requests': 'Too many verification attempts. Please try again in a few minutes.',
    'No verification code provided': 'Invalid verification link. Please use the complete link from your email.'
  }
  
  for (const [code, message] of Object.entries(errorMap)) {
    if (error.includes(code)) {
      return message
    }
  }
  
  return 'An error occurred during email verification. This might be due to:\n• The link being opened by your email client automatically\n• The verification code being used already\n• Network connectivity issues\n\nPlease try logging in or request a new verification email.'
}

// Check verification code on mount (but don't verify automatically)
onMounted(async () => {
  // Track page load time for bot detection
  window.pageLoadTime = Date.now()
  
  const actionCode = route.query.oobCode
  
  if (!actionCode) {
    verificationError.value = 'No verification code provided'
    
    // Track missing verification code error
    trackError('auth_verification_missing_code', 'Email verification page accessed without action code', {
      hasActionCode: false,
      queryParams: Object.keys(route.query).length > 0 ? Object.keys(route.query).join(',') : 'none',
      referrer: document.referrer || 'unknown',
      verificationMethod: 'email_link',
      userAgent: navigator.userAgent.substring(0, 100),
      isBot: /bot|crawler|spider/i.test(navigator.userAgent)
    })
  }
})

// SEO
useHead({
  title: 'Verify Email - DAISY',
  meta: [
    { name: 'description', content: 'Verify your email address for DAISY account.' }
  ]
})
</script> 